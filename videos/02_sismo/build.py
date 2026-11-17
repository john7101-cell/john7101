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


# ============================================================ escenas

def e_gancho(a: Anim, t0: float, d: float) -> str:
    shake(a, "cam0", 1.2, 5.2, 14)
    a.pop("#big0", .45, "50% 50%", .5)
    a.pop("#clk0", 1.3)
    a.raw(f'tl.fromTo("#flash0",{{opacity:1}},{{opacity:0,duration:.6}},{t0:.3f});')
    a.sound("glitch-1", t0, .45)
    for i, (x, w, h, c) in enumerate(((120, 300, 420, "#3a3f4b"), (460, 260, 620, "#2b2f3a"), (760, 320, 300, "#3a3f4b"),
                                      (1120, 280, 560, "#2b2f3a"), (1440, 340, 380, "#3a3f4b"))):
        a.raw(f'tl.from("#b0-{i}",{{y:300,opacity:0,duration:.8,ease:"power3.out"}},{t0 + .1 * i:.3f});')
    for i, d_ in enumerate((2.6, 3.2)):
        dust(f"gd{i}", 760 + i * 380, 900)
    dust_svg = "".join(dust(f"gd{i}", 760 + i * 380, 900) for i in range(2))
    for i in range(2):
        puff(a, f"gd{i}", 2.4 + i * .5)
    blds = "".join(building(f"b0-{i}", x, 900, w, h, c, label="") for i, (x, w, h, c) in
                   enumerate(((120, 300, 420, "#3a3f4b"), (460, 260, 620, "#2b2f3a"), (760, 320, 300, "#3a3f4b"),
                              (1120, 280, 560, "#2b2f3a"), (1440, 340, 380, "#3a3f4b"))))
    return (f'<rect width="{W}" height="{H}" fill="{DARK}"/><rect id="flash0" width="{W}" height="{H}" fill="#fff" opacity="0"/>'
            f'<g id="cam0">{blds}{dust_svg}'
            f'{text(960, 200, "19 · SEP · 1985", "huge", id_="big0")}'
            f'<g id="clk0">{pill("clkp", 960, 440, 520, "7:19 AM", RED, "tag")}</g></g>')


def e_quiz(a: Anim, t0: float, d: float) -> str:
    tr = T("quiz", 3)
    for i, (x, h, c) in enumerate(((380, 520, BLUE), (960, 340, PINK), (1540, 170, YEL))):
        sway(a, f"qb{i}", t0, d, 1.2 if i != 1 else 1.4, 2.4 + i * .6, x + 130, 880)
    fall(a, "qb1", tr, 960, 880, 88, 1.1)
    dust_svg = dust("qd", 960, 880, 1.4)
    puff(a, "qd", tr + .6)
    a.pop("#qstamp", tr + .9, "50% 50%")
    a.pop("#qlbl", T("quiz", 0), "50% 50%")
    for i, lab in enumerate("ABC"):
        a.pop(f"#tile{lab}", T("quiz", 2) + .2 + i * .25, "50% 50%", .35)
    a.sound("chime", tr + .9, .5)
    bl = "".join(building(f"qb{i}", x, 880, 260 if i != 2 else 300, h, c, floors=None, label="") for i, (x, h, c) in
                 enumerate(((380, 520, BLUE), (960, 340, PINK), (1540, 170, YEL))))
    tiles = "".join(f'<g id="tile{lab}" transform="translate({x} {y})"><rect x="-44" y="-44" width="88" height="88" rx="18" fill="{CREAM}" stroke="{INK}" stroke-width="7"/>'
                    f'{text(0, 18, lab, "tag", id_="")}</g>' for lab, x, y in zip("ABC", (510, 1090, 1670), (290, 470, 640)))
    tiles = tiles.replace('class="tag"', 'class="tagd"')
    return (sky("gq", "#fff3d6", "#ffd6a5") + f'<g id="cuadro">{ground("qg", 880, "#9c6644")}{bl}{dust_svg}</g>'
            + tiles + f'<g id="qlbl">{text(960, 200, "¿CUÁL CAYÓ?", "huge")}</g>'
            + stamp("qstamp", 960, 560, 460, "ESTE CAYÓ", RED, -6))


def e_suelo(a: Anim, t0: float, d: float) -> str:
    t1 = T("suelo", 2)
    tE = T("suelo", 3)
    a.raw(f'tl.fromTo("#lag",{{attr:{{transform:"scale(1 1)"}}}},{{attr:{{transform:"scale(1.03 1)"}},duration:.9,repeat:{max(1, int((d - 2) / .9))},yoyo:true,ease:"sine.inOut"}},{t0 + 1.5:.3f});')
    a.pop("#lbl-lago", T("suelo", 1), "50% 50%")
    a.pop("#lbl-gel", t1, "50% 50%")
    for i in range(4):
        a.raw(f'tl.from("#ep{i}",{{opacity:0,duration:.3}},{tE + i * .6:.2f});')
    for k in range(4):
        a.raw(f'tl.fromTo("#r{k}",{{attr:{{transform:"translate(330 720) scale(.1)"}},opacity:.9}},'
              f'{{attr:{{transform:"translate(330 720) scale(9)"}},opacity:0,duration:2.4,ease:"power1.out"}},{tE + .4 + k * .55:.2f});')
    a.pop("#mag", tE + .2)
    a.sound("whoosh-cinematic", tE, .4)
    rings = "".join(ring(f"r{k}", 330, 720) for k in range(4))
    city = "".join(building(f"cs{i}", x, 880, w, h, c) for i, (x, w, h, c) in
                   enumerate(((760, 180, 240, "#adb5bd"), (980, 220, 380, "#6c757d"), (1240, 170, 200, "#ced4da"),
                              (1450, 210, 460, "#adb5bd"), (1700, 170, 300, "#6c757d"))))
    star = (f'<g id="ep0"><path d="M330 690 l12 26 l28 4 l-20 18 l6 28 l-26 -14 l-26 14 l6 -28 l-20 -18 l28 -4 z" fill="{YEL}" stroke="{INK}" stroke-width="5"/></g>'
            f'<g id="ep1">{text(330, 620, "EPICENTRO", "tiny")}</g>')
    return (sky("gs", "#bde0fe", "#e0fbfc") + f'<rect x="0" y="790" width="520" height="290" fill="#219ebc"/>{wave_row("wsea", 800, "#8ecae6")}'
            + f'<g id="lag"><path d="M640 880 Q760 760 1000 780 Q1300 790 1900 850 L1900 1080 L640 1080 Z" fill="#48cae4" stroke="{INK}" stroke-width="8" opacity=".85"/>'
            + f'<g id="lbl-lago">{pill("ll", 1260, 700, 620, "LAGO DE TEXCOCO (ANTIGUO)", TEAL, "tiny")}</g></g>'
            + city + f'<g id="gel">{pill("lg", 1000, 380, 680, "SUELO COMO GELATINA", PURP, "tag")}</g>'
            + f'<g id="lbl-gel">{text(960, 460, "", "tiny")}</g>'
            + rings + star + f'<g id="mag">{pill("mg", 1480, 180, 560, "MAGNITUD ~8.1", RED, "tag")}</g>'
            + f'<g id="ep2">{pill("km", 420, 200, 540, "~400 KM DE DISTANCIA", INK, "tiny")}</g>')


def e_resonancia(a: Anim, t0: float, d: float) -> str:
    tf = T("resonancia", 5)
    a.raw(f'tl.fromTo("#gnd",{{attr:{{transform:"translate(0 880) scale(1 1) translate(0 -880)"}}}},'
          f'{{attr:{{transform:"translate(0 880) scale(1 1.035) translate(0 -880)"}},duration:.75,repeat:{max(1, int((d - 1) / .75))},yoyo:true,ease:"sine.inOut"}},{t0 + .6:.3f});')
    sway(a, "rs0", t0 + 1, d, 2.2, .8, 380, 880)
    sway(a, "rs2", t0 + 1, d, .6, 5.5, 1560, 880)
    sway(a, "rs1", T("resonancia", 2), tf - T("resonancia", 2), 3.2, 1.5, 960, 880)
    fall(a, "rs1", tf, 820, 880, 88, 1.1)
    puff(a, "rd", tf + .6)
    a.pop("#rl0", T("resonancia", 1), "50% 50%")
    a.pop("#rl1", T("resonancia", 3), "50% 50%")
    a.pop("#rl2", T("resonancia", 4), "50% 50%")
    a.pop("#rok", tf + 1.0)
    a.sound("impact-bass-2", tf, .45)
    b0 = building("rs0", 240, 880, 280, 300, "#adb5bd", label="")
    b1 = building("rs1", 820, 880, 280, 520, PINK, label="")
    b2 = building("rs2", 1420, 880, 300, 780, BLUE, label="")
    return (sky("gr", "#ffe8d6", "#ffc8dd") + f'<g id="gnd">{wave_row("gw", 880, TEAL, amp=34)}</g>'
            + f'<rect x="-60" y="880" width="{W + 120}" height="260" fill="#9c6644" stroke="{INK}" stroke-width="8"/>'
            + b0 + b1 + b2 + f'<g id="rd">{dust("rdd", 960, 880, 1.6)}</g>'
            + f'<g id="rl0">{pill("rl0p", 380, 180, 420, "RITMO RÁPIDO", GRAY, "tiny")}</g>'
            + f'<g id="rl1">{pill("rl1p", 960, 220, 540, "MISMO RITMO QUE EL SUELO", RED, "tiny")}</g>'
            + f'<g id="rl2">{pill("rl2p", 1560, 120, 420, "RITMO LENTO", BLUE, "tiny")}</g>'
            + f'<g id="rok">{stamp("rokp", 1560, 470, 520, "SÍ AGUANTÓ", GREEN, 4)}</g>')


def e_hospital(a: Anim, t0: float, d: float) -> str:
    tc = T("hospital", 1)
    shake(a, "camh", t0 + .5, 3.0, 9)
    fall(a, "hb", tc, 700, 900, 84, 1.6)
    puff(a, "hd", tc + .8, 1.8)
    puff(a, "hd2", tc + 1.2, 1.6)
    a.pop("#hl", T("hospital", 0), "50% 50%")
    a.pop("#hs", tc + 2.0, "50% 50%")
    a.sound("impact-bass-1", tc, .5)
    hosp = building("hb", 700, 900, 520, 700, "#e9ecef", floors=12, label="")
    cross = f'<g transform="translate(960 660)"><rect x="-44" y="-14" width="88" height="28" fill="{RED}" stroke="{INK}" stroke-width="5"/><rect x="-14" y="-44" width="28" height="88" fill="{RED}" stroke="{INK}" stroke-width="5"/></g>'
    return (sky("gh", "#cfd8dc", "#90a4ae") + f'<g id="camh">{hosp}{cross}'
            + f'<g id="hd">{dust("hdd", 950, 900, 1.5)}</g><g id="hd2">{dust("hdd2", 1120, 900, 1.2)}</g></g>'
            + ground("hgr", 900) + f'<g id="hl">{pill("hlp", 960, 240, 760, "HOSPITAL JUÁREZ", INK, "tag")}</g>'
            + f'<g id="hs">{stamp("hsp", 960, 480, 560, "12 PISOS", RED, -5)}</g>')


def e_bebes(a: Anim, t0: float, d: float) -> str:
    tn = T("bebes", 1)
    counter("cnt", tn, 1.6, 14)
    a.pop("#bebe", t0 + .1, "50% 100%")
    a.pop("#hijos", tn + .4)
    a.sound("sparkle", tn, .4)
    a.sound("chime", tn + .4, .35)
    baby = (f'<g id="bebe" transform="translate(560 720)"><rect x="-170" y="-20" width="340" height="230" rx="110" fill="{PINK}" stroke="{INK}" stroke-width="9"/>'
            f'<circle cx="0" cy="-60" r="110" fill="{SKIN}" stroke="{INK}" stroke-width="9"/>'
            f'<path d="M-50 -70 Q-40 -88 -30 -70 M30 -70 Q40 -88 50 -70" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<path d="M-30 -18 Q0 6 30 -18" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<circle cx="-62" cy="-20" r="16" fill="{PINK}" opacity=".6"/><circle cx="62" cy="-20" r="16" fill="{PINK}" opacity=".6"/></g>')
    return (sky("gb", "#ffd6e0", "#fff1e6") + f'<g filter="url(#glow)"></g>' + baby
            + f'<g transform="translate(1320 560)">{text(0, 40, "0", "huge", id_="cnt")}{text(0, 170, "BEBÉS RESCATADOS", "mid")}</g>'
            + f'<g id="hijos">{stamp("hsd", 960, 900, 880, "HIJOS DE LA NACIÓN", RED, -3)}</g>')


def e_topos(a: Anim, t0: float, d: float) -> str:
    tt = T("topos", 2)
    shake(a, "camt", T("topos", 3), 1.2, 6)
    a.pop("#topo-ttl", T("topos", 0), "50% 50%")
    for i in range(3):
        for k in range(int(d / 1.1)):
            a.pose(f"tp{i}", t0 + .4 + k * 1.1 + i * .15, .45, "sine.inOut", uaR=-150 if k % 2 == 0 else -40, faR=-30 if k % 2 == 0 else -80)
        a.face(f"tp{i}", t0, "flat", (0, 0), (6, -2))
    a.pop("#topo-ttl2", tt + .2)
    a.sound("impact-bass-1", tt + .3, .3)
    crew = "".join(rig(f"tp{i}", x, 880, .8, shirt=c, prop_r="") for i, (x, c) in enumerate(zip((420, 760, 1400), (YEL, RED, BLUE))))
    dirt = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#a47148" stroke="{INK}" stroke-width="4"/>' for x, y, r in
                   ((260, 830, 60), (420, 800, 80), (560, 840, 50), (1260, 830, 70), (1490, 800, 90), (1640, 840, 60)))
    return (sky("gt", "#ffe8a3", "#f4a261") + f'<g id="camt">{dirt}{crew}</g>' + ground("tgr", 880, "#8d5524")
            + f'<g id="topo-ttl">{text(960, 240, "LOS TOPOS", "huge")}</g>'
            + f'<g id="topo-ttl2">{stamp("tts", 960, 470, 600, "VOLUNTARIOS", INK, -3)}</g>')


def e_cifras(a: Anim, t0: float, d: float) -> str:
    tm = T("cifras", 1)
    a.pop("#qq", t0 + .2, "50% 50%")
    a.raw(f'tl.fromTo("#mk",{{attr:{{transform:"translate(260 640)"}}}},{{attr:{{transform:"translate(1660 640)"}},duration:{d - 3:.2f},ease:"power2.inOut"}},{tm - .4:.2f});')
    for i in range(3):
        a.pop(f"#lb{i}", T("cifras", 1) + .1 + i * .35, "50% 100%")
    a.sound("riser", t0, .5)
    bar = f'<rect x="260" y="620" width="1400" height="40" rx="20" fill="#dee2e6" stroke="{INK}" stroke-width="7"/>'
    marks = "".join(f'<g id="lb{i}">{text(x, 590, lab, "tiny")}</g>' for i, (x, lab) in enumerate(((330, "MILES"), (1000, "+10,000"), (1600, "¿50,000?"))))
    marker = f'<g id="mk" transform="translate(260 640)"><circle r="34" fill="{RED}" stroke="{INK}" stroke-width="7"/></g>'
    return (sky("gcf", "#e0c3fc", "#fbc4ab") + bar + marks + marker
            + f'<g id="qq">{text(960, 250, "¿CUÁNTOS?", "huge")}</g>'
            + text(960, 420, "Nadie lo sabe con exactitud", "mid")
            + pill("note", 960, 820, 1000, "Oficial · Cruz Roja · Especialistas", CREAM, "tiny"))


def e_cambio(a: Anim, t0: float, d: float) -> str:
    a.face("c0", t0, "smile", (-6, 6), (10, -4))
    a.face("c1", t0, "smile", (-6, 6), (-10, -4))
    a.face("c2", t0, "smile", (-6, 6), (0, -2))
    for i in range(3):
        a.pose(f"c{i}", t0 + .4 + i * .15, .4, uaR=-160, faR=-20, uaL=-160 if i == 1 else 20, faL=-20)
    a.pop("#cv1", T("cambio", 0), "50% 50%")
    a.pop("#cv2", T("cambio", 1), "50% 50%")
    a.breathe("c1", t0, d)
    return (sky("gcg", "#b5e48c", "#d9ed92") + ground("cgr", 900, "#80b918")
            + "".join(rig(f"c{i}", x, 900, .95, shirt=c) for i, (x, c) in enumerate(zip((360, 680, 1280), (BLUE, PINK, ORANGE))))
            + f'<g id="cv1">{pill("cvp1", 1500, 300, 600, "ORGANIZACIÓN CIVIL", PURP, "tag")}</g>'
            + f'<g id="cv2">{pill("cvp2", 1500, 480, 620, "NORMAS DE CONSTRUCCIÓN", TEAL, "tiny")}</g>')


def e_consejo(a: Anim, t0: float, d: float) -> str:
    a.face("ck", t0, "flat", (0, 0), (-4, 4))
    a.attr("#ck-body", "scale(1 .72)", t0 + .8, .5, "power2.out")
    a.attr("#ck", "translate(960 900) scale(1)", t0 + .8, .4)
    for i, k in enumerate(("cA", "cB", "cC")):
        a.pop(f"#{k}", T("consejo", i) + .1, "50% 50%")
    a.pop("#alert", T("consejo", 0), "50% 50%")
    for k in range(int(d / .55)):
        a.raw(f'tl.to("#alert",{{opacity:{0 if k % 2 == 0 else 1},duration:.2}},{T("consejo", 0) + .4 + k * .55:.2f});')
    a.sound("chime", T("consejo", 0), .4)
    a.sound("pop", T("consejo", 1), .4)
    table = f'<rect x="690" y="470" width="540" height="46" rx="10" fill="#a47148" stroke="{INK}" stroke-width="8"/>'
    return (sky("gco", "#fde4cf", "#ffcfd2") + ground("cog", 900, "#cdb4db") + table
            + rig("ck", 960, 900, 1.1, **JUL)
            + f'<g id="alert">{pill("alp", 960, 180, 880, "ALERTA SÍSMICA", RED, "tag")}</g>'
            + f'<g id="cA">{pill("cap1", 420, 380, 480, "AGÁCHATE", YEL, "tag", -3)}</g>'
            + f'<g id="cB">{pill("cap2", 1480, 380, 500, "CÚBRETE", TEAL, "tag", 3)}</g>'
            + f'<g id="cC">{pill("cap3", 1480, 600, 500, "AGÁRRATE", PURP, "tag", -2)}</g>')


def e_cierre(a: Anim, t0: float, d: float) -> str:
    tf = T("cierre", 1)
    a.raw(f'tl.from("#cfin",{{scale:.3,opacity:0,transformOrigin:"50% 50%",duration:.5,ease:"back.out(2)"}},{T("cierre", 2) + .3:.2f});')
    a.pop("#cstamp", tf + .3, "50% 50%")
    a.pop("#cbell", T("cierre", 2) + 1.6, "50% 50%")
    a.sound("chime", T("cierre", 2) + 1.6, .45)
    fall(a, "cfb", tf, 720, 900, 88, 1.0)
    puff(a, "cfd", tf + .5, 1.3)
    sway(a, "cfa", t0, tf - t0, 1.2, 2.2, 380, 880)
    a.face("cj", t0, "smile", (-6, 6), (8, -4))
    a.blink("cj", t0 + 2)
    a.breathe("cj", t0, d)
    return (sky("gcl", "#ff7b54", "#ffd56b") + f'<circle cx="1500" cy="330" r="120" fill="{YEL}"/>' + ground("clg", 900, "#9c6644")
            + building("cfa", 240, 900, 300, 520, PINK, label="") + building("cfb", 720, 900, 280, 360, YEL, label="")
            + building("cfc", 1380, 900, 320, 200, BLUE, label="") + f'<g id="cfd">{dust("cfdd", 860, 900, 1.2)}</g>'
            + rig("cj", 1050, 900, 1.1, **JUL)
            + f'<g id="cstamp">{stamp("csp", 860, 170, 520, "EL DE ALTURA MEDIA", RED, -4)}</g>'
            + f'<g id="cfin">{card("cfc2", 1580, 280, 520, 380, "MIRA ESTO", YEL, text(0, 90, "LA ISLA DE LAS", "tiny") + text(0, 150, "MUÑECAS", "tiny"), 4)}</g>'
            + f'<g id="cbell">{pill("cbp", 1580, 760, 520, "SUSCRÍBETE", RED, "tiny")}</g>')


ESC = {"gancho": e_gancho, "quiz": e_quiz, "suelo": e_suelo, "resonancia": e_resonancia, "hospital": e_hospital,
       "bebes": e_bebes, "topos": e_topos, "cifras": e_cifras, "cambio": e_cambio, "consejo": e_consejo, "cierre": e_cierre}


# ============================================================ subtítulos

CLAVE = {"niña", "edificio", "edificios", "cayó", "ciudad", "suelo", "resonancia", "ritmo", "pisos", "bebés", "hospital",
         "topos", "voluntarios", "muertos", "exactitud", "alerta", "agáchate", "cúbrete", "agárrate", "lago", "gelatina",
         "terremoto", "sismo", "vive", "vida", "clave", "cartón", "resonancia"}
NUM = {"mil novecientos ochenta y cinco": "1985", "siete y diecinueve": "7:19", "cuatrocientos kilómetros": "400 km",
       "ocho punto uno": "8.1", "doce pisos": "12 pisos", "catorce": "14", "diez mil": "10,000"}


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
