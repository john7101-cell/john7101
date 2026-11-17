"""Genera index.html (composición HyperFrames) del video 1 en estilo stickman.

Cada escena es un <div class="clip"> con su inicio y duración; las animaciones van en una
sola línea de tiempo GSAP. Por ahora construye la prueba del gancho (0-30 s); cuando llegue
la narración se retiman las escenas con los tiempos de palabra del audio.
"""

from __future__ import annotations

import json
from pathlib import Path

W, H = 1920, 1080
INK = "#1b1b1b"
PAPER = "#f3eee4"
RED = "#b8322a"
WATER = "#3d6f9e"
GHOST = "#9aa3ab"


# ---------------------------------------------------------------- dibujos

def stick(id_: str, x: int, y: int, s: float = 1.0, color: str = INK, extra: str = "",
          dash: bool = False, hat: bool = False, girl: bool = False) -> str:
    """Monigote con extremidades animables. (x, y) = pies; altura ~300*s."""
    sw = 9
    d = ' stroke-dasharray="14 10"' if dash else ""
    hat_svg = (f'<path d="M-46 -262 L46 -262 M-24 -262 Q0 -300 24 -262" stroke="{color}" '
               f'stroke-width="8" fill="none" stroke-linecap="round"/>') if hat else ""
    hair = (f'<path d="M-30 -240 Q-44 -200 -40 -175 M30 -240 Q44 -200 40 -175" stroke="{color}" '
            f'stroke-width="7" fill="none" stroke-linecap="round"/>') if girl else ""
    dress = (f'<path d="M0 -150 L-34 -90 L34 -90 Z" fill="{color}" opacity="0.85"/>') if girl else ""
    return f'''
<g id="{id_}" transform="translate({x} {y}) scale({s})">
 <g stroke="{color}" stroke-width="{sw}" stroke-linecap="round" fill="none"{d}>
  <circle cx="0" cy="-225" r="36" fill="{PAPER}"/>
  <line x1="0" y1="-189" x2="0" y2="-90"/>
  <line id="{id_}-al" x1="0" y1="-165" x2="-50" y2="-110"/>
  <line id="{id_}-ar" x1="0" y1="-165" x2="50" y2="-110"/>
  <line id="{id_}-ll" x1="0" y1="-90" x2="-34" y2="0"/>
  <line id="{id_}-lr" x1="0" y1="-90" x2="34" y2="0"/>
 </g>{hair}{dress}{hat_svg}{extra}
</g>'''


def doll(id_: str, x: int, y: int, s: float = 1.0) -> str:
    """Muñequita colgada de un hilo (cabeza grande, ojos en X o punto)."""
    return f'''
<g id="{id_}" transform="translate({x} {y}) scale({s})">
 <line x1="0" y1="-60" x2="0" y2="-28" stroke="{INK}" stroke-width="3"/>
 <circle cx="0" cy="-10" r="18" fill="#fff" stroke="{INK}" stroke-width="5"/>
 <circle cx="-6" cy="-12" r="3" fill="{INK}"/><path d="M3 -16 l7 7 M10 -16 l-7 7" stroke="{INK}" stroke-width="3"/>
 <path d="M0 8 L-14 40 L14 40 Z" fill="{INK}" opacity="0.8"/>
</g>'''


def waves(id_: str, y: int, n: int = 3) -> str:
    rows = []
    for i in range(n):
        yy = y + i * 34
        path = " ".join(f"Q{x + 60} {yy - 18} {x + 120} {yy} T{x + 240} {yy}" for x in range(-240, W + 480, 240))
        rows.append(f'<path class="{id_}-row" d="M-240 {yy} {path}" stroke="{WATER}" stroke-width="7" '
                    f'fill="none" stroke-linecap="round" opacity="{1 - i * 0.25}"/>')
    return f'<g id="{id_}">' + "".join(rows) + "</g>"


def tree(x: int, y: int, s: float = 1.0) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-width="10" '
            f'stroke-linecap="round" fill="none">'
            f'<path d="M0 0 L0 -260 M0 -170 L-110 -250 M0 -200 L100 -290 M0 -120 L90 -170 M-60 -215 L-130 -200"/>'
            f'</g>')


# ---------------------------------------------------------------- escenas

def escenas() -> tuple[list[str], list[str]]:
    """Devuelve (html de escenas, líneas JS de la línea de tiempo)."""
    html, js = [], []

    def scene(sid: str, t0: float, dur: float, svg: str, caption: str = "") -> None:
        cap = f'<div class="cap" id="{sid}-cap">{caption}</div>' if caption else ""
        html.append(f'<div id="{sid}" class="clip scene" data-start="{t0}" data-duration="{dur}">'
                    f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}">{svg}</svg>{cap}</div>')
        if caption:
            js.append(f'tl.from("#{sid}-cap",{{opacity:0,y:30,duration:.5,ease:"power2.out"}},{t0 + .2});')

    # 1 · 2001, el canal, el sombrero flotando
    t = 0
    scene("s1", t, 6.5, waves("w1", 760, 4) + f'''
      <g transform="translate(960 770)"><g id="s1-hat"><path d="M-80 0 L80 0 M-42 0 Q0 -70 42 0"
        stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round"/></g></g>
      <text id="s1-year" x="960" y="380" text-anchor="middle" class="big">2001</text>
      <text id="s1-place" x="960" y="470" text-anchor="middle" class="small">XOCHIMILCO · MÉXICO</text>''')
    js += [f'tl.from("#s1-year",{{scale:.4,opacity:0,transformOrigin:"960px 340px",duration:.6,ease:"back.out(2)"}},{t + .3});',
           f'tl.from("#s1-place",{{opacity:0,y:20,duration:.5}},{t + .9});',
           f'tl.to(".w1-row",{{x:-240,duration:6.5,ease:"none"}},{t});',
           f'tl.fromTo("#s1-hat",{{y:0,rotation:-4}},{{y:14,rotation:4,duration:1.1,repeat:5,yoyo:true,ease:"sine.inOut",transformOrigin:"50% 100%"}},{t});']

    # 2 · "50 años antes": la niña fantasma
    t = 6.5
    scene("s2", t, 6.0, waves("w2", 800, 3) + stick("girl", 960, 760, 1.0, GHOST, dash=True, girl=True) + f'''
      <g id="s2-stamp" transform="translate(1420 300) rotate(-8)">
        <rect x="-300" y="-70" width="600" height="140" fill="none" stroke="{RED}" stroke-width="8"/>
        <text x="0" y="22" text-anchor="middle" class="stamp">50 AÑOS ANTES</text></g>''',
          "Según él, aquí se ahogó una niña")
    js += [f'tl.from("#s2-stamp",{{scale:2.2,opacity:0,transformOrigin:"1420px 300px",duration:.35,ease:"power3.in"}},{t + .4});',
           f'tl.from("#girl",{{opacity:0,duration:1.2}},{t + 1.0});',
           f'tl.to("#girl",{{opacity:0,y:-40,duration:1.6}},{t + 4.2});',
           f'tl.to(".w2-row",{{x:-240,duration:6,ease:"none"}},{t});']

    # 3 · la isla se llena de muñecas
    t = 12.5
    dolls_pos = [(560, 540), (640, 470), (500, 610), (930, 470), (1010, 400), (870, 560),
                 (1300, 520), (1380, 450), (1250, 600), (700, 620), (1080, 560), (1440, 600),
                 (780, 430), (1180, 430), (600, 680)]
    dolls = "".join(doll(f"d{i}", x, y, 1.0) for i, (x, y) in enumerate(dolls_pos))
    island = (f'<path d="M260 860 Q960 700 1660 860 Z" fill="#cdbf9f" stroke="{INK}" stroke-width="8"/>'
              + tree(640, 800, 1.2) + tree(960, 760, 1.4) + tree(1330, 800, 1.2))
    scene("s3", t, 6.0, waves("w3", 900, 2) + island + dolls ,
          "Medio siglo llenando una isla de muñecas")
    for i in range(len(dolls_pos)):
        js.append(f'tl.from("#d{i}",{{scale:0,opacity:0,transformOrigin:"center",duration:.3,ease:"back.out(3)"}},{t + .6 + i * .3:.2f});')

    # 4 · el detective busca a la niña
    t = 18.5
    lupa = (f'<g id="lupa"><circle cx="95" cy="-170" r="34" fill="none" stroke="{INK}" stroke-width="8"/>'
            f'<line x1="72" y1="-146" x2="50" y2="-112" stroke="{INK}" stroke-width="10" stroke-linecap="round"/></g>')
    scene("s4", t, 5.5, f'<line x1="0" y1="860" x2="{W}" y2="860" stroke="{INK}" stroke-width="6"/>'
          + stick("det", 300, 860, 1.4, extra=lupa, hat=True)
          + f'<text id="q1" x="1250" y="420" class="q">?</text><text id="q2" x="1420" y="330" class="q">?</text>',
          "Pero cuando buscas a la niña…")
    js += [f'tl.to("#det",{{x:700,duration:3.2,ease:"none"}},{t});',
           f'tl.fromTo("#det-ll",{{rotation:-18}},{{rotation:18,duration:.4,repeat:7,yoyo:true,svgOrigin:"0 -90",ease:"sine.inOut"}},{t});',
           f'tl.fromTo("#det-lr",{{rotation:18}},{{rotation:-18,duration:.4,repeat:7,yoyo:true,svgOrigin:"0 -90",ease:"sine.inOut"}},{t});',
           f'tl.from("#q1",{{scale:0,opacity:0,transformOrigin:"1270px 380px",duration:.4,ease:"back.out(3)"}},{t + 3.4});',
           f'tl.from("#q2",{{scale:0,opacity:0,transformOrigin:"1440px 290px",duration:.4,ease:"back.out(3)"}},{t + 3.8});']

    # 5 · el expediente vacío
    t = 24.0
    filas = "".join(f'<text x="-360" y="{-60 + i * 90}" class="field">{k}</text>'
                    f'<text id="f{i}" x="360" y="{-60 + i * 90}" text-anchor="end" class="field red">???</text>'
                    for i, k in enumerate(["NOMBRE", "FECHA", "REGISTRO"]))
    scene("s5", t, 6.0, f'''
      <g id="card" transform="translate(960 560)">
        <rect x="-440" y="-300" width="880" height="560" rx="14" fill="#fff" stroke="{INK}" stroke-width="8"/>
        <text x="-360" y="-200" class="mid">EXPEDIENTE: LA NIÑA</text>
        <line x1="-360" y1="-170" x2="360" y2="-170" stroke="{INK}" stroke-width="4"/>{filas}
      </g>
      <g id="s5-stamp" transform="translate(1180 820) rotate(-10)">
        <rect x="-280" y="-75" width="560" height="150" fill="{PAPER}" fill-opacity=".6" stroke="{RED}" stroke-width="10"/>
        <text x="0" y="26" text-anchor="middle" class="stamp">SIN PRUEBAS</text></g>''')
    js += [f'tl.from("#card",{{y:200,opacity:0,duration:.6,ease:"power3.out"}},{t + .2});']
    js += [f'tl.from("#f{i}",{{opacity:0,duration:.25}},{t + 1.2 + i * .6:.2f});' for i in range(3)]
    js.append(f'tl.from("#s5-stamp",{{scale:2.4,opacity:0,transformOrigin:"1180px 820px",duration:.3,ease:"power3.in"}},{t + 3.4});')
    return html, js


def build(duracion: float = 30.0) -> str:
    html, js = escenas()
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="./gsap.min.js"></script>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{PAPER}; }}
  #root {{ width:100%; height:100%; position:relative; font-family:Lato, sans-serif; color:{INK}; }}
  .scene {{ position:absolute; inset:0; background:{PAPER}; }}
  .scene svg {{ position:absolute; inset:0; }}
  .big {{ font: 900 220px Lato, sans-serif; fill:{INK}; }}
  .mid {{ font: 900 56px Lato, sans-serif; fill:{INK}; }}
  .small {{ font: 700 44px Lato, sans-serif; letter-spacing:.2em; fill:{INK}; }}
  .stamp {{ font: 900 64px Lato, sans-serif; letter-spacing:.06em; fill:{RED}; }}
  .q {{ font: 900 170px Lato, sans-serif; fill:{RED}; }}
  .field {{ font: 800 50px Lato, sans-serif; fill:{INK}; }}
  .field.red {{ fill:{RED}; }}
  .cap {{ position:absolute; left:0; right:0; bottom:70px; text-align:center;
         font: 800 54px Lato, sans-serif; color:{INK}; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{duracion}" data-width="{W}" data-height="{H}">
{chr(10).join(html)}
</div>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join("  " + l for l in js)}
  window.__timelines["main"] = tl;
  tl.seek(0);
</script>
</body>
</html>
'''


if __name__ == "__main__":
    out = Path(__file__).with_name("index.html")
    out.write_text(build(), encoding="utf-8")
    print("escrito", out)
