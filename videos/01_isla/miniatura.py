"""Miniatura del video 1 (1280x720) con el mismo estilo stickman. Escribe miniatura.png."""
from pathlib import Path
from rig_lib import INK, PINK, RED, YEL, Anim, doll, rig
from build import ghost_filter

ROOT = Path(__file__).parent
a = Anim()
a.face("jt", 0, "o", (-28, 28), (-16, -2))
a.pose("jt", 0, .01, uaL=135, faL=30, uaR=-135, faR=-30, head=-6)
JUL = dict(shirt="#f1faee", pants="#6c757d", hat="sombrero", mustache=True)
svg = f'''
<defs><radialGradient id="bg" cx="65%" cy="45%" r="80%"><stop offset="0" stop-color="#9d0208"/>
<stop offset=".55" stop-color="#3c096c"/><stop offset="1" stop-color="#10002b"/></radialGradient></defs>
<rect width="1920" height="1080" fill="url(#bg)"/>
{ghost_filter()}
<g filter="url(#glow)" opacity=".7">{rig("gt", 1250, 1000, 1.05, girl=True, ghost=True)}</g>
<line x1="930" y1="-20" x2="930" y2="300" stroke="{INK}" stroke-width="10"/>
{doll("dt", 930, 620, PINK, 6.5)}
{rig("jt", 1610, 1560, 2.5, **JUL)}
<g transform="translate(70 300) rotate(-4)"><text x="0" y="0" class="t">¿Y LA</text><text x="0" y="200" class="t y">NIÑA?</text></g>
<g transform="translate(420 880) rotate(-6)"><rect x="-330" y="-80" width="660" height="160" rx="14" fill="{RED}" stroke="{INK}" stroke-width="12"/>
<text x="0" y="32" text-anchor="middle" class="s">SIN PRUEBAS</text></g>'''
html = f'''<!doctype html><html><head><meta charset="utf-8"><script src="./gsap.min.js"></script><style>
html,body{{margin:0;width:1280px;height:720px;overflow:hidden;background:#000}}
svg{{width:1280px;height:720px;display:block}}
.t{{font:900 230px Lato,sans-serif;fill:#fff;stroke:{INK};stroke-width:22px;paint-order:stroke}}
.t.y{{fill:{YEL}}}
.s{{font:900 92px Lato,sans-serif;fill:#fff;letter-spacing:.04em}}
</style></head><body><svg viewBox="0 0 1920 1080">{svg}</svg>
<script>const tl=gsap.timeline({{paused:true}});
{chr(10).join(a.lines)}
tl.progress(1);</script></body></html>'''
(ROOT / "miniatura.html").write_text(html, encoding="utf-8")
