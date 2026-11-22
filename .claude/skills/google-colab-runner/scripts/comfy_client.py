#!/usr/bin/env python3
"""Minimal ComfyUI API client (Python stdlib only).

Works with any ComfyUI server URL: local, a Google Colab tunnel, or a
self-hosted/cloud instance that exposes the standard ComfyUI HTTP API.

Commands:
  run      submit an API-format workflow, wait, download outputs
  submit   submit only; prints prompt_id
  wait     wait for one or more prompt_ids (timeout returns live status, not an error)
  fetch    download outputs of a finished prompt_id
  cancel   cancel a prompt_id (POST /interrupt if running, POST /queue delete if queued)
  upload   upload an image/audio/video input file (POST /upload/image)

Overrides: --set NODE_ID.INPUT=VALUE (VALUE parsed as JSON when possible).
Auth: set COMFY_API_KEY to send "Authorization: Bearer <key>" (unverified for
any particular hosted provider; check its docs). Wait/cancel semantics are adapted
from jalajbhandula/motionfield job_wait/job_cancel (MIT); see NOTICE.
"""
import argparse, json, mimetypes, os, sys, time, uuid
import urllib.parse, urllib.request, urllib.error

DEFAULT_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188")


def _req(base, path, data=None, method=None, headers=None, raw=False, timeout=60):
    url = base.rstrip("/") + path
    h = {"User-Agent": "skills-comfy-client/1"}
    if os.environ.get("COMFY_API_KEY"):
        h["Authorization"] = "Bearer " + os.environ["COMFY_API_KEY"]
    if headers:
        h.update(headers)
    if isinstance(data, (dict, list)):
        data = json.dumps(data).encode()
        h["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, method=method, headers=h)
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        body = resp.read()
    if raw:
        return body
    return json.loads(body) if body else {}


def load_workflow(path, sets=()):
    wf = json.load(open(path))
    if "nodes" in wf:
        sys.exit("UI-format workflow; export it with 'Save (API)' first")
    for s in sets:
        key, _, val = s.partition("=")
        nid, _, inp = key.partition(".")
        if nid not in wf:
            sys.exit(f"--set: node {nid} not in workflow")
        try:
            val = json.loads(val)
        except ValueError:
            pass
        wf[nid].setdefault("inputs", {})[inp] = val
    return wf


def submit(base, wf, client_id=None):
    r = _req(base, "/prompt", {"prompt": wf, "client_id": client_id or uuid.uuid4().hex})
    if r.get("node_errors"):
        raise RuntimeError(json.dumps(r["node_errors"]))
    return r["prompt_id"]


def status(base, pid):
    h = _req(base, f"/history/{pid}")
    if pid in h:
        st = h[pid].get("status", {})
        return {"id": pid, "status": "error" if st.get("status_str") == "error" else "done",
                "outputs": h[pid].get("outputs", {}), "messages": st.get("messages", [])[-3:]}
    q = _req(base, "/queue")
    if any(item[1] == pid for item in q.get("queue_running", [])):
        return {"id": pid, "status": "running"}
    if any(item[1] == pid for item in q.get("queue_pending", [])):
        return {"id": pid, "status": "queued"}
    return {"id": pid, "status": "unknown"}


def wait(base, pids, timeout_s=600, poll_s=2.0):
    """Wait for all ids. On timeout each id returns its live status; errors are reported in place."""
    deadline = time.time() + timeout_s
    res = {}
    while True:
        for pid in pids:
            if pid in res and res[pid].get("status") in ("done", "error"):
                continue
            try:
                res[pid] = status(base, pid)
            except Exception as e:  # one bad id must not sink the batch
                res[pid] = {"id": pid, "status": "fetch_error", "error": str(e)}
        if all(r.get("status") in ("done", "error", "fetch_error") for r in res.values()):
            return list(res.values())
        if time.time() >= deadline:
            for r in res.values():
                r.setdefault("timed_out", r.get("status") not in ("done", "error"))
            return list(res.values())
        time.sleep(poll_s)


def fetch(base, pid, out_dir):
    st = status(base, pid)
    os.makedirs(out_dir, exist_ok=True)
    files = []
    for nid, out in st.get("outputs", {}).items():
        for kind in ("images", "gifs", "videos", "audio", "files"):
            for f in out.get(kind, []) or []:
                if not isinstance(f, dict) or "filename" not in f:
                    continue
                q = urllib.parse.urlencode({"filename": f["filename"], "subfolder": f.get("subfolder", ""),
                                            "type": f.get("type", "output")})
                dst = os.path.join(out_dir, f["filename"])
                with open(dst, "wb") as fh:
                    fh.write(_req(base, "/view?" + q, raw=True, timeout=600))
                files.append(dst)
    return files


def texts(outputs):
    """Text results from nodes such as PreviewAny (ui key "text"), e.g. ASR segments JSON."""
    out = []
    for nid, o in outputs.items():
        for x in o.get("text", []) or []:
            out.append({"node": nid, "text": x})
    return out


def cancel(base, pid):
    st = status(base, pid)
    if st["status"] == "running":
        _req(base, "/interrupt", {"prompt_id": pid}, method="POST")
    elif st["status"] == "queued":
        _req(base, "/queue", {"delete": [pid]}, method="POST")
    return {"id": pid, "was": st["status"], "cancelled": st["status"] in ("running", "queued")}


def upload(base, path, overwrite=True):
    b = uuid.uuid4().hex
    ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
    name = os.path.basename(path)
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\n"
            f"Content-Type: {ctype}\r\n\r\n").encode() + open(path, "rb").read() + \
           (f"\r\n--{b}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\n"
            f"{'true' if overwrite else 'false'}\r\n--{b}--\r\n").encode()
    return _req(base, "/upload/image", body, method="POST",
                headers={"Content-Type": f"multipart/form-data; boundary={b}"})


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--url", default=DEFAULT_URL)
    sp = p.add_subparsers(dest="cmd", required=True)
    for c in ("run", "submit"):
        s = sp.add_parser(c); s.add_argument("workflow"); s.add_argument("--set", action="append", default=[])
        s.add_argument("--out", default="out"); s.add_argument("--timeout", type=float, default=1800)
    s = sp.add_parser("wait"); s.add_argument("ids", nargs="+"); s.add_argument("--timeout", type=float, default=600)
    s = sp.add_parser("fetch"); s.add_argument("id"); s.add_argument("--out", default="out")
    s = sp.add_parser("cancel"); s.add_argument("id")
    s = sp.add_parser("upload"); s.add_argument("file")
    a = p.parse_args(argv)
    if a.cmd in ("run", "submit"):
        pid = submit(a.url, load_workflow(a.workflow, a.set))
        if a.cmd == "submit":
            print(json.dumps({"prompt_id": pid})); return
        r = wait(a.url, [pid], a.timeout)[0]
        if r["status"] == "done":
            r["files"] = fetch(a.url, pid, a.out)
            r["texts"] = texts(r.get("outputs", {}))
        r.pop("outputs", None)
        print(json.dumps(r, indent=1))
    elif a.cmd == "wait":
        print(json.dumps([{k: v for k, v in r.items() if k != "outputs"} for r in wait(a.url, a.ids, a.timeout)], indent=1))
    elif a.cmd == "fetch":
        print(json.dumps(fetch(a.url, a.id, a.out), indent=1))
    elif a.cmd == "cancel":
        print(json.dumps(cancel(a.url, a.id)))
    elif a.cmd == "upload":
        print(json.dumps(upload(a.url, a.file)))


if __name__ == "__main__":
    main()
