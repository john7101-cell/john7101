#!/usr/bin/env python3
"""video-director driver (Python stdlib only).

Chains the collection's per-skill scripts (comfy_client.py, preflight.py,
judge.py, assemble.py, make_srt.py) around ONE resumable production manifest,
enforcing tiers, gates and caps. Every step updates the manifest, so a killed
run resumes where it stopped. Steps whose status is "done" are skipped.

  python direct.py routes                              # parsed routing table
  python direct.py validate manifest.json              # schema + routing + LTX/caps rules
  python direct.py tier manifest.json                  # pick draft/standard/max from VRAM, preflight, budget
  python direct.py run manifest.json --dry-run         # print the full plan; NO network, NO subprocess
  python direct.py run manifest.json --url $COMFY_URL  # execute (resumable)
  python direct.py approve manifest.json plan          # pass a human gate (bible|plan|spend|final)
  python direct.py package --target google-colab manifest.json         # Google Colab bundle + notebook
  python direct.py run manifest.json --target google-colab --url $TUNNEL # drive a Google Colab ComfyUI

Env: COMFY_URL, VLM_ENDPOINT, VLM_MODEL (judge). Nothing here calls a closed API.
"""
import argparse, json, math, os, re, shlex, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SKILLS = os.path.dirname(SKILL)
ROUTING = os.path.join(SKILL, "references", "routing.md")
SCHEMA = os.path.join(SKILL, "references", "manifest.schema.json")

# Tier presets. width/height are the LTX two-pass *base* latent (final = 2x).
TIERS = {
    "draft":    {"min_vram": 16, "still_route": "still.flux2_4b", "still_wh": (1024, 576), "video_wh": (512, 288),
                 "caps": {"still_retries": 1, "still_variants": 1, "video_retries": 0, "continuity_regens": 0, "pass_mean": 3.0, "pass_min": 2},
                 "transition": "transition.cut", "upscale": False, "grade": False},
    "standard": {"min_vram": 24, "still_route": "still.klein", "still_wh": (1280, 704), "video_wh": (640, 352),
                 "caps": {"still_retries": 2, "still_variants": 1, "video_retries": 1, "continuity_regens": 1, "pass_mean": 3.5, "pass_min": 3},
                 "transition": "transition.cut", "upscale": False, "grade": True},
    "max":      {"min_vram": 40, "still_route": "still.klein_base", "still_wh": (1280, 704), "video_wh": (768, 448),
                 "caps": {"still_retries": 3, "still_variants": 2, "video_retries": 2, "continuity_regens": 2, "pass_mean": 4.0, "pass_min": 3},
                 "transition": "transition.flf", "upscale": True, "grade": True},
}
ORDER = ["draft", "standard", "max"]
# Seconds per render on a 24 GB-class GPU. PLACEHOLDER ASSUMPTIONS (unverified); override in manifest.cost.rates_s_per_render.
RATES = {"still": 20, "still.klein_base": 70, "still-fix": 30, "video": 180, "video@max": 420, "video@draft": 90,
         "qa": 8, "audio": 40, "post": 240, "transition": 360, "vfx": 300, "video-fix": 300}
STATIC = re.compile(r"\b(static|locked|tripod|still camera|no camera move)\b", re.I)


# ---------------------------------------------------------------- routing
def load_routes(path=ROUTING):
    routes, header = {}, None
    for line in open(path):
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 9:
            continue
        if cells[0] == "id":
            header = cells; continue
        if header is None or set(cells[0]) <= set("-"):
            continue
        r = dict(zip(header, cells))
        inputs = {}
        if r["inputs"] not in ("-", ""):
            for pair in r["inputs"].split("; "):
                role, _, targets = pair.partition("=")
                inputs[role.strip()] = [t.strip() for t in targets.split(",")]
        r["inputs"] = inputs
        r["tiers"] = ORDER if r["tiers"] == "*" else [t for t in r["tiers"].split(",") if t and t != "-"]
        routes[r["id"]] = r
    return routes


PH = re.compile(r"\{\{([A-Z_]+)\}\}")


def sidecar(r):
    """Optional workflows/<file>.defaults.json: {"placeholders": {...}, "fps": 16, "frame_rule": "4n+1", "duration_placeholder": "DURATION"}."""
    if r["workflow"] in ("-",) or r["workflow"].startswith("script:"): return {}
    p = os.path.join(SKILLS, r["skill"], "workflows", r["workflow"].replace(".api.json", ".defaults.json"))
    return json.load(open(p)) if os.path.isfile(p) else {}


def placeholders(wf):
    loc = {}
    for nid, n in wf.items():
        if isinstance(n, dict):
            for k, v in n.get("inputs", {}).items():
                if isinstance(v, str):
                    for ph in PH.findall(v): loc.setdefault(ph, []).append(f"{nid}.{k}")
    return loc


def check_routes(routes):
    errs = []
    for rid, r in routes.items():
        d = os.path.join(SKILLS, r["skill"])
        if not os.path.isfile(os.path.join(d, "SKILL.md")):
            errs.append(f"{rid}: skill '{r['skill']}' not in collection")
            continue
        w = r["workflow"]
        if w.startswith("script:"):
            if not os.path.isfile(os.path.join(d, "scripts", w[7:])):
                errs.append(f"{rid}: missing script {w}")
        elif w != "-":
            p = os.path.join(d, "workflows", w)
            if not os.path.isfile(p):
                errs.append(f"{rid}: missing workflow {w}"); continue
            wf = json.load(open(p))
            for role, tg in r["inputs"].items():
                for t in tg:
                    nid, _, inp = t.rpartition(".")
                    if nid not in wf:
                        errs.append(f"{rid}: input {role} -> node {nid} not in {w}")
        if r["fallback"] != "-" and r["fallback"] not in routes:
            errs.append(f"{rid}: fallback {r['fallback']} unknown")
    return errs


def resolve(routes, rid, m):
    """Follow fallbacks until preflight says a route is ready (unknown = assume ready)."""
    ready = m["target"].get("preflight", {}).get("ready", {})
    seen = []
    while rid and rid != "-" and rid not in seen:
        seen.append(rid)
        r = routes.get(rid, {})
        ui_only = r.get("workflow") == "-" and r.get("stage") in ("still", "still-fix", "video", "video-fix", "vfx", "post", "transition")
        if ready.get(rid, True) and not ui_only:
            return rid, seen
        rid = routes[rid]["fallback"]
    return None, seen


# ---------------------------------------------------------------- schema (subset validator)
def validate(inst, schema, root=None, path="$"):
    root = root or schema; errs = []
    if "$ref" in schema:
        node = root
        for part in schema["$ref"].lstrip("#/").split("/"):
            node = node[part]
        return validate(inst, node, root, path)
    t = schema.get("type")
    if t:
        types = t if isinstance(t, list) else [t]
        ok = any({"string": isinstance(inst, str), "boolean": isinstance(inst, bool), "null": inst is None,
                  "object": isinstance(inst, dict), "array": isinstance(inst, list),
                  "integer": isinstance(inst, int) and not isinstance(inst, bool),
                  "number": isinstance(inst, (int, float)) and not isinstance(inst, bool)}[x] for x in types)
        if not ok:
            return [f"{path}: expected {t}"]
    if "enum" in schema and inst not in schema["enum"]:
        errs.append(f"{path}: {inst!r} not in {schema['enum']}")
    if isinstance(inst, str) and "pattern" in schema and not re.search(schema["pattern"], inst):
        errs.append(f"{path}: does not match {schema['pattern']}")
    if isinstance(inst, (int, float)) and not isinstance(inst, bool):
        if "minimum" in schema and inst < schema["minimum"]: errs.append(f"{path}: < {schema['minimum']}")
        if "maximum" in schema and inst > schema["maximum"]: errs.append(f"{path}: > {schema['maximum']}")
    if isinstance(inst, dict):
        for k in schema.get("required", []):
            if k not in inst: errs.append(f"{path}: missing '{k}'")
        props = schema.get("properties", {})
        for k, v in inst.items():
            if k in props:
                errs += validate(v, props[k], root, f"{path}.{k}")
            elif schema.get("additionalProperties") is False:
                errs.append(f"{path}: unexpected '{k}'")
            elif isinstance(schema.get("additionalProperties"), dict):
                errs += validate(v, schema["additionalProperties"], root, f"{path}.{k}")
    if isinstance(inst, list):
        if len(inst) < schema.get("minItems", 0): errs.append(f"{path}: fewer than {schema['minItems']} items")
        if "items" in schema:
            for i, v in enumerate(inst): errs += validate(v, schema["items"], root, f"{path}[{i}]")
    return errs


def rules(m, routes):
    """Production rules beyond the schema."""
    errs = []
    total = sum(s["duration_s"] for s in m["shots"])
    if abs(total - m["brief"]["length_s"]) > max(1.0, 0.1 * m["brief"]["length_s"]):
        errs.append(f"shot durations sum to {total:.1f}s, brief says {m['brief']['length_s']}s")
    t = 0.0
    for s in m["shots"]:
        if abs(s["start_s"] - t) > 0.05: errs.append(f"{s['id']}: start_s {s['start_s']} != running total {t:.2f}")
        t += s["duration_s"]
        for part in ("still", "video"):
            j = s[part]
            if j["route"] not in routes: errs.append(f"{s['id']}.{part}: unknown route {j['route']}")
            elif part == "video":
                need = [r for r in ("video", "audio") if r in routes[j["route"]]["inputs"] and r != "image"
                        and not (r == "audio" and j["route"].startswith("video.lipsync"))]
                miss = [r for r in need if not (j.get("params") or {}).get(r)]
                if miss: errs.append(f"{s['id']}.video: route {j['route']} needs params {miss} (control clip / audio stem)")
        v = s["video"]
        if routes.get(v["route"], {}).get("skill") in ("ltx25-image-to-video", "lip-sync", "one-take-vfx", "shot-transitions", "ltx-iclora-utils") and not sidecar(routes[v["route"]]):
            if "frames" in v and (v["frames"] - 1) % 8: errs.append(f"{s['id']}: frames {v['frames']} not 8n+1")
            for k in ("width", "height"):
                if k in v and v[k] % 32: errs.append(f"{s['id']}: {k} {v[k]} not a multiple of 32")
        for x in s.get("extra", []):
            if x["route"] not in routes: errs.append(f"{s['id']}.extra: unknown route {x['route']}")
    for k in ("voiceover", "music"):
        if isinstance(m["audio"].get(k), dict) and m["audio"][k].get("route") not in routes: errs.append(f"audio.{k}: unknown route")
    return errs


# ---------------------------------------------------------------- planning helpers
def frames_for(dur, fps):
    return 8 * math.ceil(dur * fps / 8) + 1


def apply_tier(m):
    tp = TIERS[m["tier"]]; fps = m["brief"].get("fps", 24)
    for k, v in tp["caps"].items():
        m["caps"].setdefault(k, v)
    for s in m["shots"]:
        st, vd = s["still"], s["video"]
        st.setdefault("width", tp["still_wh"][0]); st.setdefault("height", tp["still_wh"][1])
        vd.setdefault("width", tp["video_wh"][0]); vd.setdefault("height", tp["video_wh"][1])
        vd.setdefault("fps", fps); vd.setdefault("frames", frames_for(s["duration_s"], fps))
        vd.setdefault("strength1", 1.0 if STATIC.search(s.get("camera", "")) else 0.7)
        vd.setdefault("strength2", 1.0)
    if m["brief"]["aspect"] == "9:16":
        for s in m["shots"]:
            for j in (s["still"], s["video"]):
                if j["width"] > j["height"]: j["width"], j["height"] = j["height"], j["width"]
    elif m["brief"]["aspect"] in ("1:1",):
        for s in m["shots"]:
            for j in (s["still"], s["video"]):
                side = min(j["width"], j["height"]); j["width"] = j["height"] = side


def estimate(m, tier=None):
    tier = tier or m["tier"]; caps = TIERS[tier]["caps"]; rates = {**RATES, **m["cost"].get("rates_s_per_render", {})}
    n = len(m["shots"])
    still_r = rates["still.klein_base"] if TIERS[tier]["still_route"] == "still.klein_base" else rates["still"]
    vid_r = rates.get(f"video@{tier}", rates["video"])
    exp_still = caps["still_variants"] + caps["still_retries"] * 0.5      # expect half the retries
    exp_vid = 1 + caps["video_retries"] * 0.5 + caps["continuity_regens"] * 0.25
    sec = n * (exp_still * (still_r + rates["qa"]) + exp_vid * (vid_r + 3 * rates["qa"]))
    sec += rates["audio"] * (1 + len(m["audio"].get("sfx", []))) + (n * rates["post"] if TIERS[tier]["upscale"] else 0)
    renders = math.ceil(n * (caps["still_variants"] + caps["still_retries"] + 1 + caps["video_retries"] + caps["continuity_regens"]) + 4)
    return round(sec / 60, 1), renders


def pick_tier(m):
    vram = m["target"].get("vram_gb") or 0
    budget = (m["target"].get("budget") or {}).get("max_gpu_minutes")
    ready = m["target"].get("preflight", {}).get("ready", {})
    chosen, why = "draft", []
    for t in ORDER:
        mins, _ = estimate(m, t)
        if vram and vram < TIERS[t]["min_vram"]: why.append(f"{t}: needs {TIERS[t]['min_vram']} GB, have {vram}"); continue
        if budget is not None and mins > budget: why.append(f"{t}: est {mins} GPU-min > budget {budget}"); continue
        if ready and ready.get(TIERS[t]["still_route"]) is False: why.append(f"{t}: {TIERS[t]['still_route']} not ready"); continue
        chosen = t
    return chosen, "; ".join(why) or "all tiers fit; chose highest"


# ---------------------------------------------------------------- execution
class Runner:
    def __init__(s, path, url, dry, routes, only=None):
        s.path, s.url, s.dry, s.routes = path, url, dry, routes
        s.only = set(only or [])  # worker mode (multi-gpu-dispatch): stills+video for these shots only
        s.m = json.load(open(path)); s.step = 0
        s.work = os.path.join(os.path.dirname(os.path.abspath(path)), s.m["id"])

    def save(s):
        if not s.dry:
            tmp = s.path + ".tmp"; json.dump(s.m, open(tmp, "w"), indent=1); os.replace(tmp, s.path)

    def log(s, event, detail=None):
        s.m["log"].append({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": event, **({"detail": detail} if detail else {})})

    def sh(s, cmd, label):
        s.step += 1
        print(f"[{s.step:03}] {label}\n      $ {' '.join(shlex.quote(str(c)) for c in cmd)}")
        if s.dry:
            return {"status": "done", "files": [f"<{label}>"], "verdict": "pass", "name": "<upload>", "texts": []}
        r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
        if r.returncode not in (0, 1):
            raise RuntimeError(f"{label}: {r.stderr[-800:]}")
        try:
            return json.loads(r.stdout[r.stdout.index("{") if r.stdout.lstrip()[0] == "{" else r.stdout.index("["):])
        except Exception:
            return {"raw": r.stdout[-2000:], "returncode": r.returncode}

    def budget_ok(s, kind):
        c = s.m["cost"]; caps = s.m["caps"]
        if c["renders"] >= caps["max_renders"]:
            s.log("cap_hit", {"cap": "max_renders", "at": kind}); return False
        lim = caps.get("max_gpu_minutes")
        if lim is not None and (c.get("actual_gpu_minutes") or 0) >= lim:
            s.log("cap_hit", {"cap": "max_gpu_minutes", "at": kind}); return False
        return True

    def client(s, skill):
        return [sys.executable, os.path.join(SKILLS, skill, "scripts", "comfy_client.py"), "--url", s.url]

    def render(s, rid, values, label, out):
        r = s.routes[rid]; sets = []
        for role, val in values.items():
            if val is None or role not in r["inputs"]:
                continue
            if role in ("image", "last_image", "video", "audio", "voice", "mask") and not str(val).startswith("<"):
                val = s.sh(s.client(r["skill"]) + ["upload", val], f"upload {os.path.basename(str(val))}").get("name", val)
            for t in r["inputs"][role]:
                sets += ["--set", f"{t}={json.dumps(val) if not isinstance(val, str) else val}"]
        wf = os.path.join(SKILLS, r["skill"], "workflows", r["workflow"])
        loc = placeholders(json.load(open(wf)))
        if loc:  # {{PLACEHOLDER}} graphs (motionfield, forkfield): sidecar defaults, then UPPERCASE params, must cover all
            sc = sidecar(r); fill = dict(sc.get("placeholders", {}))
            fill.update({k: v for k, v in values.items() if k.isupper() and v is not None})
            done = {x.split("=", 1)[0] for x in sets[1::2]}
            for ph, ts in loc.items():
                if ph in fill:
                    for tg in ts:
                        if tg not in done: sets += ["--set", f"{tg}={json.dumps(fill[ph]) if not isinstance(fill[ph], str) else fill[ph]}"]; done.add(tg)
            left = sorted(ph for ph, ts in loc.items() if any(tg not in done for tg in ts))
            if left:
                s.log("unfilled_placeholders", {"route": rid, "left": left})
                if not s.dry: raise RuntimeError(f"{rid}: unfilled placeholders {left} - add them to the sidecar or job params")
                print(f"      ! dry-run: unfilled placeholders {left}")
        t0 = time.time()
        res = s.sh(s.client(r["skill"]) + ["run", wf, "--out", out, *sets], label)
        s.m["cost"]["renders"] += 1
        s.m["cost"]["actual_gpu_minutes"] = round((s.m["cost"].get("actual_gpu_minutes") or 0) + (0 if s.dry else (time.time() - t0) / 60), 2)
        files = res.get("files") or []
        return files[0] if files else None

    def judge(s, image, prompt, ref=None):
        cmd = [sys.executable, os.path.join(SKILLS, "still-qa", "scripts", "judge.py"), "--image", image, "--prompt", prompt]
        bible = (s.m.get("bible") or {}).get("path")
        if bible: cmd += ["--bible", bible]
        if ref: cmd += ["--ref", ref]
        return s.sh(cmd, f"judge {os.path.basename(str(image))}")

    def qc(s, video, sh):
        cmd = [sys.executable, os.path.join(SKILLS, "shot-qc", "scripts", "shot_qc.py"), video, "--duration", str(sh["duration_s"]), "--json"]
        if re.search(r"static|locked|tripod", sh.get("camera", ""), re.I): cmd.append("--static")
        return s.sh(cmd, f"shot-qc {sh['id']}")

    def passed(s, j):
        caps = s.m["caps"]; sc = j.get("scores") or {}
        if j.get("verdict") == "pass" and not sc: return True
        return bool(sc) and min(sc.values()) >= caps.get("pass_min", 3) and sum(sc.values()) / len(sc) >= caps.get("pass_mean", 3.5)

    def frame(s, video, where, out):
        args = ["-sseof", "-0.05"] if where == "last" else (["-ss", "50%"] if where == "mid" else [])
        if where == "mid":  # seek to half the probed duration (the select filter has no n_frames constant)
            half = "0"
            if not s.dry:
                pr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)], capture_output=True, text=True)
                try: half = f"{float(pr.stdout.strip()) / 2:.3f}"
                except ValueError: pass
            cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", half, "-i", video, "-frames:v", "1", out]
        else:
            cmd = ["ffmpeg", "-y", "-loglevel", "error", *args, "-i", video, "-frames:v", "1", out]
        s.sh(cmd, f"frame {where} of {os.path.basename(str(video))}")
        return out

    def gate(s, name):
        g = s.m["gates"].get(name, "auto")
        if g == "human":
            s.log("awaiting_approval", {"gate": name}); s.save()
            print(f"== GATE '{name}': waiting for human approval. Run: direct.py approve {s.path} {name}")
            return s.dry  # dry-run continues to show the rest of the plan
        return g != "rejected"

    # ---- stages
    def run(s):
        m = s.m; os.makedirs(s.work, exist_ok=True) if not s.dry else None
        errs = validate(m, json.load(open(SCHEMA))) + rules(m, s.routes)
        if errs:
            print("manifest invalid:\n  " + "\n  ".join(errs)); return 2
        apply_tier(m)
        mins, renders = estimate(m)
        m["cost"]["estimate_gpu_minutes"] = mins
        m["caps"].setdefault("max_renders", renders)
        print(f"== {m['id']}: tier={m['tier']} shots={len(m['shots'])} est={mins} GPU-min (rates are assumptions) caps={m['caps']}")
        st = m["stages"]
        if st.get("preflight") != "done":
            wfs = sorted({os.path.join(SKILLS, r["skill"], "workflows", r["workflow"]) for r in s.routes.values()
                          if r["workflow"] not in ("-",) and not r["workflow"].startswith("script:")})
            pf = [sys.executable, os.path.join(SKILLS, "comfyui-preflight", "scripts", "preflight.py"), "--url", s.url]
            ready = m["target"].setdefault("preflight", {"ran": False, "ready": {}, "missing_nodes": [], "missing_weights": []})
            if s.dry:
                s.sh(pf + [f"<{len(wfs)} routed workflows>"], "preflight (one call per workflow)")
            else:
                for rid, r in s.routes.items():
                    if r["workflow"] == "-" or r["workflow"].startswith("script:"): continue
                    res = s.sh(pf + [os.path.join(SKILLS, r["skill"], "workflows", r["workflow"])], f"preflight {rid}")
                    ready["ready"][rid] = bool(res.get("ready"))
                    ready["missing_nodes"] = sorted(set(ready["missing_nodes"]) | set(res.get("missing_node_types", [])))
                    ready["missing_weights"] = sorted(set(ready["missing_weights"]) | {w["file"] for w in res.get("missing_weight_files", [])})
                ready["ran"] = True
                t_, why = pick_tier(m)
                if ORDER.index(t_) < ORDER.index(m["tier"]):
                    s.log("tier_downgrade", {"from": m["tier"], "to": t_, "why": why}); m["tier"], m["tier_reason"] = t_, why
                    apply_tier(m)
            st["preflight"] = "done"
        for g, stage in (("bible", "bible"), ("plan", "plan")):
            if st.get(stage) != "done":
                if not s.gate(g): return 3
                st[stage] = "done"
        if not s.gate("spend"): return 3
        if s.only:  # worker mode: no stage-level status writes; the coordinator run does continuity onward
            for stage, fn in (("stills", s.stills), ("video", s.videos)):
                print(f"-- worker stage: {stage} {sorted(s.only)}"); r = fn() or "done"; s.save()
                if r != "done": print(f"worker stopped at {stage}: {r}"); return 4
            return 0
        for stage, fn in (("stills", s.stills), ("video", s.videos), ("continuity", s.continuity), ("audio", s.audio),
                          ("post", s.post), ("assembly", s.assemble), ("critique", s.critique)):
            if st.get(stage) == "done":
                print(f"-- {stage}: done (resume skip)"); continue
            print(f"-- stage: {stage}")
            st[stage] = "running"; s.save()
            st[stage] = fn() or "done"; s.save()
            if st[stage] in ("blocked", "failed", "awaiting_approval"):
                print(f"stopped at {stage}: {st[stage]}"); return 4
        if s.dry:
            print(f"== dry run complete: {s.step} steps planned, est {mins} GPU-min, render cap {m['caps']['max_renders']}. No network calls were made.")
        return 0

    def stills(s):
        caps, out = s.m["caps"], os.path.join(s.work, "stills"); blocked = False
        for sh in s.m["shots"]:
            j = sh["still"]
            if j["status"] == "done" or (s.only and sh["id"] not in s.only): continue
            rid, chain = resolve(s.routes, j["route"], s.m)
            if not rid: j["status"] = "blocked"; s.log("no_route", {"shot": sh["id"], "tried": chain}); blocked = True; continue
            j.setdefault("attempts", []); prompt = j.get("prompt", ""); seed = j.get("seed") or 1000 + int(sh["id"][1:3]) * 7
            ref = j.get("ref")
            for n in range(len(j["attempts"]) + 1, 2 + caps["still_retries"] + caps.get("still_variants", 1) - 1):
                if not s.budget_ok("still"): j["status"] = "blocked"; return "blocked"
                f = s.render(rid, {"prompt": prompt, "seed": seed, "width": j["width"], "height": j["height"]}, f"still {sh['id']} #{n} ({rid})", out)
                v = s.judge(f, prompt, ref)
                ok = s.passed(v)
                j["attempts"].append({"n": n, "route": rid, "seed": seed, "prompt": prompt, "ref": ref, "file": f,
                                      "scores": v.get("scores", {}), "verdict": "pass" if ok else "retry", "fix": v.get("fix")})
                s.save()
                if ok and n >= caps.get("still_variants", 1):
                    break
                # judge loop: re-prompt with the judge's fix, new seed; on identity issues swap the reference
                fix = v.get("fix") or ""
                if fix and not s.dry: prompt = f"{prompt} {fix}".strip()
                if any("identity" in str(i).lower() for i in v.get("issues", [])) and sh.get("cast"):
                    ref = next((c.get("ref_image") for c in s.m.get("bible", {}).get("cast", []) if c["id"] == sh["cast"][0]), ref)
                seed += 1
            best = max(j["attempts"], key=lambda a: (a["verdict"] == "pass", sum((a.get("scores") or {}).values())))
            if best["verdict"] == "pass" or s.m["tier"] == "draft":
                j["approved"], j["seed"], j["status"] = best["file"], best["seed"], "done"
            else:
                j["status"] = "awaiting_approval"; blocked = True
                s.log("still_cap_reached", {"shot": sh["id"], "best": best["file"]})
        return "awaiting_approval" if blocked else "done"

    def video_one(s, sh, why):
        j = sh["video"]; caps = s.m["caps"]; out = os.path.join(s.work, "video")
        rid, chain = resolve(s.routes, j["route"], s.m)
        if not rid: j["status"] = "blocked"; return False
        sc = sidecar(s.routes[rid])
        if sc.get("fps"):  # Wan-family graphs: own fps + 4n+1 frame lattice instead of the LTX 8n+1 default
            step = 4 if sc.get("frame_rule") == "4n+1" else 8
            j["fps"] = sc["fps"]; j["frames"] = step * math.ceil(sh["duration_s"] * sc["fps"] / step) + 1
        if sc.get("duration_placeholder"):
            j.setdefault("params", {}).setdefault(sc["duration_placeholder"], str(max(2, round(sh["duration_s"]))))
        prev = next((x for x in s.m["shots"] if x["id"] == sh.get("chain_from")), None)
        start_img, last = sh["still"].get("approved"), None
        if prev and prev["video"].get("approved"):
            # keyframe chaining: shot N's last frame starts shot N+1; the approved still becomes the end target if the route takes one
            chained = s.frame(prev["video"]["approved"], "last", f"{prev['video']['approved']}.chain.png")
            if "last_image" in s.routes[rid]["inputs"]:
                start_img, last = chained, sh["still"].get("approved")
            else:
                start_img = chained
        j.setdefault("attempts", []); seed = j.get("seed") or 5000 + int(sh["id"][1:3]) * 11
        start = len([a for a in j["attempts"]]) + 1
        for n in range(start, start + 1 + caps["video_retries"]):
            if not s.budget_ok("video"): return False
            vals = {"image": start_img, "last_image": last, "prompt": j.get("prompt", ""), "seed": seed,
                    "width": j["width"], "height": j["height"], "frames": j["frames"],
                    "strength1": j.get("strength1"), "strength2": j.get("strength2"), "fps": j.get("fps"),
                    "audio": (sh.get("extra") or [{}])[0].get("params", {}).get("audio") if rid.startswith("video.lipsync") else None,
                    "negative": ""}
            vals.update(j.get("params") or {})  # e.g. {"video": control clip, "audio": stem} for control/audio-driven routes
            f = s.render(rid, vals, f"video {sh['id']} #{n} ({rid}) [{why}]", out)
            q = s.qc(f, sh)  # shot-qc measurements: freeze/black = failed attempt (numbers beat the VLM)
            frames = [s.frame(f, w, f"{f}.{w}.png") for w in ("first", "mid", "last")]
            verdicts = [s.judge(fr, j.get("prompt", ""), sh["still"].get("approved")) for fr in frames]
            ok = all(s.passed(v) for v in verdicts) and q.get("pass", True)
            j["attempts"].append({"n": n, "route": rid, "seed": seed, "prompt": j.get("prompt", ""), "file": f,
                                  "verdict": "pass" if ok else "retry", "fix": next((v.get("fix") for v in verdicts if v.get("fix")), None)})
            s.save()
            if ok: j["approved"], j["seed"], j["status"] = f, seed, "done"; return True
            seed += 1
        best = j["attempts"][-1]; j["approved"] = best["file"]
        j["status"] = "done" if s.m["tier"] == "draft" else "awaiting_approval"
        return j["status"] == "done"

    def videos(s):
        bad = False
        for sh in s.m["shots"]:
            if s.only and sh["id"] not in s.only: continue
            if sh["video"]["status"] != "done":
                bad |= not s.video_one(sh, "first pass")
            for x in sh.get("extra", []):
                if x["status"] != "done":
                    rid, _ = resolve(s.routes, x["route"], s.m)
                    if rid:
                        x["file"] = s.render(rid, {**x.get("params", {}), "video": sh["video"].get("approved")}, f"extra {sh['id']} ({rid})", os.path.join(s.work, "extra"))
                        x["status"] = "done"
            sh["status"] = "done" if sh["video"]["status"] == "done" else sh["video"]["status"]
        return "awaiting_approval" if bad else "done"

    def continuity(s):
        caps = s.m["caps"]; shots = s.m["shots"]
        for a, b in zip(shots, shots[1:]):
            c = b.setdefault("continuity", {"status": "pending", "regens": 0, "findings": []})
            if c["status"] == "done": continue
            while True:
                fa = s.frame(a["video"]["approved"], "last", f"{a['video']['approved']}.last.png")
                fb = s.frame(b["video"]["approved"], "first", f"{b['video']['approved']}.first.png")
                v = s.judge(fb, "Same characters, wardrobe, props, lighting and screen direction as the reference frame?", fa)
                c["findings"].append({"join": f"{a['id']}->{b['id']}", "verdict": v.get("verdict"), "fix": v.get("fix")})
                if s.passed(v) or b.get("transition_in") in ("flf",):
                    c["status"] = "done"; break
                if c["regens"] >= caps["continuity_regens"]:
                    c["status"] = "done"; s.log("continuity_cap", {"join": f"{a['id']}->{b['id']}"}); break
                c["regens"] += 1; b["video"]["status"] = "pending"; b["video"]["seed"] = (b["video"].get("seed") or 0) + 101
                s.video_one(b, f"continuity regen {c['regens']}")
            if b.get("transition_in") == "flf":
                rid, _ = resolve(s.routes, TIERS[s.m["tier"]]["transition"], s.m)
                if rid and s.routes[rid]["workflow"] != "-":
                    s.render(rid, {"image": fa, "last_image": fb, "prompt": f"seamless transition from {a['id']} to {b['id']}"},
                             f"transition {a['id']}->{b['id']} ({rid})", os.path.join(s.work, "transitions"))
            s.save()
        return "done"

    def audio(s):
        au, out = s.m["audio"], os.path.join(s.work, "audio")
        vo = au.get("voiceover")
        if vo and vo["status"] != "done":
            text = " ".join(x["narration"] for x in s.m["shots"] if x.get("narration"))
            vo["file"] = s.render(vo["route"], {"text": text, "seed": vo.get("seed") or 7, **vo.get("params", {})}, "voiceover", out); vo["status"] = "done"
        mu = au.get("music")
        if mu and mu["status"] != "done":
            p = {"seconds": s.m["brief"]["length_s"] + 2, "seed": mu.get("seed") or 11, **mu.get("params", {})}
            mu["file"] = p.get("file") or s.render(resolve(s.routes, mu["route"], s.m)[0], p, "music", out); mu["status"] = "done"
        for i, fx in enumerate(au.get("sfx", [])):
            if fx["status"] != "done":
                fx["file"] = s.render(resolve(s.routes, fx["route"], s.m)[0], {"seed": 20 + i, **fx.get("params", {})}, f"sfx {i+1}", out); fx["status"] = "done"
        return "done"

    def post(s):
        tp = TIERS[s.m["tier"]]
        for sh in s.m["shots"]:
            if tp["upscale"] and not any(p.get("params", {}).get("shot") == sh["id"] for p in s.m.get("post", [])):
                s.m.setdefault("post", []).append({"route": "post.upscale", "status": "pending", "params": {"shot": sh["id"]}})
        for p in s.m.get("post", []):
            if p["status"] == "done": continue
            sh = next((x for x in s.m["shots"] if x["id"] == p.get("params", {}).get("shot")), None)
            rid, _ = resolve(s.routes, p["route"], s.m)
            if rid and sh:
                p["file"] = s.render(rid, {**p["params"], "video": sh["video"]["approved"]}, f"post {rid} {sh['id']}", os.path.join(s.work, "post"))
                sh["video"]["approved"] = p["file"] or sh["video"]["approved"]
            p["status"] = "done"
        return "done"

    def assemble(s):
        m, a = s.m, s.m["assembly"]; out = os.path.join(s.work, f"{m['id']}.mp4")
        clips = [x["video"]["approved"] for x in m["shots"]]
        cmd = [sys.executable, os.path.join(SKILLS, "film-assembly", "scripts", "assemble.py"), "--clips", *clips,
               "--aspect", m["brief"]["aspect"], "--fps", str(m["brief"].get("fps", 24)), "--xfade", str(a.get("xfade", 0)),
               "--durations", *[str(x["duration_s"]) for x in m["shots"]], "--out", out, "--run"]
        if m["audio"].get("voiceover", {}).get("file"): cmd += ["--narration", m["audio"]["voiceover"]["file"]]
        if m["audio"].get("music", {}).get("file"): cmd += ["--music", m["audio"]["music"]["file"]]
        if a.get("beats_file"): cmd += ["--beats", a["beats_file"]]
        s.sh(cmd, "assemble")
        cap = a.get("captions", m["brief"].get("captions", "sidecar"))
        if cap != "off":
            srt = out.replace(".mp4", ".srt")
            c = [sys.executable, os.path.join(SKILLS, "subtitles-captions", "scripts", "make_srt.py"), "--manifest", s.path, "--out", srt]
            if cap in ("burned", "both"): c += ["--burn", out, "--burned", out.replace(".mp4", "_captioned.mp4"), "--run"]
            s.sh(c, "captions")
        for e in a.get("exports", []):
            if e["aspect"] != m["brief"]["aspect"]:
                if e.get("method") == "reframe":
                    print(f"      (export {e['aspect']}: reframe route post.reframe per shot, then re-assemble)")
                else:
                    ec = list(cmd); ec[ec.index("--aspect") + 1] = e["aspect"]
                    ec[ec.index("--out") + 1] = out.replace(".mp4", f"_{e['aspect'].replace(':', 'x')}.mp4")
                    s.sh(ec, f"export {e['aspect']}")
        a["output"] = out
        return "done"

    def critique(s):
        m = s.m; rep = os.path.join(s.work, "REPORT.md")
        mid = [s.frame(m["assembly"]["output"], "mid", rep.replace("REPORT.md", "final_mid.png"))]
        v = s.judge(mid[0], m["brief"]["prompt"] + " | style: " + m["brief"]["style"])
        m.setdefault("critique", {})["scores"] = v.get("scores", {})
        lines = [f"# {m['id']}: production report", f"- tier: {m['tier']} ({m.get('tier_reason', '')})",
                 f"- renders: {m['cost']['renders']} / cap {m['caps']['max_renders']}; GPU-min est {m['cost'].get('estimate_gpu_minutes')} actual {m['cost'].get('actual_gpu_minutes')}",
                 "", "| shot | still route/seed | video route/seed | attempts | continuity regens |", "|---|---|---|---|---|"]
        for x in m["shots"]:
            lines.append(f"| {x['id']} | {x['still']['route']}/{x['still'].get('seed')} | {x['video']['route']}/{x['video'].get('seed')} | "
                         f"{len(x['still'].get('attempts', []))}+{len(x['video'].get('attempts', []))} | {x.get('continuity', {}).get('regens', 0)} |")
        lines += ["", "Weight licenses: see each skill's references/requirements.md. LTX weights: Lightricks LTX license (not OSI)."]
        if not s.dry:
            open(rep, "w").write("\n".join(lines) + "\n")
        print("      (report) " + rep)
        m["critique"]["report"] = rep
        return "done"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("routes")
    for c in ("validate", "tier"):
        sp.add_parser(c).add_argument("manifest")
    r = sp.add_parser("run"); r.add_argument("manifest"); r.add_argument("--url", default=os.environ.get("COMFY_URL", "http://127.0.0.1:8188"))
    r.add_argument("--dry-run", action="store_true")
    r.add_argument("--target", choices=["comfyui", "google-colab"], default="comfyui",
                   help="google-colab: drive a running Google Colab ComfyUI (CU estimate, spend gate, hard cap, resume)")
    r.add_argument("--max-cu", type=float, help="google-colab: hard compute-unit cap (default target.budget.max_credits)")
    r.add_argument("--teardown", choices=["offer", "on-cap", "auto"], default="offer")
    pk = sp.add_parser("package", help="build a self-contained bundle for another runtime")
    pk.add_argument("--target", choices=["google-colab"], required=True); pk.add_argument("manifest")
    pk.add_argument("--out", default="dist"); pk.add_argument("--no-zip", action="store_true")
    r.add_argument("--only", default="", help="comma shot ids: worker mode for multi-gpu-dispatch (stills+video only)")
    ap = sp.add_parser("approve"); ap.add_argument("manifest"); ap.add_argument("gate", choices=["bible", "plan", "spend", "final"])
    a = p.parse_args()
    routes = load_routes()
    if a.cmd == "routes":
        for rid, rr in routes.items():
            print(f"{rid:20} {rr['stage']:11} {rr['skill']:22} {rr['workflow']:45} -> {rr['fallback']}")
        errs = check_routes(routes); print("route errors:", errs or "none"); return 1 if errs else 0
    if a.cmd == "package" or (a.cmd == "run" and a.target == "google-colab" and not a.dry_run):
        sys.path.insert(0, os.path.join(SKILLS, "google-colab-runner", "scripts"))
        import colab
        if a.cmd == "package":
            return colab.main(["package", a.manifest, "--out", a.out] + (["--no-zip"] if a.no_zip else []))
        return colab.main(["orchestrate", a.manifest, "--url", a.url, "--teardown", a.teardown] + (["--max-cu", str(a.max_cu)] if a.max_cu is not None else []))
    m = json.load(open(a.manifest))
    if a.cmd == "validate":
        errs = validate(m, json.load(open(SCHEMA))) + rules(m, routes) + check_routes(routes)
        print(json.dumps({"manifest": a.manifest, "valid": not errs, "errors": errs}, indent=1)); return 1 if errs else 0
    if a.cmd == "tier":
        t, why = pick_tier(m); print(json.dumps({"tier": t, "reason": why, "estimates": {k: estimate(m, k) for k in ORDER}})); return 0
    if a.cmd == "approve":
        m["gates"][a.gate] = "approved"; json.dump(m, open(a.manifest, "w"), indent=1); print(f"gate {a.gate} approved"); return 0
    return Runner(a.manifest, a.url, a.dry_run, routes, [x for x in a.only.split(",") if x]).run()


if __name__ == "__main__":
    sys.exit(main())
