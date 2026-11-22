#!/usr/bin/env python3
"""Static end-to-end tests for google-colab-runner. No Google Colab session, no GPU, no compute units.

  python tests/test_static.py

1. package the 3 example manifests; validate JSON, nbformat 4 structure (and nbformat if installed),
   and that no notebook or bundle file contains a token-shaped string.
2. run the bundle runner against mock_comfy.py, including a dropped session and a resume.
3. drive the mock as a Google Colab ComfyUI with direct.py --target google-colab: spend gate,
   hard cap, full QA loop, drop + resume with cached-asset re-upload, teardown request, ingest.
"""
import base64, io, json, os, re, shutil, socket, subprocess, sys, tempfile, time, urllib.request, zipfile

T = os.path.dirname(os.path.abspath(__file__)); SKILL = os.path.dirname(T); SKILLS = os.path.dirname(SKILL)
DIRECT = os.path.join(SKILLS, "video-director", "scripts", "direct.py")
COLAB = os.path.join(SKILL, "scripts", "colab.py")
EX = os.path.join(SKILLS, "video-director", "references", "examples")
PY = sys.executable; W = tempfile.mkdtemp(prefix="gcr-test-"); OK = []
SECRET = re.compile(r"(hf_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{10,}\.eyJ)")


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg); OK.append(bool(cond))


def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


def mock(port, *extra):
    p = subprocess.Popen([PY, os.path.join(T, "mock_comfy.py"), "--port", str(port), *extra], stdout=subprocess.PIPE, text=True)
    p.stdout.readline(); return p


def run(*cmd, env=None):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, env={**os.environ, **(env or {})})
    return r.returncode, r.stdout + r.stderr


# ------------------------------------------------ 1. package
try:
    import nbformat
except ImportError:
    nbformat = None
bundles = {}
for f in sorted(os.listdir(EX)):
    if not f.endswith(".manifest.json"): continue
    code, out = run(PY, DIRECT, "package", "--target", "google-colab", os.path.join(EX, f), "--out", os.path.join(W, "dist"))
    check(code == 0, f"package {f}")
    mid = json.load(open(os.path.join(EX, f)))["id"]; b = os.path.join(W, "dist", f"{mid}-google-colab"); bundles[mid] = b
    nbp = os.path.join(b, f"{mid}.ipynb"); nb = json.load(open(nbp))
    check(nb["nbformat"] == 4 and all(c["cell_type"] in ("markdown", "code") and isinstance(c["source"], list) for c in nb["cells"]), f"{mid}: nbformat 4 structure ({len(nb['cells'])} cells)")
    if nbformat:
        try: nbformat.validate(nbformat.reads(open(nbp).read(), as_version=4)); check(True, f"{mid}: nbformat.validate")
        except Exception as e: check(False, f"{mid}: nbformat.validate {e}")
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            src = "".join(c["source"])
            try: compile(src, "cell", "exec")
            except SyntaxError as e: check(False, f"{mid}: cell does not compile: {e}")
    check(all(SECRET.search(open(os.path.join(r, x), errors="ignore").read()) is None for r, _, fs in os.walk(b) for x in fs), f"{mid}: no token-shaped strings in the bundle")
    payload = re.search(r'PAYLOAD = "([^"]+)"', "".join("".join(c["source"]) for c in nb["cells"])).group(1)
    names = zipfile.ZipFile(io.BytesIO(base64.b64decode(payload))).namelist()
    check("jobs.json" in names and "runner.py" in names and "comfy_client.py" in names, f"{mid}: payload embeds jobs, runner, client ({len(names)} files)")
    jobs = json.load(open(os.path.join(b, "jobs.json")))
    for t, p in jobs["tiers"].items():
        for j in p["jobs"]:
            wf = json.load(open(os.path.join(b, j["workflow"])))
            if not all("class_type" in n for n in wf.values()) or "nodes" in wf:
                check(False, f"{mid}/{j['id']}: not API format")
    check(True, f"{mid}: {sum(len(p['jobs']) for p in jobs['tiers'].values())} API workflows across tiers {list(jobs['tiers'])}")
    check(os.path.isfile(b + ".zip"), f"{mid}: zip written")

# ------------------------------------------------ 2. bundle runner vs mock (with a drop)
b = bundles["lighthouse-short"]; port = free_port(); url = f"http://127.0.0.1:{port}"
m = mock(port, "--drop-after", "3")
code, out = run(PY, os.path.join(b, "runner.py"), "--url", url, "--gpu-name", "NVIDIA L4", "--vram-gb", "24", "--out", os.path.join(W, "out"))
check(code == 5 and "unreachable" in out, f"runner: dropped session detected (exit {code})")
m.wait(10); m = mock(port)
code, out = run(PY, os.path.join(b, "runner.py"), "--url", url, "--gpu-name", "NVIDIA L4", "--vram-gb", "24", "--out", os.path.join(W, "out"))
st = json.load(open(os.path.join(W, "out", "state.json")))
check(code == 0 and all(v["status"] == "done" for v in st["jobs"].values()), f"runner: resumed and finished {len(st['jobs'])} jobs at tier {st['tier']}")
check(out.count("skip ") >= 2, "runner: finished jobs were skipped on resume")
code, out = run(PY, os.path.join(b, "runner.py"), "--list", "--gpu-name", "Tesla T4", "--vram-gb", "15")
check("tier draft" in out, "runner: T4 picks the draft tier")
zp = shutil.make_archive(os.path.join(W, "lighthouse-outputs"), "zip", os.path.join(W, "out"))
mf = os.path.join(W, "ingest.manifest.json"); shutil.copy(os.path.join(EX, "story-short-30s.manifest.json"), mf)
code, out = run(PY, COLAB, "ingest", mf, zp)
check(code == 0 and "ingested" in out, "ingest: outputs attached as unjudged attempts")
m.terminate(); m.wait()

# ------------------------------------------------ 3. orchestrate vs mock
d = os.path.join(W, "orch"); os.makedirs(d); mf = os.path.join(d, "lighthouse.manifest.json")
man = json.load(open(os.path.join(EX, "story-short-30s.manifest.json")))
man["target"]["budget"]["max_credits"] = 0.1
bib = os.path.join(d, "bible.md"); open(bib, "w").write("# bible\nKeeper: grey beard, navy coat.\n"); man.setdefault("bible", {})["path"] = bib
json.dump(man, open(mf, "w"), indent=1)
port = free_port(); url = f"http://127.0.0.1:{port}"; env = {"VLM_ENDPOINT": url + "/v1"}
code, out = run(PY, DIRECT, "run", mf, "--target", "google-colab", "--url", url, env=env)
check(code == 5, "orchestrate: unreachable URL refused before any work")
m = mock(port, "--drop-after", "6")
code, out = run(PY, DIRECT, "run", mf, "--target", "google-colab", "--url", url, env=env)
check(code == 6 and "hard cap" in out, "orchestrate: estimate over the compute-unit cap is refused")
man = json.load(open(mf)); man["target"]["budget"]["max_credits"] = 50; json.dump(man, open(mf, "w"), indent=1)
code, out = run(PY, DIRECT, "run", mf, "--target", "google-colab", "--url", url, env=env)
check(code == 3 and "GATE 'spend'" in out, "orchestrate: spend gate asks before starting (even when the manifest said auto)")
run(PY, DIRECT, "approve", mf, "spend"); run(PY, DIRECT, "approve", mf, "plan")
code, out = run(PY, DIRECT, "run", mf, "--target", "google-colab", "--url", url, env=env)
check(code == 5 and "session dropped" in out, f"orchestrate: dropped session saved and reported (exit {code})")
m.wait(10); port2 = free_port(); url2 = f"http://127.0.0.1:{port2}"; m = mock(port2)
code, out = run(PY, DIRECT, "run", mf, "--target", "google-colab", "--url", url2, env={"VLM_ENDPOINT": url2 + "/v1"})
man = json.load(open(mf))
check(code == 0, f"orchestrate: resumed on a new session URL and finished (exit {code})" + ("" if code == 0 else "\n" + out[-1500:]))
check(man["target"]["colab"].get("drops") == 1 and any(x["event"] == "session_resumed" for x in man["log"]), "orchestrate: drop recorded, CU carried over")
check(all(s["video"]["status"] == "done" for s in man["shots"]) and man["stages"].get("critique") == "done", "orchestrate: all shots done through critique")
check("upload" in out, "orchestrate: cached local assets re-uploaded to the new session")
code, out = run(PY, COLAB, "teardown", "--url", url2)
check(code == 0 and "teardown requested" in out, "teardown: sentinel uploaded for the notebook watchdog")
m.terminate(); m.wait()

print(f"\n{sum(OK)}/{len(OK)} checks passed. work dir: {W}")
sys.exit(0 if all(OK) else 1)
