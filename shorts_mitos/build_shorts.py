"""Genera las composiciones HyperFrames verticales (1080x1920) de los 3 Shorts de mitos y leyendas."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "videos/01_isla"))
from rig_lib import INK, RED, YEL, TEAL, PURP, BLUE, PINK, Anim, rig
GREEN = "#2bb673"

ROOT = Path(__file__).parent
W, H = 1080, 1920
G = json.loads((ROOT / "guiones.json").read_text())
DUR = {"llorona": 19.6, "cadejo": 23.76, "patasola": 23.44}
JUL = dict(shirt="#f1faee", pants="#6c757d", hat="sombrero", mustache=True)
DET = dict(shirt="#a47148", pants="#3d405b", hat="fedora")
FIG = dict(shirt="#2a9d8f", pants="#264653")


def glow():
    return ('<defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')


def sky(id_, a, b):
    return f'<defs><linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#{id_})"/>'


def moon(x, y, r=110):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff6d5" opacity=".95"/>'


def stars(seed=3):
    pts = [(120, 180), (360, 90), (700, 220), (930, 130), (540, 380), (200, 520), (860, 560), (980, 380), (110, 800)]
    return "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" opacity=".8"/>' for x, y in pts)


def tree(x, y, s=1.0, col="#2b2d42"):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0 L0 -320 M0 -200 L-120 -300 M0 -240 L110 -340" stroke="{col}" stroke-width="22" stroke-linecap="round" fill="none"/>'
            f'<path d="M-20 -330 Q0 -460 20 -330" fill="none"/></g>')


def pill(id_, x, y, w, label, fill=INK, cls="tag"):
    w = max(w, len(label) * 40 + 80)
    return (f'<g id="{id_}"><rect x="{x - w / 2}" y="{y - 60}" width="{w}" height="120" rx="60" fill="{fill}" stroke="{INK}" stroke-width="9"/>'
            f'<text x="{x}" y="{y + 18}" text-anchor="middle" class="{cls}">{label}</text></g>')


def big(id_, x, y, txt, cls="big", col="#fff"):
    return f'<text id="{id_}" x="{x}" y="{y}" text-anchor="middle" class="{cls}" fill="{col}">{txt}</text>'


def ghost_woman(id_, x, y, s=1.0):
    return (f'<g filter="url(#glow)"><g id="{id_}" transform="translate({x} {y}) scale({s})">'
            f'<path d="M-70 -200 Q0 -260 70 -200 L110 40 Q0 70 -110 40 Z" fill="#e9f5ff" opacity=".85" stroke="#9ad0ff" stroke-width="6"/>'
            f'<circle cx="0" cy="-260" r="58" fill="#e9f5ff" opacity=".9" stroke="#9ad0ff" stroke-width="6"/>'
            f'<path d="M-50 -270 Q-40 -350 0 -340 Q40 -350 50 -270" fill="#9ad0ff" opacity=".7"/>'
            f'<circle cx="-20" cy="-262" r="6" fill="{INK}"/><circle cx="20" cy="-262" r="6" fill="{INK}"/></g></g>')


def dog(id_, x, y, s=1.0):
    return (f'<g id="{id_}" transform="translate({x} {y}) scale({s})">'
            f'<ellipse cx="0" cy="0" rx="210" ry="110" fill="#14141a" stroke="#000" stroke-width="8"/>'
            f'<circle cx="-210" cy="-60" r="95" fill="#14141a"/>'
            f'<path d="M-290 -110 L-250 -190 L-215 -110 Z M-190 -140 L-160 -220 L-130 -135 Z" fill="#14141a"/>'
            f'<path d="M-120 60 L-120 170 M-40 60 L-40 170 M90 60 L90 170 M170 60 L170 170" stroke="#14141a" stroke-width="34" stroke-linecap="round"/>'
            f'<path d="M210 -30 Q280 -80 300 -40" stroke="#14141a" stroke-width="26" fill="none" stroke-linecap="round"/>'
            f'<g filter="url(#glow)"><circle id="{id_}-e1" cx="-240" cy="-70" r="20" fill="#ff1f1f"/><circle id="{id_}-e2" cx="-180" cy="-70" r="20" fill="#ff1f1f"/></g></g>')


def patasola(id_, x, y, s=1.0):
    return (f'<g id="{id_}" transform="translate({x} {y}) scale({s})">'
            f'<circle cx="0" cy="-260" r="58" fill="#f4d6c2" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M-50 -270 Q0 -360 50 -270 Q40 -320 0 -330 Q-40 -320 -50 -270" fill="#3d2b1f"/>'
            f'<circle cx="-18" cy="-258" r="6" fill="{INK}"/><circle cx="20" cy="-258" r="6" fill="{INK}"/>'
            f'<path d="M-40 -190 Q0 -170 40 -190 L40 -40 Q0 -20 -40 -40 Z" fill="#7b2cbf" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M-20 -40 L-20 60" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>'
            f'<path d="M-20 60 Q-10 130 -40 150" stroke="{INK}" stroke-width="18" fill="none" stroke-linecap="round"/></g>')


def lamp(x, y):
    return (f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y - 300}" stroke="{INK}" stroke-width="14"/>'
            f'<circle cx="{x}" cy="{y - 320}" r="36" fill="#ffd60a" stroke="{INK}" stroke-width="7"/>')


def scenes_for(sid):
    if sid == "llorona":
        return [
            ('<rect width="1080" height="1920" fill="#0b1026"/>' + stars() + moon(860, 300)
             + '<path d="M0 1080 Q270 1000 540 1080 T1080 1080 L1080 1920 L0 1920 Z" fill="#1d3557" stroke="#000" stroke-width="8"/>'
             + f'<path d="M0 1200 Q270 1140 540 1200 T1080 1200" stroke="#457b9d" stroke-width="8" fill="none"/>'
             + big("t1", 540, 620, "NO TE ASOMES", "huge", YEL)),
            (sky("g2", "#0b1026", "#2b2d42") + moon(860, 300) + stars()
             + '<path d="M0 1080 L1080 1080 L1080 1920 L0 1920 Z" fill="#1d3557" stroke="#000" stroke-width="8"/>'
             + ghost_woman("gw", 540, 1000, 1.2) + big("t2", 540, 360, "LA LLORONA", "huge", "#fff")),
            (sky("g3", "#0b1026", "#2b2d42") + stars() + moon(860, 300)
             + '<path d="M0 1080 L1080 1080 L1080 1920 L0 1920 Z" fill="#1d3557" stroke="#000" stroke-width="8"/>'
             + ghost_woman("gw3", 820, 1000, 1.0) + rig("ml", 300, 1080, 1.4, **FIG)
             + pill("pq", 540, 380, 900, "QUIEN LA SIGUE NO VUELVE", RED, "tag")),
            (sky("g4", "#14002e", "#3c096c") + stars() + big("t4", 540, 230, "¿LA", "huge", "#fff")
             + big("t4b", 540, 380, "ESCUCHARÍAS?", "mid2", YEL) + rig("mq", 540, 1150, 1.25, **JUL)
             ),
        ]
    if sid == "cadejo":
        road = ('<path d="M380 1920 L540 1000 L700 1920 Z" fill="#2b2d42" stroke="#000" stroke-width="8"/>'
                '<path d="M530 1900 L540 1600 L550 1900" stroke="#fff" stroke-width="10" fill="none" opacity=".8"/>')
        return [
            (sky("c1", "#0b1026", "#2b2d42") + stars() + road + lamp(260, 1000) + lamp(820, 1000)
             + big("t1", 540, 500, "¿CAMINAS SOLO?", "huge", YEL)),
            (sky("c2", "#0b1026", "#2b2d42") + road + stars() + '<rect y="1500" width="1080" height="420" fill="#14141a" opacity=".6"/>'
             + dog("cd", 540, 1000, 1.0) + big("t2", 540, 420, "PERRO NEGRO", "huge", "#fff") + big("t2b", 540, 560, "OJOS ROJOS", "huge", RED)),
            (sky("c3", "#1d3557", "#14141a") + stars() + road
             + rig("c3m", 540, 1080, 1.4, **FIG)
             + pill("p1", 260, 700, 440, "PROTECCIÓN", GREEN, "tag") + pill("p2", 820, 700, 440, "MAL PRESAGIO", RED, "tag")
             + big("t3", 540, 420, "¿QUÉ ES?", "huge", YEL)),
            (sky("c4", "#14002e", "#3c096c") + stars() + big("t4", 540, 230, "¿PROTECCIÓN", "mid2", "#fff")
             + big("t4b", 540, 380, "O MALDICIÓN?", "mid2", YEL) + rig("c4m", 540, 1180, 1.25, **JUL)
             ),
        ]
    if sid == "patasola":
        return [
            (sky("p1", "#0b1026", "#1b4332") + tree(120, 1900, 1.8, "#081c15") + tree(950, 1900, 1.7, "#081c15")
             + tree(520, 1900, 1.4, "#0b2e20") + rig("pm", 540, 1080, 1.4, **FIG, prop_r="")
             + big("t1", 540, 520, "SE PERDIÓ", "huge", YEL) + big("t1b", 540, 680, "EN EL BOSQUE", "huge", "#fff")),
            (sky("p2", "#0b1026", "#1b4332") + tree(120, 1900, 1.8, "#081c15") + tree(950, 1900, 1.7, "#081c15")
             + f'<g id="pw"><g id="pwf">{patasola("pat", 800, 1040, 1.45)}</g></g>'
             + f'<path id="bub" d="M180 360 Q180 240 300 240 L780 240 Q900 240 900 360 Q900 480 780 480 L340 480 L250 560 L270 480 Q180 470 180 360 Z" fill="#fff" stroke="{INK}" stroke-width="9"/>'
             + big("t2", 540, 390, "¡JUAN!", "huge", INK)),
            (sky("p3", "#081c15", "#0b2e20") + tree(120, 1900, 1.8, "#041a12") + tree(950, 1900, 1.7, "#041a12")
             + rig("p3m", 400, 1080, 1.35, **FIG) + patasola("pat3", 800, 1040, 1.3)
             + pill("pn", 540, 380, 900, "NO REGRESA", RED, "tag") + big("t3", 540, 580, "LA SIGUE", "huge", "#fff")),
            (sky("p4", "#14002e", "#3c096c") + stars() + big("t4", 540, 230, "¿TE PERDERÍAS", "mid2", "#fff")
             + big("t4b", 540, 380, "POR UNA VOZ?", "mid2", YEL) + rig("p4m", 540, 1180, 1.25, **JUL)
             ),
        ]


def caption(sid, lines, starts, durs):
    out = []
    for i, (ln, s, d) in enumerate(zip(lines, starts, durs)):
        words = ln.split()
        spans = "".join(f'<span class="w">{w}</span>' for w in words)
        out.append(f'<div class="clip cap" data-start="{s:.3f}" data-duration="{d:.3f}" id="cap{i}">{spans}</div>')
    return "\n".join(out)


def build(sid):
    g = next(x for x in G["shorts"] if x["id"] == sid)
    lines = g["lineas"]
    total = DUR[sid]
    words = [len(l.split()) for l in lines]
    pausa = .3
    k = (total - pausa * (len(lines) - 1)) / sum(words)
    starts, durs, t = [], [], 0.0
    for w in words:
        d = w * k
        starts.append(t); durs.append(d); t += d + pausa
    scenes = scenes_for(sid)
    a = Anim()
    html = []
    for i, (svg, s, d) in enumerate(zip(scenes, starts, durs)):
        win_end = starts[i + 1] - .05 if i + 1 < len(starts) else total
        dd = round(win_end - s, 3)
        sid_ = f"sc{i}"
        html.append(f'<div id="{sid_}" class="clip scene" data-start="{s:.3f}" data-duration="{dd}"><svg viewBox="0 0 {W} {H}" width="{W}" height="{H}">{svg}</svg></div>')
        a.raw(f'tl.fromTo("#{sid_} svg",{{scale:1.04}},{{scale:1.12,duration:{dd},ease:"none",transformOrigin:"50% 55%"}},{s:.3f});')
        if i:
            a.raw(f'tl.from("#{sid_} svg",{{opacity:0,duration:.2}},{s:.3f});')
    # animaciones de personaje por escena
    if sid == "llorona":
        a.raw(f'tl.to("#gw",{{attr:{{transform:"translate(540 860) scale(1.4)"}},duration:2.5,yoyo:true,repeat:-1,ease:"sine.inOut"}},{starts[1]:.3f});') if False else None
        a.raw(f'tl.fromTo("#gw",{{y:0}},{{y:-40,duration:2.4,yoyo:true,repeat:6,ease:"sine.inOut"}},{starts[1]:.3f});')
        a.raw(f'tl.fromTo("#gw3",{{x:0}},{{x:-160,duration:{durs[2]:.2f},ease:"none"}},{starts[2]:.3f});')
    if sid == "cadejo":
        a.raw(f'tl.fromTo("#cd-e1",{{opacity:.2}},{{opacity:1,duration:.4,yoyo:true,repeat:10,ease:"none"}},{starts[1]:.3f});')
        a.raw(f'tl.fromTo("#cd-e2",{{opacity:.2}},{{opacity:1,duration:.4,yoyo:true,repeat:10,ease:"none"}},{starts[1]:.3f});')
        a.raw(f'tl.fromTo("#cd",{{x:-60}},{{x:60,duration:1.6,yoyo:true,repeat:5,ease:"sine.inOut"}},{starts[1]:.3f});')
    if sid == "patasola":
        a.raw(f'tl.fromTo("#pw",{{x:-200}},{{x:0,duration:1.8,ease:"power1.out"}},{starts[1]:.3f});')
        a.raw(f'tl.fromTo("#pwf",{{y:0}},{{y:-30,duration:1.0,yoyo:true,repeat:8,ease:"sine.inOut"}},{starts[1]:.3f});')
        a.raw(f'tl.from("#bub",{{scale:0,opacity:0,transformOrigin:"50% 50%",duration:.4,ease:"back.out(2)"}},{starts[1]:.3f});')
    a.raw(f'tl.from("#t1",{{scale:.4,opacity:0,transformOrigin:"50% 50%",duration:.4,ease:"back.out(2)"}},{starts[0]:.3f});') if sid != "x" else None
    cap = caption(sid, lines, starts, durs)
    js = "\n".join("  " + l for l in a.lines)
    html_doc = f'''<!doctype html><html lang="es"><head><meta charset="UTF-8"/><meta name="viewport" content="width={W}, height={H}"/>
<script src="./gsap.min.js"></script><style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#0b1026}}
#root{{width:100%;height:100%;position:relative;overflow:hidden;font-family:Lato,sans-serif}}
.scene{{position:absolute;inset:0;overflow:hidden}} .scene svg{{position:absolute;inset:0}}
.big{{font:900 170px Lato,sans-serif;fill:#fff;stroke:{INK};stroke-width:14px;paint-order:stroke}}
.mid2{{font:900 118px Lato,sans-serif;fill:#fff;stroke:{INK};stroke-width:12px;paint-order:stroke}}
.huge{{font:900 132px Lato,sans-serif;fill:#fff;stroke:{INK};stroke-width:14px;paint-order:stroke}}
.tag{{font:900 56px Lato,sans-serif;fill:#fff;letter-spacing:.04em}}
.cap{{position:absolute;left:60px;right:60px;bottom:200px;display:flex;flex-wrap:wrap;gap:0 18px;justify-content:center;z-index:10}}
.cap .w{{display:inline-block;font:900 86px Lato,sans-serif;color:#fff;text-transform:uppercase;-webkit-text-stroke:12px {INK};paint-order:stroke fill}}
</style></head><body>
<svg width="0" height="0" style="position:absolute">{glow()}</svg>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}">
<audio id="voz" src="assets/narracion.wav" data-start="0" data-duration="{total}" data-volume="2.5"></audio>
<audio id="musica" src="assets/musica.wav" data-start="0" data-duration="{total}" data-volume="1"></audio>
<audio id="efectos" src="assets/sfx.wav" data-start="0" data-duration="{total}" data-volume="0.55"></audio>
{chr(10).join(html)}
{cap}
</div>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
{js}
  window.__timelines["main"] = tl;
  tl.seek(0);
</script></body></html>'''
    d = ROOT / sid
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(html_doc, encoding="utf-8")
    (d / "gsap.min.js").write_text((ROOT / "gsap.min.js").read_text(), encoding="utf-8")
    (d / "assets").mkdir(exist_ok=True)
    (d / "assets/narracion.wav").write_bytes((ROOT / f"assets/{sid}.wav").read_bytes())
    (d / "assets/segmentos.json").write_text(json.dumps([{"escena": f"l{i}", "mood": g["mood"], "texto": l, "ini": round(s, 3), "fin": round(s + dd, 3)}
                                                         for i, (l, s, dd) in enumerate(zip(lines, starts, durs))], ensure_ascii=False, indent=1), encoding="utf-8")
    print(sid, "escrito", d / "index.html", "duración", total)


if __name__ == "__main__":
    for sid in sys.argv[1:] or ["llorona", "cadejo", "patasola"]:
        build(sid)
