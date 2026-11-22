#!/usr/bin/env python3
"""Static preflight for ComfyUI API workflows (stdlib only).

Checks, BEFORE you submit, that a server has (1) every node class_type the
workflow uses and (2) every model/weight file named in a loader input, and that
each such file is one of the values that server offers for that input.
It only reads GET /object_info (and GET /models/<folder> as a fallback); it
submits nothing. Technique adapted from rossaai/rosesfield
scripts/checks/cloud-graphs (MIT); see NOTICE.

  python preflight.py --url http://127.0.0.1:8188 workflows/*.json
  python preflight.py --object-info saved_object_info.json workflows/x.json   # fully offline
Exit code 0 = all ready, 1 = something missing.
"""
import argparse, json, os, re, sys, urllib.request

WEIGHT = re.compile(r"\.(safetensors|sft|ckpt|pt|pth|bin|gguf|onnx)$", re.I)


def get(url, path):
    h = {"Authorization": "Bearer " + os.environ["COMFY_API_KEY"]} if os.environ.get("COMFY_API_KEY") else {}
    with urllib.request.urlopen(urllib.request.Request(url.rstrip("/") + path, headers=h), timeout=60) as r:
        return json.loads(r.read())


def choices(spec):
    """Return the allowed values list of an object_info input spec, if it is a combo."""
    if isinstance(spec, list) and spec:
        if isinstance(spec[0], list):
            return spec[0]
        if spec[0] == "COMBO" and len(spec) > 1 and isinstance(spec[1], dict):
            return spec[1].get("options")
    return None


def check(wf, info):
    missing_nodes, missing_files, ok_files = set(), [], []
    for nid, node in wf.items():
        if not isinstance(node, dict) or "class_type" not in node:
            continue
        ct = node["class_type"]
        if ct not in info:
            missing_nodes.add(ct)
            continue
        req = info[ct].get("input", {})
        specs = {**req.get("required", {}), **req.get("optional", {})}
        for k, v in node.get("inputs", {}).items():
            if isinstance(v, str) and WEIGHT.search(v):
                allowed = choices(specs.get(k))
                if allowed is not None and v not in allowed:
                    missing_files.append({"node": nid, "class_type": ct, "input": k, "file": v})
                else:
                    ok_files.append(v)
    return sorted(missing_nodes), missing_files, ok_files


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("workflows", nargs="+")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--url"); g.add_argument("--object-info", help="saved /object_info JSON (offline)")
    a = p.parse_args()
    info = json.load(open(a.object_info)) if a.object_info else get(a.url, "/object_info")
    bad = False
    for path in a.workflows:
        wf = json.load(open(path))
        if "nodes" in wf:
            print(json.dumps({"workflow": path, "error": "UI format; preflight needs API format"})); bad = True; continue
        mn, mf, okf = check(wf, info)
        bad |= bool(mn or mf)
        print(json.dumps({"workflow": path, "ready": not (mn or mf), "missing_node_types": mn,
                          "missing_weight_files": mf, "weights_found": len(okf)}, indent=1))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
