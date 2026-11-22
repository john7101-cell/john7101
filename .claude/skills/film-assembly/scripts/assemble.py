#!/usr/bin/env python3
"""Assemble a film from shot clips + narration + music with ffmpeg (stdlib only).
Prints the ffmpeg command; add --run to execute it (needs ffmpeg/ffprobe on PATH).

  python assemble.py --clips s01.mp4 s02.mp4 s03.mp4 --narration vo.wav \
      --music bed.mp3 --aspect 16:9 --xfade 0.4 --out film.mp4 [--beats beats.txt] [--run]

--beats: a text file of beat times in seconds (one per line, e.g. from a beat
tracker). Cuts are snapped to the nearest beat: idea adapted from
jalajbhandula/motionfield beat-cut recipe (MIT); see NOTICE.
Music is ducked under narration with sidechaincompress.
"""
# Web-safe H.264: 4:2:0 + High profile play in browsers, GitHub and Discord; faststart moves the index up front.
WEB_SAFE = ["-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart"]
import argparse, json, shlex, subprocess

SIZES = {"9:16": (1080, 1920), "1:1": (1080, 1080), "16:9": (1920, 1080), "4:5": (1080, 1350)}


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    return float(json.loads(out)["format"]["duration"])


def snap(t, beats):
    return min(beats, key=lambda b: abs(b - t)) if beats else t


def build(a, durations):
    W, H = SIZES[a.aspect]
    beats = [float(x) for x in open(a.beats).read().split()] if a.beats else []
    inputs, filt = [], []
    for i, c in enumerate(a.clips):
        inputs += ["-i", c]
        filt.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
                    f"setsar=1,settb=AVTB,setpts=PTS-STARTPTS,fps={a.fps},format=yuv420p[v{i}]")
    cur, t = "v0", durations[0]
    for i in range(1, len(a.clips)):
        cut = snap(t, beats)
        off = max(0.0, cut - a.xfade)
        if a.xfade > 0:
            filt.append(f"[{cur}][v{i}]xfade=transition=fade:duration={a.xfade:.3f}:offset={off:.3f}[j{i}]")
            t = off + durations[i]
        else:
            filt.append(f"[{cur}][v{i}]concat=n=2:v=1:a=0[j{i}]"); t += durations[i]
        cur = f"j{i}"
    total = t
    n = len(a.clips)
    amap = []
    if a.narration and a.music:
        inputs += ["-i", a.narration, "-stream_loop", "-1", "-i", a.music]
        filt.append(f"[{n+1}:a]volume={a.music_gain}[m];[{n}:a]asplit=2[vo][sc];"
                    f"[m][sc]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=400[duck];"
                    f"[vo][duck]amix=inputs=2:duration=longest:normalize=0,atrim=0:{total:.3f},"
                    f"afade=t=out:st={max(0,total-1.5):.3f}:d=1.5[aout]")
        amap = ["-map", "[aout]"]
    elif a.narration or a.music:
        inputs += (["-stream_loop", "-1"] if a.music and not a.narration else []) + ["-i", a.narration or a.music]
        filt.append(f"[{n}:a]atrim=0:{total:.3f},afade=t=out:st={max(0,total-1.5):.3f}:d=1.5[aout]")
        amap = ["-map", "[aout]"]
    return (["ffmpeg", "-hide_banner", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", f"[{cur}]", *amap,
             "-t", f"{total:.3f}", "-c:v", "libx264", "-crf", "16", "-preset", "medium", *WEB_SAFE, "-c:a", "aac", "-b:a", "192k",
             a.out])


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--clips", nargs="+", required=True); p.add_argument("--narration"); p.add_argument("--music")
    p.add_argument("--music-gain", type=float, default=0.35); p.add_argument("--aspect", default="16:9", choices=SIZES)
    p.add_argument("--fps", type=int, default=24); p.add_argument("--xfade", type=float, default=0.0)
    p.add_argument("--beats"); p.add_argument("--durations", nargs="*", type=float, help="skip ffprobe")
    p.add_argument("--out", default="film.mp4"); p.add_argument("--run", action="store_true")
    a = p.parse_args()
    d = a.durations or [probe(c) for c in a.clips]
    cmd = build(a, d)
    print(" ".join(shlex.quote(x) for x in cmd))
    if a.run:
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
