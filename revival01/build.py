#!/usr/bin/env python3
"""Montaje del spot "1984 -> 2026" (reimaginación no oficial).

Uso:  python3 build.py          -> genera export/ (final, clean, .srt)
Requiere: ffmpeg/ffprobe, fuentes en fonts/, clips en clips/, voz en audio/.
"""
import json, os, subprocess, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
CLIPS, AUDIO, FONTS, EXPORT = (os.path.join(ROOT, d) for d in ("clips", "audio", "fonts", "export"))
TMP = os.path.join(ROOT, ".tmp")
W, H, FPS = 1080, 1920, 24
os.makedirs(TMP, exist_ok=True)
os.makedirs(EXPORT, exist_ok=True)


def run(cmd):
    print("$", " ".join(cmd)[:160], "...")
    subprocess.run(cmd, check=True)


# ---------------------------------------------------------------- 1. Planos
# (nombre, clip, entrada, salida, zoom, centro_x, centro_y, transición_de_entrada)
# zoom > 1 = reencuadre para simular cambio de ángulo.
SHOTS = [
    ("A",  "escena01", 0.0, 6.6, 1.00, .5, .5,  None),          # TV + golpe
    ("B1", "escena02", 1.2, 5.0, 1.00, .5, .5,  ("fade", .25)),  # humo -> túnel
    ("B2", "escena02", 5.0, 8.0, 1.15, .5, .42, None),          # ángulo cerrado
    ("C1", "escena03", 0.5, 4.0, 1.00, .5, .5,  None),          # avanza
    ("C2", "escena03", 4.0, 7.75, 1.00, .5, .5, None),          # auditorio + golpe
    ("D",  "escena05", 0.0, 4.0, 1.00, .5, .5,  None),          # chispas + carrera
    ("E",  "escena04", 0.5, 4.5, 1.00, .5, .5,  None),          # persecución
    ("F",  "escena05", 5.0, 6.5, 1.20, .5, .38, None),          # ángulo cerrado
    ("G",  "escena04", 5.0, 7.6, 1.00, .5, .5,  None),          # persecución
    ("H",  "escena06", 0.0, 7.4, 1.00, .5, .5,  None),          # lanzamiento + impacto
    ("I",  "escena07", 0.0, 7.6, 1.00, .5, .5,  ("fade", .5)),  # levantan la mirada
    ("J",  "escena08", 0.0, 7.7, 1.00, .5, .5,  None),          # se va, fundido a negro
    ("K",  None,       0.0, 5.5, 1.00, .5, .5,  None),          # negro: cierre
]
IMPACT_IN_H = 2.267  # fotograma exacto del impacto en escena06

SRC_W, SRC_H = 360, 640


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
    vf = (f"crop={cw}:{ch}:{x}:{y},"
          f"scale={W}:{H}:flags=lanczos+accurate_rnd+full_chroma_int,"
          f"unsharp=5:5:0.55:5:5:0.0,setsar=1,fps={FPS},format=yuv420p")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0}", "-t", f"{dur}",
         "-i", os.path.join(CLIPS, clip + ".mp4"),
         "-vf", vf, "-af", "aresample=48000,aformat=channel_layouts=stereo",
         "-c:v", "libx264", "-qp", "0", "-preset", "ultrafast",
         "-c:a", "pcm_s16le", out])
    return out


def duration(path):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path]).strip())


# ---------------------------------------------------------------- 2. Línea de tiempo
files, starts, durs = [], [], []
t = 0.0
for i, (name, clip, t0, t1, z, cx, cy, trans) in enumerate(SHOTS):
    f = render_shot(name, clip, t0, t1, z, cx, cy)
    d = duration(f)
    if trans:
        t -= trans[1]
    files.append(f); starts.append(t); durs.append(d)
    t += d
TOTAL = t
h_start = starts[[s[0] for s in SHOTS].index("H")]
IMPACT = h_start + IMPACT_IN_H
SILENCE_FROM = IMPACT - 0.42

# ---------------------------------------------------------------- 3. Voz
# Fragmentos dentro de audio/voz_algoritmo.mp3 (medidos con detección de silencios + Whisper)
VO = {
    "e03": (0.00, 8.55),
    "e05": (8.85, 11.75),
    "e06": (12.15, 17.10),
    "e07": (17.40, 19.72),
}
vo_len = {k: b - a for k, (a, b) in VO.items()}
vo_at = {}
vo_at["e07"] = SILENCE_FROM - vo_len["e07"]        # "Sigue mir—" muere en el silencio
vo_at["e06"] = vo_at["e07"] - 0.38 - vo_len["e06"]
vo_at["e05"] = vo_at["e06"] - 0.40 - vo_len["e05"]
vo_at["e03"] = 9.0                                  # túnel -> auditorio

# Subtítulos: (voz, desde, hasta relativos a la voz, texto)
SUBS = [
    ("e03", 0.00, 1.60, "Bienvenidos."),
    ("e03", 2.00, 4.70, "Aquí todo está decidido por ustedes."),
    ("e03", 5.22, 6.90, "No hace falta buscar…"),
    ("e03", 7.08, 8.50, "ya sé lo que quieren ver."),
    ("e05", 0.15, 1.30, "No pienses."),
    ("e05", 1.59, 2.85, "Sigue deslizando."),
    ("e06", 0.07, 2.30, "Lo que ves… es lo que eres."),
    ("e06", 2.75, 4.90, "Lo que eres… es lo que ves."),
    ("e07", 0.00, 1.00, "Sigue mirando."),
    ("e07", 1.39, 2.32, "Sigue mir—"),
]

# ---------------------------------------------------------------- 4. Textos
F_VHS = os.path.join(FONTS, "VT323.woff")
F_SERIF = os.path.join(FONTS, "Cormorant-500.woff")
F_SERIF_B = os.path.join(FONTS, "Cormorant-600.woff")
F_SANS = os.path.join(FONTS, "Inter-400.woff")
F_SANS_B = os.path.join(FONTS, "Inter-600.woff")
END = TOTAL
K_START = starts[-1]

TEXTS = []  # (texto, fuente, tamaño, color, y_rel, t0, t1, fade_in, fade_out, flicker)


def add(text, font, size, color, y, t0, t1, fi=.33, fo=.25, flicker=False):
    TEXTS.append((text, font, size, color, y, t0, t1, fi, fo, flicker))


# Apertura VHS
add("1984.", F_VHS, 150, "white", .17, .30, 3.70, .15, .25, True)
add("Un anuncio que se emitió", F_VHS, 74, "white", .245, .55, 3.70, .15, .25, True)
add("UNA sola vez.", F_VHS, 74, "white", .285, .80, 3.70, .15, .25, True)
add("Reimaginación no oficial · Hecho con IA", F_SANS, 32, "white@0.8", .75, .30, 3.70)

# Subtítulos de la voz
for k, a, b, txt in SUBS:
    t0, t1 = vo_at[k] + a, vo_at[k] + b
    hard_out = txt.endswith("—")
    add(txt, F_SANS_B, 46, "white", .68, t0, t1, .12, 0 if hard_out else .12)

# Cierre
e1 = K_START - 1.2
add("En 1984 nos prometieron", F_SERIF, 64, "white", .40, e1, K_START + 1.9, .6, .4)
add("que el futuro no sería", F_SERIF, 64, "white", .438, e1 + .15, K_START + 1.9, .6, .4)
add("como “1984”.", F_SERIF, 64, "white", .476, e1 + .3, K_START + 1.9, .6, .4)
add("Y ahora, ¿qué estás mirando tú?", F_SERIF, 60, "white", .40, K_START + 2.2, END, .5, .5)
add("Levanta la mirada.", F_SERIF_B, 92, "0xFF4A1C", .48, K_START + 2.9, END, .5, .5)
add("Reimaginación no oficial y homenaje a un anuncio de 1984.", F_SANS, 27, "white@0.72", .74, K_START + 2.4, END, .4, .5)
add("Sin afiliación con ninguna marca. Contenido generado con IA.", F_SANS, 27, "white@0.72", .758, K_START + 2.4, END, .4, .5)


def alpha_expr(t0, t1, fi, fo, flicker):
    fin = f"if(lt(t,{t0}),0,if(lt(t,{t0+fi}),(t-{t0})/{fi},1))" if fi else f"gte(t,{t0})"
    fout = f"if(gt(t,{t1}),0,if(gt(t,{t1-fo}),({t1}-t)/{fo},1))" if fo else f"lte(t,{t1})"
    a = f"{fin}*{fout}"
    if flicker:
        a += "*(0.82+0.18*gt(sin(t*37)+sin(t*23),0.4))"
    return a


def drawtexts():
    parts = []
    for i, (txt, font, size, color, y, t0, t1, fi, fo, flicker) in enumerate(TEXTS):
        tf = os.path.join(TMP, f"t{i}.txt")
        with open(tf, "w", encoding="utf-8") as fh:
            fh.write(txt)
        parts.append(
            f"drawtext=fontfile='{font}':textfile='{tf}':fontsize={size}:fontcolor={color}"
            f":x=(w-text_w)/2:y=h*{y}-text_h/2"
            f":shadowcolor=black@0.6:shadowx=0:shadowy=3:borderw=2:bordercolor=black@0.4"
            f":enable='between(t,{t0-0.01},{t1+0.01})':alpha='{alpha_expr(t0, t1, fi, fo, flicker)}'")
    return ",".join(parts)


# ---------------------------------------------------------------- 5. Grafo de filtros
inputs = []
for f in files:
    inputs += ["-i", f]
vo_idx = len(files)
inputs += ["-i", os.path.join(AUDIO, "voz_algoritmo.mp3")]

g = []
for i in range(len(files)):
    g.append(f"[{i}:v]fps={FPS},setpts=PTS-STARTPTS,settb=1/{FPS*1000}[in{i}]")
cur_v, cur_a, cur_len = "in0", "0:a", durs[0]
for i in range(1, len(files)):
    trans = SHOTS[i][7]
    nv, na = f"v{i}", f"a{i}"
    if trans:
        d = trans[1]
        off = cur_len - d
        g.append(f"[{cur_v}][in{i}]xfade=transition=fade:duration={d}:offset={off:.4f},settb=1/{FPS*1000}[{nv}]")
        g.append(f"[{cur_a}][{i}:a]acrossfade=d={d}:c1=tri:c2=tri[{na}]")
        cur_len = cur_len + durs[i] - d
    else:
        # micro fundido de audio en cortes secos para evitar clics
        g.append(f"[{i}:a]afade=t=in:d=0.04[ai{i}]")
        g.append(f"[{cur_v}][{cur_a}][in{i}][ai{i}]concat=n=2:v=1:a=1[c{nv}][{na}]")
        g.append(f"[c{nv}]settb=1/{FPS*1000}[{nv}]")
        cur_len += durs[i]
    cur_v, cur_a = nv, na

# Imagen: grano fino uniforme
g.append(f"[{cur_v}]noise=alls=5:allf=t+u,format=yuv420p,split[vbase][vclean]")
g.append(f"[vbase]{drawtexts()}[vtxt]")

# Audio de clips: silencio previo al impacto + cierre
g.append(f"[{cur_a}]volume=0:enable='between(t,{SILENCE_FROM:.3f},{IMPACT:.3f})',"
         f"afade=t=out:st={K_START-1.2:.3f}:d=1.4,asplit=2[sfx][sfx_sc_in]")

# Voz: cada frase recortada, procesada y colocada
vo_labels = []
for k, (a, b) in VO.items():
    lab = f"vo_{k}"
    ms = int(round(vo_at[k] * 1000))
    g.append(f"[{vo_idx}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,"
             f"afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03,"
             f"highpass=f=80,acompressor=threshold=0.1:ratio=3:attack=10:release=200:makeup=2,"
             f"aecho=0.85:0.6:70|130:0.22|0.12,"
             f"aformat=channel_layouts=stereo,adelay={ms}|{ms}[{lab}]")
    vo_labels.append(f"[{lab}]")
g.append("".join(vo_labels) + f"amix=inputs={len(vo_labels)}:normalize=0,apad=whole_dur={TOTAL:.3f},asplit=2[vo][vo_key]")

# Ducking de efectos bajo la voz
g.append("[sfx][vo_key]sidechaincompress=threshold=0.04:ratio=4:attack=50:release=300:makeup=1[sfx_d]")
g.append("[sfx_sc_in]anullsink")
g.append("[sfx_d][vo]amix=inputs=2:normalize=0:weights=1 1.15,"
         f"atrim=0:{TOTAL:.3f},alimiter=limit=0.9[amix]")

graph = os.path.join(TMP, "graph.txt")
with open(graph, "w", encoding="utf-8") as fh:
    fh.write(";\n".join(g))

mix_wav = os.path.join(TMP, "mix.wav")
master = os.path.join(TMP, "master.mkv")
run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex_script", graph,
     "-map", "[vtxt]", "-map", "[vclean]", "-map", "[amix]",
     "-c:v", "libx264", "-qp", "0", "-preset", "ultrafast",
     "-c:a", "pcm_s24le", "-t", f"{TOTAL:.3f}", master])

# ---------------------------------------------------------------- 6. Loudness -14 LUFS (2 pasadas)
meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", master, "-map", "0:a",
                       "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
                      capture_output=True, text=True).stderr
m = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
      f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
      f":offset={m['target_offset']}:linear=true,aresample=48000")

enc = ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high",
       "-pix_fmt", "yuv420p", "-r", str(FPS), "-maxrate", "16M", "-bufsize", "32M",
       "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart"]
final = os.path.join(EXPORT, "revival01_1984-2026.mp4")
clean = os.path.join(EXPORT, "revival01_clean.mp4")
run(["ffmpeg", "-v", "error", "-y", "-i", master, "-map", "0:v:0", "-map", "0:a", "-af", ln, *enc, final])
run(["ffmpeg", "-v", "error", "-y", "-i", master, "-map", "0:v:1", "-map", "0:a", "-af", ln, *enc, clean])

# ---------------------------------------------------------------- 7. SRT + informe


def ts(x):
    h, r = divmod(x, 3600); mi, s = divmod(r, 60)
    return f"{int(h):02}:{int(mi):02}:{int(s):02},{int(round((s % 1) * 1000)) % 1000:03}"


with open(os.path.join(EXPORT, "revival01.srt"), "w", encoding="utf-8") as fh:
    for n, (k, a, b, txt) in enumerate(SUBS, 1):
        fh.write(f"{n}\n{ts(vo_at[k]+a)} --> {ts(vo_at[k]+b)}\n{txt}\n\n")

report = {"duracion_total": round(TOTAL, 2), "impacto": round(IMPACT, 3),
          "silencio_previo": [round(SILENCE_FROM, 3), round(IMPACT, 3)],
          "planos": [{"plano": s[0], "clip": s[1], "fuente": [s[2], s[3]], "zoom": s[4],
                      "inicio": round(st, 2), "fin": round(st + d, 2),
                      "transicion": s[7][0] if s[7] else "corte"}
                     for s, st, d in zip(SHOTS, starts, durs)],
          "voz": {k: round(v, 2) for k, v in vo_at.items()},
          "loudness_medida_antes": m["input_i"]}
with open(os.path.join(EXPORT, "informe.json"), "w", encoding="utf-8") as fh:
    json.dump(report, fh, ensure_ascii=False, indent=2)
print(json.dumps(report, ensure_ascii=False, indent=1))
