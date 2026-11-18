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
            + f'<g id="qt3">{text(960, 170, "¿CUÁNTOS SOBREVIVIERON?", "huge")}</g>'
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
            + f'<path id="avl" d="M600 420 L980 760 L740 980 L460 720 Z" fill="{NIEVE}" stroke="{INK}" stroke-width="7" opacity=".0"/>'
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
    a.raw(f'tl.fromTo("#cp",{{attr:{{transform:"translate(180 880) scale(.9)"}}}},{{attr:{{transform:"translate(1080 880) scale(.9)"}},duration:{tc - t0:.2f},ease:"none"}},{t0:.3f});')
    a.raw(f'tl.fromTo("#cq",{{attr:{{transform:"translate(120 880) scale(.9)"}}}},{{attr:{{transform:"translate(1020 880) scale(.9)"}},duration:{tc - t0:.2f},ease:"none"}},{t0 + .1:.3f});')
    a.raw(f'tl.from("#cat",{{opacity:0,duration:.6}},{tc + .2:.3f});')
    a.pop("#pill10", t0 + .3)
    a.pop("#pillcat", tc + .4)
    a.sound("riser", t0, .4)
    return (sky("gc6", "#7ec8e3", "#e0fbfc") + montanas("mg6") + ground("cg6", 900, "#dbe9f4")
            + rig("cp", 180, 880, .9, **ANA, prop_r="") + rig("cq", 120, 880, .9, **JUL)
            + f'<g id="cat" transform="translate(1500 880)">{rig("catr", 0, 0, .9, shirt="#c77dff", pants="#3d405b", hat="fedora")}</g>'
            + f'<g id="pill10">{pill("p10", 560, 240, 720, "10 DÍAS DE CAMINO", INK, "tag")}</g>'
            + f'<g id="pillcat">{pill("pc", 1500, 260, 560, "SERGIO CATALÁN", TEAL, "tiny")}</g>')


def e_rescate3(a: Anim, t0: float, d: float) -> str:
    tr = T("rescate", 1)
    tc = T("rescate", 2)
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
            + heli + f'<g id="dias">{text(960, 500, "", "tiny")}</g>'
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
            + f'<g id="cfin3">{card("cf3", 1520, 620, 560, 380, "MIRA ESTO", YEL, text(0, 100, "LA ISLA DE LAS", "tiny") + text(0, 160, "MUÑECAS", "tiny"), 3)}</g>')


ESC = {"gancho": e_gancho3, "quiz": e_quiz3, "impacto": e_impacto3, "espera": e_espera3, "caminata": e_caminata3,
       "rescate": e_rescate3, "cierre": e_cierre3}

