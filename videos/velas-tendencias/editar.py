"""Edición del reel "Tendencias en velas" a partir de los 6 clips del avatar.

- Cámaras virtuales: cada toma se parte en 2-3 "cámaras" (abierto, medio con inclinación, cerrado),
  con zoom lento, giro leve y un vaivén de cámara en mano, cortando en las pausas de la voz.
- Transiciones suaves entre tomas (xfade) sin que se monte el audio.
- Subtítulos estilo TikTok (2-3 palabras) que entran con giro y rebote; la palabra que se dice
  se ilumina en ámbar.

Uso:
  python videos/velas-tendencias/editar.py toma1.mp4 ... toma6.mp4 --words words.json --out reel.mp4
`words.json`: [{"words": [[palabra, inicio, fin], ...]}, ...] una entrada por toma (Whisper).
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path

W, H, FPS = 1080, 1920, 24
UP = 2  # trabajar a 2x (2160x3840) para que el zoom sea suave
XF = 0.25  # duración de la transición entre tomas
TAIL = 0.25  # aire después de la última palabra de cada toma

# Cámaras virtuales: zoom inicial→final, giro (grados) inicial→final, foco (x, y) en fracción del cuadro.
CAMS = {
    "abierto":      dict(z=(1.06, 1.12), r=(0.0, 0.0),  f=(0.50, 0.50)),
    "abierto_bajo": dict(z=(1.12, 1.18), r=(0.0, 0.0),  f=(0.50, 0.56)),
    "medio_izq":    dict(z=(1.24, 1.30), r=(1.6, 0.6),  f=(0.50, 0.46)),
    "medio_der":    dict(z=(1.22, 1.28), r=(-1.6, -0.6), f=(0.50, 0.46)),
    "cerrado":      dict(z=(1.50, 1.58), r=(-0.8, 0.0), f=(0.50, 0.40)),
    "cerrado_der":  dict(z=(1.42, 1.50), r=(0.9, 0.2),  f=(0.50, 0.42)),
    "intimo":       dict(z=(1.20, 1.32), r=(0.0, 0.0),  f=(0.50, 0.42)),
}

# Por toma: inicio del recorte y cortes de cámara (segundo de la toma, cámara desde ahí).
PLAN = [
    {"start": 2.40, "cams": [(2.40, "medio_izq"), (5.62, "cerrado")], "xfade": "smoothleft"},
    {"start": 0.00, "cams": [(0.00, "abierto"), (2.45, "medio_der"), (5.25, "cerrado")], "xfade": "fade"},
    {"start": 0.00, "cams": [(0.00, "abierto"), (4.20, "cerrado_der")], "xfade": "zoomin"},
    {"start": 0.00, "cams": [(0.00, "medio_izq"), (3.55, "intimo"), (5.90, "cerrado")], "xfade": "smoothup"},
    {"start": 0.00, "cams": [(0.00, "abierto"), (3.10, "medio_der")], "xfade": "smoothright"},
    {"start": 0.00, "cams": [(0.00, "abierto"), (2.40, "abierto_bajo"), (5.60, "cerrado_der")], "xfade": None},
]

# Correcciones de la transcripción (lo que dice el guion).
FIX = {"5": "cinco", "3": "tres", "2.": "dos.", "4.": "cuatro.", "uno,": "uno:", "dos.": "dos:"}
MERGE = {("En", "bases"): "envases"}
KEYWORDS = {"cinco", "tres", "uno", "dos", "cuatro", "secreta", "forma", "madera", "aromas",
            "envases", "tierra", "nadie", "vainilla", "café"}


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def camera_filter(cam: dict, dur: float, seed: int) -> str:
    """Escala 2x, gira y encuadra con zoom animado (zoompan) + vaivén de cámara en mano."""
    z0, z1 = cam["z"]
    r0, r1 = cam["r"]
    fx, fy = cam["f"]
    T = max(dur, 0.1)
    p = f"(it/{T:.3f})"
    ease = f"(0.5-0.5*cos(PI*min({p},1)))"  # entrada y salida suaves
    z = f"({z0}+({z1}-{z0})*{ease})"
    ph = seed * 1.7
    # vaivén leve: dos senos lentos, amplitud ~0.35 % del cuadro
    sx = f"(0.0035*sin(2*PI*0.23*it+{ph:.2f})+0.002*sin(2*PI*0.51*it+{ph*2:.2f}))"
    sy = f"(0.0030*sin(2*PI*0.19*it+{ph+1:.2f})+0.002*sin(2*PI*0.43*it+{ph*3:.2f}))"
    # mantener el recorte dentro del cuadro (con margen si hay giro para no ver esquinas)
    m = 0.045 if (r0 or r1) else 0.0
    cx = f"max(0.5/zoom+{m},min(1-0.5/zoom-{m},{fx}+{sx}))"
    cy = f"max(0.5/zoom+{m},min(1-0.5/zoom-{m},{fy}+{sy}))"
    x = f"iw*({cx})-iw/zoom/2"
    y = f"ih*({cy})-ih/zoom/2"
    parts = [f"scale={W*UP}:{H*UP}:flags=lanczos", "setsar=1"]
    if r0 or r1:
        ang = f"({r0}+({r1}-{r0})*(0.5-0.5*cos(PI*min(t/{T:.3f},1))))*PI/180"
        parts.append(f"rotate='{ang}':ow=iw:oh=ih:fillcolor=black@1")
    parts.append(f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps={FPS}")
    return ",".join(parts)


def last_word_end(words) -> float:
    return float(words[-1][2])


def build_segments(clips, plan, words, tmp: Path):
    """Devuelve por toma: archivo de video (con cola para la transición) y duración del audio."""
    out = []
    seed = 0
    for i, (clip, pl, ws) in enumerate(zip(clips, plan, words)):
        a_end = last_word_end(ws) + TAIL
        if pl["xfade"] is None:
            a_end += 0.6  # remate final
        v_end = a_end + (XF if pl["xfade"] else 0.0)
        cuts = pl["cams"] + [(v_end, None)]
        parts = []
        for j in range(len(cuts) - 1):
            s, cam = cuts[j]
            e = cuts[j + 1][0]
            f = tmp / f"t{i}_{j}.mp4"
            vf = camera_filter(CAMS[cam], e - s, seed)
            seed += 1
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-to", f"{e:.3f}", "-i", str(clip),
                 "-vf", vf, "-an", "-r", str(FPS), "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                 "-pix_fmt", "yuv420p", str(f)])
            parts.append(f)
        lst = tmp / f"t{i}.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        vid = tmp / f"t{i}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(vid)])
        aud = tmp / f"a{i}.wav"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{pl['start']:.3f}", "-to", f"{a_end:.3f}", "-i", str(clip),
             "-vn", "-ac", "2", "-ar", "48000",
             "-af", f"afade=t=in:d=0.02,afade=t=out:st={a_end - pl['start'] - 0.04:.3f}:d=0.04", str(aud)])
        out.append({"video": vid, "audio": aud, "dur": a_end - pl["start"], "start": pl["start"],
                    "xfade": pl["xfade"]})
    return out


def join(segs, tmp: Path) -> tuple[Path, Path, list[float]]:
    """Encadena con xfade (video) y concat (audio). Devuelve offsets de cada toma en la línea final."""
    offsets, acc = [], 0.0
    for s in segs:
        offsets.append(acc)
        acc += s["dur"]
    inputs, fc = [], []
    for s in segs:
        inputs += ["-i", str(s["video"])]
    last = "[0:v]"
    for i in range(1, len(segs)):
        lab = f"[x{i}]"
        fc.append(f"{last}[{i}:v]xfade=transition={segs[i-1]['xfade']}:duration={XF}:offset={offsets[i]:.3f}{lab}")
        last = lab
    vid = tmp / "video.mp4"
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", last,
         "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", str(vid)])
    lst = tmp / "audio.txt"
    lst.write_text("".join(f"file '{s['audio']}'\n" for s in segs))
    aud = tmp / "audio.wav"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", str(aud)])
    return vid, aud, offsets


# ---------- subtítulos ----------

def ass_time(t: float) -> str:
    t = max(t, 0)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def clean_words(ws):
    out, i = [], 0
    while i < len(ws):
        w, s, e = ws[i]
        if i + 1 < len(ws) and (w, ws[i + 1][0]) in MERGE:
            nxt = ws[i + 1]
            w2 = MERGE[(w, nxt[0])]
            if nxt[0][-1:] in ".,:?":
                w2 += nxt[0][-1]
            out.append([w2, s, nxt[2]])
            i += 2
            continue
        out.append([FIX.get(w, w), s, e])
        i += 1
    return out


def groups(ws, max_words=3, max_chars=16):
    g, out = [], []
    for w in ws:
        txt = " ".join(x[0] for x in g + [w])
        if g and (len(g) >= max_words or len(txt) > max_chars):
            out.append(g)
            g = []
        g.append(w)
        if w[0][-1:] in ".,:?":
            out.append(g)
            g = []
    if g:
        out.append(g)
    return out


def bare(w: str) -> str:
    return w.strip(".,:?¿¡!").lower()


def make_ass(all_words, segs, offsets, path: Path, end_time: float):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat Thin Black,92,&H00FFFFFF,&H00FFFFFF,&H00151515,&H64000000,0,0,0,0,100,100,1,0,1,7,4,5,60,60,0

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    HI = "&H004DB8FF&"   # ámbar cálido (BGR)
    KEY = "&H0080D8FF&"  # dorado claro para palabras clave
    WHITE = "&H00FFFFFF&"
    lines = []
    n = 0
    events = []
    for ws, seg, off in zip(all_words, segs, offsets):
        for g in groups(clean_words(ws)):
            t0 = off + g[0][1] - seg["start"]
            t1 = off + g[-1][2] - seg["start"]
            events.append([t0, t1, g, off, seg["start"]])
    for k, (t0, t1, g, off, st) in enumerate(events):
        nxt = events[k + 1][0] if k + 1 < len(events) else end_time
        end = min(max(t1 + 0.15, t0 + 0.45), nxt)
        tilt = (-3, 3)[n % 2]
        n += 1
        y = 1330
        anim = (f"{{\\an5\\pos({W//2},{y})\\frz{tilt*4}\\fscx55\\fscy55\\alpha&HFF&"
                f"\\t(0,90,\\alpha&H00&)"
                f"\\t(0,160,\\frz{-tilt*0.5:.1f}\\fscx112\\fscy112)"
                f"\\t(160,260,\\frz{tilt}\\fscx100\\fscy100)}}")
        body = []
        for w, s, e in g:
            ms0 = int((off + s - st - t0) * 1000)
            ms1 = int((off + e - st - t0) * 1000)
            base = KEY if bare(w) in KEYWORDS else WHITE
            word = w.upper().strip(",.:")
            body.append(f"{{\\1c{base}\\t({max(ms0,0)},{max(ms0,0)+60},\\1c{HI}\\fscx108\\fscy108)"
                        f"\\t({ms1},{ms1+80},\\1c{base}\\fscx100\\fscy100)}}{word}")
        # salida: pequeño giro y desvanecido
        dur_ms = int((end - t0) * 1000)
        out = f"{{\\t({max(dur_ms-90,0)},{dur_ms},\\alpha&HFF&\\fscx90\\fscy90)}}"
        lines.append(f"Dialogue: 0,{ass_time(t0)},{ass_time(end)},Cap,,0,0,0,,{anim}{out}{' '.join(body)}")
    path.write_text(head + "\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clips", nargs=6)
    ap.add_argument("--words", required=True)
    ap.add_argument("--fonts", default=None, help="carpeta con Montserrat Black .ttf")
    ap.add_argument("--out", default="output/velas/reel_velas.mp4")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    words = [d["words"] for d in json.loads(Path(a.words).read_text())]
    tmp = Path(a.work or tempfile.mkdtemp())
    tmp.mkdir(parents=True, exist_ok=True)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    segs = build_segments(a.clips, PLAN, words, tmp)
    vid, aud, offsets = join(segs, tmp)
    total = sum(s["dur"] for s in segs)
    ass = out.with_suffix(".ass")
    make_ass(words, segs, offsets, ass, total)
    fontsdir = f":fontsdir={a.fonts}" if a.fonts else ""
    vf = (f"eq=contrast=1.05:saturation=1.06,colorbalance=rs=0.02:bs=-0.02,"
          f"unsharp=5:5:0.6:5:5:0.0,ass={ass}{fontsdir},fade=t=in:d=0.2")
    run(["ffmpeg", "-v", "error", "-y", "-i", str(vid), "-i", str(aud), "-vf", vf,
         "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "17", "-preset", "slow",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
         "-t", f"{total:.3f}", str(out)])
    print(f"Listo: {out}  ({total:.1f} s)")


if __name__ == "__main__":
    main()
