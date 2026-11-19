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


# ============================================================ escenas del video 4 (túnel, 2015)
# Helpers de build.py: shake, sway, fall, puff, counter, pill, stamp, card, dust, building, rig, ground, sky.
CEL = "#c9d6df"
TIERRA = "#8d5524"
ROCA = "#5c4033"


def e_gancho4(a, t0, d):
    tc = T("gancho", 1)
    a.pop("#dren", t0 + .5, "50% 50%", .5)
    a.raw(f'tl.fromTo("#zoomd",{{attr:{{transform:"translate(0 0) scale(1)"}}}},{{attr:{{transform:"translate(-860 -560) scale(3.2)"}},duration:{d - .5:.2f},ease:"power1.inOut"}},{t0 + .3:.3f});')
    shake(a, "camg", tc, 1.0, 8)
    a.pop("#tt", T("gancho", 0) + .3)
    a.sound("glitch-1", t0, .4)
    return (f'<rect width="{W}" height="{H}" fill="#2b2d42"/>'
            f'<g id="camg"><g id="zoomd">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="{CEL}"/>'
            f'<rect x="0" y="760" width="{W}" height="320" fill="#adb5bd" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="700" y="60" width="520" height="700" fill="#e9ecef" stroke="{INK}" stroke-width="8"/>'
            f'<line x1="960" y1="90" x2="960" y2="200" stroke="{INK}" stroke-width="12"/>'
            f'<circle cx="960" cy="230" r="46" fill="#a8dadc" stroke="{INK}" stroke-width="7"/>'
            f'<circle id="dren" cx="960" cy="800" r="46" fill="{ROCA}" stroke="{INK}" stroke-width="7"/></g></g>'
            + f'<g id="tt">{text(960, 170, "PRISIÓN DE MÁXIMA SEGURIDAD", "tiny")}</g>')


def e_quiz4(a, t0, d):
    tr = T("quiz", 3)
    opts = [("1 MES", 380), ("6 MESES", 760), ("1–2 AÑOS", 1140), ("5 AÑOS", 1520)]
    a.pop("#qtl", t0 + .2, "50% 50%")
    for i, (lab, x) in enumerate(opts):
        a.pop(f"#o{i}", t0 + .6 + i * .2, "50% 100%", .35)
    a.raw(f'tl.to("#o2",{{attr:{{transform:"translate(0 0) scale(1.15)"}}}},.5,{tr:.3f});') if False else None
    a.pop("#ok", tr + .3)
    a.sound("sparkle", tr, .45)
    cols = [GRAY, GRAY, GREEN, GRAY]
    bars = "".join(f'<g id="o{i}" transform="translate({x} 780)"><rect x="-150" y="{-(120 + i * 60)}" width="300" height="{120 + i * 60}" rx="16" fill="{cols[i]}" stroke="{INK}" stroke-width="8"/>'
                   f'{text(0, 60, lab, "tiny")}</g>' for i, (lab, x) in enumerate(opts))
    return (sky("gq4", "#fff3d6", "#ffd6a5") + f'<g id="qtl">{text(960, 170, "¿CUÁNTO TARDÓ?", "huge")}</g>'
            + bars + f'<g id="ok">{stamp("okp", 1140, 420, 520, "ENTRE 1 Y 2 AÑOS", GREEN, -4)}</g>')


def e_tunel4(a, t0, d):
    a.raw(f'tl.fromTo("#moto",{{attr:{{transform:"translate(330 620)"}}}},{{attr:{{transform:"translate(1600 620)"}},duration:{d - 1:.2f},ease:"none"}},{t0 + .4:.3f});')
    a.raw(f'tl.to(".luz",{{opacity:.25,duration:.5,repeat:-1,yoyo:true,ease:"sine.inOut",stagger:.2}},{t0:.3f});') if False else None
    a.pop("#km", T("tunel", 0) + .2)
    a.pop("#vent", T("tunel", 1) + .2)
    a.pop("#rail", T("tunel", 1) + .4)
    a.sound("whoosh-cinematic", t0 + .4, .35)
    luces = "".join(f'<circle cx="{x}" cy="600" r="7" fill="#ffd60a" stroke="{INK}" stroke-width="3"/>' for x in range(420, 1600, 110))
    return (sky("gt4", "#cfd8dc", "#8d99ae") + ground("tg4", 540, "#9c6644")
            + f'<rect x="0" y="540" width="{W}" height="540" fill="{TIERRA}" stroke="{INK}" stroke-width="8"/>'
            + f'<path d="M300 590 L1620 590 L1620 640 L300 640 Z" fill="#3a3a3a" stroke="{INK}" stroke-width="6"/>'
            + f'<g id="rail"><line x1="300" y1="650" x2="1620" y2="650" stroke="#adb5bd" stroke-width="10"/>'
            + f'<line x1="300" y1="672" x2="1620" y2="672" stroke="#adb5bd" stroke-width="10"/></g>'
            + luces + f'<g id="moto" transform="translate(330 620)"><rect x="-70" y="-40" width="140" height="48" rx="10" fill="{RED}" stroke="{INK}" stroke-width="7"/>'
            f'<circle cx="-40" cy="20" r="18" fill="{INK}"/><circle cx="40" cy="20" r="18" fill="{INK}"/></g>'
            + f'<g id="vent"><path d="M300 480 L1620 480" stroke="#7bdff2" stroke-width="16"/>{text(960, 430, "VENTILACIÓN", "tiny")}</g>'
            + f'<g id="km">{pill("kmp", 960, 200, 620, "1,5 KM DE TÚNEL", RED, "tag")}</g>'
            + f'<g>{pill("pen", 360, 340, 300, "PENAL", INK, "tag")}{pill("cas", 1560, 340, 360, "CASA", TEAL, "tag")}</g>')


def e_tiempo4(a, t0, d):
    a.raw(f'tl.from("#barra",{{scaleX:0,transformOrigin:"0% 50%",duration:1.4,ease:"power2.out"}},{t0 + .3:.3f});')
    a.pop("#rango", T("tiempo", 0) + .4)
    a.pop("#camiones", T("tiempo", 1) + .3)
    a.sound("riser", t0, .35)
    meses = "".join(f'<text x="{300 + i * 100}" y="700" text-anchor="middle" class="tiny">{i}</text>' for i in range(0, 25, 3))
    trucks = "".join(f'<g transform="translate({280 + i * 90} 880)"><rect x="-40" y="-40" width="60" height="40" fill="{GRAY}" stroke="{INK}" stroke-width="5"/>'
                     f'<circle cx="-22" cy="4" r="9" fill="{INK}"/><circle cx="20" cy="4" r="9" fill="{INK}"/></g>' for i in range(12))
    return (sky("gti4", "#e0fbfc", "#ffffff") + f'<text x="960" y="170" text-anchor="middle" class="huge">¿CUÁNTOS MESES?</text>'
            + f'<line x1="300" y1="640" x2="1620" y2="640" stroke="{INK}" stroke-width="8"/>{meses}'
            + f'<rect id="barra" x="300" y="520" width="1320" height="60" rx="30" fill="{YEL}" stroke="{INK}" stroke-width="7"/>'
            + f'<g id="rango">{pill("rg", 960, 440, 740, "ESTIMADO: 12 A 24 MESES", RED, "tag")}</g>'
            + f'<g id="camiones">{trucks}{text(960, 800, "CIENTOS DE CAMIONES DE TIERRA", "tiny")}</g>')


def e_seguridad4(a, t0, d):
    a.face("dt4", t0, "flat", (6, -6), (-10, 2))
    a.pose("dt4", t0 + .3, .5, uaR=-120, faR=-40, head=-6)
    a.raw(f'tl.from("#plano",{{opacity:0,scale:.8,transformOrigin:"50% 50%",duration:.8,ease:"power2.out"}},{t0 + .2:.3f});')
    a.pop("#hint", T("seguridad", 1) + .2)
    a.pop("#ojo", T("seguridad", 2) + .2)
    a.sound("pop", t0 + .3, .3)
    plano = (f'<g id="plano" transform="translate(960 420)"><rect x="-420" y="-260" width="840" height="520" rx="18" fill="#dbe9f4" stroke="{INK}" stroke-width="9"/>'
             + "".join(f'<line x1="{-380 + i * 90}" y1="-220" x2="{-380 + i * 90}" y2="220" stroke="#8ecae6" stroke-width="3"/>' for i in range(10))
             + f'<rect x="-120" y="-80" width="240" height="160" fill="none" stroke="{RED}" stroke-width="8" stroke-dasharray="18 12"/>'
             + f'{text(0, 100, "¿?", "tag")}</g>')
    return (sky("gs4", "#f1faee", "#dbe9f4") + ground("sg4", 880, "#adb5bd") + plano
            + rig("dt4", 300, 900, 1.2, **DET, prop_r="")
            + f'<g id="hint">{pill("hn", 1400, 230, 620, "LOS PLANOS IMPORTAN", INK, "tag")}</g>'
            + f'<g id="ojo">{pill("ojp", 1450, 700, 560, "ALGO NO CUADRA", RED, "tag")}</g>')


def e_complicidad4(a, t0, d):
    a.pop("#st4", T("complicidad", 0) + .3)
    a.pop("#tag4", T("complicidad", 1) + .2)
    a.sound("impact-bass-2", T("complicidad", 0) + .3, .4)
    return (sky("gc4", "#2b2d42", "#6d597a") + card("cc4", 960, 480, 900, 560, "PLANOS DEL PENAL", YEL,
            text(0, 60, "¿QUIÉN LOS TENÍA?", "mid") + text(0, 150, "ANÁLISIS DE EXPERTOS", "tiny"), -2)
            + f'<g id="st4">{stamp("sp4", 960, 880, 720, "NO ES UN HECHO CONFIRMADO", RED, -3)}</g>'
            + f'<g id="tag4">{pill("tg4p", 960, 110, 760, "COMPLICIDAD", PURP, "tag")}</g>')


def e_desenlace4(a, t0, d):
    a.pop("#e15", t0 + .2); a.pop("#e16", T("desenlace", 0) + .2); a.pop("#e17", T("desenlace", 0) + 1.2)
    a.raw(f'tl.fromTo("#linea",{{attr:{{transform:"scale(0 1)"}}}},{{attr:{{transform:"scale(1 1)"}},duration:1.6,ease:"power2.out"}},{t0 + .4:.3f});')
    a.sound("chime", T("desenlace", 0) + .2, .35)
    return (sky("gd4", "#3a0ca3", "#10002b") + f'<g id="linea" transform="translate(0 0)"><line x1="260" y1="560" x2="1660" y2="560" stroke="{YEL}" stroke-width="12"/></g>'
            + f'<g id="e15">{pill("p15", 420, 560, 360, "2015 · FUGA", RED, "tag")}</g>'
            + f'<g id="e16">{pill("p16", 960, 560, 420, "RECAPTURA", INK, "tag")}</g>'
            + f'<g id="e17">{pill("p17", 1500, 560, 420, "2017 · EXTRADICIÓN", GREEN, "tag")}</g>'
            + f'<g>{text(960, 300, "MESES DESPUÉS", "huge")}</g>')


def e_cierre4(a, t0, d):
    a.pop("#qq4", t0 + .2)
    a.pop("#cf4", T("cierre", 1) + .2)
    a.sound("chime", T("cierre", 1) + .4, .4)
    a.face("cz4", t0, "smile", (-6, 6), (8, -4))
    a.breathe("cz4", t0, d)
    return (sky("gz4", "#ff7b54", "#ffd56b") + ground("zg4", 880, "#9c6644") + rig("cz4", 960, 880, 1.2, **DET, prop_r="")
            + f'<g id="qq4">{text(960, 240, "¿CUÁNTO TARDÓ?", "huge")}</g>'
            + f'<g id="cf4">{card("cfa4", 1620, 620, 520, 340, "MIRA ESTO", YEL, text(0, 90, "LA ISLA DE LAS", "tiny") + text(0, 150, "MUÑECAS", "tiny"), 3)}</g>')


ESC = {"gancho": e_gancho4, "quiz": e_quiz4, "tunel": e_tunel4, "tiempo": e_tiempo4, "seguridad": e_seguridad4,
       "complicidad": e_complicidad4, "desenlace": e_desenlace4, "cierre": e_cierre4}

# ============================================================ subtítulos

CLAVE = {"sobrevivieron", "montaña", "avalancha", "radio", "búsqueda", "dieciséis", "veintinueve", "helicópteros", "caminar", "niña", "edificio", "edificios", "cayó", "ciudad", "suelo", "resonancia", "ritmo", "pisos", "bebés", "hospital",
         "topos", "voluntarios", "muertos", "exactitud", "alerta", "agáchate", "cúbrete", "agárrate", "lago", "gelatina",
         "terremoto", "sismo", "vive", "vida", "clave", "cartón", "resonancia"}
NUM = [("dos mil quince", "2015"), ("dos mil diecisiete", "2017"), ("kilómetro y medio", "1,5 km"), ("doce meses", "12 meses"), ("cincuenta", "50")]


def subtitulos(a: Anim) -> str:
    cues = []
    n = 0
    for si, s in enumerate(SEG):
        txt = s["texto"]
        for k, v in NUM:
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
