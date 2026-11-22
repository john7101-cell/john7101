#!/usr/bin/env python3
"""Write SRT captions from a production manifest (narration per shot) or from
Whisper segments JSON, and optionally print/run an ffmpeg burn-in. Stdlib only.

  python make_srt.py --manifest manifest.json --out captions.srt
  python make_srt.py --segments segments.json --out captions.srt --burn film.mp4 --burned out.mp4 [--run]
"""
import argparse, json, shlex, subprocess, textwrap


def stamp(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def split_line(text, start, end, max_chars=42, max_lines=2):
    """Split long text into caption blocks of <= max_lines x max_chars, timed by length."""
    lines = textwrap.wrap(" ".join(text.split()), max_chars) or [""]
    blocks = [lines[i:i + max_lines] for i in range(0, len(lines), max_lines)]
    total = sum(len(" ".join(b)) for b in blocks) or 1
    out, t = [], start
    for b in blocks:
        d = (end - start) * len(" ".join(b)) / total
        out.append((t, t + d, "\n".join(b))); t += d
    return out


def from_manifest(m):
    cues, t = [], 0.0
    for sh in m.get("shots", []):
        d = float(sh.get("duration_s", 0))
        if sh.get("narration"):
            cues += split_line(sh["narration"], t + 0.1, t + d - 0.1)
        t += d
    return cues


def from_segments(seg):
    seg = seg.get("segments", seg) if isinstance(seg, dict) else seg
    cues = []
    for s in seg:
        st = s.get("start", s.get("timestamp", [0, 0])[0]); en = s.get("end", s.get("timestamp", [0, 0])[1])
        cues += split_line(s.get("text", ""), float(st), float(en))
    return cues


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group(required=True); g.add_argument("--manifest"); g.add_argument("--segments")
    p.add_argument("--out", default="captions.srt"); p.add_argument("--burn"); p.add_argument("--burned", default="captioned.mp4")
    p.add_argument("--run", action="store_true")
    a = p.parse_args()
    cues = from_manifest(json.load(open(a.manifest))) if a.manifest else from_segments(json.load(open(a.segments)))
    with open(a.out, "w") as f:
        for i, (s, e, t) in enumerate(cues, 1):
            f.write(f"{i}\n{stamp(s)} --> {stamp(e)}\n{t}\n\n")
    print(json.dumps({"srt": a.out, "cues": len(cues)}))
    if a.burn:
        cmd = ["ffmpeg", "-y", "-i", a.burn, "-vf", f"subtitles={a.out}:force_style='Fontsize=22,MarginV=40,Outline=2'",
               "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
               "-c:a", "copy", a.burned]
        print(" ".join(shlex.quote(x) for x in cmd))
        if a.run:
            subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
