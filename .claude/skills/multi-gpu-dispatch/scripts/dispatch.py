#!/usr/bin/env python3
"""Shard a video-director manifest's shots across several ComfyUI servers. Stdlib only. Original, this collection (MIT).

  dispatch.py plan  manifest.json --url U1 --url U2 [--weights 2,1]
  dispatch.py run   manifest.json --url U1 --url U2 [--dry-run]     # parallel workers, then merge
  dispatch.py merge manifest.json                                    # merge worker copies back
Each worker runs `video-director/scripts/direct.py run <copy> --url U --only s01,s03` (stills + video only) on its
OWN manifest copy (no concurrent writes); `merge` copies those shots back. Then run direct.py on the merged
manifest for continuity, audio, post, assembly. Chained shots stay on their parent's server.
"""
import argparse, json, os, subprocess, sys, threading

HERE = os.path.dirname(os.path.abspath(__file__))
DIRECT = os.path.join(HERE, "..", "..", "video-director", "scripts", "direct.py")


def plan(m, urls, weights):
    w = weights or [1] * len(urls); load = [0.0] * len(urls); asg = {}
    for sh in m["shots"]:
        if sh["video"].get("status") == "done" and sh["still"].get("status") == "done": continue
        p = sh.get("chain_from")
        if p and p in asg: i = asg[p]
        else: i = min(range(len(urls)), key=lambda k: (load[k] / w[k], k))
        asg[sh["id"]] = i; load[i] += sh["duration_s"]
    out = {u: [sid for sid, i in asg.items() if i == k] for k, u in enumerate(urls)}
    return {u: v for u, v in out.items() if v}


def copy_path(mp, k): return f"{os.path.splitext(mp)[0]}.worker{k}.json"


def main(argv=None):
    a = argparse.ArgumentParser(); a.add_argument("cmd", choices=["plan", "run", "merge"]); a.add_argument("manifest")
    a.add_argument("--url", action="append", default=[]); a.add_argument("--weights"); a.add_argument("--dry-run", action="store_true")
    a = a.parse_args(argv)
    m = json.load(open(a.manifest))
    if a.cmd == "merge":
        n = 0
        for k, (u, ids) in enumerate(json.load(open(a.manifest + ".dispatch.json")).items()):
            cp = copy_path(a.manifest, k)
            if not os.path.exists(cp): print("missing", cp); continue
            w = {s["id"]: s for s in json.load(open(cp))["shots"]}
            for i, sh in enumerate(m["shots"]):
                if sh["id"] in ids: m["shots"][i] = w[sh["id"]]; n += 1
        m["log"].append({"event": "dispatch_merge", "shots": n}); json.dump(m, open(a.manifest, "w"), indent=1); print("merged", n, "shots"); return 0
    if not a.url: sys.exit("give at least one --url")
    ws = [float(x) for x in a.weights.split(",")] if a.weights else None
    pl = plan(m, a.url, ws)
    print(json.dumps(pl, indent=1))
    if a.cmd == "plan": return 0
    if not a.dry_run: json.dump(pl, open(a.manifest + ".dispatch.json", "w"), indent=1)
    rc = {}

    def work(k, u, ids):
        cp = copy_path(a.manifest, k)
        cmd = [sys.executable, DIRECT, "run", cp, "--url", u, "--only", ",".join(ids)] + (["--dry-run"] if a.dry_run else [])
        if a.dry_run:
            print(f"[dry] copy {a.manifest} -> {cp}\n[dry] $ {' '.join(cmd)}"); rc[u] = 0; return
        json.dump(m, open(cp, "w"), indent=1)
        rc[u] = subprocess.call(cmd)

    ts = [threading.Thread(target=work, args=(k, u, ids)) for k, (u, ids) in enumerate(pl.items())]
    [t.start() for t in ts]; [t.join() for t in ts]
    print(json.dumps({"exit_codes": rc}))
    if not a.dry_run: print("next: dispatch.py merge", a.manifest, "&& direct.py run", a.manifest)
    return 0 if all(v == 0 for v in rc.values()) else 4


if __name__ == "__main__":
    sys.exit(main())
