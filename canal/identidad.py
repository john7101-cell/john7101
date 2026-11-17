"""Banner (2560x1440) y foto de perfil (800x800) del canal, estilo stickman a color."""
import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "videos/01_isla"))
from rig_lib import INK, PINK, RED, YEL, BLUE, TEAL, PURP, Anim, doll, rig, trajinera, tree
from build import ghost_filter

D = Path(__file__).parent
GSAP = "../videos/01_isla/gsap.min.js"
JUL = dict(shirt="#f1faee", pants="#6c757d", hat="sombrero", mustache=True)
DET = dict(shirt="#a47148", pants="#3d405b", hat="fedora")
LUPA = (f'<g transform="rotate(-90)"><line x1="0" y1="0" x2="0" y2="56" stroke="#5b3a29" stroke-width="12" stroke-linecap="round"/>'
        f'<circle cx="0" cy="88" r="36" fill="#bde0fe" fill-opacity=".6" stroke="{INK}" stroke-width="9"/></g>')
STYLE = f""".t{{font:900 120px Lato,sans-serif;fill:#fff;stroke:{INK};stroke-width:16px;paint-order:stroke;text-anchor:middle}}
.t.y{{fill:{YEL}}} .p{{font:900 50px Lato,sans-serif;fill:#fff;letter-spacing:.12em;text-anchor:middle}}
.boat{{font:900 44px Lato,sans-serif;fill:{RED};letter-spacing:.08em}}"""

# ---------------------------------------------------------------- banner
a = Anim()
a.face("dt", 0, "smile", (-8, 8), (12, -4))
a.pose("dt", 0, .01, uaR=-100, faR=-20, uaL=10)
a.face("jl", 0, "o", (-20, 20), (12, -4))
a.pose("jl", 0, .01, uaL=135, faL=30, uaR=-135, faR=-30)
stars = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" opacity=".8"/>' for x, y in
                [(200, 150), (520, 260), (900, 120), (1250, 210), (1600, 140), (1980, 250), (2300, 160), (2450, 380), (120, 420)])
water_y = 1010
waves = "".join(f'<path d="M-40 {water_y + 70 + i * 70} ' + " ".join(f"Q{x + 80} {water_y + 50 + i * 70} {x + 160} {water_y + 70 + i * 70}" for x in range(-40, 2600, 160))
                + f'" stroke="#7fdcd3" stroke-width="8" fill="none" opacity=".7"/>' for i in range(4))
dolls = "".join(doll(f"bd{i}", x, y, c, 1.3) for i, (x, y, c) in enumerate(
    [(30, 660, PINK), (130, 600, BLUE), (210, 690, YEL), (2390, 640, TEAL), (2480, 590, PURP), (2540, 690, RED)]))
banner_svg = f'''<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3c096c"/>
<stop offset=".55" stop-color="#c9184a"/><stop offset="1" stop-color="#ff9e00"/></linearGradient></defs>
<rect width="2560" height="1440" fill="url(#sk)"/>{ghost_filter()}{stars}
<circle cx="1280" cy="1010" r="300" fill="{YEL}" opacity=".35"/>
{tree(110, 1000, 1.5)}{tree(2470, 1000, 1.5)}{dolls}
<path d="M-40 {water_y} {" ".join(f"Q{x + 80} {water_y - 26} {x + 160} {water_y}" for x in range(-40, 2600, 160))} L2600 1440 L-40 1440 Z" fill="#0f8b8d" stroke="{INK}" stroke-width="9"/>{waves}
{trajinera("tb", 1280, 1180, RED, TEAL, "LUPITA", .8)}
{rig("dt", 420, 960, 1.25, **DET, prop_r=LUPA)}
{rig("jl", 2150, 960, 1.25, **JUL)}
<g filter="url(#glow)" opacity=".85">{rig("gg", 2380, 930, .9, girl=True, ghost=True)}</g>
<text x="1280" y="660" class="t">HISTORIAS Y MISTERIOS</text>
<text x="1280" y="790" class="t y">DE LATINOAMÉRICA</text>
<rect x="890" y="836" width="780" height="80" rx="40" fill="{RED}" stroke="{INK}" stroke-width="7"/>
<text x="1280" y="893" class="p">LO QUE NO TE CONTARON</text>'''

# ---------------------------------------------------------------- perfil (mascota: el detective)
b = Anim()
b.face("dp", 0, "smile", (-14, 14), (14, -6))
b.pose("dp", 0, .01, uaR=-150, faR=-40, uaL=10, head=-8)
perfil_svg = f'''<defs><radialGradient id="pf" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="{YEL}"/>
<stop offset="1" stop-color="#ff6d00"/></radialGradient></defs><rect width="800" height="800" fill="url(#pf)"/>
<circle cx="400" cy="400" r="330" fill="none" stroke="#fff" stroke-width="10" stroke-dasharray="20 18" opacity=".6"/>
{rig("dp", 360, 1150, 2.3, **DET, prop_r=LUPA)}'''

for name, w, h, svg, anim in [("banner", 2560, 1440, banner_svg, a), ("perfil", 800, 800, perfil_svg, b)]:
    html = (f'<!doctype html><html><head><meta charset="utf-8"><script src="{GSAP}"></script><style>'
            f'html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden}} svg{{display:block}} {STYLE}</style></head><body>'
            f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{svg}</svg><script>const tl=gsap.timeline({{paused:true}});'
            f'{"".join(anim.lines)} tl.progress(1);</script></body></html>')
    (D / f"{name}.html").write_text(html, encoding="utf-8")

js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
for (const [n,w,h] of [['banner',2560,1440],['perfil',800,800]]){const p=await b.newPage({viewport:{width:w,height:h}});
await p.goto('file://'+process.argv[1]+'/'+n+'.html');await p.waitForTimeout(300);await p.screenshot({path:process.argv[1]+'/'+n+'.png'});await p.close();}
await b.close();})();"""
subprocess.run(["node", "-e", js, str(D)], check=True)
print("ok")
