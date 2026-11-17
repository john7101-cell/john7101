"""Genera index.html (composición HyperFrames) del video 1 en estilo stickman a color.

Monigotes con rig: brazos y piernas con codo/rodilla, cabeza con ojos (parpadeo y mirada),
cejas y bocas por emoción. Todo se anima con tweens de atributos `transform` (deterministas,
sin callbacks), así cada render es idéntico.

Por ahora construye el gancho (0-30 s). Cuando llegue la narración, los tiempos de cada escena
se ajustan a las palabras del audio.
"""

from __future__ import annotations

from pathlib import Path

W, H = 1920, 1080
INK = "#14141a"
CREAM = "#fff8ec"
RED = "#e63946"
YEL = "#ffc93c"
TEAL = "#1fb5a8"
PINK = "#ff5d8f"
BLUE = "#3a86ff"
PURP = "#7b2cbf"
SKIN = "#fff3e0"

SW = 11  # grosor de trazo de los monigotes


# ======================================================================= rig del monigote

def rig(id_: str, x: float, y: float, s: float = 1.0, shirt: str = BLUE, pants: str = INK,
        hat: str = "", girl: bool = False, mustache: bool = False, ghost: bool = False,
        prop_r: str = "") -> str:
    """Monigote articulado. (x, y) = pies. Altura ~330 * s.

    Grupos animables (todos con transform inicial para poder tweenear el atributo):
      {id}         translate(x y) scale(s)       posición / escala
      {id}-body    scale(1 1)                    squash & stretch desde los pies
      {id}-uaL/R   rotate(a)  brazo superior (hombro)   {id}-faL/R rotate(a) antebrazo (codo)
      {id}-thL/R   rotate(a)  muslo (cadera)            {id}-shL/R rotate(a) pierna (rodilla)
      {id}-head    rotate(a)  cabeza                    {id}-eyes  scale(1 1) parpadeo
      {id}-pup     translate(dx dy) mirada              {id}-brL/R rotate(a) cejas
      {id}-m-<boca> opacidad: smile, open, frown, flat, o
    """
    st = f'stroke="{INK}" stroke-width="{SW}" stroke-linecap="round" fill="none"'
    op = ' opacity="0.55"' if ghost else ""
    col = "#bde0fe" if ghost else None

    def limb(name: str, ox: float, oy: float, a1: float, a2: float, l1: float, l2: float,
             color: str, end: str = "") -> str:
        return (f'<g transform="translate({ox} {oy})"><g id="{id_}-{name[0]}{name[1]}" transform="rotate({a1})">'
                f'<line x1="0" y1="0" x2="0" y2="{l1}" stroke="{color}" stroke-width="{SW + 6}" stroke-linecap="round"/>'
                f'<line x1="0" y1="0" x2="0" y2="{l1}" {st} stroke-opacity="0"/>'
                f'<g transform="translate(0 {l1})"><g id="{id_}-{name[2]}{name[1]}" transform="rotate({a2})">'
                f'<line x1="0" y1="0" x2="0" y2="{l2}" stroke="{color}" stroke-width="{SW + 2}" stroke-linecap="round"/>'
                f'{end}</g></g></g></g>')

    shirt_c = col or shirt
    pants_c = col or pants
    hand = f'<circle cx="0" cy="62" r="11" fill="{col or SKIN}" stroke="{INK}" stroke-width="5"/>'
    shoe = f'<ellipse cx="10" cy="74" rx="22" ry="11" fill="{INK}"/>'
    legs = (limb("tLs", -16, -150, 8, -4, 78, 74, pants_c, shoe).replace(f"{id_}-tL", f"{id_}-thL").replace(f"{id_}-sL", f"{id_}-shL")
            + limb("tRs", 16, -150, -8, 4, 78, 74, pants_c, shoe).replace(f"{id_}-tR", f"{id_}-thR").replace(f"{id_}-sR", f"{id_}-shR"))
    arm_r_end = hand + (f'<g transform="translate(0 62)">{prop_r}</g>' if prop_r else "")
    arms_back = limb("uLf", -30, -262, 22, -14, 62, 62, shirt_c, hand).replace(f"{id_}-uL", f"{id_}-uaL").replace(f"{id_}-fL", f"{id_}-faL")
    arms_front = limb("uRf", 30, -262, -22, 14, 62, 62, shirt_c, arm_r_end).replace(f"{id_}-uR", f"{id_}-uaR").replace(f"{id_}-fR", f"{id_}-faR")
    torso = (f'<path d="M-34 -276 Q0 -292 34 -276 L30 -150 Q0 -140 -30 -150 Z" fill="{shirt_c}" stroke="{INK}" stroke-width="7"/>'
             if not girl else
             f'<path d="M-26 -278 Q0 -290 26 -278 L58 -140 Q0 -126 -58 -140 Z" fill="{col or PINK}" stroke="{INK}" stroke-width="7"/>')

    hats = {
        "sombrero": f'<ellipse cx="0" cy="-58" rx="92" ry="18" fill="{YEL}" stroke="{INK}" stroke-width="6"/>'
                    f'<path d="M-44 -60 Q-40 -122 0 -124 Q40 -122 44 -60 Z" fill="{YEL}" stroke="{INK}" stroke-width="6"/>'
                    f'<path d="M-42 -76 L42 -76" stroke="{RED}" stroke-width="9"/>',
        "fedora": f'<ellipse cx="0" cy="-60" rx="74" ry="14" fill="#5a3e2b" stroke="{INK}" stroke-width="6"/>'
                  f'<path d="M-46 -62 L-40 -116 Q0 -100 40 -116 L46 -62 Z" fill="#5a3e2b" stroke="{INK}" stroke-width="6"/>'
                  f'<path d="M-44 -76 L44 -76" stroke="{RED}" stroke-width="8"/>',
    }
    braids = (f'<path d="M-50 -10 Q-70 40 -58 80 M50 -10 Q70 40 58 80" stroke="{INK}" stroke-width="12" '
              f'fill="none" stroke-linecap="round"/><circle cx="-58" cy="84" r="9" fill="{PINK}"/>'
              f'<circle cx="58" cy="84" r="9" fill="{PINK}"/>') if girl else ""
    stache = (f'<path d="M-24 22 Q-12 12 0 20 Q12 12 24 22 Q12 30 0 24 Q-12 30 -24 22 Z" fill="#e8e8e8" '
              f'stroke="{INK}" stroke-width="4"/>') if mustache else ""
    mouths = {
        "smile": '<path d="M-18 30 Q0 48 18 30" {s}/>',
        "open": '<path d="M-18 28 Q0 62 18 28 Z" fill="#7a1f2b" stroke="{k}" stroke-width="6"/>',
        "frown": '<path d="M-18 40 Q0 24 18 40" {s}/>',
        "flat": '<path d="M-16 34 L16 34" {s}/>',
        "o": '<ellipse cx="0" cy="36" rx="11" ry="15" fill="#7a1f2b" stroke="{k}" stroke-width="6"/>',
    }
    ms = f'stroke="{INK}" stroke-width="6" stroke-linecap="round" fill="none"'
    mouth_svg = "".join(f'<g id="{id_}-m-{k}" opacity="{1 if k == "flat" else 0}">{v.format(s=ms, k=INK)}</g>'
                        for k, v in mouths.items())
    head = f'''
  <g transform="translate(0 -340)"><g id="{id_}-head" transform="rotate(0)">
   {braids}
   <circle cx="0" cy="0" r="58" fill="{col or SKIN}" stroke="{INK}" stroke-width="8"/>
   <circle cx="-34" cy="22" r="10" fill="{PINK}" opacity="0.45"/><circle cx="34" cy="22" r="10" fill="{PINK}" opacity="0.45"/>
   <g transform="translate(0 -8)"><g id="{id_}-eyes" transform="scale(1 1)">
     <ellipse cx="-20" cy="0" rx="14" ry="17" fill="#fff" stroke="{INK}" stroke-width="5"/>
     <ellipse cx="20" cy="0" rx="14" ry="17" fill="#fff" stroke="{INK}" stroke-width="5"/>
     <g id="{id_}-pup" transform="translate(0 0)"><circle cx="-20" cy="2" r="7" fill="{INK}"/><circle cx="20" cy="2" r="7" fill="{INK}"/>
       <circle cx="-17" cy="-1" r="2.5" fill="#fff"/><circle cx="23" cy="-1" r="2.5" fill="#fff"/></g>
   </g></g>
   <g transform="translate(-20 -32)"><g id="{id_}-brL" transform="rotate(0)"><path d="M-13 0 L13 0" {ms} stroke-width="7"/></g></g>
   <g transform="translate(20 -32)"><g id="{id_}-brR" transform="rotate(0)"><path d="M-13 0 L13 0" {ms} stroke-width="7"/></g></g>
   {stache}{mouth_svg}{hats.get(hat, "")}
  </g></g>'''
    return (f'<g id="{id_}" transform="translate({x} {y}) scale({s})"{op}>'
            f'<ellipse cx="0" cy="4" rx="70" ry="12" fill="{INK}" opacity="0.18"/>'
            f'<g id="{id_}-body" transform="scale(1 1)">{arms_back}{legs}'
            f'<line x1="0" y1="-282" x2="0" y2="-300" stroke="{INK}" stroke-width="{SW}"/>{torso}{head}{arms_front}</g></g>')


class Anim:
    """Acumula líneas de la línea de tiempo GSAP."""

    def __init__(self) -> None:
        self.lines: list[str] = []

    def raw(self, line: str) -> None:
        self.lines.append(line)

    def attr(self, sel: str, value: str, t: float, dur: float = .35, ease: str = "power2.inOut") -> None:
        self.lines.append(f'tl.to("{sel}",{{attr:{{transform:"{value}"}},duration:{dur},ease:"{ease}"}},{t:.3f});')

    def pose(self, id_: str, t: float, dur: float = .35, ease: str = "back.out(1.6)", **j: float) -> None:
        """Ángulos por articulación: uaL faL uaR faR thL shL thR shR head."""
        for k, v in j.items():
            self.attr(f"#{id_}-{k}", f"rotate({v})", t, dur, ease)

    def move(self, id_: str, t: float, x: float, y: float, s: float, dur: float, ease: str = "power1.inOut") -> None:
        self.attr(f"#{id_}", f"translate({x} {y}) scale({s})", t, dur, ease)

    def face(self, id_: str, t: float, mouth: str | None = None, brows: tuple[float, float] | None = None,
             look: tuple[float, float] | None = None) -> None:
        if mouth:
            for m in ("smile", "open", "frown", "flat", "o"):
                self.lines.append(f'tl.to("#{id_}-m-{m}",{{opacity:{1 if m == mouth else 0},duration:.08}},{t:.3f});')
        if brows:
            self.attr(f"#{id_}-brL", f"rotate({brows[0]})", t, .2, "power2.out")
            self.attr(f"#{id_}-brR", f"rotate({brows[1]})", t, .2, "power2.out")
        if look:
            self.attr(f"#{id_}-pup", f"translate({look[0]} {look[1]})", t, .2, "power2.out")

    def blink(self, id_: str, t: float) -> None:
        self.attr(f"#{id_}-eyes", "scale(1 0.1)", t, .07, "power1.in")
        self.attr(f"#{id_}-eyes", "scale(1 1)", t + .09, .08, "power1.out")

    def squash(self, id_: str, t: float, amount: float = .12) -> None:
        self.attr(f"#{id_}-body", f"scale({1 + amount} {1 - amount})", t, .1, "power2.out")
        self.attr(f"#{id_}-body", f"scale({1 - amount * .6} {1 + amount * .6})", t + .1, .12, "power2.out")
        self.attr(f"#{id_}-body", "scale(1 1)", t + .22, .25, "elastic.out(1,0.5)")

    def walk(self, id_: str, t: float, dur: float, step: float = .32, arms: bool = True) -> None:
        n = int(dur / step)
        for i in range(n):
            a = 26 if i % 2 == 0 else -26
            tt = t + i * step
            arm = {"uaL": -a * .7, "uaR": a * .7} if arms else {"uaL": -a * .7}
            self.pose(id_, tt, step, "sine.inOut", thL=a, shL=-abs(a) * .5 if a < 0 else 6,
                      thR=-a, shR=-abs(a) * .5 if a > 0 else 6, **arm)
        self.pose(id_, t + n * step, .25, "power2.out", thL=8, shL=-4, thR=-8, shR=4)

    def breathe(self, id_: str, t: float, dur: float) -> None:
        n = max(1, int(dur / 2.4))
        self.raw(f'tl.to("#{id_}-body",{{attr:{{transform:"scale(1.015 0.985)"}},duration:1.2,repeat:{n * 2 - 1},'
                 f'yoyo:true,ease:"sine.inOut"}},{t:.3f});')

    def pop(self, sel: str, t: float, origin: str = "50% 50%", dur: float = .45) -> None:
        self.lines.append(f'tl.from("{sel}",{{scale:0,opacity:0,transformOrigin:"{origin}",duration:{dur},ease:"back.out(2.4)"}},{t:.3f});')


# ======================================================================= decorados

def sky(id_: str, top: str, bottom: str) -> str:
    return (f'<defs><linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#{id_})"/>')


def water(id_: str, y: int, color: str = "#0f8b8d", light: str = "#7fdcd3") -> str:
    path = " ".join(f"Q{x + 60} {y - 22} {x + 120} {y} T{x + 240} {y}" for x in range(-240, W + 480, 240))
    rows = "".join(f'<path class="{id_}-row" d="M-240 {y + 40 + i * 46} ' +
                   " ".join(f"Q{x + 60} {y + 40 + i * 46 - 14} {x + 120} {y + 40 + i * 46} T{x + 240} {y + 40 + i * 46}"
                            for x in range(-240, W + 480, 240)) +
                   f'" stroke="{light}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".7"/>'
                   for i in range(3))
    return (f'<g id="{id_}" data-layout-allow-overflow><path d="M-240 {y} {path} L{W + 480} {H} L-240 {H} Z" fill="{color}" '
            f'stroke="{INK}" stroke-width="7"/>{rows}</g>')


def trajinera(id_: str, x: int, y: int, body: str, arch: str, name: str, s: float = 1.0) -> str:
    """Trajinera de Xochimilco: casco, techo y arco con nombre."""
    return f'''<g id="{id_}" transform="translate({x} {y}) scale({s})">
  <path d="M-260 0 L260 0 L220 60 L-220 60 Z" fill="{body}" stroke="{INK}" stroke-width="7"/>
  <path d="M-250 18 L250 18" stroke="{YEL}" stroke-width="8"/>
  <line x1="-200" y1="0" x2="-200" y2="-150" stroke="{INK}" stroke-width="8"/><line x1="200" y1="0" x2="200" y2="-150" stroke="{INK}" stroke-width="8"/>
  <path d="M-230 -150 L230 -150 L200 -180 L-200 -180 Z" fill="{arch}" stroke="{INK}" stroke-width="7"/>
  <path d="M-170 -180 Q0 -280 170 -180 Z" fill="{YEL}" stroke="{INK}" stroke-width="7"/>
  <text x="0" y="-200" text-anchor="middle" class="boat">{name}</text>
  <g fill="{PINK}" stroke="{INK}" stroke-width="4"><circle cx="-120" cy="-215" r="12"/><circle cx="120" cy="-215" r="12"/></g>
</g>'''


def tree(x: int, y: int, s: float = 1.0) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M0 0 L0 -270 M0 -170 L-110 -250 M0 -205 L100 -295 M0 -120 L90 -170 M-62 -215 L-135 -200" '
            f'stroke="#5b3a29" stroke-width="16" stroke-linecap="round" fill="none"/>'
            f'<g fill="#2bb673" stroke="{INK}" stroke-width="6" opacity=".95">'
            f'<circle cx="-110" cy="-270" r="46"/><circle cx="100" cy="-310" r="54"/><circle cx="0" cy="-300" r="60"/>'
            f'<circle cx="92" cy="-185" r="36"/></g></g>')


def doll(id_: str, x: int, y: int, dress: str, s: float = 1.0) -> str:
    return f'''<g id="{id_}" transform="translate({x} {y}) scale({s})">
 <line x1="0" y1="-62" x2="0" y2="-30" stroke="{INK}" stroke-width="3"/>
 <path d="M0 6 L-20 46 L20 46 Z" fill="{dress}" stroke="{INK}" stroke-width="4"/>
 <circle cx="0" cy="-12" r="20" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>
 <path d="M-20 -18 Q0 -40 20 -18" fill="#f4a261" stroke="{INK}" stroke-width="4"/>
 <circle cx="-7" cy="-11" r="3.5" fill="{INK}"/><path d="M3 -15 l8 8 M11 -15 l-8 8" stroke="{INK}" stroke-width="3"/>
</g>'''


def caption(id_: str, words: list[str], hot: set[int], color: str = YEL) -> str:
    """Subtítulo estilo viral: palabras gruesas con contorno; las 'hot' resaltadas en color."""
    spans = "".join(f'<span id="{id_}-w{i}" class="w{" hot" if i in hot else ""}" '
                    f'style="{f"--hot:{color};" if i in hot else ""}">{w}</span>' for i, w in enumerate(words))
    return f'<div class="cap" id="{id_}">{spans}</div>'


def caption_anim(a: Anim, id_: str, n: int, t: float, gap: float = .18) -> None:
    for i in range(n):
        a.raw(f'tl.from("#{id_}-w{i}",{{scale:.3,opacity:0,y:30,duration:.22,ease:"back.out(3)"}},{t + i * gap:.3f});')


# ======================================================================= escenas

def escenas() -> tuple[list[str], list[str]]:
    html: list[str] = []
    a = Anim()

    def scene(sid: str, t0: float, dur: float, svg: str, cap: str = "") -> None:
        html.append(f'<div id="{sid}" class="clip scene" data-start="{t0}" data-duration="{dur}" '
                    f'data-layout-allow-overflow><svg viewBox="0 0 {W} {H}" width="{W}" height="{H}">{svg}</svg>{cap}</div>')
        # leve "cámara" que empuja hacia adentro durante toda la escena
        a.raw(f'tl.fromTo("#{sid} svg",{{scale:1}},{{scale:1.06,duration:{dur},ease:"none",transformOrigin:"50% 55%"}},{t0});')

    # ---------------------------------------------------------- 1 · 2001, Xochimilco
    t = 0.0
    sun = f'<circle id="sun" cx="1500" cy="330" r="120" fill="{YEL}" opacity=".95"/>'
    scene("s1", t, 6.5,
          sky("g1", "#ff7b54", "#ffd56b") + sun
          + trajinera("boat1", 420, 700, RED, TEAL, "LUPITA", .85)
          + water("w1", 740)
          + f'''<g transform="translate(1180 760)"><g id="hat1" transform="rotate(0)">
                <ellipse cx="0" cy="0" rx="96" ry="20" fill="{YEL}" stroke="{INK}" stroke-width="7"/>
                <path d="M-46 -2 Q-42 -66 0 -68 Q42 -66 46 -2 Z" fill="{YEL}" stroke="{INK}" stroke-width="7"/>
                <path d="M-44 -20 L44 -20" stroke="{RED}" stroke-width="10"/></g></g>
              <g id="yr"><text x="960" y="300" text-anchor="middle" class="big">2001</text></g>
              <g id="pl"><rect x="650" y="345" width="620" height="78" rx="39" fill="{INK}"/>
                <text x="960" y="400" text-anchor="middle" class="tag">XOCHIMILCO · MÉXICO</text></g>''',
          caption("c1", ["Lo", "encontraron", "en", "el", "canal…"], {1, 4}))
    a.pop("#yr", t + .25, "50% 80%", .55)
    a.pop("#pl", t + .8)
    a.raw(f'tl.from("#boat1",{{x:-700,duration:4.5,ease:"power1.out"}},{t});')
    a.raw(f'tl.to(".w1-row",{{x:-240,duration:6.5,ease:"none"}},{t});')
    a.raw(f'tl.fromTo("#hat1",{{attr:{{transform:"rotate(-6)"}}}},{{attr:{{transform:"rotate(6)"}},duration:1,repeat:5,yoyo:true,ease:"sine.inOut"}},{t});')
    caption_anim(a, "c1", 5, t + 2.0)

    # ---------------------------------------------------------- 2 · 50 años antes: Julián y la niña
    t = 6.5
    moon = f'<circle cx="1620" cy="190" r="80" fill="#fff6d5"/><circle cx="1650" cy="170" r="80" fill="#3b2a6b" opacity=".0"/>'
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#fff" opacity=".8"/>' for x, y in
                    [(200, 120), (420, 200), (760, 90), (980, 180), (1200, 110), (1380, 240), (300, 320), (1760, 380)])
    glow = ('<defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
    scene("s2", t, 6.0,
          sky("g2", "#1b1446", "#5a3d9a") + glow + stars + moon
          + f'<path d="M-50 760 L760 760 L700 1100 L-50 1100 Z" fill="#2d6a4f" stroke="{INK}" stroke-width="7"/>'
          + water("w2", 790, "#21487a", "#6fa8dc")
          + rig("jul", 420, 780, 1.05, shirt="#f1faee", pants="#6c757d", hat="sombrero", mustache=True)
          + f'<g filter="url(#glow)">{rig("girl", 1330, 740, 1.0, girl=True, ghost=True)}</g>'
          + f'''<g id="st2" transform="translate(860 210) rotate(-6)">
                <rect x="-310" y="-72" width="620" height="144" rx="10" fill="{RED}" stroke="{INK}" stroke-width="7"/>
                <text x="0" y="24" text-anchor="middle" class="stamp">50 AÑOS ANTES</text></g>''',
          caption("c2", ["Según", "él,", "aquí", "se", "ahogó", "una", "niña"], {4, 6}, PINK))
    a.pop("#st2", t + .3, "50% 50%", .35)
    a.raw(f'tl.from("#girl",{{opacity:0,duration:1.2}},{t + 1.2});')
    a.raw(f'tl.to("#girl",{{attr:{{transform:"translate(1330 700) scale(1)"}},duration:1.6,repeat:2,yoyo:true,ease:"sine.inOut"}},{t + 1.2});')
    a.breathe("jul", t, 6)
    a.face("jul", t, "flat", (0, 0), (6, 0))
    a.blink("jul", t + .9)
    # la ve: susto con anticipación → salto → manos a la cara
    a.face("jul", t + 2.0, "o", (-18, 18), (10, -2))
    a.squash("jul", t + 2.0, .14)
    a.pose("jul", t + 2.05, .3, uaL=-150, faL=-30, uaR=150, faR=30, head=-6)
    a.attr("#jul", "translate(380 780) scale(1.05)", t + 2.05, .3, "power2.out")
    a.blink("jul", t + 3.6)
    a.face("jul", t + 4.3, "frown", (14, -14), (12, 4))
    a.pose("jul", t + 4.3, .5, "power2.inOut", uaL=30, faL=-60, uaR=-30, faR=60, head=8)
    caption_anim(a, "c2", 7, t + .8)

    # ---------------------------------------------------------- 3 · la isla se llena de muñecas
    t = 12.5
    colors = [PINK, BLUE, YEL, TEAL, RED, PURP, "#ff9f1c", PINK, BLUE, TEAL, YEL, RED, PURP, "#ff9f1c"]
    pos = [(480, 470), (560, 400), (640, 480), (920, 400), (1000, 330), (1080, 420), (1290, 430),
           (1370, 370), (1450, 450), (760, 540), (1180, 520), (860, 300), (1220, 330), (420, 560)]
    dolls = "".join(doll(f"d{i}", x, y, c) for i, ((x, y), c) in enumerate(zip(pos, colors)))
    island = (f'<path d="M180 880 Q960 690 1740 880 Z" fill="#9c6644" stroke="{INK}" stroke-width="8"/>'
              f'<path d="M230 868 Q960 720 1690 868" stroke="#2bb673" stroke-width="22" fill="none"/>'
              + tree(560, 790, 1.15) + tree(980, 745, 1.35) + tree(1380, 790, 1.15))
    held = (f'<g id="held">{doll("dh", 0, 40, PINK, .9)}</g>')
    scene("s3", t, 6.0,
          sky("g3", "#4cc9f0", "#b8f2e6") + water("w3", 900) + island + dolls
          + rig("jul2", 1640, 860, .9, shirt="#f1faee", pants="#6c757d", hat="sombrero", mustache=True, prop_r=held),
          caption("c3", ["Medio", "siglo", "colgando", "muñecas"], {2, 3}))
    for i in range(len(pos)):
        a.pop(f"#d{i}", t + .9 + i * .28, "50% 0%", .35)
    a.breathe("jul2", t, 6)
    a.face("jul2", t, "flat", (10, -10), (-8, -6))
    a.pose("jul2", t + .2, .5, "power2.inOut", uaR=-160, faR=-10, head=-10)
    a.blink("jul2", t + 1.6)
    a.face("jul2", t + 3.4, "smile", (-6, 6), (-6, -4))
    a.pose("jul2", t + 3.4, .5, "power2.inOut", uaR=-30, faR=40, uaL=10, faL=-20, head=4)
    a.blink("jul2", t + 4.4)
    caption_anim(a, "c3", 4, t + .5, .25)

    # ---------------------------------------------------------- 4 · el detective busca a la niña
    t = 18.5
    lupa = (f'<g transform="rotate(-90)"><line x1="0" y1="0" x2="0" y2="56" stroke="#5b3a29" stroke-width="12" stroke-linecap="round"/>'
            f'<circle cx="0" cy="88" r="36" fill="#bde0fe" fill-opacity=".6" stroke="{INK}" stroke-width="9"/></g>')
    scene("s4", t, 5.5,
          sky("g4", "#ffd60a", "#ffc300")
          + f'<rect x="0" y="860" width="{W}" height="220" fill="#ff9f1c" stroke="{INK}" stroke-width="7"/>'
          + rig("det", 200, 900, 1.25, shirt="#a47148", pants="#3d405b", hat="fedora", prop_r=lupa)
          + f'<text id="q1" x="1300" y="430" class="q">?</text><text id="q2" x="1480" y="340" class="q">?</text>'
          + f'<text id="q3" x="1620" y="460" class="q">?</text>',
          caption("c4", ["Pero", "cuando", "buscas", "a", "la", "niña…"], {2, 5}, RED))
    a.face("det", t, "flat", (-8, 8), (10, 0))
    a.pose("det", t, .3, uaR=-100, faR=-20)
    a.walk("det", t, 2.9, arms=False)
    a.raw(f'tl.to("#det",{{attr:{{transform:"translate(860 900) scale(1.25)"}},duration:2.9,ease:"none"}},{t});')
    a.pose("det", t, .3, uaR=-80, faR=-10)
    a.face("det", t + 3.0, None, None, (-12, 0))
    a.face("det", t + 3.5, None, None, (12, 0))
    a.face("det", t + 4.0, "frown", (20, -20), (0, -6))
    a.pose("det", t + 4.0, .4, "back.out(2)", uaL=-170, faL=-70, head=10)  # se rasca la cabeza
    a.blink("det", t + 4.6)
    a.pop("#q1", t + 3.1, "50% 100%")
    a.pop("#q2", t + 3.5, "50% 100%")
    a.pop("#q3", t + 3.9, "50% 100%")
    caption_anim(a, "c4", 6, t + .3)

    # ---------------------------------------------------------- 5 · expediente vacío
    t = 24.0
    filas = "".join(f'<text x="-350" y="{-50 + i * 92}" class="field">{k}</text>'
                    f'<text id="f{i}" x="350" y="{-50 + i * 92}" text-anchor="end" class="field red">???</text>'
                    for i, k in enumerate(["NOMBRE", "FECHA", "REGISTRO"]))
    scene("s5", t, 6.0,
          sky("g5", "#2b2d42", "#8d0801")
          + f'''<g id="card" transform="translate(860 450) rotate(-2)">
                <rect x="-440" y="-300" width="880" height="560" rx="18" fill="{CREAM}" stroke="{INK}" stroke-width="9"/>
                <rect x="-440" y="-300" width="880" height="110" rx="18" fill="{YEL}" stroke="{INK}" stroke-width="9"/>
                <text x="0" y="-228" text-anchor="middle" class="mid">EXPEDIENTE: LA NIÑA</text>{filas}</g>
              <g id="st5" transform="translate(1060 730) rotate(-9)">
                <rect x="-300" y="-78" width="600" height="156" rx="12" fill="{RED}" stroke="{INK}" stroke-width="9"/>
                <text x="0" y="28" text-anchor="middle" class="stamp">SIN PRUEBAS</text></g>'''
          + rig("det2", 1620, 960, 1.1, shirt="#a47148", pants="#3d405b", hat="fedora"),
          caption("c5", ["No", "aparece", "por", "ningún", "lado"], {1, 3}, YEL))
    a.raw(f'tl.from("#card",{{y:260,opacity:0,rotation:-8,duration:.6,ease:"back.out(1.6)"}},{t + .2});')
    for i in range(3):
        a.pop(f"#f{i}", t + 1.1 + i * .5, "100% 50%", .3)
    a.raw(f'tl.from("#st5",{{scale:2.6,opacity:0,transformOrigin:"50% 50%",duration:.28,ease:"power4.in"}},{t + 3.0});')
    a.face("det2", t, "flat", (0, 0), (-12, 0))
    a.breathe("det2", t, 6)
    a.blink("det2", t + 1.4)
    a.squash("det2", t + 3.0, .18)
    a.face("det2", t + 3.05, "open", (-22, 22), (-12, -6))
    a.pose("det2", t + 3.05, .3, uaL=-140, faL=-40, uaR=140, faR=40, head=-8)
    a.blink("det2", t + 4.8)
    caption_anim(a, "c5", 5, t + 3.4, .2)

    return html, a.lines


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
  html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{INK}; }}
  #root {{ width:100%; height:100%; position:relative; overflow:hidden; font-family:Lato, sans-serif; color:{INK}; }}
  .scene {{ position:absolute; inset:0; overflow:hidden; }}
  .scene svg {{ position:absolute; inset:0; }}
  .big {{ font: 900 230px Lato, sans-serif; fill:#fff; stroke:{INK}; stroke-width:12px; paint-order:stroke; }}
  .tag {{ font: 900 40px Lato, sans-serif; letter-spacing:.14em; fill:#fff; }}
  .mid {{ font: 900 54px Lato, sans-serif; fill:{INK}; }}
  .boat {{ font: 900 44px Lato, sans-serif; fill:{RED}; letter-spacing:.08em; }}
  .stamp {{ font: 900 68px Lato, sans-serif; letter-spacing:.05em; fill:#fff; }}
  .q {{ font: 900 190px Lato, sans-serif; fill:{RED}; stroke:{INK}; stroke-width:8px; paint-order:stroke; }}
  .field {{ font: 900 52px Lato, sans-serif; fill:{INK}; }}
  .field.red {{ fill:{RED}; }}
  .cap {{ position:absolute; left:120px; right:120px; bottom:64px; display:flex; flex-wrap:wrap; gap:0 22px;
          justify-content:center; }}
  .cap .w {{ display:inline-block; font: 900 74px Lato, sans-serif; color:#fff; text-transform:uppercase;
             -webkit-text-stroke: 12px {INK}; paint-order: stroke fill; }}
  .cap .w.hot {{ color: var(--hot); }}
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
