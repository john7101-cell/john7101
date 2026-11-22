#!/usr/bin/env python3
"""Verify and apply a template binding (motion-previs-studio <id>.binding.json contract) to a ComfyUI API graph.
Stdlib only, no network. Original implementation, this collection (MIT).

  binding_apply.py check <graph.api.json> <binding.json>
  binding_apply.py apply <graph.api.json> <binding.json> field=value ... --out filled.json
Binding: {"nodes": {"<id>": "<class_type>"}, "fields": {"<field>": {"node": "<id>", "input": "<name>", "fixed": <opt>}}}
"""
import argparse, json, sys


def check(g, b):
    err = []
    for nid, ct in (b.get("nodes") or {}).items():
        if nid not in g: err.append(f"node {nid} missing")
        elif g[nid].get("class_type") != ct: err.append(f"node {nid}: class_type {g[nid].get('class_type')} != {ct}")
    for f, t in (b.get("fields") or {}).items():
        n = g.get(str(t.get("node")))
        if n is None: err.append(f"field {f}: node {t.get('node')} missing")
        elif t.get("input") not in n.get("inputs", {}): err.append(f"field {f}: input {t.get('input')} not on node {t.get('node')}")
    return err


def main(argv=None):
    a = argparse.ArgumentParser(); a.add_argument("cmd", choices=["check", "apply"]); a.add_argument("graph"); a.add_argument("binding")
    a.add_argument("values", nargs="*"); a.add_argument("--out"); a = a.parse_args(argv)
    g, b = json.load(open(a.graph)), json.load(open(a.binding))
    err = check(g, b)
    if err: print("\n".join(err)); return 1
    if a.cmd == "check": print("binding ok:", len(b.get("fields", {})), "fields"); return 0
    for kv in a.values:
        k, _, v = kv.partition("=")
        t = b["fields"].get(k)
        if t is None: sys.exit(f"unknown field {k}; known: {sorted(b['fields'])}")
        if "fixed" in t: sys.exit(f"field {k} is fixed to {t['fixed']}")
        if "patch" in t: sys.exit(f"field {k} uses a studio-specific patch ({t['patch']}); edit that input by hand")
        try: v = json.loads(v)
        except ValueError: pass
        g[str(t["node"])]["inputs"][t["input"]] = v
    for k, t in b["fields"].items():
        if "fixed" in t: g[str(t["node"])]["inputs"][t["input"]] = t["fixed"]
    json.dump(g, open(a.out or "filled.api.json", "w"), indent=1); print("wrote", a.out or "filled.api.json"); return 0


if __name__ == "__main__":
    sys.exit(main())
