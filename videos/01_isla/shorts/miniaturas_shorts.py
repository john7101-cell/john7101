"""Miniaturas verticales (1080x1920) de los 3 Shorts, estilo stickman del canal."""
import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from rig_lib import INK, PINK, RED, YEL, Anim, doll, rig
from build import ghost_filter, card, stamp

D = Path(__file__).parent
JUL = dict(shirt="#f1faee", pants="#6c757d", hat="sombrero", mustache=True)
DET = dict(shirt="#a47148", pants="#3d405b", hat="fedora")
ANA = dict(shirt="#2bb673", pants="#264653")


def bg(a, b):
    return (f'<defs><radialGradient id="bg" cx="50%" cy="55%" r="75%"><stop offset="0" stop-color="{a}"/>'
            f'<stop offset="1" stop-color="{b}"/></radialGradient></defs><rect width="1080" height="1920" fill="url(#bg)"/>{ghost_filter()}')


def titulo(l1, l2, y=260):
    fs = min(170, int(1000 / (max(len(l1), len(l2)) * .62)))
    return (f'<text x="540" y="{y}" class="t">{l1}</text><text x="540" y="{y + int(fs * 1.12)}" class="t y">{l2}</text>')


def water(y):
    return (f'<path d="M-20 {y} Q135 {y - 30} 270 {y} T540 {y} T810 {y} T1100 {y} L1100 1920 L-20 1920 Z" fill="#1d3557" stroke="{INK}" stroke-width="8"/>'
            + "".join(f'<path d="M-20 {y + 60 + i * 60} Q135 {y + 40 + i * 60} 270 {y + 60 + i * 60} T540 {y + 60 + i * 60} T810 {y + 60 + i * 60} T1100 {y + 60 + i * 60}" '
                      f'stroke="#457b9d" stroke-width="7" fill="none"/>' for i in range(4)))


SOMBRERO = (f'<ellipse cx="0" cy="0" rx="190" ry="40" fill="{YEL}" stroke="{INK}" stroke-width="10"/>'
            f'<path d="M-92 -4 Q-84 -132 0 -136 Q84 -132 92 -4 Z" fill="{YEL}" stroke="{INK}" stroke-width="10"/>'
            f'<path d="M-88 -40 L88 -40" stroke="{RED}" stroke-width="18"/>')

piezas = {}

a = Anim()
piezas["miniatura_short1"] = (a, bg("#9d0208", "#10002b") + titulo("¿LA NIÑA", "EXISTIÓ?")
    + f'<g filter="url(#glow)">{rig("g1", 690, 1640, 2.2, girl=True, ghost=True)}</g>'
    + f'<line x1="250" y1="480" x2="250" y2="760" stroke="{INK}" stroke-width="9"/>{doll("d1", 250, 1060, PINK, 6)}'
    + stamp("s1", 540, 1760, 640, "SIN PRUEBAS", RED, -5))

b = Anim()
b.face("an", 0, "o", (-28, 28), (14, 8))
b.pose("an", 0, .01, uaL=135, faL=30, uaR=-135, faR=-30, head=6)
piezas["miniatura_short2"] = (b, bg("#7209b7", "#10002b") + titulo("LO ENCONTRARON", "EN EL MISMO LUGAR")
    + f'<path d="M-20 1230 L520 1230 L480 1920 L-20 1920 Z" fill="#6f4518" stroke="{INK}" stroke-width="8"/>' + water(1260)
    + rig("an", 280, 1240, 1.9, **ANA) + f'<g transform="translate(780 1290) rotate(-6)">{SOMBRERO}</g>'
    + f'<g filter="url(#glow)" opacity=".8">{rig("g2", 800, 1180, 1.1, girl=True, ghost=True)}</g>'
    + stamp("s2", 760, 690, 360, "2001", RED, 6))

c = Anim()
c.face("dt", 0, "open", (-26, 26), (-14, -6))
c.pose("dt", 0, .01, uaL=135, faL=30, uaR=-135, faR=-30, head=-6)
filas = "".join(f'<text x="-330" y="{-40 + i * 100}" class="f">{k}</text><text x="330" y="{-40 + i * 100}" text-anchor="end" class="f r">???</text>'
                for i, k in enumerate(["NOMBRE", "FECHA", "REGISTRO"]))
piezas["miniatura_short3"] = (c, bg("#8d0801", "#1b1b2f") + titulo("NO HAY NOMBRE.", "NO HAY FECHA.")
    + card("cd", 540, 870, 820, 520, "EXPEDIENTE: LA NIÑA", body=filas, rot=-3)
    + stamp("s3", 470, 1200, 600, "SIN PRUEBAS", RED, -8) + rig("dt", 800, 1920, 1.45, **DET))

for name, (anim, svg) in piezas.items():
    html = f'''<!doctype html><html><head><meta charset="utf-8"><script src="../gsap.min.js"></script><style>
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#000}} svg{{display:block}}
.t{{font:900 {{FS}}px Lato,sans-serif;fill:#fff;stroke:{INK};stroke-width:20px;paint-order:stroke;text-anchor:middle}}
.t.y{{fill:{YEL}}} .mid{{font:900 50px Lato,sans-serif;fill:{INK}}} .stamp{{font:900 68px Lato,sans-serif;fill:#fff;letter-spacing:.04em}}
.f{{font:900 52px Lato,sans-serif;fill:{INK}}} .f.r{{fill:{RED}}}
</style></head><body><svg width="1080" height="1920" viewBox="0 0 1080 1920">{svg}</svg>
<script>const tl=gsap.timeline({{paused:true}});{"".join(anim.lines)} tl.progress(1);</script></body></html>'''
    largo = max(len(x) for x in ["¿LA NIÑA", "LO ENCONTRARON", "EN EL MISMO LUGAR", "NO HAY NOMBRE."] if x in svg)
    fs = min(170, int(1000 / (largo * .62)))
    html = html.replace("{FS}", str(fs)).replace("FSV_", "")
    (D / f"{name}.html").write_text(html, encoding="utf-8")

js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for (const n of process.argv.slice(1)){await p.goto('file://'+n+'.html');await p.waitForTimeout(300);await p.screenshot({path:n+'.png'});}await b.close();})();"""
subprocess.run(["node", "-e", js, *[str(D / n) for n in piezas]], check=True)
print("ok")
