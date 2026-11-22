#!/usr/bin/env python3
"""Stdlib mock of the ComfyUI HTTP API (plus an OpenAI-style VLM judge) for static tests.

  python mock_comfy.py --port 8199 [--gpu "NVIDIA L4" --vram-gb 24] [--drop-after N]

It accepts /prompt, /history, /queue, /upload/image, /view, /interrupt, /system_stats and
/v1/chat/completions. Each prompt "renders" instantly: a PNG for image graphs, an MP4 for video
graphs and a WAV for audio graphs, made once with ffmpeg. --drop-after N makes the server exit
after N prompts, to simulate a dropped Google Colab session. No GPU, no models, no network.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile, threading, time, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

A = None; STATE = {"history": {}, "n": 0, "uploads": 0}
TMP = tempfile.mkdtemp(prefix="mockcomfy-")
VIDEO = {"SaveVideo", "VHS_VideoCombine", "CreateVideo", "SaveWEBM", "SaveAnimatedWEBP"}
AUDIO = {"SaveAudio", "SaveAudioMP3", "SaveAudioOpus", "SaveAudioFLAC"}


def object_info():
    import glob
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    cls = set()
    for p in glob.glob(os.path.join(root, "*", "workflows", "**", "*.api.json"), recursive=True):
        try: cls |= {n["class_type"] for n in json.load(open(p)).values() if isinstance(n, dict) and "class_type" in n}
        except Exception: pass
    return {c: {"input": {"required": {}, "optional": {}}, "output_node": c.startswith(("Save", "VHS_VideoCombine", "Preview"))} for c in cls}


OBJECT_INFO = object_info()


def make_media():
    ff = ["ffmpeg", "-y", "-loglevel", "error"]
    subprocess.run(ff + ["-f", "lavfi", "-i", "testsrc=size=320x192:rate=24", "-frames:v", "1", f"{TMP}/still.png"], check=True)
    subprocess.run(ff + ["-f", "lavfi", "-i", "testsrc=size=320x192:rate=24:duration=10", "-f", "lavfi", "-i", "sine=f=440:duration=10",
                         "-pix_fmt", "yuv420p", "-c:v", "libx264", "-c:a", "aac", "-shortest", f"{TMP}/clip.mp4"], check=True)
    subprocess.run(ff + ["-f", "lavfi", "-i", "sine=f=330:duration=40", f"{TMP}/sound.wav"], check=True)


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send(self, obj, code=200, raw=None, ctype="application/json"):
        body = raw if raw is not None else json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)

    def gone(self):
        if STATE.get("dead"):
            self.close_connection = True; self.connection.close(); return True
        return False

    def do_GET(self):
        if self.gone(): return
        u = urlparse(self.path)
        if u.path == "/system_stats":
            return self.send({"system": {"os": "mock", "comfyui_version": "mock"}, "devices": [{"name": A.gpu, "type": "cuda", "vram_total": int(A.vram_gb * 2**30)}]})
        if u.path.startswith("/history/"):
            pid = u.path.split("/")[-1]
            return self.send({pid: STATE["history"][pid]} if pid in STATE["history"] else {})
        if u.path == "/queue":
            return self.send({"queue_running": [], "queue_pending": []})
        if u.path == "/view":
            fn = parse_qs(u.query)["filename"][0]
            p = os.path.join(TMP, "out", fn)
            return self.send(None, raw=open(p, "rb").read(), ctype="application/octet-stream") if os.path.isfile(p) else self.send({"error": "nf"}, 404)
        if u.path == "/object_info":  # every class the collection's API workflows use, with open input specs
            return self.send(OBJECT_INFO)
        self.send({"error": "not found"}, 404)

    def do_POST(self):
        if self.gone(): return
        u = urlparse(self.path); n = int(self.headers.get("Content-Length") or 0); data = self.rfile.read(n)
        if u.path == "/prompt":
            wf = json.loads(data)["prompt"]
            bad = [k for k, v in wf.items() if not isinstance(v, dict) or "class_type" not in v]
            if bad: return self.send({"error": "invalid prompt", "node_errors": {k: "no class_type" for k in bad}}, 400)
            for nid, v in wf.items():  # every upstream link must point at a node in the graph
                for k, x in v.get("inputs", {}).items():
                    if isinstance(x, list) and len(x) == 2 and isinstance(x[1], int) and str(x[0]) not in wf:
                        return self.send({"error": "bad link", "node_errors": {nid: f"{k} -> {x[0]}"}}, 400)
            left = [m for v in wf.values() for x in v.get("inputs", {}).values() if isinstance(x, str) for m in re.findall(r"\{\{[A-Z_]+\}\}", x)]
            if left: return self.send({"error": "unfilled placeholders", "node_errors": {"*": left}}, 400)
            STATE["n"] += 1; pid = uuid.uuid4().hex; types = {v["class_type"] for v in wf.values()}
            audio = bool(types & AUDIO) or any("Save" in t and "Audio" in t for t in types)
            kind = "videos" if types & VIDEO else ("audio" if audio else "images")
            src = {"videos": "clip.mp4", "audio": "sound.wav", "images": "still.png"}[kind]
            ext = os.path.splitext(src)[1]; fn = f"mock_{STATE['n']:04d}{ext}"
            os.makedirs(os.path.join(TMP, "out"), exist_ok=True); shutil.copy(os.path.join(TMP, src), os.path.join(TMP, "out", fn))
            STATE["history"][pid] = {"status": {"status_str": "success", "messages": []},
                                     "outputs": {"9": {kind: [{"filename": fn, "subfolder": "", "type": "output"}]}}}
            self.send({"prompt_id": pid, "number": STATE["n"], "node_errors": {}})
            if A.drop_after and STATE["n"] >= A.drop_after:
                STATE["dead"] = True  # the next request finds the "session" gone
                threading.Thread(target=lambda: (time.sleep(2), os._exit(0)), daemon=True).start()
            return
        if u.path == "/upload/image":
            m = re.search(rb'filename="([^"]+)"', data); name = m.group(1).decode() if m else "upload.bin"
            STATE["uploads"] += 1
            os.makedirs(os.path.join(TMP, "input"), exist_ok=True); open(os.path.join(TMP, "input", name), "wb").write(data)
            return self.send({"name": name, "subfolder": "", "type": "input"})
        if u.path in ("/interrupt", "/queue", "/free"):
            return self.send({})
        if u.path.endswith("/chat/completions"):
            verdict = {"scores": {"prompt": 4, "identity": 4, "composition": 4, "artifacts": 4}, "verdict": "pass", "issues": [], "fix": ""}
            return self.send({"choices": [{"message": {"content": json.dumps(verdict)}}]})
        self.send({"error": "not found"}, 404)


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--port", type=int, default=8199)
    p.add_argument("--gpu", default="NVIDIA L4"); p.add_argument("--vram-gb", type=float, default=24)
    p.add_argument("--drop-after", type=int, default=0)
    A = p.parse_args(); make_media()
    print(f"mock ComfyUI on 127.0.0.1:{A.port} ({A.gpu}, {A.vram_gb} GB) media in {TMP}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", A.port), H).serve_forever()
