#!/usr/bin/env python3
"""Montaje del spot "La Colina" (1971 -> 2026), reimaginación no oficial.

Uso:  python3 build.py   -> export/ (final, clean, ligero, .srt, informe)
Requiere: ffmpeg, clips/clipN.mp4, audio/cancion.mp3, ../revival01/fonts/
"""
import json, os, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
CLIPS, AUDIO, EXPORT = (os.path.join(ROOT, d) for d in ("clips", "audio", "export"))
FONTS = os.path.join(ROOT, "..", "revival01", "fonts")
TMP = os.path.join(ROOT, ".tmp")
W, H, FPS = 1080, 1920, 24
SRC_W, SRC_H = 360, 640
os.makedirs(TMP, exist_ok=True)
os.makedirs(EXPORT, exist_ok=True)


def run(cmd):
    print("$", " ".join(cmd)[:150], "...")
    subprocess.run(cmd, check=True)


# (nombre, clip, entrada, salida, zoom, cx, cy, transición de entrada)
SHOTS = [
    ("A",  "clip1", 0.0, 7.6, 1.00, .5, .5,  None),          # TV con la colina
    ("B",  "clip2", 0.5, 8.0, 1.00, .5, .5,  ("fade", .6)),  # Valeria, azotea
    ("C1", "clip3", 0.0, 4.0, 1.00, .5, .5,  None),          # Ernesto, ventana
    ("C2", "clip3", 4.0, 8.0, 1.15, .45, .36, None),         # ángulo cerrado: sonrisa
    ("D",  "clip4", 0.0, 8.0, 1.00, .5, .5,  None),          # Kenji, autobús
    ("E",  "clip5", 0.6, 8.0, 1.00, .5, .5,  ("fade", .5)),  # ascenso
    ("F1", "clip6", 1.1, 4.5, 1.00, .5, .5,  None),          # encuentro
    ("F2", "clip6", 4.5, 8.0, 1.12, .5, .44, None),          # ángulo cerrado: abrazo
    ("G",  "clip8", 0.0, 8.0, 1.00, .5, .5,  None),          # botella + aérea
    ("K",  None,    0.0, 5.8, 1.00, .5, .5,  ("fade", .8)),  # negro: cierre
]
MUSIC_START = 3.6


def render_shot(name, clip, t0, t1, z, cx, cy):
    out = os.path.join(TMP, f"{name}.mkv")
    dur = t1 - t0
    if clip is None:
        run(["ffmpeg", "-v", "error", "-y",
             "-f", "lavfi", "-i", f"color=black:s={W}x{H}:r={FPS}:d={dur}",
             "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={dur}",
             "-c:v", "libx264", "-qp", "0", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
             "-c:a", "pcm_s16le", "-shortest", out])
        return out
    cw, ch = round(SRC_W / z / 2) * 2, round(SRC_H / z / 2) * 2
    x = max(0, min(SRC_W - cw, round(SRC_W * cx - cw / 2)))
    y = max(0, min(SRC_H - ch, round(SRC_H * cy - ch / 2)))
    vf = (f"crop={cw}:{ch}:{x}:{y},scale={W}:{H}:flags=lanczos+accurate_rnd+full_chroma_int,"
          f"unsharp=5:5:0.55:5:5:0.0,setsar=1,fps={FPS},format=yuv420p")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0}", "-t", f"{dur}",
         "-i", os.path.join(CLIPS, clip + ".mp4"),
         "-vf", vf, "-af", "aresample=48000,aformat=channel_layouts=stereo",
         "-c:v", "libx264", "-qp", "0", "-preset", "ultrafast", "-c:a", "pcm_s16le", out])
    return out


def duration(path):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path]).strip())


files, starts, durs = [], [], []
t = 0.0
for name, clip, t0, t1, z, cx, cy, trans in SHOTS:
    f = render_shot(name, clip, t0, t1, z, cx, cy)
    d = duration(f)
    if trans:
        t -= trans[1]
    files.append(f); starts.append(t); durs.append(d)
    t += d
TOTAL = t
S = {s[0]: st for s, st in zip(SHOTS, starts)}
K_START = S["K"]

# ---------------------------------------------------------------- textos
F_VHS = os.path.join(FONTS, "VT323.woff")
F_SERIF = os.path.join(FONTS, "Cormorant-500.woff")
F_SERIF_B = os.path.join(FONTS, "Cormorant-600.woff")
F_SANS = os.path.join(FONTS, "Inter-400.woff")
TEXTS = []


def add(text, font, size, color, y, t0, t1, fi=.33, fo=.25, flicker=False):
    TEXTS.append((text, font, size, color, y, t0, t1, fi, fo, flicker))


add("1971.", F_VHS, 150, "white", .12, .30, 4.2, .15, .3, True)
add("Un anuncio que le enseñó", F_VHS, 72, "white", .195, .55, 4.2, .15, .3, True)
add("al mundo a cantar junto.", F_VHS, 72, "white", .232, .80, 4.2, .15, .3, True)
add("Reimaginación no oficial · Hecho con IA", F_SANS, 32, "white@0.8", .78, .30, 4.2)

# Letra de la canción como subtítulo poético (tiempos en LYRICS, relativos a la canción)
LYRICS = json.load(open(os.path.join(AUDIO, "letra_tiempos.json"), encoding="utf-8")) \
    if os.path.exists(os.path.join(AUDIO, "letra_tiempos.json")) else []
for a, b, txt in LYRICS:
    t0, t1 = MUSIC_START + a, MUSIC_START + b
    if t1 < K_START - 4.5:  # que no choque con los textos finales
        add(txt, F_SERIF, 58, "white", .70, t0, t1, .3, .3)

e1 = S["G"] + 3.2
add("En 1971 nos pidieron", F_SERIF, 64, "white", .27, e1, K_START + 1.7, .6, .5)
add("cantar en armonía.", F_SERIF, 64, "white", .305, e1 + .15, K_START + 1.7, .6, .5)
add("En 2026 basta con", F_SERIF, 64, "white", .36, e1 + 1.4, K_START + 1.7, .6, .5)
add("subir a la colina.", F_SERIF, 64, "white", .395, e1 + 1.55, K_START + 1.7, .6, .5)
add("Comparte algo real.", F_SERIF_B, 96, "0xF2B544", .45, K_START + 2.1, TOTAL, .6, .6)
add("Reimaginación no oficial y homenaje a un anuncio de 1971.", F_SANS, 27, "white@0.72", .74, K_START + 2.6, TOTAL, .4, .6)
add("Sin afiliación con ninguna marca. Contenido generado con IA.", F_SANS, 27, "white@0.72", .758, K_START + 2.6, TOTAL, .4, .6)


def alpha_expr(t0, t1, fi, fo, flicker):
    fin = f"if(lt(t,{t0}),0,if(lt(t,{t0+fi}),(t-{t0})/{fi},1))"
    fout = f"if(gt(t,{t1}),0,if(gt(t,{t1-fo}),({t1}-t)/{fo},1))"
    a = f"{fin}*{fout}"
    if flicker:
        a += "*(0.82+0.18*gt(sin(t*37)+sin(t*23),0.4))"
    return a


def drawtexts():
    parts = []
    for i, (txt, font, size, color, y, t0, t1, fi, fo, flicker) in enumerate(TEXTS):
        tf = os.path.join(TMP, f"t{i}.txt")
        open(tf, "w", encoding="utf-8").write(txt)
        parts.append(
            f"drawtext=fontfile='{font}':textfile='{tf}':fontsize={size}:fontcolor={color}"
            f":x=(w-text_w)/2:y=h*{y}-text_h/2"
            f":shadowcolor=black@0.6:shadowx=0:shadowy=3:borderw=2:bordercolor=black@0.4"
            f":enable='between(t,{t0-0.01},{t1+0.01})':alpha='{alpha_expr(t0, t1, fi, fo, flicker)}'")
    return ",".join(parts)


# ---------------------------------------------------------------- grafo
inputs = []
for f in files:
    inputs += ["-i", f]
mi = len(files)
inputs += ["-i", os.path.join(AUDIO, "cancion.mp3")]

g = [f"[{i}:v]fps={FPS},setpts=PTS-STARTPTS,settb=1/{FPS*1000}[in{i}]" for i in range(len(files))]
cur_v, cur_a, cur_len = "in0", "0:a", durs[0]
for i in range(1, len(files)):
    trans = SHOTS[i][7]
    nv, na = f"v{i}", f"a{i}"
    if trans:
        d = trans[1]
        g.append(f"[{cur_v}][in{i}]xfade=transition=fade:duration={d}:offset={cur_len-d:.4f},settb=1/{FPS*1000}[{nv}]")
        g.append(f"[{cur_a}][{i}:a]acrossfade=d={d}:c1=tri:c2=tri[{na}]")
        cur_len += durs[i] - d
    else:
        g.append(f"[{i}:a]afade=t=in:d=0.05[ai{i}]")
        g.append(f"[{cur_v}][{cur_a}][in{i}][ai{i}]concat=n=2:v=1:a=1[c{nv}][{na}]")
        g.append(f"[c{nv}]settb=1/{FPS*1000}[{nv}]")
        cur_len += durs[i]
    cur_v, cur_a = nv, na

g.append(f"[{cur_v}]noise=alls=4:allf=t+u,format=yuv420p,split[vbase][vclean]")
g.append(f"[vbase]{drawtexts()}[vtxt]")
ms = int(MUSIC_START * 1000)
g.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=2.5,"
         f"adelay={ms}|{ms},apad=whole_dur={TOTAL:.3f},atrim=0:{TOTAL:.3f},"
         f"afade=t=out:st={TOTAL-3.0:.3f}:d=3.0[mus]")
# Sonido ambiente de los clips por debajo de la música
g.append(f"[{cur_a}]volume=0.55,afade=t=out:st={K_START-0.5:.3f}:d=1.0[amb]")
g.append(f"[amb][mus]amix=inputs=2:normalize=0,atrim=0:{TOTAL:.3f},alimiter=limit=0.9[amix]")

graph = os.path.join(TMP, "graph.txt")
open(graph, "w", encoding="utf-8").write(";\n".join(g))
master = os.path.join(TMP, "master.mkv")
run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex_script", graph,
     "-map", "[vtxt]", "-map", "[vclean]", "-map", "[amix]",
     "-c:v", "libx264", "-qp", "0", "-preset", "ultrafast", "-c:a", "pcm_s24le",
     "-t", f"{TOTAL:.3f}", master])

meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", master, "-map", "0:a",
                       "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
                      capture_output=True, text=True).stderr
m = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
      f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
      f":offset={m['target_offset']}:linear=true,aresample=48000")
enc = ["-c:v", "libx264", "-preset", "slow", "-profile:v", "high", "-pix_fmt", "yuv420p",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart"]
hq = ["-crf", "16", "-maxrate", "16M", "-bufsize", "32M"]
lite = ["-crf", "20", "-maxrate", "7M", "-bufsize", "14M"]
run(["ffmpeg", "-v", "error", "-y", "-i", master, "-map", "0:v:0", "-map", "0:a", "-af", ln, *enc, *hq,
     os.path.join(EXPORT, "revival02_la-colina.mp4")])
run(["ffmpeg", "-v", "error", "-y", "-i", master, "-map", "0:v:0", "-map", "0:a", "-af", ln, *enc, *lite,
     os.path.join(EXPORT, "revival02_la-colina_ligero.mp4")])
run(["ffmpeg", "-v", "error", "-y", "-i", master, "-map", "0:v:1", "-map", "0:a", "-af", ln, *enc, *hq,
     os.path.join(EXPORT, "revival02_clean.mp4")])


def ts(x):
    h, r = divmod(x, 3600); mi_, s = divmod(r, 60)
    return f"{int(h):02}:{int(mi_):02}:{int(s):02},{int(round((s % 1) * 1000)) % 1000:03}"


with open(os.path.join(EXPORT, "revival02.srt"), "w", encoding="utf-8") as fh:
    for n, (a, b, txt) in enumerate(LYRICS, 1):
        fh.write(f"{n}\n{ts(MUSIC_START+a)} --> {ts(MUSIC_START+b)}\n{txt}\n\n")

report = {"duracion_total": round(TOTAL, 2), "loudness_antes": m["input_i"],
          "planos": [{"plano": s[0], "clip": s[1], "fuente": [s[2], s[3]], "zoom": s[4],
                      "inicio": round(st, 2), "fin": round(st + d, 2),
                      "transicion": s[7][0] if s[7] else "corte"}
                     for s, st, d in zip(SHOTS, starts, durs)]}
json.dump(report, open(os.path.join(EXPORT, "informe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps(report, ensure_ascii=False))
