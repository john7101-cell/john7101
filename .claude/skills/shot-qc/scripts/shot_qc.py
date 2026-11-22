#!/usr/bin/env python3
"""Model-free shot QC with ffprobe/ffmpeg measurements -> flags + 0-100 score. Stdlib only.
Original implementation for this collection (MIT). NovaField (AGPL-3.0) was a design reference only; no code copied.

  shot_qc.py <video> [--duration S] [--ratio 16:9] [--audio] [--fps 24] [--static] [--json]
Thresholds are starting values (UNVERIFIED at scale); tune per project.
"""
import argparse, json, os, re, shutil, statistics, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from media_info import media_info

W = {"duration": 15, "aspect": 15, "no_audio": 10, "freeze": 20, "black": 20, "cuts": 15, "flicker": 15, "soft": 10, "clipping": 5}
FF = shutil.which("ffmpeg") or "ffmpeg"


def ff(video, vf, timeout=300):
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", video, "-an", "-vf", vf, "-f", "null", "-"], capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stderr


def has_filter(name):
    r = subprocess.run([FF, "-hide_banner", "-filters"], capture_output=True, text=True)
    return re.search(rf"\s{name}\s", r.stdout) is not None


def measure(video, static=False):
    m = {}
    _, e = ff(video, "freezedetect=n=0.003:d=0.5")
    m["freezes"] = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", e)]
    _, e = ff(video, "blackdetect=d=0.1:pix_th=0.10")
    m["black"] = [float(x) for x in re.findall(r"black_duration:([\d.]+)", e)]
    _, e = ff(video, "select='gt(scene,0.35)',showinfo")
    m["cuts"] = len(re.findall(r"pts_time:", e))
    _, e = ff(video, "signalstats,metadata=mode=print")
    yavg = [float(x) for x in re.findall(r"lavfi\.signalstats\.YAVG=([\d.]+)", e)]
    ymax = [float(x) for x in re.findall(r"lavfi\.signalstats\.YMAX=([\d.]+)", e)]
    ymin = [float(x) for x in re.findall(r"lavfi\.signalstats\.YMIN=([\d.]+)", e)]
    jumps = sorted(abs(b - a) for a, b in zip(yavg, yavg[1:]))
    m["flicker_p95"] = jumps[int(0.95 * (len(jumps) - 1))] if jumps else 0.0
    n = max(1, len(ymax))
    m["clip_frac"] = (sum(1 for v in ymax if v >= 250) + sum(1 for v in ymin if v <= 5)) / (2 * n) if ymax else 0.0
    m["frames"] = len(yavg)
    if has_filter("blurdetect"):
        _, e = ff(video, "blurdetect,metadata=mode=print")
        b = [float(x) for x in re.findall(r"lavfi\.blur=([\d.]+)", e)]
        m["blur_median"] = statistics.median(b) if b else None
    else:
        m["blur_median"] = None
    return m


def evaluate(info, m, duration=None, ratio=None, audio=False, static=False):
    f = []
    if duration is not None and abs(info["video_duration"] - duration) > max(0.6, duration * 0.05): f.append("duration")
    if ratio and info["width"] and info["height"]:
        w, h = (int(x) for x in ratio.split(":"))
        if abs(info["width"] / info["height"] - w / h) > 0.03 * w / h: f.append("aspect")
    if audio and not info["has_audio"]: f.append("no_audio")
    if m["freezes"] and not static: f.append("freeze")
    if m["black"]: f.append("black")
    if m["cuts"] > 0: f.append("cuts")
    if m["flicker_p95"] > 12: f.append("flicker")
    if m["blur_median"] is not None and m["blur_median"] > 8: f.append("soft")
    if m["clip_frac"] >= 0.05: f.append("clipping")
    score = max(0, 100 - sum(W[x] for x in f))
    return {"flags": f, "score": score, "pass": score >= 70 and not {"freeze", "black"} & set(f)}


def main(argv=None):
    a = argparse.ArgumentParser(); a.add_argument("video"); a.add_argument("--duration", type=float); a.add_argument("--ratio")
    a.add_argument("--audio", action="store_true"); a.add_argument("--fps", type=float); a.add_argument("--static", action="store_true")
    a.add_argument("--json", action="store_true"); a = a.parse_args(argv)
    info = media_info(a.video); m = measure(a.video, a.static); r = evaluate(info, m, a.duration, a.ratio, a.audio, a.static)
    out = {"video": a.video, "info": info, "measured": m, **r}
    print(json.dumps(out, indent=None if a.json else 1)); return 0 if r["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
