"""Video 2: El día que la Ciudad de México se rompió. Composición HyperFrames (estilo stickman a color).

Cada escena empieza en la primera frase de su bloque del guion (assets/segmentos.json), así la
animación queda pegada a la narración. Subtítulos palabra por palabra, y efectos en cada golpe.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01_isla"))
from rig_lib import (BLUE, CREAM, H, INK, PINK, PURP, RED, SKIN, TEAL, W, YEL, Anim, doll, rig, sky,  # noqa: E402
                     trajinera, tree, water)

ROOT = Path(__file__).parent
SEG = json.loads((ROOT / "assets/segmentos.json").read_text())
FIN = round(SEG[-1]["fin"] + 2.0, 2)
GREEN, ORANGE, GRAY, DARK = "#2bb673", "#ff9f1c", "#8d99ae", "#14141a"
JUL = dict(shirt="#f1faee", pants="#6c757d", hat="sombrero", mustache=True)
DET = dict(shirt="#a47148", pants="#3d405b", hat="fedora")
ANA = dict(shirt=GREEN, pants="#264653")

# primera línea de cada escena -> tiempo de inicio
FIRST: dict[str, int] = {}
for i, s in enumerate(SEG):
    FIRST.setdefault(s["escena"], i)


def T(esc: str, k: int = 0) -> float:
    return SEG[FIRST[esc] + k]["ini"]


# ============================================================ piezas gráficas

def text(x, y, s, cls="mid", anchor="middle", id_=""):
    i = f' id="{id_}"' if id_ else ""
    return f'<text{i} x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{s}</text>'


def pill(id_, x, y, w, label, fill=INK, cls="tag", rot=0):
    w = max(w, len(label) * 31 + 90)
    return (f'<g id="{id_}" transform="translate({x} {y}) rotate({rot})"><rect x="{-w / 2}" y="-44" width="{w}" height="88" rx="44" '
            f'fill="{fill}" stroke="{INK}" stroke-width="7"/>{text(0, 16, label, cls)}</g>')


def stamp(id_, x, y, w, label, fill=RED, rot=-7):
    w = max(w, len(label) * 42 + 80)
    return (f'<g id="{id_}" transform="translate({x} {y}) rotate({rot})"><rect x="{-w / 2}" y="-72" width="{w}" height="144" rx="12" '
            f'fill="{fill}" stroke="{INK}" stroke-width="8"/>{text(0, 25, label, "stamp")}</g>')


def building(id_, x, base, w, h, color, floors=None, label=""):
    """Edificio de fachada con ventanas. (x, base) = esquina inferior izquierda."""
    floors = floors or max(2, int(h // 58))
    cols = max(2, int(w // 62))
    win = []
    fh = (h - 30) / floors
    for r in range(floors):
        for c in range(cols):
            wx = x + 18 + c * ((w - 36) / cols)
            wy = base - h + 18 + r * fh
            lit = YEL if (r * 7 + c * 3) % 5 == 0 else "#dbe7f0"
            win.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{(w - 36) / cols - 16:.1f}" height="{fh * .45:.1f}" fill="{lit}" stroke="{INK}" stroke-width="3"/>')
    lab = text(x + w / 2, base - h - 14, label, "tiny") if label else ""
    return (f'<g id="{id_}"><rect x="{x}" y="{base - h}" width="{w}" height="{h}" fill="{color}" stroke="{INK}" stroke-width="8"/>'
            + "".join(win) + lab + "</g>")


def dust(id_, x, y, s=1.0):
    puffs = "".join(f'<circle cx="{dx}" cy="{dy}" r="{r}" fill="#e6e1d6" stroke="{INK}" stroke-width="4" opacity=".92"/>'
                    for dx, dy, r in ((-60, -10, 46), (10, -40, 58), (70, -6, 44), (-20, 20, 38)))
    return f'<g id="{id_}" transform="translate({x} {y}) scale({s})" opacity="0">{puffs}</g>'


def ring(id_, cx, cy, color=TEAL):
    return (f'<g id="{id_}" transform="translate({cx} {cy}) scale(.1)" opacity=".9">'
            f'<circle r="60" fill="none" stroke="{color}" stroke-width="10"/></g>')


def ghost_filter():
    return ('<defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')


def card(id_, x, y, w, h, title, fill=YEL, body="", rot=0):
    return (f'<g id="{id_}" transform="translate({x} {y}) rotate({rot})">'
            f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="22" fill="{CREAM}" stroke="{INK}" stroke-width="9"/>'
            f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="104" rx="22" fill="{fill}" stroke="{INK}" stroke-width="9"/>'
            f'{text(0, -h / 2 + 70, title)}{body}</g>')


def wave_row(id_, y, color=TEAL, x0=-40, x1=1960, amp=26):
    d = f"M{x0} {y} " + " ".join(f"Q{x + 80} {y - amp} {x + 160} {y}" for x in range(x0, x1, 160))
    return f'<path id="{id_}" d="{d}" stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round"/>'


def ground(id_, y, color="#9c6644"):
    return f'<g id="{id_}"><rect x="-60" y="{y}" width="{W + 120}" height="{H - y + 60}" fill="{color}" stroke="{INK}" stroke-width="8"/></g>'


# ============================================================ animación auxiliar

def shake(a: Anim, cam: str, t: float, dur: float, amp: float = 12) -> None:
    a.raw(f'tl.fromTo("#{cam}",{{attr:{{transform:"translate(0 0)"}}}},{{attr:{{transform:"translate({amp} {-amp * .5})"}},'
          f'duration:.05,repeat:{max(1, int(dur / .05))},yoyo:true,ease:"none"}},{t:.3f});')


def sway(a: Anim, id_: str, t: float, dur: float, amp: float, period: float, cx: float, cy: float) -> None:
    n = max(1, int(dur / (period / 2)))
    a.raw(f'tl.fromTo("#{id_}",{{attr:{{transform:"rotate({-amp} {cx} {cy})"}}}},{{attr:{{transform:"rotate({amp} {cx} {cy})"}},'
          f'duration:{period / 2:.3f},repeat:{n},yoyo:true,ease:"sine.inOut"}},{t:.3f});')


def fall(a: Anim, id_: str, t: float, cx: float, cy: float, deg: float = 88, dur: float = 1.1) -> None:
    a.raw(f'tl.to("#{id_}",{{attr:{{transform:"rotate({deg} {cx} {cy})"}},duration:{dur},ease:"power2.in"}},{t:.3f});')


def puff(a: Anim, id_: str, t: float, dur: float = 1.4) -> None:
    a.raw(f'tl.fromTo("#{id_}",{{opacity:0}},{{opacity:.95,duration:.25}},{t:.3f});')
    a.raw(f'tl.to("#{id_}",{{opacity:0,duration:{dur}}},{t + .25:.3f});')
    a.sound("impact-bass-1", t, .4)


def counter(id_: str, t: float, dur: float, end: int, fmt: str = "{}") -> None:
    a_lines.append(f'(function(){{const o={{n:0}};const el=document.querySelector("#{id_}");'
                   f'tl.to(o,{{n:{end},duration:{dur},ease:"power2.out",onUpdate:()=>{{el.textContent="{fmt}".replace("{{}}",Math.round(o.n));}}}},{t:.3f});}})();')


a_lines: list[str] = []


def finish(a: Anim) -> None:
    a.lines.extend(a_lines)


# ============================================================ escenas del video 3 (Los Andes, 1972)
# Se inserta en build.py: usa los mismos helpers (shake, sway, fall, puff, counter, pill, stamp, card, rig).

NIEVE = "#f8f9fa"


def montanas(id_: str = "mont") -> str:
    tri = [(-100, 1080, 300, 260), (250, 1080, 760, 120), (640, 1080, 1180, 300), (1080, 1080, 1620, 80), (1480, 1080, 1900, 260)]
    out = []
    for x0, y0, px, py in tri:
        out.append(f'<path d="M{x0} {y0} L{px} {py} L{px + 420} {y0} Z" fill="#5c677d" stroke="{INK}" stroke-width="7"/>')
        out.append(f'<path d="M{px - 110} {py + 120} L{px} {py} L{px + 110} {py + 120} Z" fill="{NIEVE}" stroke="{INK}" stroke-width="6"/>')
    return f'<g id="{id_}">' + "".join(out) + "</g>"


def avion(id_: str, x: float, y: float, s: float = 1.0) -> str:
    return (f'<g id="{id_}" transform="translate({x} {y}) scale({s})">'
            f'<path d="M-160 0 L140 -6 Q190 0 150 14 L-160 18 Z" fill="{NIEVE}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
            f'<path d="M-10 -4 L-60 -90 L-30 -92 L30 -6 Z" fill="{NIEVE}" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M-130 2 L-170 -40 L-150 -40 L-110 0 Z" fill="{NIEVE}" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="20" y="-28" width="16" height="16" fill="{BLUE}"/><rect x="50" y="-28" width="16" height="16" fill="{BLUE}"/>'
            f'<rect x="80" y="-28" width="16" height="16" fill="{BLUE}"/></g>')


def e_gancho3(a: Anim, t0: float, d: float) -> str:
    tc = t0 + 2.6
    a.raw(f'tl.from("#av",{{opacity:1,duration:0.01}},{t0:.3f});')
    a.raw(f'tl.fromTo("#av",{{attr:{{transform:"translate(1700 180) scale(.9) rotate(18)"}}}},'
          f'{{attr:{{transform:"translate(1020 560) scale(.9) rotate(30)"}},duration:2.3,ease:"power2.in"}},{t0 + .2:.3f});')
    shake(a, "cam3", tc, 1.4, 16)
    puff(a, "cd3", tc, 1.8)
    a.pop("#hz1", t0 + .3, "50% 50%", .5)
    a.pop("#hz2", t0 + 1.0, "50% 50%", .5)
    a.sound("impact-bass-2", tc, .5)
    return (sky("gg3", "#0b1d3a", "#3a5a80") + f'<g id="cam3">{montanas("mg3")}'
            + avion("av", 1700, 180, .9) + f'<g id="cd3">{dust("cdd3", 1020, 600, 1.6)}</g></g>'
            + f'<g id="hz1">{text(960, 180, "LOS DIERON", "huge")}</g>'
            + f'<g id="hz2">{text(960, 340, "POR MUERTOS", "huge")}</g>')


def e_quiz3(a: Anim, t0: float, d: float) -> str:
    tr = T("quiz", 2)
    dots = []
    for i in range(45):
        r_, c_ = divmod(i, 9)
        x, y = 470 + c_ * 110, 330 + r_ * 110
        dots.append((i, x, y))
    for i, x, y in dots:
        a.pop(f"#p{i}", t0 + .4 + i * .02, "50% 50%", .25)
    for k, i in enumerate(range(16)):
        a.raw(f'tl.to("#p{i}",{{attr:{{fill:"{YEL}"}},duration:.2,delay:0}},{tr + .1 + k * .05:.2f});')
    a.pop("#cnt3", tr + .4)
    a.sound("sparkle", tr, .45)
    grid = "".join(f'<g id="p{i}" transform="translate({x} {y})"><circle r="34" fill="#adb5bd" stroke="{INK}" stroke-width="6"/></g>'
                   for i, x, y in dots)
    return (sky("gq3", "#fff3d6", "#ffd6a5") + grid
            + f'<g id="qt3" transform="translate(960 170) scale(.68)">{text(0, 0, "¿CUÁNTOS SOBREVIVIERON?", "huge")}</g>'
            + f'<g id="cnt3">{pill("c3", 960, 900, 720, "16 DE 45", RED, "tag")}</g>')


def e_impacto3(a: Anim, t0: float, d: float) -> str:
    tav = T("impacto", 1)
    a.raw(f'tl.fromTo("#av2",{{attr:{{transform:"translate(1200 -100) scale(.9)"}}}},'
          f'{{attr:{{transform:"translate(930 640) scale(.9)"}},duration:1.6,ease:"power2.in"}},{t0 + .2:.3f});')
    shake(a, "cam4", t0 + 1.8, 1.4, 14)
    puff(a, "cd4", t0 + 1.8, 1.8)
    a.raw(f'tl.fromTo("#avl",{{attr:{{transform:"translate(0 0)"}},opacity:.95}},'
          f'{{attr:{{transform:"translate(-260 300)"}},opacity:.9,duration:2.6,ease:"power1.in"}},{tav:.3f});')
    a.pop("#pl4", tav + .4)
    a.pop("#st4", T("impacto", 0) + .2)
    a.sound("whoosh-cinematic", tav, .5)
    a.sound("impact-bass-1", t0 + 1.8, .5)
    return (sky("gi4", "#4a5568", "#a0aec0") + f'<g id="cam4">{montanas("mg4")}'
            + f'<path id="avl" d="M700 380 L860 500 L800 700 L650 580 Z" fill="{NIEVE}" stroke="{INK}" stroke-width="7" opacity=".0"/>'
            + avion("av2", 1200, -100, .9) + f'<g id="cd4">{dust("cdd4", 930, 640, 1.8)}</g></g>'
            + f'<g id="st4">{stamp("stp4", 960, 200, 620, "13 OCT 1972", INK, -4)}</g>'
            + f'<g id="pl4">{pill("pp4", 1400, 760, 620, "8 MÁS EN LA AVALANCHA", RED, "tiny")}</g>')


def e_espera3(a: Anim, t0: float, d: float) -> str:
    tr = T("espera", 2)
    a.face("e1", t0, "flat", (6, -6), (-6, 0))
    a.face("e2", t0, "flat", (-6, 6), (6, -2))
    a.face("e3", t0, "flat", (0, 0), (0, 0))
    for i in range(3):
        a.pose(f"e{i + 1}", t0 + .3, .5, "power2.inOut", uaR=-40, faR=-20, uaL=10)
    a.blink("e1", t0 + 1.6)
    a.pop("#radio", tr - .2, "50% 50%")
    a.pop("#bus", tr + .3)
    a.sound("error", tr + .3, .4)
    a.raw(f'tl.to("#snow",{{y:40,duration:{d},repeat:-1,ease:"none"}},{t0});')
    snow = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" opacity=".85"/>' for x, y in
                   [(160, 120), (420, 320), (900, 160), (1300, 240), (1640, 120), (640, 480), (1480, 420)])
    tent = f'<path d="M780 860 L960 620 L1140 860 Z" fill="#ef476f" stroke="{INK}" stroke-width="8"/>'
    radio = (f'<g id="radio" transform="translate(1500 760)"><rect x="-80" y="-44" width="160" height="88" rx="14" fill="#343a40" stroke="{INK}" stroke-width="7"/>'
             f'<line x1="50" y1="-44" x2="90" y2="-140" stroke="{INK}" stroke-width="8"/><circle cx="-40" cy="0" r="18" fill="{YEL}" stroke="{INK}" stroke-width="5"/></g>')
    return (sky("ge5", "#1d2d50", "#4a6fa5") + montanas("mg5") + f'<g id="snow">{snow}</g>' + tent
            + rig("e1", 760, 900, .85, shirt="#f1faee", pants="#6c757d")
            + rig("e2", 960, 900, .85, shirt=YEL, pants="#264653")
            + rig("e3", 1140, 900, .85, shirt=BLUE, pants="#3d405b")
            + radio + f'<g id="bus">{pill("bsp", 960, 220, 860, "BÚSQUEDA SUSPENDIDA", RED, "tag")}</g>')


def e_caminata3(a: Anim, t0: float, d: float) -> str:
    tc = T("caminata", 2)
    a.walk("cp", t0, tc - t0, .34)
    a.walk("cq", t0 + .1, tc - t0, .34)
    a.raw(f'tl.fromTo("#cp",{{attr:{{transform:"translate(40 830) scale(.85)"}}}},{{attr:{{transform:"translate(940 830) scale(.85)"}},duration:{tc - t0:.2f},ease:"none"}},{t0:.3f});')
    a.raw(f'tl.fromTo("#cq",{{attr:{{transform:"translate(10 930) scale(1)"}}}},{{attr:{{transform:"translate(910 930) scale(1)"}},duration:{tc - t0:.2f},ease:"none"}},{t0 + .1:.3f});')
    a.raw(f'tl.from("#cat",{{opacity:0,duration:.6}},{tc + .2:.3f});')
    a.pop("#pill10", t0 + .3)
    a.pop("#pillcat", tc + .4)
    a.sound("riser", t0, .4)
    return (sky("gc6", "#7ec8e3", "#e0fbfc") + montanas("mg6") + ground("cg6", 900, "#dbe9f4")
            + rig("cp", 40, 830, .85, **ANA, prop_r="") + rig("cq", 10, 930, 1.0, **JUL)
            + f'<g id="cat" transform="translate(1500 880)">{rig("catr", 0, 0, .9, shirt="#c77dff", pants="#3d405b", hat="fedora")}</g>'
            + f'<g id="pill10">{pill("p10", 560, 150, 720, "10 DÍAS DE CAMINO", INK, "tag")}</g>'
            + f'<g id="pillcat">{pill("pc", 1500, 260, 560, "SERGIO CATALÁN", TEAL, "tiny")}</g>')


def e_rescate3(a: Anim, t0: float, d: float) -> str:
    tr = T("rescate", 1)
    tc = T("rescate", 1) + 1.2
    a.raw(f'tl.fromTo("#heli",{{attr:{{transform:"translate(-300 180)"}}}},{{attr:{{transform:"translate(1900 180)"}},duration:{d - 1:.2f},ease:"none"}},{t0:.3f});')
    a.raw(f'tl.to(".rot",{{attr:{{transform:"rotate(360 0 0)"}},duration:.25,repeat:{int(d * 4)},ease:"none"}},{t0:.3f});')
    a.raw(f'tl.from("#dias",{{opacity:0,duration:.5}},{t0 + .3:.3f});')
    counter("cntd", t0 + .3, 1.8, 72)
    a.pop("#s16", tr + .2)
    a.pop("#s29", tc + .4)
    a.sound("sparkle", tr, .4)
    heli = (f'<g id="heli" transform="translate(0 180)"><ellipse cx="0" cy="0" rx="130" ry="60" fill="{RED}" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="-190" y="-14" width="110" height="18" fill="{INK}"/><line x1="-160" y1="-72" x2="190" y2="-72" stroke="{INK}" stroke-width="10" class="rot"/>'
            f'<circle cx="0" cy="-70" r="8" fill="{INK}"/></g>')
    return (sky("gr7", "#ffe8a3", "#b5e48c") + montanas("mg7") + ground("rg7", 900, "#dbe9f4")
            + heli + f'<g id="dias">{text(960, 585, "DÍAS DESDE EL CHOQUE", "tiny")}</g>'
            + f'<g transform="translate(960 480)">{text(0, 0, "", "tiny")}<text id="cntd" x="0" y="0" text-anchor="middle" class="huge">0</text></g>'
            + f'<g id="s16">{stamp("sv16", 560, 760, 520, "16 VIVOS", GREEN, -4)}</g>'
            + f'<g id="s29">{pill("pn29", 1400, 760, 600, "29 NO VOLVIERON", INK, "tag")}</g>')


def e_cierre3(a: Anim, t0: float, d: float) -> str:
    a.walk("cz", t0, d - 3, .34)
    a.raw(f'tl.fromTo("#cz",{{attr:{{transform:"translate(200 880) scale(1)"}}}},{{attr:{{transform:"translate(1100 880) scale(1)"}},duration:{d - 3:.2f},ease:"none"}},{t0:.3f});')
    a.pop("#qq3", t0 + .2)
    a.pop("#pqh", T("cierre", 1) + .5)
    a.raw(f'tl.from("#cfin3",{{scale:.3,opacity:0,transformOrigin:"50% 50%",duration:.5,ease:"back.out(2)"}},{T("cierre", 1) + 2:.2f});')
    a.sound("chime", T("cierre", 1) + 2, .4)
    return (sky("gz8", "#ff7b54", "#ffd56b") + f'<circle cx="1500" cy="330" r="120" fill="{YEL}"/>' + montanas("mg8") + ground("zg8", 900, "#dbe9f4")
            + rig("cz", 200, 880, 1.0, **ANA)
            + f'<g id="qq3">{text(960, 240, "¿QUÉ HARÍAS TÚ?", "huge")}</g>'
            + f'<g id="pqh">{pill("ph3", 960, 430, 780, "COMENTA TU RESPUESTA", PURP, "tag")}</g>'
            + f'<g id="cfin3">{card("cf3", 1540, 760, 520, 340, "MIRA ESTO", YEL, text(0, 100, "LA ISLA DE LAS", "tiny") + text(0, 160, "MUÑECAS", "tiny"), 3)}</g>')


ESC = {"gancho": e_gancho3, "quiz": e_quiz3, "impacto": e_impacto3, "espera": e_espera3, "caminata": e_caminata3,
       "rescate": e_rescate3, "cierre": e_cierre3}

# ============================================================ subtítulos

CLAVE = {"sobrevivieron", "montaña", "avalancha", "radio", "búsqueda", "dieciséis", "veintinueve", "helicópteros", "caminar", "niña", "edificio", "edificios", "cayó", "ciudad", "suelo", "resonancia", "ritmo", "pisos", "bebés", "hospital",
         "topos", "voluntarios", "muertos", "exactitud", "alerta", "agáchate", "cúbrete", "agárrate", "lago", "gelatina",
         "terremoto", "sismo", "vive", "vida", "clave", "cartón", "resonancia"}
NUM = {"Dieciséis de cuarenta y cinco": "16 de 45", "cuarenta y cinco": "45", "mil novecientos setenta y dos": "1972",
       "setenta y dos días": "72 días", "trece de octubre": "13 de octubre", "veintidós de diciembre": "22 de diciembre",
       "veintitrés de diciembre": "23 de diciembre", "diez días": "10 días", "Veintinueve": "29", "ocho personas": "8 personas"}


def subtitulos(a: Anim) -> str:
    cues = []
    n = 0
    for si, s in enumerate(SEG):
        txt = s["texto"]
        for k, v in NUM.items():
            txt = txt.replace(k, v)
        words = txt.split()
        dur = s["fin"] - s["ini"]
        groups, cur = [], []
        for w in words:
            cur.append(w)
            if sum(len(x) + 1 for x in cur) > 26 or re.search(r"[.?!:…]$", w):
                groups.append(cur); cur = []
        if cur:
            groups.append(cur)
        total = sum(len(w) + 2 for w in words)
        acc = 0
        for g in groups:
            glen = sum(len(w) + 2 for g_ in [g] for w in g_)
            g0 = s["ini"] + dur * acc / total
            g1 = s["ini"] + dur * (acc + glen) / total
            spans, wacc = [], acc
            for w in g:
                wt = s["ini"] + dur * wacc / total
                hot = re.sub(r"[^\wáéíóúñ]", "", w.lower()) in CLAVE
                spans.append(f'<span id="cw{n}" class="w{" hot" if hot else ""}">{w}</span>')
                a.raw(f'tl.from("#cw{n}",{{scale:.4,opacity:0,y:24,duration:.18,ease:"back.out(3)"}},{wt:.3f});')
                wacc += len(w) + 2
                n += 1
            cues.append([g0, g1, "".join(spans)])
            acc += glen
    html = []
    for i, (g0, g1, sp) in enumerate(cues):
        nxt = cues[i + 1][0] if i + 1 < len(cues) else FIN
        end = min(nxt, g1 + .6)
        html.append(f'<div id="cap{i}" class="clip cap" data-start="{g0:.3f}" data-duration="{max(.3, end - g0 - .02):.3f}">{sp}</div>')
    return "\n".join(html)


# ============================================================ composición

def build() -> str:
    a = Anim()
    order = [e["id"] for e in json.loads((ROOT / "guion.json").read_text())["escenas"]]
    starts = {}
    for esc in order:
        starts[esc] = 0.0 if esc == order[0] else round(T(esc) - .15, 3)
    html = []
    for idx, esc in enumerate(order):
        t0 = starts[esc]
        t1 = starts[order[idx + 1]] if idx + 1 < len(order) else FIN
        d = round(t1 - t0, 3)
        svg = ESC[esc](a, t0, d)
        sid = f"sc{idx:02d}"
        html.append(f'<div id="{sid}" class="clip scene" data-start="{t0:.3f}" data-duration="{d}" data-layout-allow-overflow>'
                    f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}">{svg}</svg></div>')
        a.raw(f'tl.fromTo("#{sid} svg",{{scale:1}},{{scale:1.05,duration:{d},ease:"none",transformOrigin:"50% 55%"}},{t0:.3f});')
        if idx:
            a.raw(f'tl.from("#{sid} svg",{{opacity:.0,duration:.2}},{t0:.3f});')
            a.sound("whoosh-short", t0 - .05, .3)
    caps = subtitulos(a)
    finish(a)
    (ROOT / "assets/sfx_events.json").write_text(json.dumps(sorted(a.sfx, key=lambda x: x[1])))
    js = "\n".join("  " + l for l in a.lines)
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="./gsap.min.js"></script>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{DARK}; }}
  #root {{ width:100%; height:100%; position:relative; overflow:hidden; font-family:Lato, sans-serif; color:{INK}; }}
  .scene {{ position:absolute; inset:0; overflow:hidden; }}
  .scene svg {{ position:absolute; inset:0; }}
  .huge {{ font: 900 150px Lato, sans-serif; fill:#fff; stroke:{INK}; stroke-width:12px; paint-order:stroke; }}
  .tag {{ font: 900 46px Lato, sans-serif; letter-spacing:.06em; fill:#fff; }}
  .tagd {{ font: 900 60px Lato, sans-serif; fill:{INK}; }}
  .tiny {{ font: 900 40px Lato, sans-serif; letter-spacing:.06em; fill:{INK}; }}
  .mid {{ font: 900 54px Lato, sans-serif; fill:{INK}; }}
  .stamp {{ font: 900 66px Lato, sans-serif; letter-spacing:.05em; fill:#fff; }}
  .cap {{ position:absolute; left:120px; right:120px; bottom:56px; display:flex; flex-wrap:wrap; gap:0 22px;
          justify-content:center; z-index:10; }}
  .cap .w {{ display:inline-block; margin:0 .1em; font: 900 72px Lato, sans-serif; color:#fff; text-transform:uppercase;
             -webkit-text-stroke: 12px {INK}; paint-order: stroke fill; }}
  .cap .w.hot {{ color:{YEL}; }}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute">{ghost_filter()}</svg>
<div id="root" data-composition-id="main" data-start="0" data-duration="{FIN}" data-width="{W}" data-height="{H}">
<audio id="voz" src="assets/narracion.wav" data-start="0" data-duration="{FIN}" data-volume="2.5"></audio>
<audio id="musica" src="assets/musica.wav" data-start="0" data-duration="{FIN}" data-volume="1"></audio>
<audio id="efectos" src="assets/sfx.wav" data-start="0" data-duration="{FIN}" data-volume="0.55"></audio>
{chr(10).join(html)}
{caps}
</div>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
{js}
  window.__timelines["main"] = tl;
  tl.seek(0);
</script>
</body>
</html>
'''


if __name__ == "__main__":
    (ROOT / "index.html").write_text(build(), encoding="utf-8")
    print("escrito index.html ·", FIN, "s ·", len(ESC), "escenas")
