#!/usr/bin/env python3
"""Validate API-format workflows against a ComfyUI /object_info dump (stdlib only).

  python validate_api.py object_info.json skills/*/workflows/api/*.api.json

Checks: every class_type exists, required inputs are present (autogrow inputs as `name.x` keys),
links point at nodes in the graph, there is an output node, and no closed hosted API node is used.
"""
import json, sys


def check(oi, wf):
    errs = []
    for nid, n in wf.items():
        d = oi.get(n.get("class_type"))
        if not d: errs.append(f"{nid}: unknown class {n.get('class_type')}"); continue
        if d.get("api_node"): errs.append(f"{nid}: closed hosted API node {n['class_type']}")
        for k, spec in (d["input"].get("required") or {}).items():
            if spec and spec[0] == "COMFY_AUTOGROW_V3":
                if not any(x.startswith(k + ".") for x in n["inputs"]): errs.append(f"{nid}: autogrow input {k} empty")
            elif k not in n["inputs"]: errs.append(f"{nid} {n['class_type']}: missing required input {k}")
        for k, v in n["inputs"].items():
            if isinstance(v, list) and len(v) == 2 and isinstance(v[0], str) and isinstance(v[1], int) and v[0] not in wf:
                errs.append(f"{nid}.{k}: link to missing node {v[0]}")
    if not any(oi.get(n.get("class_type"), {}).get("output_node") for n in wf.values()): errs.append("no output node")
    return errs


if __name__ == "__main__":
    oi = json.load(open(sys.argv[1])); bad = 0
    for p in sys.argv[2:]:
        e = check(oi, json.load(open(p))); bad += bool(e)
        print(("ok  " if not e else "BAD ") + p + ("" if not e else "\n    " + "\n    ".join(e[:10])))
    sys.exit(1 if bad else 0)
