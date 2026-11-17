"""Genera index.html: video 1 completo (Isla de las Muñecas) en estilo stickman a color.

Cada escena arranca en una frase de la narración (assets/segmentos.json) y dura hasta la siguiente.
Los subtítulos usan el texto del guion, repartido dentro de la duración de cada frase.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from rig_lib import (BLUE, CREAM, H, INK, PINK, PURP, RED, SKIN, TEAL, W, YEL, Anim, doll, rig, sky,
                     trajinera, tree, water)

ROOT = Path(__file__).parent
SEGS = json.loads((ROOT / "assets/segmentos.json").read_text())
FIN = round(SEGS[-1]["fin"] + 1.8, 2)
GREEN = "#2bb673"
ORANGE = "#ff9f1c"


def S(i: int) -> float:
    return SEGS[i]["ini"]


# ======================================================================= piezas extra

JUL = dict(shirt="#f1faee", pants="#6c757d", hat="sombrero", mustache=True)
DET = dict(shirt="#a47148", pants="#3d405b", hat="fedora")
ANA = dict(shirt=GREEN, pants="#264653")


def text(x, y, s, cls="mid", anchor="middle", id_=""):
    i = f' id="{id_}"' if id_ else ""
    return f'<text{i} x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{s}</text>'


def pill(id_, x, y, w, label, fill=INK, cls="tag", rot=0):
    w = max(w, len(label) * 31 + 90)
    return (f'<g id="{id_}" transform="translate({x} {y}) rotate({rot})"><rect x="{-w / 2}" y="-44" width="{w}" height="88" rx="44" '
            f'fill="{fill}" stroke="{INK}" stroke-width="7"/>{text(0, 16, label, cls)}</g>')


def stamp(id_, x, y, w, label, fill=RED, rot=-7):
    return (f'<g id="{id_}" transform="translate({x} {y}) rotate({rot})"><rect x="{-w / 2}" y="-72" width="{w}" height="144" rx="12" '
            f'fill="{fill}" stroke="{INK}" stroke-width="8"/>{text(0, 25, label, "stamp")}</g>')


def bubble(id_, x, y, w, h, inner, thought=False, tail=(0, 1)):
    tx, ty = tail
    if thought:
        t = (f'<circle cx="{tx * 40}" cy="{h / 2 + 40}" r="20" fill="#fff" stroke="{INK}" stroke-width="6"/>'
             f'<circle cx="{tx * 70}" cy="{h / 2 + 85}" r="12" fill="#fff" stroke="{INK}" stroke-width="6"/>')
        body = f'<ellipse cx="0" cy="0" rx="{w / 2}" ry="{h / 2}" fill="#fff" stroke="{INK}" stroke-width="8"/>'
    else:
        t = f'<path d="M{-20 + tx * 30} {h / 2 - 6} L{tx * 90} {h / 2 + 70} L{30 + tx * 30} {h / 2 - 6} Z" fill="#fff" stroke="{INK}" stroke-width="7"/>'
        body = f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="40" fill="#fff" stroke="{INK}" stroke-width="8"/>'
    cover = '' if thought else f'<rect x="{-25 + tx * 30}" y="{h / 2 - 14}" width="60" height="14" fill="#fff"/>'
    return f'<g id="{id_}" transform="translate({x} {y})">{t}{body}{cover}{inner}</g>'


def canoe(id_, x, y, s=1.0, inner=""):
    return (f'<g id="{id_}" transform="translate({x} {y}) scale({s})">{inner}'
            f'<path d="M-230 -10 Q0 60 230 -10 L200 30 Q0 90 -200 30 Z" fill="#8b5a2b" stroke="{INK}" stroke-width="7"/></g>')


def house(x, y, s=1.0, color=ORANGE):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-150" y="-200" width="300" height="200" fill="{color}" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M-180 -200 L0 -330 L180 -200 Z" fill="{RED}" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="-40" y="-110" width="80" height="110" fill="#5b3a29" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="70" y="-160" width="56" height="56" fill="#bde0fe" stroke="{INK}" stroke-width="6"/></g>')


def check(id_, x, y, ok=True):
    mark = (f'<path d="M-26 0 L-6 22 L30 -24" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            if ok else f'<path d="M-22 -22 L22 22 M22 -22 L-22 22" stroke="#fff" stroke-width="14" stroke-linecap="round"/>')
    return (f'<g id="{id_}" transform="translate({x} {y})"><circle r="44" fill="{GREEN if ok else RED}" stroke="{INK}" '
            f'stroke-width="7"/>{mark}</g>')


def camera(id_, x, y, s=1.0):
    return (f'<g id="{id_}" transform="translate({x} {y}) scale({s})"><rect x="-50" y="-34" width="100" height="68" rx="10" fill="{INK}"/>'
            f'<circle r="22" fill="#bde0fe" stroke="#fff" stroke-width="6"/><rect x="-36" y="-48" width="30" height="16" fill="{INK}"/></g>')


def flash(id_, x, y):
    return (f'<g id="{id_}" transform="translate({x} {y})" opacity="0"><path d="M0 -90 L22 -22 L90 0 L22 22 L0 90 L-22 22 L-90 0 L-22 -22 Z" '
            f'fill="#fff" stroke="{YEL}" stroke-width="6"/></g>')


def card(id_, x, y, w, h, title, fill=YEL, body="", rot=0):
    return (f'<g id="{id_}" transform="translate({x} {y}) rotate({rot})">'
            f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="22" fill="{CREAM}" stroke="{INK}" stroke-width="9"/>'
            f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="104" rx="22" fill="{fill}" stroke="{INK}" stroke-width="9"/>'
            f'{text(0, -h / 2 + 70, title)}{body}</g>')


def ground(color="#2d6a4f", y=860):
    return f'<rect x="-60" y="{y}" width="{W + 120}" height="{H - y + 60}" fill="{color}" stroke="{INK}" stroke-width="7"/>'


def island(x=960, y=880, w=780, trees=True):
    out = (f'<path d="M{x - w} {y} Q{x} {y - 190} {x + w} {y} Z" fill="#9c6644" stroke="{INK}" stroke-width="8"/>'
           f'<path d="M{x - w + 50} {y - 12} Q{x} {y - 160} {x + w - 50} {y - 12}" stroke="{GREEN}" stroke-width="22" fill="none"/>')
    if trees:
        out += tree(x - 400, y - 90, 1.1) + tree(x + 20, y - 135, 1.3) + tree(x + 420, y - 90, 1.1)
    return out


def ghost_filter():
    return ('<defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')


def night(gid="gn"):
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#fff" opacity=".8"/>' for x, y in
                    [(200, 120), (420, 200), (760, 90), (980, 180), (1200, 110), (1380, 240), (300, 320), (1760, 380)])
    return sky(gid, "#1b1446", "#5a3d9a") + ghost_filter() + stars + '<circle cx="1620" cy="190" r="80" fill="#fff6d5"/>'


def tree_eyes(id_, x, y):
    return (f'<g transform="translate({x} {y})"><g id="{id_}" transform="scale(1 1)">'
            f'<ellipse cx="-16" cy="0" rx="13" ry="16" fill="#fff" stroke="{INK}" stroke-width="5"/>'
            f'<ellipse cx="16" cy="0" rx="13" ry="16" fill="#fff" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="-14" cy="3" r="6" fill="{RED}"/><circle cx="18" cy="3" r="6" fill="{RED}"/></g></g>')


# ======================================================================= escenas
# Cada función recibe (a, t, d) y devuelve el SVG de la escena. t = inicio absoluto, d = duración.

def e_2001(a, t, d):
    a.pop("#yr", t + .25, "50% 80%", .55)
    a.pop("#pl", t + .8)
    a.raw(f'tl.from("#boat1",{{x:-700,duration:4.5,ease:"power1.out"}},{t});')
    a.raw(f'tl.fromTo("#hat1",{{attr:{{transform:"rotate(-6)"}}}},{{attr:{{transform:"rotate(6)"}},duration:1,repeat:5,yoyo:true,ease:"sine.inOut"}},{t});')
    return (sky("g1", "#ff7b54", "#ffd56b") + f'<circle cx="1500" cy="330" r="120" fill="{YEL}"/>'
            + trajinera("boat1", 420, 700, RED, TEAL, "LUPITA", .85) + water("w1", 740)
            + f'''<g transform="translate(1180 760)"><g id="hat1" transform="rotate(0)">
                <ellipse cx="0" cy="0" rx="96" ry="20" fill="{YEL}" stroke="{INK}" stroke-width="7"/>
                <path d="M-46 -2 Q-42 -66 0 -68 Q42 -66 46 -2 Z" fill="{YEL}" stroke="{INK}" stroke-width="7"/>
                <path d="M-44 -20 L44 -20" stroke="{RED}" stroke-width="10"/></g></g>
              <g id="yr">{text(960, 300, "2001", "big")}</g>
              <g id="pl"><rect x="650" y="345" width="620" height="78" rx="39" fill="{INK}"/>{text(960, 400, "XOCHIMILCO · MÉXICO", "tag")}</g>''')


def e_noche(a, t, d):
    a.pop("#st2", t + .3, "50% 50%", .35)
    a.raw(f'tl.from("#girl",{{opacity:0,duration:1.2}},{t + 1.2});')
    a.raw(f'tl.to("#girl",{{attr:{{transform:"translate(1330 700) scale(1)"}},duration:1.6,repeat:2,yoyo:true,ease:"sine.inOut"}},{t + 1.2});')
    a.breathe("jul", t, d)
    a.face("jul", t, "flat", (0, 0), (6, 0))
    a.blink("jul", t + .9)
    a.face("jul", t + 2.0, "o", (-18, 18), (10, -2))
    a.squash("jul", t + 2.0, .14)
    a.pose("jul", t + 2.05, .3, uaL=-150, faL=-30, uaR=150, faR=30, head=-6)
    a.blink("jul", t + 3.6)
    a.face("jul", t + 4.3, "frown", (14, -14), (12, 4))
    a.pose("jul", t + 4.3, .5, "power2.inOut", uaL=30, faL=-60, uaR=-30, faR=60, head=8)
    return (night("g2") + '<path d="M-50 760 L760 760 L700 1100 L-50 1100 Z" fill="#2d6a4f" stroke="#14141a" stroke-width="7"/>'
            + water("w2", 790, "#21487a", "#6fa8dc") + rig("jul", 420, 780, 1.05, **JUL)
            + f'<g filter="url(#glow)">{rig("girl", 1330, 740, 1.0, girl=True, ghost=True)}</g>'
            + stamp("st2", 860, 210, 620, "50 AÑOS ANTES", rot=-6))


def e_isla(a, t, d, idp="", n=14):
    colors = [PINK, BLUE, YEL, TEAL, RED, PURP, ORANGE] * 3
    pos = [(480, 470), (560, 400), (640, 480), (920, 400), (1000, 330), (1080, 420), (1290, 430),
           (1370, 370), (1450, 450), (760, 540), (1180, 520), (860, 300), (1220, 330), (420, 560)][:n]
    dolls = "".join(doll(f"d{idp}{i}", x, y, c) for i, ((x, y), c) in enumerate(zip(pos, colors)))
    gap = min(.28, (d - 1.5) / max(1, n))
    for i in range(n):
        a.pop(f"#d{idp}{i}", t + .9 + i * gap, "50% 0%", .35)
    j = f"jul2{idp}"
    a.breathe(j, t, d)
    a.face(j, t, "flat", (10, -10), (-8, -6))
    a.pose(j, t + .2, .5, "power2.inOut", uaR=-160, faR=-10, head=-10)
    a.blink(j, t + 1.6)
    a.face(j, t + d * .55, "smile", (-6, 6), (-6, -4))
    a.pose(j, t + d * .55, .5, "power2.inOut", uaR=-30, faR=40, uaL=10, faL=-20, head=4)
    a.blink(j, t + d * .75)
    return (sky(f"g3{idp}", "#4cc9f0", "#b8f2e6") + water(f"w3{idp}", 900) + island(960, 880, 780) + dolls
            + rig(j, 1640, 860, .9, **JUL, prop_r=f'<g>{doll(f"dh{idp}", 0, 40, PINK, .9)}</g>'))


def e_detective(a, t, d):
    lupa = (f'<g transform="rotate(-90)"><line x1="0" y1="0" x2="0" y2="56" stroke="#5b3a29" stroke-width="12" stroke-linecap="round"/>'
            f'<circle cx="0" cy="88" r="36" fill="#bde0fe" fill-opacity=".6" stroke="{INK}" stroke-width="9"/></g>')
    a.face("det", t, "flat", (-8, 8), (10, 0))
    a.pose("det", t, .3, uaR=-100, faR=-20)
    a.walk("det", t, 2.9, arms=False)
    a.raw(f'tl.to("#det",{{attr:{{transform:"translate(860 900) scale(1.25)"}},duration:2.9,ease:"none"}},{t});')
    a.face("det", t + 3.2, None, None, (-12, 0))
    a.face("det", t + 3.8, None, None, (12, 0))
    a.face("det", t + 4.4, "frown", (20, -20), (0, -6))
    a.pose("det", t + 4.4, .4, "back.out(2)", uaL=-170, faL=-70, head=10)
    a.blink("det", t + 5.4)
    for i, dt in enumerate((3.4, 3.8, 4.2)):
        a.pop(f"#q{i}", t + dt, "50% 100%")
    return (sky("g4", "#ffd60a", "#ffc300") + ground(ORANGE, 860) + rig("det", 200, 900, 1.25, **DET, prop_r=lupa)
            + text(1300, 430, "?", "q", id_="q0") + text(1480, 340, "?", "q", id_="q1") + text(1620, 460, "?", "q", id_="q2"))


def e_expediente(a, t, d, idp="", marks=(1.1, 1.6, 2.1), seal=2.6, label="SIN PRUEBAS"):
    filas = "".join(f'<text x="-350" y="{-50 + i * 92}" class="field">{k}</text>'
                    f'<text id="f{idp}{i}" x="350" y="{-50 + i * 92}" text-anchor="end" class="field red">???</text>'
                    for i, k in enumerate(["NOMBRE", "FECHA", "REGISTRO"]))
    a.raw(f'tl.from("#card{idp}",{{y:260,opacity:0,duration:.6,ease:"back.out(1.6)"}},{t + .1});')
    for i, m in enumerate(marks):
        a.pop(f"#f{idp}{i}", m, "100% 50%", .3)
    a.sound("impact-bass-2", seal, .5)
    a.raw(f'tl.from("#st5{idp}",{{scale:2.6,opacity:0,transformOrigin:"50% 50%",duration:.28,ease:"power4.in"}},{seal});')
    dd = f"det2{idp}"
    a.face(dd, t, "flat", (0, 0), (-12, 0))
    a.breathe(dd, t, d)
    a.blink(dd, t + 1.0)
    a.squash(dd, seal, .18)
    a.face(dd, seal + .05, "open", (-22, 22), (-12, -6))
    a.pose(dd, seal + .05, .3, uaL=-140, faL=-40, uaR=140, faR=40, head=-8)
    return (sky(f"g5{idp}", "#2b2d42", "#8d0801") + card(f"card{idp}", 860, 450, 880, 560, "EXPEDIENTE: LA NIÑA", body=filas, rot=-2)
            + stamp(f"st5{idp}", 1060, 730, 600, label, rot=-9) + rig(dd, 1620, 960, 1.1, **DET))


def e_balanza(a, t, d):
    k = S(7) + .2
    a.pop("#bl", t + .3, "50% 100%")
    a.pop("#br", t + .9, "50% 100%")
    a.face("det3", t, "smile", (-8, 8), (-10, 0))
    a.pose("det3", t + .3, .4, uaL=-120, faL=-20)
    a.face("det3", t + 1.0, None, None, (10, 0))
    a.pose("det3", t + 1.0, .4, uaL=10, uaR=120, faR=20)
    a.raw(f'tl.to("#beam",{{attr:{{transform:"rotate(-8)"}},duration:.8,ease:"elastic.out(1,0.4)"}},{k});')
    a.face("det3", k, "flat", (14, -14), (0, 0))
    a.pose("det3", k, .4, uaL=-30, faL=-80, uaR=30, faR=80)
    a.blink("det3", k + 1.4)
    a.pop("#tr", S(8), "50% 50%")
    beam = (f'<g transform="translate(960 380)"><g id="beam" transform="rotate(0)"><line x1="-420" y1="0" x2="420" y2="0" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
            f'<g id="bl" transform="translate(-420 0)"><line x1="0" y1="0" x2="0" y2="120" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="-190" y="120" width="380" height="110" rx="20" fill="{GREEN}" stroke="{INK}" stroke-width="8"/>{text(0, 192, "COMPROBADO", "tag")}</g>'
            f'<g id="br" transform="translate(420 0)"><line x1="0" y1="0" x2="0" y2="120" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="-160" y="120" width="320" height="110" rx="20" fill="{PURP}" stroke="{INK}" stroke-width="8"/>{text(0, 192, "LEYENDA", "tag")}</g>'
            f'</g></g><path d="M960 380 L960 820 M860 840 L1060 840" stroke="{INK}" stroke-width="18" stroke-linecap="round"/>')
    return (sky("g6", "#caf0f8", "#90e0ef") + ground("#48cae4", 860) + beam
            + rig("det3", 330, 900, 1.15, **DET) + pill("tr", 1340, 190, 560, "MÁS TRISTE · MÁS HUMANA", RED, rot=4))


def e_mapa(a, t, d):
    lake = ("M420 300 Q620 180 860 260 Q1080 200 1240 320 Q1420 420 1380 600 Q1300 780 1060 760 "
            "Q900 860 700 780 Q480 760 420 600 Q360 440 420 300 Z")
    a.raw(f'tl.from("#lake",{{opacity:0,scale:.7,transformOrigin:"50% 50%",duration:1,ease:"power2.out"}},{t + .2});')
    a.pop("#pin1", t + 2.0, "50% 100%")
    a.pop("#pin2", t + 4.5, "50% 100%")
    a.pop("#lbl", t + 6.0)
    pin = lambda id_, x, y, c, lab: (f'<g id="{id_}" transform="translate({x} {y})"><path d="M0 0 Q-44 -60 -44 -96 A44 44 0 1 1 44 -96 Q44 -60 0 0 Z" '
                                     f'fill="{c}" stroke="{INK}" stroke-width="7"/><circle cx="0" cy="-96" r="16" fill="#fff"/>'
                                     f'<rect x="56" y="-140" width="{len(lab) * 34 + 50}" height="76" rx="38" fill="{INK}"/>{text(80, -86, lab, "tag", "start")}</g>')
    return (f'<rect width="{W}" height="{H}" fill="#e9d8a6"/>'
            + "".join(f'<path d="M0 {y} L{W} {y}" stroke="#d4c08a" stroke-width="3"/>' for y in range(60, H, 120))
            + f'<g id="lake"><path d="{lake}" fill="#48cae4" stroke="{INK}" stroke-width="9"/>'
            f'<path d="M560 420 Q760 380 900 460 M640 600 Q860 560 1120 640" stroke="#fff" stroke-width="7" fill="none" opacity=".6"/></g>'
            + pin("pin1", 900, 470, RED, "CIUDAD DE MÉXICO") + pin("pin2", 980, 720, YEL, "XOCHIMILCO")
            + pill("lbl", 960, 120, 820, "UN SISTEMA DE LAGOS ANTIGUO", TEAL))


def e_chinampa(a, t, d):
    a.raw(f'tl.from("#ch",{{y:300,opacity:0,duration:.7,ease:"back.out(1.4)"}},{t + .2});')
    for i, lab in enumerate(("lodo", "raices", "canal")):
        a.pop(f"#lb-{lab}", t + 1.4 + i * .9, "0% 50%")
    a.breathe("far", t, d)
    a.face("far", t, "smile", (-6, 6), (8, 0))
    a.pose("far", t + .5, .5, "power2.inOut", uaR=-150, faR=-20, uaL=-130, faL=10)
    a.blink("far", t + 3)
    chin = (f'<g id="ch"><rect x="560" y="560" width="800" height="220" fill="#7f5539" stroke="{INK}" stroke-width="8"/>'
            + "".join(f'<path d="M{x} 780 Q{x + 20} 830 {x - 10} 880" stroke="#dda15e" stroke-width="7" fill="none"/>' for x in range(600, 1340, 70))
            + f'<rect x="560" y="530" width="800" height="40" fill="{GREEN}" stroke="{INK}" stroke-width="7"/>'
            + "".join(f'<g transform="translate({x} 530)"><path d="M0 0 L0 -40 M0 -30 L-20 -55 M0 -30 L20 -55" stroke="{GREEN}" stroke-width="10" stroke-linecap="round"/>'
                      f'<circle cx="0" cy="-60" r="14" fill="{RED}" stroke="{INK}" stroke-width="5"/></g>' for x in range(640, 1300, 110))
            + tree(600, 540, .8) + tree(1320, 540, .8) + '</g>')
    return (sky("g7", "#bde0fe", "#e0fbfc") + water("w7", 700, "#219ebc", "#8ecae6") + chin
            + rig("far", 1560, 610, .8, shirt=ORANGE, pants="#264653", hat="sombrero")
            + pill("lb-lodo", 330, 640, 300, "LODO", "#7f5539") + pill("lb-raices", 330, 820, 340, "RAÍCES", "#dda15e")
            + pill("lb-canal", 1640, 900, 320, "CANAL", "#219ebc"))


def e_unesco(a, t, d):
    k = S(13) + .3
    crowd = "".join(rig(f"cr{i}", x, 900, .55, shirt=c) for i, (x, c) in
                    enumerate(zip(range(180, 1800, 190), [PINK, BLUE, YEL, TEAL, RED, PURP, ORANGE, GREEN, PINK])))
    for i in range(9):
        a.face(f"cr{i}", t, "smile", (-6, 6), (0, -4))
        a.pose(f"cr{i}", t + .2 + i * .07, .35, uaL=-150 + i * 4, uaR=150 - i * 4, faL=-30, faR=30)
        a.squash(f"cr{i}", t + .4 + i * .07, .1)
    a.pop("#big1", t + .5)
    a.pop("#badge", k, "50% 50%", .6)
    a.sound("sparkle", k, .4)
    a.raw(f'tl.to("#badge-r",{{attr:{{transform:"rotate(360)"}},duration:{d - (k - t)},ease:"none"}},{k});')
    rays = "".join(f'<path d="M0 0 L{300 * __import__("math").cos(i * .5236):.0f} {300 * __import__("math").sin(i * .5236):.0f}" '
                   f'stroke="{YEL}" stroke-width="40" opacity=".35"/>' for i in range(12))
    badge = (f'<g id="badge" transform="translate(960 380)"><g id="badge-r" transform="rotate(0)">{rays}</g>'
             f'<circle r="190" fill="{TEAL}" stroke="{INK}" stroke-width="10"/><circle r="160" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="10 10"/>'
             f'{text(0, -40, "PATRIMONIO", "tag")}{text(0, 10, "DE LA", "tag")}{text(0, 60, "HUMANIDAD", "tag")}'
             f'<rect x="-110" y="100" width="220" height="70" rx="35" fill="{RED}" stroke="{INK}" stroke-width="6"/>{text(0, 150, "1987", "tag")}</g>')
    return (sky("g8", "#ffafcc", "#ffd6a5") + ground("#80b918", 900)
            + f'<g id="big1">{text(960, 150, "UNA DE LAS CIUDADES MÁS GRANDES", "mid")}</g>' + badge + crowd)


def e_fiesta(a, t, d):
    a.raw(f'tl.from("#tb1",{{x:-900,duration:2,ease:"power2.out"}},{t});')
    a.raw(f'tl.from("#tb2",{{x:900,duration:2,ease:"power2.out"}},{t + .3});')
    for i in range(3):
        a.face(f"pa{i}", t, "open" if i == 1 else "smile", (-8, 8), (0, -2))
        for k in range(int(d / .5)):
            up = k % 2 == 0
            a.pose(f"pa{i}", t + .2 + k * .5 + i * .08, .25, "sine.inOut",
                   uaL=-140 if up else -60, uaR=60 if up else 140, faL=-20, faR=20, head=-6 if up else 6)
    notes = "".join(f'<text id="n{i}" x="{x}" y="{y}" class="note">♪</text>' for i, (x, y) in enumerate([(300, 260), (900, 180), (1500, 280), (1200, 220)]))
    for i in range(4):
        a.raw(f'tl.fromTo("#n{i}",{{y:20,opacity:0}},{{y:-30,opacity:1,duration:1,repeat:{int(d) - 1},yoyo:true,ease:"sine.inOut"}},{t + i * .3:.2f});')
    a.raw(f'tl.from("#party",{{x:-900,duration:2,ease:"power2.out"}},{t});')
    party = "".join(rig(f"pa{i}", x, 690, .5, shirt=c) for i, (x, c) in enumerate(zip((300, 440, 580), (PINK, YEL, BLUE))))
    return (sky("g9", "#ff99c8", "#fcf6bd") + notes
            + trajinera("tb1", 440, 700, BLUE, PINK, "XOCHITL", .95) + f'<g id="party">{party}</g>'
            + trajinera("tb2", 1460, 700, GREEN, YEL, "LUPITA", .95)
            + water("w9", 740, "#0f8b8d", "#7fdcd3"))


def e_oscuro(a, t, d):
    k = S(17) + .4
    a.raw(f'tl.to("#cv",{{opacity:.75,duration:{max(1, k - t - 1)},ease:"power1.in"}},{t});')
    a.raw(f'tl.to("#cn",{{attr:{{transform:"translate(1200 790) scale(.7)"}},duration:{d - 1},ease:"power1.inOut"}},{t});')
    for i in range(5):
        a.pop(f"#te{i}", k + i * .35, "50% 50%", .3)
        a.blink(f"te{i}", k + 1.8 + i * .4)
    trees = "".join(tree(x, 800, s) for x, s in ((150, 1.3), (520, 1.0), (1500, 1.1), (1820, 1.3), (900, .8)))
    eyes = "".join(tree_eyes(f"te{i}", x, y) for i, (x, y) in enumerate([(150, 470), (520, 560), (1500, 520), (1820, 450), (900, 600)]))
    return (sky("g10", "#4361ee", "#7209b7") + trees + eyes + water("w10", 800, "#1d3557", "#457b9d")
            + canoe("cn", 300, 790, 1.0, rig("rem", 0, -10, .55, **JUL))
            + f'<rect id="cv" width="{W}" height="{H}" fill="#03001c" opacity="0"/>')


def e_nombre(a, t, d):
    k = S(19)
    a.raw(f'tl.from("#nm",{{x:-900,duration:.6,ease:"back.out(1.4)"}},{t + .3});')
    a.pop("#yr21", t + 3.5)
    a.face("jn", t, "smile", (-8, 8), (-8, 0))
    a.pose("jn", t + .6, .3, uaR=-150, faR=-30)
    for i in range(4):
        a.pose("jn", t + .9 + i * .3, .3, "sine.inOut", faR=-60 if i % 2 == 0 else 0)
    a.blink("jn", t + 2.2)
    a.raw(f'tl.to("#jn",{{attr:{{transform:"translate(1400 600) scale(.75)"}},duration:.8,ease:"power2.inOut"}},{k});')
    a.raw(f'tl.from("#cn2",{{opacity:0,x:200,duration:.8}},{k});')
    for i in range(int((t + d - k) / 1.2)):
        a.pose("jn", k + .8 + i * 1.2, .6, "sine.inOut", uaR=-60, faR=-40, uaL=-40)
        a.pose("jn", k + 1.4 + i * 1.2, .6, "sine.inOut", uaR=-20, faR=-10, uaL=-10)
    return (sky("g11", "#ffbe0b", "#fb5607") + water("w11", 820)
            + canoe("cn2", 1400, 820, 1.2) + rig("jn", 1250, 880, 1.25, **JUL)
            + f'<g id="nm"><rect x="120" y="190" width="900" height="290" rx="30" fill="#fff" stroke="{INK}" stroke-width="9"/>'
            f'{text(570, 330, "JULIÁN", "huge")}{text(570, 420, "SANTANA BARRERA", "mid")}</g>'
            + pill("yr21", 570, 560, 400, "NACE EN 1921", RED))


def e_sevan(a, t, d):
    k = S(21)
    a.pop("#a50", t + .4)
    fam = "".join(rig(f"fm{i}", x, 880, s, shirt=c, girl=g) for i, (x, s, c, g) in
                  enumerate([(330, .95, BLUE, False), (470, .85, PINK, True), (590, .55, YEL, False)]))
    for i in range(3):
        a.face(f"fm{i}", t, "smile", (-6, 6), (8, 0))
        a.face(f"fm{i}", k, "frown", (14, -14), (10, 0))
        a.pose(f"fm{i}", k + .2 + i * .1, .3, uaR=-150, faR=-20)
        for j in range(3):
            a.pose(f"fm{i}", k + .6 + j * .4 + i * .1, .2, "sine.inOut", faR=-50 if j % 2 == 0 else 0)
    a.face("js", t, "flat", (10, -10), (-10, 0))
    a.face("js", k, "frown", (16, -16), (12, 0))
    a.walk("js", k, min(4.5, t + d - k - .5))
    a.raw(f'tl.to("#js",{{attr:{{transform:"translate(1500 880) scale(1)"}},duration:{min(4.5, t + d - k - .5)},ease:"none"}},{k});')
    return (sky("g12", "#a2d2ff", "#cdb4db") + ground("#90be6d", 880) + house(420, 880, 1.0) + fam
            + f'<path d="M1300 880 Q1600 820 1900 880 Z" fill="#9c6644" stroke="{INK}" stroke-width="7"/>' + tree(1700, 860, .9)
            + rig("js", 820, 880, 1.0, **JUL) + stamp("a50", 1400, 250, 460, "AÑOS 50", PURP, 6))


def e_porque(a, t, d):
    k = S(23) + 2.6
    k2 = S(24)
    a.pop("#qq", t + .1, "50% 100%", .4)
    a.face("jp", t, "flat", (18, -18), (0, -8))
    a.pose("jp", t + .2, .4, uaR=-160, faR=-60, head=8)  # mano al mentón
    a.pop("#b1", k, "0% 100%")
    a.pop("#b2", k + 1.6, "100% 100%")
    a.raw(f'tl.to(["#b1","#b2","#qq"],{{opacity:0,duration:.3}},{k2 - .2});')
    a.pop("#c50", k2 + .3)
    a.face("jp", k2, "smile", (-6, 6), (0, 0))
    a.pose("jp", k2, .4, uaR=-30, faR=30, head=0)
    a.blink("jp", k2 + 2)
    a.breathe("jp", t, d)
    return (sky("g13", "#e0aaff", "#c77dff") + ground("#9d4edd", 880) + rig("jp", 960, 900, 1.3, **JUL)
            + text(960, 300, "¿POR QUÉ?", "huge", id_="qq")
            + bubble("b1", 480, 330, 420, 200, text(0, 20, "¿PAZ?", "mid"), thought=True, tail=(1, 1))
            + bubble("b2", 1440, 330, 420, 200, text(0, 20, "¿FE?", "mid"), thought=True, tail=(-1, 1))
            + stamp("c50", 960, 250, 760, "~50 AÑOS EN LA ISLA", TEAL, -3))


def e_vida(a, t, d):
    k = S(26)
    veg = "".join(f'<circle cx="{x}" cy="-70" r="24" fill="{c}" stroke="{INK}" stroke-width="5"/>' for x, c in
                  ((-120, ORANGE), (-70, RED), (80, GREEN), (130, ORANGE)))
    a.raw(f'tl.fromTo("#cn3",{{attr:{{transform:"translate(500 800) scale(1)"}}}},{{attr:{{transform:"translate(1300 800) scale(1)"}},duration:{k - t},ease:"none"}},{t});')
    for i in range(int((k - t) / 1.2)):
        a.pose("jv", t + i * 1.2, .6, "sine.inOut", uaR=-70, faR=-40, uaL=-50)
        a.pose("jv", t + .6 + i * 1.2, .6, "sine.inOut", uaR=-20, faR=-10, uaL=-10)
    a.face("jv", t, "smile", (-6, 6), (10, 0))
    a.raw(f'tl.to("#nightv",{{opacity:1,duration:.8}},{k});')
    a.raw(f'tl.from("#lamp",{{opacity:0,duration:.6}},{k + .4});')
    a.face("jl", k, "flat", (10, -10), (-6, 4))
    a.breathe("jl", k, t + d - k)
    a.blink("jl", k + 2.2)
    lamp = (f'<g id="lamp"><circle cx="1180" cy="760" r="120" fill="{YEL}" opacity=".25"/>'
            f'<rect x="1160" y="740" width="40" height="50" rx="8" fill="{YEL}" stroke="{INK}" stroke-width="5"/></g>')
    return (sky("g14", "#8ecae6", "#ffb703") + water("w14", 820)
            + canoe("cn3", 500, 800, 1.0, rig("jv", 0, -10, .8, **JUL) + f'<g transform="translate(0 0)">{veg}</g>')
            + f'<g id="nightv" opacity="0">{night("g14n")}{island(960, 900, 700, False)}{tree(700, 830, 1.1)}{lamp}'
            + rig("jl", 1000, 830, 1.0, **JUL) + '</g>')


def e_algo(a, t, d):
    a.raw(f'tl.fromTo("#flash",{{opacity:.9}},{{opacity:0,duration:.5}},{t + 3.0});')
    a.sound("glitch-1", t + 2.95, .35)
    a.face("ja", t, "flat", (0, 0), (0, 0))
    a.attr("#ja", "translate(960 1180) scale(2.2)", t + 3.0, .4, "power3.out")
    a.face("ja", t + 3.0, "o", (-24, 24), (0, -6))
    a.squash("ja", t + 3.0, .18)
    a.pose("ja", t + 3.05, .3, uaL=-150, faL=-40, uaR=150, faR=40)
    lines = "".join(f'<line x1="{960 + 700 * __import__("math").cos(i * .3927):.0f}" y1="{540 + 700 * __import__("math").sin(i * .3927):.0f}" '
                    f'x2="{960 + 420 * __import__("math").cos(i * .3927):.0f}" y2="{540 + 420 * __import__("math").sin(i * .3927):.0f}" '
                    f'stroke="#fff" stroke-width="10" opacity=".5"/>' for i in range(16))
    return (sky("g15", "#d00000", "#370617") + f'<g id="spd" opacity=".9">{lines}</g>' + rig("ja", 960, 880, 1.2, **JUL)
            + f'<rect id="flash" width="{W}" height="{H}" fill="#fff" opacity="0"/>')


def e_leyenda(a, t, d):
    k1, k2, k3 = S(30), S(32), S(33)
    a.raw(f'tl.from("#book",{{scale:.6,opacity:0,transformOrigin:"50% 50%",duration:.6,ease:"back.out(1.6)"}},{t + .2});')
    a.raw(f'tl.from("#gl",{{opacity:0,duration:1}},{k1});')
    a.raw(f'tl.to("#gl",{{opacity:0,duration:1.2}},{S(31) + .5});')
    a.raw(f'tl.from("#fd",{{x:-600,duration:2.5,ease:"sine.out"}},{k2});')
    a.raw(f'tl.fromTo("#fd-b",{{attr:{{transform:"rotate(-8)"}}}},{{attr:{{transform:"rotate(8)"}},duration:.8,repeat:5,yoyo:true,ease:"sine.inOut"}},{k2});')
    a.face("jy", t, "flat", (0, 0), (10, 0))
    a.face("jy", S(31), "frown", (16, -16), (8, 4))
    a.face("jy", k2 + 1.5, "o", (-14, 14), (-10, 4))
    a.pose("jy", k3, .4, uaR=-170, faR=-20, head=-8)
    a.raw(f'tl.to("#fd",{{opacity:0,duration:.2}},{k3});')
    a.pop("#hung", k3 + .3, "50% 0%")
    a.face("jy", k3 + .8, "smile", (-6, 6), (8, -6))
    a.breathe("jy", t, d)
    book = (f'<g id="book"><rect x="160" y="110" width="1600" height="860" rx="30" fill="#f8edeb" stroke="{INK}" stroke-width="10"/>'
            f'<line x1="960" y1="110" x2="960" y2="970" stroke="{INK}" stroke-width="6" opacity=".4"/>'
            f'<rect x="640" y="60" width="640" height="100" rx="50" fill="{PURP}" stroke="{INK}" stroke-width="8"/>{text(960, 128, "LA LEYENDA", "tag")}</g>')
    return (sky("g16", "#6d597a", "#b56576") + book
            + water("w16", 760, "#5e60ce", "#b8c0ff").replace(f'M-240 760', 'M-240 760')
            + f'<g filter="url(#glow)">{ghost_filter()}<g id="gl">{rig("gg", 760, 740, .8, girl=True, ghost=True)}</g></g>'
            + f'<g id="fd" transform="translate(0 0)"><g transform="translate(1000 790)"><g id="fd-b" transform="rotate(0)">{doll("fdd", 0, 0, PINK, 1.3)}</g></g></g>'
            + tree(1500, 740, 1.0) + f'<g id="hung">{doll("hd", 1430, 520, PINK, 1.2)}</g>'
            + rig("jy", 1280, 730, .9, **JUL))


def e_proteger(a, t, d):
    k = S(36)
    ks = [S(37), S(38), S(39)]
    a.raw(f'tl.from("#gp",{{opacity:0,duration:1.5}},{k});')
    a.raw(f'tl.to("#gp",{{attr:{{transform:"translate(1450 690) scale(.85)"}},duration:1.4,repeat:{int((t + d - k) / 1.4)},yoyo:true,ease:"sine.inOut"}},{k});')
    a.face("jq", t, "smile", (-6, 6), (8, -4))
    a.pose("jq", t + .3, .5, uaL=-100, faL=-120, uaR=100, faR=120)  # se abraza
    a.face("jq", S(35), "flat", (14, -14), (10, 0))
    a.face("jq", k + .5, "o", (-16, 16), (14, -2))
    a.blink("jq", k + 3)
    for i, kk in enumerate(ks):
        a.pop(f"#pd{i}", kk + .1, "50% 0%")
        a.squash("jq", kk, .06)
    a.breathe("jq", t, d)
    return (night("g17") + ground("#2d6a4f", 880) + tree(1100, 880, 1.3)
            + "".join(f'<g id="pd{i}">{doll(f"pdd{i}", x, y, c, 1.1)}</g>' for i, (x, y, c) in
                      enumerate([(1000, 540, PINK), (1160, 470, BLUE), (1240, 590, YEL)]))
            + rig("jq", 640, 900, 1.15, **JUL)
            + f'<g filter="url(#glow)"><g id="gp" transform="translate(1450 720) scale(.85)">{rig("gq", 0, 0, 1, girl=True, ghost=True)}</g></g>')


def e_recoge(a, t, d):
    k = S(41)
    a.walk("jr", t, 2.6)
    a.raw(f'tl.fromTo("#jr",{{attr:{{transform:"translate(200 880) scale(1)"}}}},{{attr:{{transform:"translate(700 880) scale(1)"}},duration:2.6,ease:"none"}},{t});')
    a.face("jr", t, "flat", (0, 0), (10, 4))
    a.pose("jr", t + 2.8, .4, uaR=-80, faR=-40, head=10)
    a.raw(f'tl.from("#td",{{y:120,opacity:0,duration:.5,ease:"back.out(2)"}},{t + 3.1});')
    a.face("jr", t + 3.3, "smile", (-8, 8), (10, -6))
    a.raw(f'tl.to("#trash",{{opacity:0,duration:.4}},{k - .3});')
    a.raw(f'tl.from("#trade",{{opacity:0,duration:.4}},{k});')
    a.pop("#tv", k + .3)
    a.pop("#ta", k + 1.0)
    a.pop("#tdl", k + 1.7)
    veg = "".join(f'<circle cx="{x}" cy="0" r="56" fill="{c}" stroke="{INK}" stroke-width="7"/>' for x, c in ((-100, ORANGE), (0, RED), (100, GREEN)))
    trash = (f'<g id="trash"><g transform="translate(980 880)"><path d="M-90 0 L-110 -220 L110 -220 L90 0 Z" fill="#6c757d" stroke="{INK}" stroke-width="8"/>'
             f'<rect x="-125" y="-250" width="250" height="34" rx="12" fill="#495057" stroke="{INK}" stroke-width="7"/></g>'
             f'<g id="td">{doll("tdd", 980, 600, BLUE, 1.4)}</g></g>')
    trade = (f'<g id="trade"><g id="tv" transform="translate(1000 330)">{veg}</g>'
             f'<g id="ta"><path d="M1180 330 L1420 330 M1380 290 L1420 330 L1380 370" stroke="{INK}" stroke-width="16" fill="none" stroke-linecap="round"/></g>'
             f'<g id="tdl">{doll("tdd2", 1580, 330, PINK, 2.6)}</g></g>')
    return sky("g18", "#ffd6ff", "#e7c6ff") + ground("#b5838d", 880) + trash + trade + rig("jr", 200, 880, 1.0, **JUL)


def e_rotas(a, t, d):
    k = S(44)
    a.raw(f'tl.from("#bd",{{scale:.4,opacity:0,transformOrigin:"50% 50%",duration:.6,ease:"back.out(1.6)"}},{t + .2});')
    a.pop("#x1", S(43) + .8)
    a.pop("#x2", S(43) + 1.8)
    a.pop("#x3", S(43) + 2.8)
    for i, ic in enumerate(("sun", "rain", "drop")):
        a.pop(f"#{ic}", k + .3 + i * 1.0)
    bd = (f'<g id="bd" transform="translate(960 470) scale(5)"><line x1="0" y1="-80" x2="0" y2="-30" stroke="{INK}" stroke-width="2"/>'
          f'<path d="M0 6 L-20 46 L20 46 Z" fill="#adb5bd" stroke="{INK}" stroke-width="3"/>'
          f'<circle cx="0" cy="-12" r="20" fill="#e9ecef" stroke="{INK}" stroke-width="3"/>'
          f'<path d="M-20 -18 Q-10 -36 4 -30 L10 -36 L14 -28" fill="none" stroke="#6c584c" stroke-width="3"/>'
          f'<circle cx="-7" cy="-11" r="3" fill="{INK}"/><path d="M4 -15 l7 7 M11 -15 l-7 7" stroke="{INK}" stroke-width="2"/>'
          f'<path d="M-6 0 Q0 -4 6 0" stroke="{INK}" stroke-width="2" fill="none"/>'
          f'<path d="M14 10 l8 10" stroke="{INK}" stroke-width="2"/></g>')
    labs = (pill("x1", 380, 330, 380, "SIN BRAZOS", RED, rot=-5) + pill("x2", 1540, 330, 340, "SIN OJOS", RED, rot=5)
            + pill("x3", 1480, 720, 480, "PELO ENREDADO", RED, rot=-4))
    icons = (f'<g id="sun" transform="translate(360 760)"><circle r="70" fill="{YEL}" stroke="{INK}" stroke-width="7"/></g>'
             f'<g id="rain" transform="translate(600 760)"><ellipse rx="90" ry="54" fill="#adb5bd" stroke="{INK}" stroke-width="7"/>'
             + "".join(f'<line x1="{x}" y1="70" x2="{x - 14}" y2="110" stroke="{BLUE}" stroke-width="8" stroke-linecap="round"/>' for x in (-40, 0, 40))
             + f'</g><g id="drop" transform="translate(830 760)"><path d="M0 -70 Q50 0 0 50 Q-50 0 0 -70 Z" fill="{TEAL}" stroke="{INK}" stroke-width="7"/></g>')
    return sky("g19", "#f8f9fa", "#ced4da") + bd + labs + icons


def e_turistas(a, t, d):
    k = S(46)
    tour = "".join(rig(f"tu{i}", x, 690, .5, shirt=c) for i, (x, c) in enumerate(zip((320, 460, 600), (PINK, BLUE, YEL))))
    for i in range(3):
        a.face(f"tu{i}", t + .8 + i * .1, "open", (-24, 24), (14, -4))
        a.pose(f"tu{i}", t + .8 + i * .1, .3, uaL=-150, uaR=150, faL=-40, faR=40)
        a.squash(f"tu{i}", t + .8 + i * .1, .15)
    a.raw(f'tl.from("#boatT",{{x:-700,duration:1.2,ease:"power2.out"}},{t});')
    a.raw(f'tl.to("#scary",{{opacity:0,duration:.5}},{k - .2});')
    a.raw(f'tl.from("#calm",{{opacity:0,duration:.5}},{k});')
    a.face("jt", k, "smile", (-8, 8), (-10, -4))
    a.pose("jt", k + .5, .5, uaR=-120, faR=-30)
    a.pop("#hearts", S(47) + .3)
    a.sound("sparkle", S(47) + .3, .35)
    a.blink("jt", S(47) + 2)
    hearts = "".join(f'<path transform="translate({x} {y})" d="M0 20 C-40 -10 -20 -50 0 -26 C20 -50 40 -10 0 20 Z" fill="{PINK}" stroke="{INK}" stroke-width="5"/>'
                     for x, y in ((1250, 300), (1340, 240), (1430, 310)))
    dolls = "".join(doll(f"cd{i}", x, 780, c, 1.4) for i, (x, c) in enumerate(((760, PINK), (920, BLUE), (1520, YEL), (1660, TEAL))))
    return (f'<g id="scary">{sky("g20", "#3a0ca3", "#7209b7")}<g id="boatT">{trajinera("tb3", 460, 700, "#6c757d", "#495057", "", .95)}{tour}</g>'
            f'{water("w20", 740, "#1d3557", "#457b9d")}</g>'
            + f'<g id="calm">{sky("g20b", "#fec5bb", "#fcd5ce")}{ground(GREEN, 900)}{dolls}{rig("jt", 1220, 900, 1.15, **JUL)}<g id="hearts">{hearts}</g></g>')


def e_fama(a, t, d):
    k = S(49)
    ph = "".join(rig(f"ph{i}", x, 900, .8, shirt=c, prop_r=camera(f"cm{i}", 0, 0, .7)) for i, (x, c) in
                 enumerate(zip((260, 520, 1660), (BLUE, ORANGE, PURP))))
    for i in range(3):
        a.face(f"ph{i}", t, "smile", (-6, 6), (10 if i < 2 else -10, -4))
        a.pose(f"ph{i}", t + .3, .4, uaR=-110 if i < 2 else -120, faR=-60)
        for j in range(4):
            a.raw(f'tl.fromTo("#fl{i}",{{opacity:1}},{{opacity:0,duration:.25}},{t + 1.2 + i * .5 + j * 2.1:.2f});')
            a.sound("click", t + 1.2 + i * .5 + j * 2.1, .4)
    a.face("jf", t, "smile", (-6, 6), (0, -4))
    a.pop("#tlk", k, "0% 100%")
    a.pose("jf", k, .4, uaL=-130, faL=-40)
    a.face("jf", k, "open", (-10, 10), (0, 0))
    for j in range(5):
        a.face("jf", k + .3 + j * .35, "open" if j % 2 else "smile")
    fl = "".join(flash(f"fl{i}", x + 60, 640) for i, x in enumerate((260, 520, 1660)))
    return (sky("g21", "#90e0ef", "#caf0f8") + ground("#9c6644", 900) + tree(1250, 900, 1.2)
            + "".join(doll(f"fa{i}", x, y, c) for i, (x, y, c) in enumerate(((1150, 640, PINK), (1330, 590, BLUE), (1210, 560, YEL))))
            + rig("jf", 960, 900, 1.15, **JUL) + ph + fl
            + bubble("tlk", 1300, 300, 560, 180, text(0, 18, "ESCUCHEN…", "mid"), tail=(-1, 1)))


def e_pesca(a, t, d):
    k = S(51)
    rod = (f'<g transform="rotate(-130)"><line x1="0" y1="0" x2="0" y2="230" stroke="#5b3a29" stroke-width="9" stroke-linecap="round"/></g>')
    a.pop("#y01", t + .2)
    a.face("an", t, "smile", (-6, 6), (-10, 0))
    a.pose("an", t + .5, .3, uaR=-150, faR=-20)
    for j in range(3):
        a.pose("an", t + .8 + j * .35, .2, "sine.inOut", faR=-50 if j % 2 == 0 else 0)
    a.face("jk", t, "smile", (-6, 6), (10, 0))
    a.face("jk", k, "smile", (-6, 6), (12, 0))
    a.pose("jk", k + .3, .4, uaR=-40, faR=-30)
    a.blink("jk", k + 2)
    return (sky("g22", "#ffcad4", "#f4acb7") + water("w22", 860) + f'<path d="M-50 860 L900 860 L860 1100 L-50 1100 Z" fill="#9c6644" stroke="{INK}" stroke-width="7"/>'
            + rig("an", 340, 860, 1.0, **ANA) + rig("jk", 720, 860, 1.0, **JUL, prop_r=rod)
            + stamp("y01", 1400, 250, 340, "2001", RED, 5) + pill("lbA", 340, 380, 360, "ANASTASIO", GREEN))


def e_hallazgo(a, t, d):
    k = S(54)
    a.raw(f'tl.to("#darkh",{{opacity:.55,duration:2}},{t});')
    a.face("ah", t, "flat", (0, 0), (10, 4))
    a.walk("ah", t, 1.9)
    a.raw(f'tl.fromTo("#ah",{{attr:{{transform:"translate(200 860) scale(1)"}}}},{{attr:{{transform:"translate(700 860) scale(1)"}},duration:1.9,ease:"none"}},{t});')
    a.face("ah", t + 2.3, "o", (-22, 22), (14, 6))
    a.squash("ah", t + 2.3, .15)
    a.pose("ah", t + 2.35, .3, uaL=-150, faL=-40, uaR=-100, faR=-20)
    a.raw(f'tl.fromTo("#hat2",{{attr:{{transform:"rotate(-6)"}}}},{{attr:{{transform:"rotate(6)"}},duration:1.1,repeat:{int(d / 1.1)},yoyo:true,ease:"sine.inOut"}},{t});')
    a.raw(f'tl.from("#gh",{{opacity:0,duration:1.4}},{k + .5});')
    a.face("ah", k + 1, "frown", (16, -16), (14, 6))
    return (sky("g23", "#5a189a", "#240046") + water("w23", 860, "#1d3557", "#457b9d")
            + f'<path d="M-50 860 L900 860 L860 1100 L-50 1100 Z" fill="#6f4518" stroke="{INK}" stroke-width="7"/>'
            + f'''<g transform="translate(1180 880)"><g id="hat2" transform="rotate(0)">
                <ellipse cx="0" cy="0" rx="96" ry="20" fill="{YEL}" stroke="{INK}" stroke-width="7"/>
                <path d="M-46 -2 Q-42 -66 0 -68 Q42 -66 46 -2 Z" fill="{YEL}" stroke="{INK}" stroke-width="7"/>
                <path d="M-44 -20 L44 -20" stroke="{RED}" stroke-width="10"/></g></g>'''
            + rig("ah", 200, 860, 1.0, **ANA)
            + f'{ghost_filter()}<g filter="url(#glow)"><g id="gh">{rig("ghg", 1500, 800, .7, girl=True, ghost=True)}</g></g>'
            + f'<rect id="darkh" width="{W}" height="{H}" fill="#000" opacity="0"/>')


def e_versiones(a, t, d):
    k = S(56)
    heart = f'<path transform="translate(0 -10) scale(2.2)" d="M0 20 C-40 -10 -20 -50 0 -26 C20 -50 40 -10 0 20 Z" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
    drop = f'<path transform="scale(1.6)" d="M0 -60 Q44 0 0 40 Q-44 0 0 -60 Z" fill="{BLUE}" stroke="{INK}" stroke-width="4"/>'
    a.raw(f'tl.from("#v1",{{x:-700,duration:.6,ease:"back.out(1.4)"}},{t + .2});')
    a.raw(f'tl.from("#v2",{{x:700,duration:.6,ease:"back.out(1.4)"}},{S(55) + 2.6});')
    a.pop("#vs", S(55) + 3.2)
    a.raw(f'tl.to(["#v1","#v2","#vs"],{{opacity:.15,duration:.6}},{k});')
    a.raw(f'tl.from("#gv",{{opacity:0,scale:.6,transformOrigin:"50% 100%",duration:1.6,ease:"power2.out"}},{k + .4});')
    return (sky("g24", "#3c096c", "#10002b") + ghost_filter()
            + card("v1", 520, 520, 600, 520, "LA FAMILIA", PINK, f'<g transform="translate(0 40)">{heart}</g>{text(0, 200, "INFARTO", "mid")}', -3)
            + card("v2", 1400, 520, 600, 520, "OTROS RELATOS", BLUE, f'<g transform="translate(0 40)">{drop}</g>{text(0, 200, "AHOGADO", "mid")}', 3)
            + text(960, 560, "VS", "huge", id_="vs")
            + f'<g filter="url(#glow)"><g id="gv">{rig("gvg", 960, 900, 1.6, girl=True, ghost=True)}</g></g>')


def e_verdad(a, t, d):
    k = S(59)
    a.raw(f'tl.from("#det4",{{opacity:0,duration:.01}},{t});')
    a.squash("det4", t + .2, .15)
    a.face("det4", t + .2, "open", (-10, 10), (10, 0))
    a.pose("det4", t + .2, .3, uaR=-160, faR=-10)
    a.face("det4", k, "smile", (-6, 6), (12, 0))
    a.pose("det4", k, .4, uaR=-90, faR=-20)
    a.raw(f'tl.from("#cl",{{x:600,opacity:0,duration:.6,ease:"back.out(1.4)"}},{t + .4});')
    marks = [k + 1.4, k + 5.2, k + 9.0]
    for i, m in enumerate(marks):
        a.pop(f"#ck{i}", m, "50% 50%")
        a.blink("det4", m + .3)
    rows = "".join(f'{check(f"ck{i}", -330, -70 + i * 120)}<text x="-260" y="{-52 + i * 120}" class="field">{s}</text>' for i, s in
                   enumerate(["JULIÁN EXISTIÓ", "~50 AÑOS SOLO EN LA ISLA", "MURIÓ EN 2001, EN EL CANAL"]))
    return (sky("g25", "#b7e4c7", "#52b788") + ground("#2d6a4f", 920)
            + card("cl", 1150, 480, 960, 560, "COMPROBADO", GREEN, rows) + rig("det4", 300, 940, 1.2, **DET))


def e_sinregistro(a, t, d):
    return e_expediente(a, t, d, idp="b", marks=(S(61), S(62), S(63)), seal=S(63) + 2.0, label="NADIE LA BUSCÓ")


def e_parientes(a, t, d):
    k = S(65) + 3.0
    fam = "".join(rig(f"pr{i}", x, 900, .95, shirt=c, girl=g) for i, (x, c, g) in
                  enumerate(((240, BLUE, False), (420, PINK, True), (600, ORANGE, False))))
    for i in range(3):
        a.face(f"pr{i}", t, "flat", (10, -10), (10, 0))
        a.pose(f"pr{i}", t + .4 + i * .15, .3, uaR=-150, faR=-110)  # mano en la boca, susurran
    a.pop("#sh", t + .8)
    a.pop("#tb", k, "0% 100%", .5)
    a.raw(f'tl.from("#tbg",{{opacity:0,duration:1}},{k + .6});')
    a.face("jw", t, "flat", (0, 0), (-8, -4))
    a.face("jw", k, "smile", (-6, 6), (-6, -10))
    a.breathe("jw", t, d)
    a.blink("jw", k + 2)
    return (sky("g26", "#fde4cf", "#ffcfd2") + ground("#cdb4db", 900) + fam + rig("jw", 1300, 900, 1.15, **JUL)
            + text(420, 430, "PSST…", "mid", id_="sh")
            + ghost_filter()
            + bubble("tb", 1420, 330, 520, 330, f'<g id="tbg" filter="url(#glow)">{rig("tbr", 0, 130, .6, girl=True, ghost=True)}</g>',
                     thought=True, tail=(-1, 1))
            + pill("lbl2", 1420, 120, 520, "¿LA IMAGINÓ?", PURP))


def e_soledad(a, t, d):
    k1, k2 = S(67), S(68)
    a.raw(f'tl.fromTo("#zm",{{attr:{{transform:"translate(0 0) scale(1)"}}}},{{attr:{{transform:"translate(672 378) scale(.3)"}},duration:{k1 - t},ease:"power2.inOut"}},{t});')
    a.raw(f'tl.to("#zm",{{attr:{{transform:"translate(0 0) scale(1)"}},duration:1.2,ease:"power2.inOut"}},{k1});')
    a.raw(f'tl.from("#gs",{{opacity:0,duration:.8}},{k1 + .4});')
    a.raw(f'tl.to("#gs",{{attr:{{transform:"translate(1180 420) scale(.45)"}},opacity:.6,duration:1.6,ease:"power2.inOut"}},{k2});')
    a.pop("#tbs", k2 - .2, "0% 100%")
    a.face("jz", t, "flat", (12, -12), (0, 4))
    a.face("jz", k2, "smile", (-4, 4), (6, -8))
    a.breathe("jz", t, d)
    a.blink("jz", k1 + 1)
    a.blink("jz", k2 + 2)
    dolls = "".join(doll(f"sz{i}", x, 820, c, 1.0) for i, (x, c) in enumerate(((700, PINK), (820, BLUE), (1150, YEL), (1270, TEAL), (1390, PURP))))
    return (night("g27") + f'<g id="zm" transform="translate(0 0) scale(1)">{water("w27", 860, "#21487a", "#6fa8dc")}'
            f'{island(960, 900, 520, False)}{tree(780, 780, .9)}{tree(1270, 780, .9)}{dolls}{rig("jz", 980, 800, 1.0, **JUL)}</g>'
            + bubble("tbs", 1180, 330, 520, 300, "", thought=True, tail=(-1, 1))
            + f'<g filter="url(#glow)"><g id="gs" transform="translate(1600 900) scale(.8)">{rig("gsr", 0, 0, 1, girl=True, ghost=True)}</g></g>')


def e_hoy(a, t, d):
    a.raw(f'tl.from("#tb4",{{x:-900,duration:1.6,ease:"power2.out"}},{t});')
    a.raw(f'tl.from("#tb5",{{x:900,duration:1.6,ease:"power2.out"}},{t + .4});')
    a.pop("#sign", t + 1.5, "50% 100%")
    a.face("ao", t, "smile", (-8, 8), (-10, 0))
    a.pose("ao", t + 2, .3, uaL=-150, faL=-30)
    for j in range(4):
        a.pose("ao", t + 2.3 + j * .35, .2, "sine.inOut", faL=-60 if j % 2 == 0 else -10)
    a.pop("#lbA2", S(70) + 4.5)
    sign = (f'<g id="sign" transform="translate(1100 860)"><line x1="0" y1="0" x2="0" y2="-260" stroke="#5b3a29" stroke-width="16"/>'
            f'<rect x="-260" y="-380" width="520" height="140" rx="16" fill="{YEL}" stroke="{INK}" stroke-width="8"/>'
            f'{text(0, -330, "ISLA DE LAS", "tag2")}{text(0, -272, "MUÑECAS", "tag2")}</g>')
    return (sky("g28", "#ffbe0b", "#ff006e") + island(1180, 900, 620, False) + tree(1450, 820, 1) + sign
            + rig("ao", 1300, 840, .9, **ANA) + pill("lbA2", 1300, 330, 520, "ANASTASIO LA CUIDA", GREEN)
            + trajinera("tb4", 330, 760, BLUE, PINK, "XOCHITL", .7) + trajinera("tb5", 330, 980, RED, TEAL, "LUPITA", .6)
            + water("w28", 800).replace('class="w28-row"', 'class="w28-row"') )


def e_ofrenda(a, t, d):
    k = S(72)
    vis = "".join(rig(f"vi{i}", x, 900, .85, shirt=c) for i, (x, c) in enumerate(zip((280, 520, 1640), (PINK, BLUE, ORANGE))))
    for i in range(3):
        a.face(f"vi{i}", t, "smile", (-6, 6), (10 if i < 2 else -10, -6))
        a.pose(f"vi{i}", t + 1 + i * .4, .4, uaR=-150 if i < 2 else 150, faR=-20)
    n = 16
    for i in range(n):
        a.pop(f"#of{i}", t + 1.4 + i * ((k - t) / n), "50% 0%", .3)
    cols = [PINK, BLUE, YEL, TEAL, RED, PURP, ORANGE, GREEN] * 2
    pos = [(700 + (i % 8) * 75, 360 + (i // 8) * 110 + (i % 3) * 20) for i in range(n)]
    a.pop("#grow", k + .4)
    a.raw(f'tl.to("#jo",{{opacity:.0,duration:1.2}},{k + 1.8});')
    return (sky("g29", "#caffbf", "#9bf6ff") + ground("#80b918", 900) + tree(960, 900, 1.6)
            + "".join(doll(f"of{i}", x, y, c, 1.0) for i, ((x, y), c) in enumerate(zip(pos, cols)))
            + f'<g id="jo" opacity=".55">{rig("jox", 1240, 900, .9, **JUL)}</g>' + vis
            + pill("grow", 960, 150, 700, "LA COLECCIÓN SIGUE CRECIENDO", PURP))


def e_callback(a, t, d):
    a.raw(f'tl.fromTo("#hat3",{{attr:{{transform:"rotate(-6)"}}}},{{attr:{{transform:"rotate(6)"}},duration:1.1,repeat:{int(d / 1.1)},yoyo:true,ease:"sine.inOut"}},{t});')
    a.raw(f'tl.from("#cb1",{{opacity:0,duration:.8}},{t + 1});')
    a.pop("#cb2", S(74) + .1)
    return (sky("g30", "#ff7b54", "#ffd56b") + f'<circle cx="1500" cy="520" r="120" fill="{YEL}"/>' + water("w30", 740)
            + f'''<g transform="translate(960 760)"><g id="hat3" transform="rotate(0)">
                <ellipse cx="0" cy="0" rx="96" ry="20" fill="{YEL}" stroke="{INK}" stroke-width="7"/>
                <path d="M-46 -2 Q-42 -66 0 -68 Q42 -66 46 -2 Z" fill="{YEL}" stroke="{INK}" stroke-width="7"/>
                <path d="M-44 -20 L44 -20" stroke="{RED}" stroke-width="10"/></g></g>'''
            + f'<g id="cb1">{text(960, 330, "¿Y LA NIÑA?", "huge")}</g>' + stamp("cb2", 960, 490, 500, "ES VERDAD", RED, -4))


def e_hombre(a, t, d):
    a.raw(f'tl.from("#jm-all",{{opacity:0,duration:1}},{t});')
    a.face("jm", t, "smile", (-4, 4), (6, -8))
    a.breathe("jm", t, d)
    a.blink("jm", t + 2)
    a.blink("jm", t + 5)
    dolls = "".join(doll(f"mz{i}", x, y, c, 1.1) for i, (x, y, c) in
                    enumerate(((640, 820, PINK), (760, 840, BLUE), (1160, 840, YEL), (1280, 820, TEAL), (880, 560, PURP), (1060, 520, RED))))
    return (night("g31") + water("w31", 880, "#21487a", "#6fa8dc") + f'<g id="jm-all">{island(960, 920, 560, False)}{tree(960, 800, 1.2)}{dolls}'
            f'{rig("jm", 960, 860, 1.0, **JUL)}</g>')


def e_suscribe(a, t, d):
    k = S(78)
    a.pop("#sub", t + .6, "50% 50%", .6)
    a.sound("chime", t + 1.6, .45)
    a.raw(f'tl.to("#bell",{{attr:{{transform:"rotate(16)"}},duration:.12,repeat:9,yoyo:true,ease:"sine.inOut"}},{t + 1.6});')
    a.face("det5", t, "smile", (-8, 8), (12, 0))
    a.pose("det5", t + .5, .3, uaR=-110, faR=-30)
    a.raw(f'tl.to("#subg",{{opacity:0,duration:.4}},{k - .2});')
    a.raw(f'tl.from("#next",{{opacity:0,duration:.4}},{k});')
    a.pop("#nx", k + .3)
    a.raw(f'tl.fromTo(".bld",{{rotation:-3}},{{rotation:3,transformOrigin:"50% 100%",duration:.1,repeat:{int((t + d - k) / .1) - 4},yoyo:true}},{k + .8});')
    blds = "".join(f'<rect class="bld" x="{x}" y="{900 - h}" width="150" height="{h}" fill="{c}" stroke="{INK}" stroke-width="7"/>'
                   for x, h, c in ((260, 420, "#adb5bd"), (450, 560, "#6c757d"), (640, 380, "#ced4da"), (1150, 500, "#adb5bd"),
                                   (1340, 620, "#6c757d"), (1530, 400, "#ced4da")))
    return (f'<g id="subg">{sky("g32", "#ff006e", "#8338ec")}'
            f'<g id="sub" transform="translate(960 470)"><rect x="-380" y="-110" width="760" height="220" rx="40" fill="#ff0000" stroke="{INK}" stroke-width="10"/>'
            f'{text(-30, 30, "SUSCRÍBETE", "huge2")}<g transform="translate(290 0)"><g id="bell" transform="rotate(0)">'
            f'<path d="M-40 30 Q-40 -50 0 -54 Q40 -50 40 30 Z" fill="{YEL}" stroke="{INK}" stroke-width="7"/><circle cy="44" r="12" fill="{YEL}" stroke="{INK}" stroke-width="5"/></g></g></g>'
            f'{rig("det5", 300, 960, 1.1, **DET)}</g>'
            + f'<g id="next">{sky("g33", "#6c757d", "#343a40")}{ground("#495057", 900)}{blds}'
            f'{stamp("nx", 960, 230, 900, "PRÓXIMO: 19 · SEP · 1985", RED, -3)}</g>')


ESCENAS = [
    (0, e_2001), (1, e_noche), (2, e_isla), (3, e_detective), (5, e_expediente), (6, e_balanza), (9, e_mapa),
    (10, e_chinampa), (11, e_unesco), (14, e_fiesta), (15, e_oscuro), (18, e_nombre), (20, e_sevan), (22, e_porque),
    (25, e_vida), (28, e_algo), (29, e_leyenda), (34, e_proteger), (40, e_recoge), (42, e_rotas), (45, e_turistas),
    (48, e_fama), (50, e_pesca), (52, e_hallazgo), (55, e_versiones), (58, e_verdad), (60, e_sinregistro),
    (64, e_parientes), (66, e_soledad), (70, e_hoy), (71, e_ofrenda), (73, e_callback), (75, e_hombre), (77, e_suscribe),
]


# ======================================================================= subtítulos

CLAVE = {"niña", "muñecas", "muñeca", "isla", "canal", "julián", "nadie", "verdad", "leyenda", "comprobado", "solo",
         "espíritu", "sin", "vida", "nunca", "unesco", "chinampas", "terror", "triste", "humana", "anastasio", "infarto",
         "ahogó", "ojos", "compañía", "aterradora", "ofrenda", "suscríbete", "imaginó", "cabeza", "registro", "nombre",
         "fecha", "medio", "siglo", "cincuenta", "silencio"}
NUM = {"dos mil uno": "2001", "mil novecientos veintiuno": "1921", "mil novecientos ochenta y siete": "1987",
       "cincuenta años": "50 años", "ochenta años": "80 años"}


def subtitulos(a: Anim) -> str:
    out = []
    n = 0
    for si, s in enumerate(SEGS):
        txt = s["texto"]
        for k, v in NUM.items():
            txt = txt.replace(k, v)
        words = txt.split()
        dur = s["fin"] - s["ini"]
        total = sum(len(w) + 2 for w in words)
        # agrupa en líneas de máx. ~28 caracteres o fin de frase
        groups, cur = [], []
        for w in words:
            cur.append(w)
            if sum(len(x) + 1 for x in cur) > 26 or re.search(r"[.?!:…]$", w):
                groups.append(cur); cur = []
        if cur:
            groups.append(cur)
        acc = 0
        for g in groups:
            g0 = s["ini"] + dur * acc / total
            glen = sum(len(w) + 2 for w in g)
            g1 = s["ini"] + dur * (acc + glen) / total
            spans, wacc = [], acc
            for w in g:
                wt = s["ini"] + dur * wacc / total
                hot = re.sub(r"[^\wáéíóúñ]", "", w.lower()) in CLAVE
                spans.append(f'<span id="cw{n}" class="w{" hot" if hot else ""}">{w}</span>')
                a.raw(f'tl.from("#cw{n}",{{scale:.4,opacity:0,y:24,duration:.18,ease:"back.out(3)"}},{wt:.3f});')
                wacc += len(w) + 2
                n += 1
            out.append([g0, g1, "".join(spans)])
            acc += glen
    html = []
    for i, (g0, g1, sp) in enumerate(out):
        nxt = out[i + 1][0] if i + 1 < len(out) else FIN
        end = min(nxt, g1 + .6)
        html.append(f'<div class="clip cap" data-start="{g0:.3f}" data-duration="{max(.3, end - g0 - .02):.3f}">{sp}</div>')
    return "\n".join(html)


def build() -> str:
    a = Anim()
    html = []
    for idx, (si, fn) in enumerate(ESCENAS):
        t0 = S(si) - (.15 if si else 0)
        t1 = S(ESCENAS[idx + 1][0]) - .15 if idx + 1 < len(ESCENAS) else FIN
        d = round(t1 - t0, 3)
        svg = fn(a, round(t0, 3), d)
        sid = f"sc{idx:02d}"
        html.append(f'<div id="{sid}" class="clip scene" data-start="{t0:.3f}" data-duration="{d}" data-layout-allow-overflow>'
                    f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}">{svg}</svg></div>')
        a.raw(f'tl.fromTo("#{sid} svg",{{scale:1}},{{scale:1.06,duration:{d},ease:"none",transformOrigin:"50% 55%"}},{t0:.3f});')
        a.raw(f'tl.from("#{sid} svg",{{scale:1.12,opacity:.0,duration:.25,ease:"power2.out"}},{t0:.3f});')
        if idx:
            a.sound("whoosh-short", t0 - .1, .28)
        a.raw(f'tl.to(\'#{sid} [class$="-row"]\',{{x:-240,duration:{d},ease:"none"}},{t0:.3f});')
    caps = subtitulos(a)
    (ROOT / "assets/sfx_events.json").write_text(json.dumps(sorted(a.sfx, key=lambda x: x[1])))
    # olas: todas las que no tienen tween propio se mueven
    js = "\n".join("  " + l for l in a.lines)
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="./gsap.min.js"></script>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{INK}; }}
  #root {{ width:100%; height:100%; position:relative; overflow:hidden; font-family:Lato, sans-serif; color:{INK}; }}
  .scene {{ position:absolute; inset:0; overflow:hidden; }}
  .scene svg {{ position:absolute; inset:0; }}
  .big {{ font: 900 230px Lato, sans-serif; fill:#fff; stroke:{INK}; stroke-width:12px; paint-order:stroke; }}
  .huge {{ font: 900 150px Lato, sans-serif; fill:#fff; stroke:{INK}; stroke-width:12px; paint-order:stroke; }}
  .huge2 {{ font: 900 96px Lato, sans-serif; fill:#fff; }}
  .tag {{ font: 900 40px Lato, sans-serif; letter-spacing:.1em; fill:#fff; }}
  .tag2 {{ font: 900 46px Lato, sans-serif; letter-spacing:.06em; fill:{INK}; }}
  .mid {{ font: 900 54px Lato, sans-serif; fill:{INK}; }}
  .note {{ font: 900 110px Lato, sans-serif; fill:#fff; stroke:{INK}; stroke-width:6px; paint-order:stroke; }}
  .boat {{ font: 900 44px Lato, sans-serif; fill:{RED}; letter-spacing:.08em; }}
  .stamp {{ font: 900 68px Lato, sans-serif; letter-spacing:.05em; fill:#fff; }}
  .q {{ font: 900 190px Lato, sans-serif; fill:{RED}; stroke:{INK}; stroke-width:8px; paint-order:stroke; }}
  .field {{ font: 900 50px Lato, sans-serif; fill:{INK}; }}
  .field.red {{ fill:{RED}; }}
  .cap {{ position:absolute; left:120px; right:120px; bottom:56px; display:flex; flex-wrap:wrap; gap:0 22px;
          justify-content:center; z-index:10; }}
  .cap .w {{ display:inline-block; margin:0 .1em; font: 900 72px Lato, sans-serif; color:#fff; text-transform:uppercase;
             -webkit-text-stroke: 12px {INK}; paint-order: stroke fill; }}
  .cap .w.hot {{ color:{YEL}; }}
</style>
</head>
<body>
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
    print("escrito index.html ·", FIN, "s ·", len(ESCENAS), "escenas")
