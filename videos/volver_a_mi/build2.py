import json, subprocess, os, sys
S = os.path.dirname(os.path.abspath(__file__))
U = "/root/.claude/uploads/d60bbb93-9d71-5269-bf89-48eddddfd067/"
src = {f[:8]: U + f for f in os.listdir(U) if f.endswith(".mp4")}
tr = json.load(open(S + "/audio/tr.json"))
SEG = S + "/seg3"; os.makedirs(SEG, exist_ok=True)
XF = 0.4
INTRO = 3.2
END = 8.5
# id, in, out, chip, face-y anchor, zoom levels cycled per "camera" shot
segs = [
    ("acac8a52", 0.50, 15.95, None,                  0.30, [1.0, 1.24, 1.08, 1.30]),
    ("9a820ff3", 2.60, 17.00, "Apego emocional",     0.28, [1.0, 1.30, 1.12, 1.38]),
    ("31162a4f", 1.62, 11.80, "Creencias y heridas", 0.08, [1.0, 1.12, 1.04, 1.15]),
    ("a38847f4", 0.00, 11.30, "Límites e identidad", 0.30, [1.0, 1.22, 1.08, 1.26]),
    ("95c690a6", 0.00, 15.60, None,                  0.30, [1.0, 1.20, 1.06, 1.26]),
]
TRANS = ["zoomin", "smoothup", "circleopen", "smoothleft", "fadewhite", "fade"]

def run(c): subprocess.run(c, check=True)
def words_of(k, a, b):
    return [(w[0], w[1], w[2].strip()) for s in tr[k] for w in s["words"] if w[0] >= a - 0.05 and w[1] <= b + 0.1]

grade = "eq=contrast=1.06:saturation=1.1:brightness=0.01,colorbalance=rs=0.03:bs=-0.03:rm=0.02:bm=-0.02,unsharp=5:5:0.6"
shots_all = []
for i, (k, a, b, _, fy, zs) in enumerate(segs):
    # camera cuts at natural pauses, shots >= 2.4s
    ws = words_of(k, a, b); cuts = [0.0]
    for j in range(len(ws) - 1):
        gap = ws[j + 1][0] - ws[j][1]
        c = (ws[j][1] + ws[j + 1][0]) / 2 - a
        if gap > 0.2 and c - cuts[-1] >= 2.4 and (b - a) - c >= 2.0:
            cuts.append(c)
    cuts.append(b - a)
    changed = True
    while changed:
        changed = False
        for n in range(len(cuts) - 1):
            if cuts[n + 1] - cuts[n] > 4.6:
                mid = (cuts[n] + cuts[n + 1]) / 2
                cand = [((ws[j][1] + ws[j + 1][0]) / 2 - a) for j in range(len(ws) - 1)]
                cand = [c for c in cand if cuts[n] + 1.8 < c < cuts[n + 1] - 1.8]
                if cand:
                    cuts.insert(n + 1, min(cand, key=lambda c: abs(c - mid))); changed = True; break
    shots_all.append(cuts)
    # piecewise zoom: base level per shot + slow push-in (simulated dolly)
    expr = None
    for n in range(len(cuts) - 2, -1, -1):
        c0, c1 = cuts[n], cuts[n + 1]; z0 = zs[n % len(zs)]
        piece = f"({z0}+0.05*(t-{c0:.3f})/{c1 - c0:.3f})"
        expr = piece if expr is None else f"if(lt(t,{c1:.3f}),{piece},{expr})"
    v = "delogo=x=8:y=12:w=170:h=50," if k == "acac8a52" else ""
    vf = (f"{v}scale=w='2*trunc(540*({expr}))':h='2*trunc(960*({expr}))':eval=frame:flags=lanczos,"
          f"crop=1080:1920:x='(in_w-1080)/2':y='(in_h-1920)*{fy}',setsar=1,{grade},fps=30,format=yuv420p")
    af = "highpass=f=80,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-1.5:LRA=9,aresample=48000,aformat=channel_layouts=stereo"
    out = f"{SEG}/{i}.mkv"
    if not os.path.exists(out):
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", src[k], "-vf", vf, "-af", af,
             "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "pcm_s16le", out])

def still_card(srcvid, at, dur, out, dark):
    png = out + ".png"
    run(["ffmpeg", "-v", "error", "-y", *(["-sseof", "-0.1"] if at is None else ["-ss", str(at)]), "-i", srcvid, "-frames:v", "1", png])
    fr = int(dur * 30)
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", png, "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo",
         "-vf", f"scale=2160:3840,zoompan=z='1+0.10*on/{fr}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={fr}:s=1080x1920:fps=30,"
                f"gblur=sigma=38,eq=brightness={dark}:saturation=0.75,drawbox=c=0x2a1f1c@0.45:t=fill,format=yuv420p",
         "-t", str(dur), "-c:v", "libx264", "-crf", "16", "-c:a", "pcm_s16le", out])
still_card(src["acac8a52"], 2.0, INTRO, f"{SEG}/intro.mkv", -0.10)
still_card(f"{SEG}/{len(segs)-1}.mkv", None, END, f"{SEG}/end.mkv", -0.12)

files = [f"{SEG}/intro.mkv"] + [f"{SEG}/{i}.mkv" for i in range(len(segs))] + [f"{SEG}/end.mkv"]
durs = [INTRO] + [b - a for _, a, b, *_ in segs] + [END]
starts = [0.0]
for d in durs[:-1]: starts.append(starts[-1] + d - XF)
total = starts[-1] + durs[-1]
segstart = starts[1:1 + len(segs)]

inp = sum([["-i", f] for f in files], [])
fc = []; vl = "[0:v]"; al = "[0:a]"
for i in range(1, len(files)):
    fc.append(f"{vl}[{i}:v]xfade=transition={TRANS[(i-1) % len(TRANS)]}:duration={XF}:offset={starts[i]:.3f}[v{i}]")
    fc.append(f"{al}[{i}:a]acrossfade=d={XF}:c1=tri:c2=tri[a{i}]")
    vl = f"[v{i}]"; al = f"[a{i}]"

# ---------------- ASS ----------------
def ts(t):
    t = max(0, t); return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
ACC = "&H6DB8E8&"; ACC0 = "&H006DB8E8"
ev = []
def D(layer, st, en, style, txt): ev.append(f"Dialogue: {layer},{ts(st)},{ts(en)},{style},,0,0,0,,{txt}")

# 3D title (extruded layers + rotation in perspective)
def title3d(text, y, size, st, en, delay_ms, rot):
    org = f"\\org(540,{y})"
    depth = 16
    for d in range(depth, 0, -1):
        shade = int(0x22 + (depth - d) * 3)
        col = f"&H{shade//3:02X}{int(shade*0.55):02X}{shade:02X}&"  # dark brown-gold extrusion
        D(4, st, en, "T3D", f"{{\\fs{size}\\c{col}\\bord0\\shad0\\an5{org}\\pos({540+d*0.9:.1f},{y+d*1.3:.1f})"
          f"\\fscx40\\fscy40{rot}\\alpha&HFF&\\t({delay_ms},{delay_ms+80},\\alpha&H00&)"
          f"\\t({delay_ms},{delay_ms+650},0.6,\\fscx100\\fscy100\\frx0\\fry0)"
          f"\\t({int((en-st)*1000)-450},{int((en-st)*1000)},\\fscx135\\fscy135\\alpha&HFF&)}}{text}")
    D(5, st, en, "T3D", f"{{\\fs{size}\\an5{org}\\pos(540,{y})\\fscx40\\fscy40{rot}\\blur6\\alpha&HFF&"
      f"\\t({delay_ms},{delay_ms+80},\\alpha&H00&)\\t({delay_ms},{delay_ms+650},0.6,\\fscx100\\fscy100\\frx0\\fry0\\blur0.6)"
      f"\\t({delay_ms+700},{delay_ms+1100},\\3c&HFFFFFF&)\\t({delay_ms+1100},{delay_ms+1500},\\3c&H3A6E8C&)"
      f"\\t({int((en-st)*1000)-450},{int((en-st)*1000)},\\fscx135\\fscy135\\alpha&HFF&)}}{text}")

ie = INTRO - 0.15
D(3, 0.15, ie, "Kicker", "{\\fad(300,300)\\move(540,600,540,640,0,700)}T A L L E R")
title3d("VOLVER", 820, 205, 0.0, ie, 150, "\\frx75")
title3d("A MÍ", 1060, 260, 0.0, ie, 450, "\\fry-85")
D(3, 1.0, ie, "Info", "{\\fad(400,300)\\move(540,1300,540,1270,0,500)}TALITA KUM  ·  LAURELES, MEDELLÍN")

# subtitles with pop per group and highlighted active word
for i, (k, a, b, chip, *_r) in enumerate(segs):
    T = segstart[i] - a
    ws = words_of(k, a, b); groups = []; g = []
    for j, w in enumerate(ws):
        g.append(w); nx = ws[j + 1] if j + 1 < len(ws) else None
        if len(g) >= 4 or w[2][-1] in ".,?" or (nx and nx[0] - w[1] > 0.35) or not nx:
            groups.append(g); g = []
    for gi, g in enumerate(groups):
        nxtg = groups[gi + 1][0][0] if gi + 1 < len(groups) else 1e9
        for j, w in enumerate(g):
            st = w[0] + T; en = (g[j + 1][0] if j + 1 < len(g) else min(g[-1][1] + 0.25, nxtg)) + T
            txt = " ".join(("{\\c" + ACC + "\\fscx112\\fscy112}" + x[2].upper() + "{\\c&HFFFFFF&\\fscx100\\fscy100}") if x is w else x[2].upper() for x in g)
            pop = "{\\fscx70\\fscy70\\alpha&H80&\\t(0,120,\\fscx106\\fscy106\\alpha&H00&)\\t(120,200,\\fscx100\\fscy100)}" if j == 0 else ""
            D(1, st, en, "Sub", pop + txt)
    if chip:
        s0 = segstart[i] + 0.45
        D(2, s0, s0 + 4.2, "Chip", f"{{\\fad(250,400)\\move(380,320,540,320,0,350)\\t(0,350,\\alpha&H00&)}}{chip.upper()}")
        D(2, s0 + 0.2, s0 + 4.2, "ChipLine", "{\\fad(200,400)\\pos(540,372)\\an5\\fscx0\\t(0,450,\\fscx100)\\p1}m 0 0 l 160 0 160 5 0 5{\\p0}")
        # numbered step badge
        D(2, s0, s0 + 4.2, "Step", f"{{\\fad(250,400)\\pos(540,255)\\fscx50\\fscy50\\t(0,300,\\fscx100\\fscy100)}}0{i}")

# serif title when she says "En volver a mí"
t0 = segstart[0] + 12.45 - segs[0][1]; t1 = segstart[1]
D(3, t0, t1, "Title", "{\\fad(400,400)\\blur1\\fscx80\\fscy80\\t(0,500,\\fscx100\\fscy100)\\move(540,330,540,300,0,600)}Volver a mí")
D(3, t0 + 0.3, t1, "Kicker", "{\\fad(400,400)\\pos(540,180)}T A L L E R")
D(0, t1, starts[-1], "Brand", "{\\fad(600,300)}VOLVER A MÍ  ·  TALLER")

# end card: staggered slide-up animations
e = starts[-1]
def L(st, y, style, txt, fx=""):
    D(3, e + st, total, style, f"{{\\fad(450,0)\\move(540,{y+40},540,{y},0,450){fx}}}{txt}")
L(0.2, 300, "Kicker", "T A L L E R")
D(4, e + 0.3, total, "TitleBig", "{\\fad(500,0)\\fscx70\\fscy70\\t(0,600,0.6,\\fscx100\\fscy100)\\pos(540,430)}Volver a mí")
L(0.8, 545, "Quote", "Volver a ti es volverte a elegir")
D(3, e + 1.0, total, "ChipLine", "{\\pos(540,630)\\an5\\fscx0\\t(0,500,\\fscx100)\\p1}m 0 0 l 180 0 180 5 0 5{\\p0}")
L(1.1, 720, "Info", "TALITA KUM  ·  LAURELES, MEDELLÍN")
L(1.3, 790, "Info", "10 A 12 PM")
L(1.6, 910, "Price", "Valor $120.000")
L(1.85, 1005, "PriceBig", "Pronto pago $90.000")
L(2.1, 1100, "Small", "Recibe material de trabajo, refrigerio y obsequio")
pulse = "".join(f"\\t({s},{s+350},\\fscx107\\fscy107)\\t({s+350},{s+700},\\fscx100\\fscy100)" for s in range(900, int((END-2.6)*1000), 1100))
D(4, e + 2.5, total, "CTA", f"{{\\fad(300,0)\\pos(540,1270)\\fscx60\\fscy60\\t(0,350,\\fscx100\\fscy100){pulse}}}INSCRÍBETE AQUÍ")
L(2.8, 1375, "Url", "volver-a-mi-taller.vercel.app")
L(3.1, 1440, "Small", "Inscripciones abiertas")

ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Lato Black,66,&H00FFFFFF,&H00FFFFFF,&H40000000,&H90000000,0,0,0,0,100,100,1,0,1,3,4,2,90,90,520,1
Style: Chip,Lato Bold,42,&H00FFFFFF,&H00FFFFFF,&H00000000,&H60000000,0,0,0,0,100,100,6,0,1,0,3,5,40,40,0,1
Style: Step,EB Garamond 12,64,{ACC0},&H00FFFFFF,&H00000000,&H60000000,0,1,0,0,100,100,0,0,1,0,3,5,40,40,0,1
Style: ChipLine,Lato Bold,40,{ACC0},&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: T3D,Lato Black,200,&H00A0D9F2,&H00FFFFFF,&H003A6E8C,&H00000000,0,0,0,0,100,100,6,0,1,3,0,5,20,20,0,1
Style: Title,EB Garamond 12,140,&H00FFFFFF,&H00FFFFFF,&H00000000,&H70000000,0,1,0,0,100,100,0,0,1,0,5,5,40,40,0,1
Style: TitleBig,EB Garamond 12,165,&H00FFFFFF,&H00FFFFFF,&H00000000,&H70000000,0,1,0,0,100,100,0,0,1,0,4,5,40,40,0,1
Style: Kicker,Lato Bold,42,{ACC0},&H00FFFFFF,&H00000000,&H60000000,0,0,0,0,100,100,4,0,1,0,3,5,40,40,0,1
Style: Quote,EB Garamond 12,62,&H00F0F0F0,&H00FFFFFF,&H00000000,&H60000000,0,1,0,0,100,100,0,0,1,0,3,5,60,60,0,1
Style: Info,Lato Bold,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H70000000,0,0,0,0,100,100,4,0,1,0,3,5,40,40,0,1
Style: Price,Lato Regular,46,&H00D8D8D8,&H00FFFFFF,&H00000000,&H70000000,0,0,0,0,100,100,1,0,1,0,3,5,40,40,0,1
Style: PriceBig,Lato Black,70,{ACC0},&H00FFFFFF,&H00000000,&H70000000,0,0,0,0,100,100,1,0,1,0,4,5,40,40,0,1
Style: Small,Lato Regular,36,&H00E6E6E6,&H00FFFFFF,&H00000000,&H70000000,0,1,0,0,100,100,0,0,1,0,3,5,60,60,0,1
Style: Url,Lato Bold,44,&H00FFFFFF,&H00FFFFFF,&H00000000,&H70000000,0,0,0,0,100,100,1,0,1,0,3,5,40,40,0,1
Style: CTA,Lato Black,54,&H002A1F1C,&H00FFFFFF,{ACC0},&H00000000,0,0,0,0,100,100,5,0,3,28,0,5,60,60,0,1
Style: Brand,Lato Bold,28,&H50FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,5,0,1,0,2,8,40,40,150,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"
open(S + "/subs2.ass", "w").write(ass)

# ---------------- audio: voice + ducked music + whooshes ----------------
nf = len(files)
fc.append(f"{vl}vignette=PI/5,ass={S}/subs2.ass,format=yuv420p[vo]")
fc.append(f"[{nf}:a]atrim=0:{total:.3f},volume=0.6,afade=t=out:st={total-2.5:.3f}:d=2.5[m]")
fc.append(f"{al}asplit=2[vx][sc]")
fc.append("[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md]")
wt = [0.05] + [starts[i] - 0.45 for i in range(1, nf)]
fc.append(f"[{nf+1}:a]asplit={len(wt)}" + "".join(f"[w{i}]" for i in range(len(wt))))
for i, t in enumerate(wt):
    ms = int(max(0, t) * 1000)
    fc.append(f"[w{i}]adelay={ms}|{ms},volume=0.35[wd{i}]")
fc.append("[vx][md]" + "".join(f"[wd{i}]" for i in range(len(wt))) + f"amix=inputs={2+len(wt)}:duration=first:normalize=0,alimiter=limit=0.95[ao]")
out = sys.argv[1]
run(["ffmpeg", "-v", "error", "-y", *inp, "-i", S + "/music/bed.wav", "-i", S + "/music/whoosh.wav", "-filter_complex", ";".join(fc),
     "-map", "[vo]", "-map", "[ao]", "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-profile:v", "high", "-pix_fmt", "yuv420p",
     "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out])
print("total", round(total, 2), "starts", [round(s, 2) for s in starts], "shots", [[round(c, 1) for c in s] for s in shots_all])
