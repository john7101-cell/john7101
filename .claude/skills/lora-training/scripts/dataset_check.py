#!/usr/bin/env python3
"""Static LoRA dataset check + approval gate (stdlib only, no network). Original, this collection (MIT).

  dataset_check.py <folder> --kind character|product|style|motion [--trigger tok]
  dataset_check.py <folder> --approve "user's words"      # only after the user said yes
"""
import argparse, hashlib, json, os, struct, sys, time

IMG = (".png", ".jpg", ".jpeg", ".webp")
VID = (".mp4", ".mov", ".webm", ".mkv")
TARGET = {"character": (15, 40), "product": (15, 30), "style": (25, 60), "motion": (10, 30)}


def img_size(p):
    with open(p, "rb") as f:
        h = f.read(32)
        if h[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", h[16:24])
        if h[:2] == b"\xff\xd8":
            f.seek(2)
            while True:
                b = f.read(4)
                if len(b) < 4 or b[0] != 0xFF: return None
                m, ln = b[1], struct.unpack(">H", b[2:4])[0]
                if m in (0xC0, 0xC1, 0xC2):
                    hh, ww = struct.unpack(">xHH", f.read(5)); return ww, hh
                f.seek(ln - 2, 1)
    return None


def scan(folder):
    items = []
    for n in sorted(os.listdir(folder)):
        p = os.path.join(folder, n)
        if not n.lower().endswith(IMG + VID): continue
        cap = os.path.splitext(p)[0] + ".txt"
        items.append({"file": n, "sha256": hashlib.sha256(open(p, "rb").read()).hexdigest(),
                      "caption": open(cap).read().strip() if os.path.exists(cap) else None,
                      "size": img_size(p) if n.lower().endswith((".png", ".jpg", ".jpeg")) else None})
    return items


def set_hash(items):
    return hashlib.sha256(json.dumps([(i["file"], i["sha256"], i["caption"]) for i in items]).encode()).hexdigest()


def main(argv=None):
    a = argparse.ArgumentParser(); a.add_argument("folder"); a.add_argument("--kind", choices=TARGET, default="character")
    a.add_argument("--trigger"); a.add_argument("--min-side", type=int, default=768); a.add_argument("--approve")
    a = a.parse_args(argv)
    items = scan(a.folder); h = set_hash(items)
    if a.approve is not None:
        dj = os.path.join(a.folder, "dataset.json")
        if not os.path.exists(dj) or json.load(open(dj))["sha256"] != h:
            sys.exit("dataset changed since the last check (or never checked): run the check, show the user, then approve")
        json.dump({"sha256": h, "approved_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "user_message": a.approve},
                  open(os.path.join(a.folder, "APPROVED.json"), "w"), indent=1)
        print("approved", h[:12]); return 0
    w = []
    lo, hi = TARGET[a.kind]
    if not lo <= len(items) <= hi: w.append(f"{len(items)} items; target for {a.kind} is {lo}-{hi}")
    seen = {}
    for i in items:
        if i["sha256"] in seen: w.append(f"duplicate: {i['file']} = {seen[i['sha256']]}")
        seen.setdefault(i["sha256"], i["file"])
        if not i["caption"]: w.append(f"no caption: {i['file']}")
        elif a.trigger and a.trigger.lower() in i["caption"].lower(): w.append(f"caption contains trigger (trainer prepends it): {i['file']}")
        if i["size"] and min(i["size"]) < a.min_side: w.append(f"small ({i['size'][0]}x{i['size'][1]}): {i['file']}")
        if a.kind == "motion" and not i["file"].lower().endswith(VID): w.append(f"motion LoRA needs clips, got image: {i['file']}")
    out = {"folder": os.path.abspath(a.folder), "kind": a.kind, "trigger": a.trigger, "count": len(items), "sha256": h, "warnings": w, "items": items}
    json.dump(out, open(os.path.join(a.folder, "dataset.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("count", "sha256", "warnings")}, indent=1))
    print("NEXT: show the user a contact sheet + trigger + warnings and WAIT for approval.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
