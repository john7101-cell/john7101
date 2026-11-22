#!/usr/bin/env python3
"""google-colab-runner: package a video-director manifest for Google Colab, or drive a
running Google Colab ComfyUI from the director (Python stdlib only).

  python colab.py estimate  <manifest> [--gpu L4]             # GPU-minutes and Google Colab compute units
  python colab.py package   <manifest> [--out dist] [--zip]   # self-contained bundle + .ipynb
  python colab.py orchestrate <manifest> --url <tunnel-url>   # director drives the Google Colab ComfyUI
  python colab.py teardown  --url <tunnel-url>                # ask the notebook watchdog to release the runtime
  python colab.py ingest    <manifest> <outputs.zip|dir>      # attach packaged-run outputs to the manifest

video-director calls this as `direct.py package --target google-colab <manifest>` and
`direct.py run <manifest> --target google-colab --url <tunnel-url>`.
Nothing here starts a Google Colab session or spends compute units by itself: a person opens
the notebook and presses Run. No credential is read, stored or written by this script.
"""
import argparse, base64, copy, io, json, math, os, re, shutil, sys, time, urllib.request, urllib.error, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SKILLS = os.path.dirname(SKILL)
REF = os.path.join(SKILL, "references")
sys.path.insert(0, os.path.join(SKILLS, "video-director", "scripts"))
sys.path.insert(0, HERE)  # this skill's own copy of comfy_client.py
import direct  # noqa: E402
import comfy_client  # noqa: E402

GPUS = json.load(open(os.path.join(REF, "gpu-tiers.json")))
MODELS = json.load(open(os.path.join(REF, "models.json")))["files"]
NODES = json.load(open(os.path.join(REF, "custom-nodes.lock.json")))
FILE_ROLES = ("image", "last_image", "video", "audio", "voice", "mask")
TEARDOWN_SENTINEL = "gcr_teardown_request.txt"


# ------------------------------------------------------------ GPU, tier, estimate
def gpu_info(name=None, vram=None):
    name = (name or "").upper()
    for k, g in GPUS["gpus"].items():
        if any(x in name for x in g["match"]):
            return k, dict(g)
    g = dict(GPUS["unknown"])
    if vram:
        g["vram_gb"] = vram
        g["tier"] = max((t for t in direct.ORDER if direct.TIERS[t]["min_vram"] <= vram), key=direct.ORDER.index, default="draft")
    return "unknown", g


def tier_for(vram, wanted):
    ok = [t for t in direct.ORDER if direct.TIERS[t]["min_vram"] <= (vram or 0)] or ["draft"]
    best = ok[-1]
    return best if direct.ORDER.index(best) < direct.ORDER.index(wanted) else wanted


def download_bytes(model_files):
    return sum((MODELS.get(f) or {}).get("bytes") or 0 for f in model_files)


def estimate(m, gpu=None, cu_per_hour=None, model_files=None, tier=None):
    """Session estimate: Google Colab bills the runtime's wall clock, not GPU work, so setup and the
    collect-and-stop reserve are part of it. Every rate is an unverified assumption."""
    key, g = gpu_info(gpu or (m["target"].get("gpu")), m["target"].get("vram_gb"))
    tier = tier or tier_for(g["vram_gb"] or m["target"].get("vram_gb"), m["tier"])
    gpu_min, renders = direct.estimate(m, tier)
    if model_files is None:
        model_files = sorted({f for rid in used_routes(m) for f in route_models(rid)})
    gb = download_bytes(model_files) / 1e9
    oh = GPUS["session_overhead_minutes"]
    setup = oh["bootstrap"] + gb * oh["per_gb_download"]
    work = gpu_min * g["speed"]
    session = setup + work + oh["collect_and_stop_reserve"]
    rate = cu_per_hour or (m["target"].get("colab") or {}).get("cu_per_hour") or g["cu_per_hour"]
    return {"gpu": key, "tier": tier, "renders_cap": renders, "gpu_minutes_24gb_class": gpu_min,
            "work_minutes": round(work, 1), "setup_minutes": round(setup, 1), "download_gb": round(gb, 1),
            "session_minutes": round(session, 1), "cu_per_hour": rate, "compute_units": round(session / 60 * rate, 2),
            "assumptions": "rates, GPU speed and CU/hour are unverified placeholders; check the Google Colab Resources panel"}


# ------------------------------------------------------------ routes -> workflows, models, node packs
ROUTES = direct.load_routes()


def wf_path(rid):
    r = ROUTES[rid]
    if r["workflow"] in ("-",) or r["workflow"].startswith("script:"):
        return None
    return os.path.join(direct.SKILLS, r["skill"], "workflows", r["workflow"])


def used_routes(m):
    out = []
    for s in m["shots"]:
        out += [s["still"]["route"], s["video"]["route"]] + [x["route"] for x in s.get("extra", [])]
    for k in ("voiceover", "music"):
        if k in m["audio"]: out.append(m["audio"][k]["route"])
    out += [x["route"] for x in m["audio"].get("sfx", [])]
    seen = []
    for rid in out:  # include fallbacks: the runtime may need them
        while rid and rid != "-" and rid in ROUTES and rid not in seen:
            seen.append(rid); rid = ROUTES[rid]["fallback"]
    return seen


EXT = re.compile(r"\.(safetensors|gguf|pt|pth|ckpt|bin|onnx|sft)$")


def route_models(rid):
    p = wf_path(rid)
    if not p or not os.path.isfile(p): return []
    out = set()
    for n in json.load(open(p)).values():
        if isinstance(n, dict):
            for v in n.get("inputs", {}).values():
                if isinstance(v, str) and EXT.search(v): out.add(v.replace("\\", "/"))
    return sorted(out)


def route_packs(rid):
    """Custom node packs a workflow needs, read from the skill's generated requirements.md."""
    p = wf_path(rid)
    if not p: return []
    req = os.path.join(direct.SKILLS, ROUTES[rid]["skill"], "references", "requirements.md")
    if not os.path.isfile(req): return []
    txt = open(req).read(); name = os.path.relpath(p, os.path.join(direct.SKILLS, ROUTES[rid]["skill"]))
    sec = txt.split(f"### {name}\n", 1)
    if len(sec) < 2: return []
    body = sec[1].split("\n## ", 1)[0].split("\n### ", 1)[0]
    return sorted({u.rstrip(".") for u in re.findall(r"https://github\.com/[\w.-]+/[\w.-]+", body)} - {NODES["comfyui"]["repo"]})


# ------------------------------------------------------------ job building (shared by package)
def fill(rid, values):
    """Fill a route's API workflow with every non-file value. File roles are returned separately
    so the runner can upload them (or a previous job's output) at run time."""
    r = ROUTES[rid]; wf = json.load(open(wf_path(rid))); files = []
    for role, val in values.items():
        if val is None or role not in r["inputs"]: continue
        if role in FILE_ROLES:
            files.append({"role": role, "targets": r["inputs"][role], "from": val}); continue
        for t in r["inputs"][role]:
            nid, _, inp = t.rpartition(".")
            wf[nid].setdefault("inputs", {})[inp] = val
    loc = direct.placeholders(wf)
    if loc:
        fills = dict(direct.sidecar(r).get("placeholders", {}))
        fills.update({k: v for k, v in values.items() if k.isupper() and v is not None})
        for ph, ts in loc.items():
            if ph in fills:
                for t in ts:
                    nid, _, inp = t.rpartition(".")
                    cur = wf[nid]["inputs"][inp]
                    wf[nid]["inputs"][inp] = fills[ph] if cur == "{{%s}}" % ph else cur.replace("{{%s}}" % ph, str(fills[ph]))
        ftargets = {t for f in files for t in f["targets"]}  # filled with the uploaded name at run time
        left = sorted(ph for ph, ts in direct.placeholders(wf).items() if not set(ts) <= ftargets)
        if left: return wf, files, left
    return wf, files, []


def first_ready(rid, unusable):
    seen = []
    while rid and rid != "-" and rid not in seen:
        seen.append(rid)
        if rid in ROUTES and wf_path(rid) and os.path.isfile(wf_path(rid)) and rid not in unusable:
            return rid
        rid = ROUTES.get(rid, {}).get("fallback")
    return None


def build_jobs(m0, tier, mdir):
    m = copy.deepcopy(m0); m["tier"] = tier
    for s in m["shots"]:  # tier presets are re-applied per tier
        for k in ("width", "height", "frames", "fps"):
            s["still"].pop(k, None); s["video"].pop(k, None)
        if s["still"]["route"] == direct.TIERS[m0["tier"]]["still_route"]:
            s["still"]["route"] = direct.TIERS[tier]["still_route"]
    direct.apply_tier(m)
    jobs, notes, assets = [], [], set()

    def asset(v):
        if isinstance(v, str) and not v.startswith(("job:", "lastframe:")):
            p = v if os.path.isabs(v) else os.path.join(mdir, v)
            assets.add((v, p)); return "asset:" + v
        return v

    def add(jid, rid, vals, kind, shot=None):
        r2 = first_ready(rid, set())
        if not r2:
            notes.append(f"{jid}: route {rid} has no API workflow (UI template only); skipped"); return None
        vals = {k: (asset(v) if k in FILE_ROLES else v) for k, v in vals.items()}
        wf, files, left = fill(r2, vals)
        if left:
            notes.append(f"{jid}: {r2} has unfilled placeholders {left}; skipped"); return None
        jobs.append({"id": jid, "kind": kind, "shot": shot, "route": r2, "workflow": f"workflows/{tier}/{jid}.api.json",
                     "files": files, "_wf": wf}); return jid

    for s in m["shots"]:
        st, vd = s["still"], s["video"]; sid = s["id"]
        seed = st.get("seed") or 1000 + int(re.sub(r"\D", "", sid)[:2] or 0) * 7
        still = add(f"{sid}_still", st["route"], {"prompt": st.get("prompt", ""), "seed": seed, "width": st["width"], "height": st["height"]}, "still", sid)
        img = f"job:{still}" if still else None
        if st.get("approved") and os.path.isfile(os.path.join(mdir, st["approved"])): img = st["approved"]
        last = None; still_img = img
        if s.get("chain_from"):
            prev = f"job:{s['chain_from']}_video"
            if "last_image" in ROUTES.get(vd["route"], {}).get("inputs", {}): img, last = f"lastframe:{prev[4:]}", img
            else: img = f"lastframe:{prev[4:]}"
        r_v = first_ready(vd["route"], set())
        sc = direct.sidecar(ROUTES[r_v]) if r_v else {}
        if sc.get("fps"):  # Wan-family graphs: own fps + 4n+1 frames (mirrors direct.py video_one)
            step = 4 if sc.get("frame_rule") == "4n+1" else 8
            vd["fps"] = sc["fps"]; vd["frames"] = step * math.ceil(s["duration_s"] * sc["fps"] / step) + 1
        if sc.get("duration_placeholder"):
            vd.setdefault("params", {}).setdefault(sc["duration_placeholder"], str(max(2, round(s["duration_s"]))))
        vseed = vd.get("seed") or 5000 + int(re.sub(r"\D", "", sid)[:2] or 0) * 11
        vals = {"image": img, "last_image": last, "prompt": vd.get("prompt", ""), "seed": vseed, "width": vd["width"],
                "height": vd["height"], "frames": vd["frames"], "strength1": vd.get("strength1"), "strength2": vd.get("strength2"),
                "fps": vd.get("fps"), "negative": ""}
        vals.update(vd.get("params") or {})
        add(f"{sid}_video", vd["route"], vals, "video", sid)
        for i, x in enumerate(s.get("extra", [])):
            src = {"image": still_img} if ROUTES.get(x["route"], {}).get("stage") == "still-fix" and still_img else {"video": f"job:{sid}_video"}
            add(f"{sid}_extra{i+1}", x["route"], {**x.get("params", {}), **src}, "extra", sid)
    au = m["audio"]
    if au.get("voiceover"):
        text = " ".join(x["narration"] for x in m["shots"] if x.get("narration"))
        add("voiceover", au["voiceover"]["route"], {"text": text, "seed": au["voiceover"].get("seed") or 7, **au["voiceover"].get("params", {})}, "audio")
    if au.get("music") and not (au["music"].get("params") or {}).get("file"):
        add("music", au["music"]["route"], {"seconds": m["brief"]["length_s"] + 2, "seed": au["music"].get("seed") or 11, **au["music"].get("params", {})}, "audio")
    for i, fx in enumerate(au.get("sfx", [])):
        add(f"sfx{i+1}", fx["route"], {"seed": 20 + i, **fx.get("params", {})}, "audio")
    return m, jobs, notes, assets


# ------------------------------------------------------------ package
def package(mpath, out, make_zip=True, max_minutes=None):
    m = json.load(open(mpath)); mdir = os.path.dirname(os.path.abspath(mpath))
    errs = direct.validate(m, json.load(open(direct.SCHEMA))) + direct.rules(m, ROUTES)
    if errs:
        print("manifest invalid:\n  " + "\n  ".join(errs)); return 2
    name = f"{m['id']}-google-colab"; b = os.path.join(out, name)
    if os.path.isdir(b): shutil.rmtree(b)
    os.makedirs(os.path.join(b, "assets"))
    tiers = direct.ORDER[:direct.ORDER.index(m["tier"]) + 1]
    allmodels, allpacks, plan, missing_assets = {}, set(), {}, []
    for t in tiers:
        mt, jobs, notes, assets = build_jobs(m, t, mdir)
        os.makedirs(os.path.join(b, "workflows", t))
        models = set()
        for j in jobs:
            json.dump(j.pop("_wf"), open(os.path.join(b, j["workflow"]), "w"), indent=1)
            models |= set(route_models(j["route"])); allpacks |= set(route_packs(j["route"]))
        for v, p in sorted(assets):
            if os.path.isfile(p):
                dst = os.path.join(b, "assets", v); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(p, dst)
            elif v not in missing_assets: missing_assets.append(v)
        est = estimate(mt, {"draft": "T4", "standard": "L4", "max": "A100"}[t], None, sorted(models), tier=t)
        plan[t] = {"min_vram_gb": direct.TIERS[t]["min_vram"], "jobs": jobs, "models": sorted(models), "notes": notes, "estimate": est}
        for f in models: allmodels[f] = MODELS.get(f) or {"url": None, "license": "unknown", "dir": "diffusion_models"}
    lock = {"comfyui": NODES["comfyui"], "packs": {u: NODES["packs"].get(u) for u in sorted(allpacks)}, "bundled": []}
    for sk in sorted({ROUTES[j["route"]]["skill"] for p in plan.values() for j in p["jobs"]}):
        ad = os.path.join(SKILLS, sk, "assets")  # node packs shipped inside the collection (MIT/Apache/BSD, see NOTICE)
        for d in sorted(os.listdir(ad)) if os.path.isdir(ad) else []:
            src = os.path.join(ad, d)
            if os.path.isdir(src) and any(f.endswith(".py") for f in os.listdir(src)) and d not in lock["bundled"]:
                shutil.copytree(src, os.path.join(b, "custom_nodes", d), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                lock["bundled"].append(d)
    json.dump({"v": 1, "manifest_id": m["id"], "manifest_tier": m["tier"], "tiers": plan,
               "gpu_tiers": GPUS, "max_session_minutes": max_minutes or (m["target"].get("budget") or {}).get("max_gpu_minutes"),
               "missing_assets": missing_assets}, open(os.path.join(b, "jobs.json"), "w"), indent=1)
    json.dump({"v": 1, "files": allmodels}, open(os.path.join(b, "models.json"), "w"), indent=1)
    json.dump(lock, open(os.path.join(b, "nodes.lock.json"), "w"), indent=1)
    shutil.copy2(mpath, os.path.join(b, "manifest.json"))
    shutil.copy2(os.path.join(SKILL, "templates", "runner.py"), os.path.join(b, "runner.py"))
    shutil.copy2(os.path.join(HERE, "comfy_client.py"), os.path.join(b, "comfy_client.py"))
    sys.path.insert(0, HERE); import notebook  # noqa: E402
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, fs in os.walk(b):
            for f in fs:
                rel = os.path.relpath(os.path.join(root, f), b)
                if not rel.startswith("assets" + os.sep): zf.write(os.path.join(root, f), rel)
    if os.listdir(os.path.join(b, "assets")):
        shutil.make_archive(os.path.join(out, f"{name}-assets"), "zip", b, "assets")
    nb = notebook.build(m, plan, lock, allmodels, base64.b64encode(buf.getvalue()).decode())
    json.dump(nb, open(os.path.join(b, f"{m['id']}.ipynb"), "w"), indent=1)
    open(os.path.join(b, "README.md"), "w").write(notebook.readme(m, plan, lock, allmodels, missing_assets))
    print(json.dumps({"bundle": b, "tiers": {t: {"jobs": len(p["jobs"]), "models": len(p["models"]), "skipped": len(p["notes"]),
                                                 "est_cu": p["estimate"]["compute_units"]} for t, p in plan.items()},
                      "unresolved_model_urls": sorted(f for f, v in allmodels.items() if not v.get("url")),
                      "missing_assets": missing_assets}, indent=1))
    if make_zip:
        z = shutil.make_archive(b, "zip", out, name); print("zip:", z)
    return 0


# ------------------------------------------------------------ orchestrate
def probe(url, timeout=10):
    try:
        return comfy_client._req(url, "/system_stats", timeout=timeout)
    except Exception:
        return None


class SessionDropped(RuntimeError):
    pass


class GoogleColabRunner(direct.Runner):
    """direct.Runner plus the Google Colab session meter (wall-clock compute units against the hard
    cap) and drop detection: a ComfyUI call that produced nothing while the server is unreachable
    stops the run with the manifest saved, instead of recording empty attempts."""
    def sh(s, cmd, label):
        res = direct.Runner.sh(s, cmd, label)
        talks_to_comfy = "--url" in [str(c) for c in cmd] or any("judge.py" in str(c) for c in cmd)
        if talks_to_comfy and ("raw" in res or res.get("status") not in (None, "done")) and not probe(s.url, 5):
            raise SessionDropped(f"{label}: ComfyUI unreachable")
        return res

    def budget_ok(s, kind):
        c = s.m["target"]["colab"]
        spent = (time.time() - c["session_started_epoch"]) / 60 / 60 * c["cu_per_hour"] if c.get("session_started_epoch") else 0
        c["cu_spent_estimate"] = round(c.get("cu_spent_prior", 0) + spent, 3)
        reserve = GPUS["session_overhead_minutes"]["collect_and_stop_reserve"] / 60 * c["cu_per_hour"]
        if c.get("cu_cap") is not None and c["cu_spent_estimate"] + reserve >= c["cu_cap"]:
            s.log("cap_hit", {"cap": "google_colab_compute_units", "at": kind, "spent": c["cu_spent_estimate"], "cap_cu": c["cu_cap"]})
            return False
        return direct.Runner.budget_ok(s, kind)


def orchestrate(a):
    mpath = a.manifest; m = json.load(open(mpath))
    st = probe(a.url)
    if not st:
        print(f"Google Colab ComfyUI not reachable at {a.url}. Start the notebook (cells 1-5), copy the tunnel URL it prints, then re-run.")
        return 5
    dev = (st.get("devices") or [{}])[0]
    vram = round((dev.get("vram_total") or 0) / 2**30) or None
    key, g = gpu_info(dev.get("name", ""), vram)
    t = m.setdefault("target", {}); t.update(kind="google_colab", url=a.url, gpu=dev.get("name", key), vram_gb=vram or g["vram_gb"])
    c = t.setdefault("colab", {})
    c.update(gpu=key, cu_per_hour=a.cu_per_hour or c.get("cu_per_hour") or g["cu_per_hour"])
    budget = t.get("budget") or {}
    c["cu_cap"] = a.max_cu if a.max_cu is not None else budget.get("max_credits")
    fit = tier_for(t["vram_gb"], m["tier"])
    if fit != m["tier"]:
        m.setdefault("log", []).append({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": "tier_downgrade", "detail": {"from": m["tier"], "to": fit, "why": f"{key} {t['vram_gb']} GB"}})
        m["tier"], m["tier_reason"] = fit, f"Google Colab {key} has {t['vram_gb']} GB"
    est = estimate(m, key, c["cu_per_hour"]); c["estimate"] = est
    json.dump(m, open(mpath, "w"), indent=1)
    print(f"== Google Colab estimate ({key}, tier {est['tier']}): ~{est['session_minutes']} session-min = ~{est['compute_units']} compute units "
          f"at {c['cu_per_hour']} CU/h; cap {c['cu_cap']} CU. {est['assumptions']}.")
    if c["cu_cap"] is None and not a.no_cap_ok:
        print("Refusing: no compute-unit cap. Set target.budget.max_credits or pass --max-cu."); return 6
    if c["cu_cap"] is not None and est["compute_units"] > c["cu_cap"]:
        print(f"Refusing: the estimate {est['compute_units']} CU is over the hard cap {c['cu_cap']} CU. Lower the tier or shot count, or raise the cap."); return 6
    if m["gates"].get("spend") != "approved":
        m["gates"]["spend"] = "human"; json.dump(m, open(mpath, "w"), indent=1)
        print(f"== GATE 'spend': show the estimate above to the user. After a yes: direct.py approve {mpath} spend, then re-run."); return 3
    m = json.load(open(mpath)); c = m["target"]["colab"]
    if c.get("session_started_epoch") and c.get("session_url") != a.url:  # new session after a drop
        c["cu_spent_prior"] = c.get("cu_spent_estimate", 0); c["drops"] = c.get("drops", 0) + 1
        m["log"].append({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": "session_resumed", "detail": {"drops": c["drops"]}})
        c["session_started_epoch"] = time.time()
    c.setdefault("session_started_epoch", time.time()); c["session_url"] = a.url
    json.dump(m, open(mpath, "w"), indent=1)
    r = GoogleColabRunner(mpath, a.url, False, ROUTES)
    try:
        code = r.run()
    except RuntimeError as e:
        r.save()
        if isinstance(e, SessionDropped) or not probe(a.url, 5):
            r.log("session_dropped", {"error": str(e)[-300:]}); r.save()
            print("== Google Colab session dropped. The manifest is saved; finished work is kept locally and is re-uploaded on resume.\n"
                  "   Restart the notebook (it reinstalls and re-downloads), copy the new tunnel URL, then re-run this command with --url <new>.")
            return 5
        raise
    capped = any(x.get("event") == "cap_hit" for x in r.m["log"])
    if a.teardown == "auto" or (a.teardown == "on-cap" and capped):
        teardown(a.url)
    else:
        print(f"== Offer teardown to the user: colab.py teardown --url {a.url}  (or Runtime > Disconnect and delete runtime). "
              "Google Colab keeps billing while the runtime is connected.")
    return code


def teardown(url):
    """Ask the notebook watchdog cell to release the runtime: clear the queue, then upload a sentinel
    file that the watchdog polls for in ComfyUI/input. Requires the watchdog cell to be running."""
    try:
        comfy_client._req(url, "/queue", {"clear": True}, method="POST")
        comfy_client._req(url, "/interrupt", {}, method="POST")
    except Exception as e:
        print("queue clear failed:", e)
    tmp = os.path.join(os.environ.get("TMPDIR", "/tmp"), TEARDOWN_SENTINEL)
    open(tmp, "w").write(f"teardown requested {time.strftime('%Y-%m-%dT%H:%M:%S')}\n")
    try:
        comfy_client.upload(url, tmp); print("teardown requested: the notebook watchdog releases the runtime within ~30 s. "
                                            "Confirm in Google Colab (Runtime > Manage sessions) that it is gone.")
        return 0
    except Exception as e:
        print("teardown request failed (session may already be gone):", e); return 1


# ------------------------------------------------------------ ingest packaged-run outputs
def ingest(mpath, src):
    m = json.load(open(mpath)); mdir = os.path.dirname(os.path.abspath(mpath))
    dst = os.path.join(mdir, m["id"], "google-colab")
    if os.path.isfile(src):
        zipfile.ZipFile(src).extractall(dst)
    else:
        shutil.copytree(src, dst, dirs_exist_ok=True)
    state = json.load(open(os.path.join(dst, "state.json")))
    n = 0
    for s in m["shots"]:
        for part in ("still", "video"):
            j = state["jobs"].get(f"{s['id']}_{part}")
            if j and j.get("status") == "done" and j.get("files"):
                f = os.path.relpath(os.path.join(dst, j["files"][0]), mdir)
                s[part].setdefault("attempts", []).append({"n": len(s[part]["attempts"]) + 1, "route": j["route"], "seed": j.get("seed"),
                                                           "file": f, "verdict": "unjudged", "source": "google-colab package run"})
                n += 1
    m["log"].append({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": "google_colab_ingest", "detail": {"files": n, "tier": state.get("tier")}})
    json.dump(m, open(mpath, "w"), indent=1)
    print(f"ingested {n} outputs as unjudged attempts. Judge them with still-qa / shot-qc, then run direct.py run for continuity onward.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    e = sp.add_parser("estimate"); e.add_argument("manifest"); e.add_argument("--gpu"); e.add_argument("--cu-per-hour", type=float)
    k = sp.add_parser("package"); k.add_argument("manifest"); k.add_argument("--out", default="dist"); k.add_argument("--no-zip", action="store_true")
    k.add_argument("--max-session-minutes", type=float)
    o = sp.add_parser("orchestrate"); o.add_argument("manifest"); o.add_argument("--url", required=True)
    o.add_argument("--max-cu", type=float); o.add_argument("--cu-per-hour", type=float)
    o.add_argument("--no-cap-ok", action="store_true", help="allow a run with no compute-unit cap (render caps still apply)")
    o.add_argument("--teardown", choices=["offer", "on-cap", "auto"], default="offer")
    t = sp.add_parser("teardown"); t.add_argument("--url", required=True)
    i = sp.add_parser("ingest"); i.add_argument("manifest"); i.add_argument("outputs")
    a = p.parse_args(argv)
    if a.cmd == "estimate":
        m = json.load(open(a.manifest)); print(json.dumps(estimate(m, a.gpu, a.cu_per_hour), indent=1)); return 0
    if a.cmd == "package": return package(a.manifest, a.out, not a.no_zip, a.max_session_minutes)
    if a.cmd == "orchestrate": return orchestrate(a)
    if a.cmd == "teardown": return teardown(a.url)
    if a.cmd == "ingest": return ingest(a.manifest, a.outputs)


if __name__ == "__main__":
    sys.exit(main())
