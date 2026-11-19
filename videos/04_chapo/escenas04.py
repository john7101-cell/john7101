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
            + f'<g>{pill("pen", 360, 340, 300, "PENAL", INK, "tiny")}{pill("cas", 1560, 340, 360, "CASA", TEAL, "tiny")}</g>')


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
            + f'<g id="rango">{pill("rg", 960, 440, 740, "ESTIMADO: 12 A 24 MESES", RED, "tiny")}</g>'
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
            + f'<g id="hint">{pill("hn", 1400, 230, 620, "LOS PLANOS IMPORTAN", INK, "tiny")}</g>'
            + f'<g id="ojo">{pill("ojp", 1450, 700, 560, "ALGO NO CUADRA", RED, "tiny")}</g>')


def e_complicidad4(a, t0, d):
    a.pop("#st4", T("complicidad", 0) + .3)
    a.pop("#tag4", T("complicidad", 1) + .2)
    a.sound("impact-bass-2", T("complicidad", 0) + .3, .4)
    return (sky("gc4", "#2b2d42", "#6d597a") + card("cc4", 960, 480, 900, 560, "PLANOS DEL PENAL", YEL,
            text(0, 60, "¿QUIÉN LOS TENÍA?", "mid") + text(0, 150, "ANÁLISIS DE EXPERTOS", "tiny"), -2)
            + f'<g id="st4">{stamp("sp4", 960, 880, 720, "NO ES UN HECHO CONFIRMADO", RED, -3)}</g>'
            + f'<g id="tag4">{pill("tg4p", 960, 190, 760, "COMPLICIDAD", PURP, "tag")}</g>')


def e_desenlace4(a, t0, d):
    a.pop("#e15", t0 + .2); a.pop("#e16", T("desenlace", 0) + .2); a.pop("#e17", T("desenlace", 0) + 1.2)
    a.raw(f'tl.fromTo("#linea",{{attr:{{transform:"scale(0 1)"}}}},{{attr:{{transform:"scale(1 1)"}},duration:1.6,ease:"power2.out"}},{t0 + .4:.3f});')
    a.sound("chime", T("desenlace", 0) + .2, .35)
    return (sky("gd4", "#3a0ca3", "#10002b") + f'<g id="linea" transform="translate(0 0)"><line x1="260" y1="560" x2="1660" y2="560" stroke="{YEL}" stroke-width="12"/></g>'
            + f'<g id="e15">{pill("p15", 420, 560, 360, "2015 · FUGA", RED, "tiny")}</g>'
            + f'<g id="e16">{pill("p16", 960, 560, 420, "RECAPTURA", INK, "tiny")}</g>'
            + f'<g id="e17">{pill("p17", 1500, 560, 420, "2017 · EXTRADICIÓN", GREEN, "tiny")}</g>'
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
