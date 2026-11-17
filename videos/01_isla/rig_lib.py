"""Biblioteca de dibujo y animación (rig de monigotes, decorados). Antes: genera index.html (composición HyperFrames) del video 1 en estilo stickman a color.

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
        self.sfx: list[tuple[str, float, float]] = []  # (nombre, tiempo, volumen)

    def sound(self, name: str, t: float, vol: float = .5) -> None:
        self.sfx.append((name, round(t, 3), vol))

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
        if amount >= .14:
            self.sound("impact-bass-1", t, .35)
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
        sello = sel.lstrip("#") in {"st2", "c50", "a50", "y01", "cb2", "nx", "x1", "x2", "x3", "vs"}
        if sello:
            self.sound("impact-bass-2", t, .45)
        elif not any(n == "pop" and abs(tt - t) < .22 for n, tt, _ in self.sfx):
            self.sound("pop", t, .22)
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


