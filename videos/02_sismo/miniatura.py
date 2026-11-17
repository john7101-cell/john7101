"""Miniatura del video 2 (1280x720): "¿CUÁL CAYÓ?" con el edificio de altura media cayendo."""
import sys
from pathlib import Path
import subprocess
import importlib.util
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01_isla"))
from rig_lib import INK, RED, YEL, BLUE, PINK, TEAL, CREAM, Anim, rig
_spec = importlib.util.spec_from_file_location("b2", Path(__file__).parent / "build.py")
b2 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(b2)
building, stamp, ghost_filter, dust = b2.building, b2.stamp, b2.ghost_filter, b2.dust

ROOT = Path(__file__).parent
a = Anim()
a.face("dm", 0, "o", (-28, 28), (-16, -2))
a.pose("dm", 0, .01, uaL=135, faL=30, uaR=-135, faR=-30, head=-6)
DET = dict(shirt="#a47148", pants="#3d405b", hat="fedora")
svg = f'''
<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7b54"/><stop offset="1" stop-color="#ffd56b"/></linearGradient></defs>
<rect width="1920" height="1080" fill="url(#bg)"/>
<rect x="-60" y="900" width="2040" height="200" fill="#9c6644" stroke="{INK}" stroke-width="9"/>
{building("ta", 80, 900, 300, 640, BLUE)}
<g transform="rotate(-24 700 900)">{building("tb", 700, 900, 300, 470, PINK)}</g>
{building("tc", 1320, 900, 320, 260, YEL)}
<g transform="translate(0 0)">{dust("td", 860, 900, 1.6)}</g>
<text x="700" y="180" text-anchor="middle" class="t">¿CUÁL CAYÓ?</text>
{stamp("st", 720, 470, 560, "ESTE CAYÓ", RED, -8)}
{rig("dm", 1690, 1000, 1.6, **DET)}'''
html = f'''<!doctype html><html><head><meta charset="utf-8"><script src="./gsap.min.js"></script><style>
html,body{{margin:0;width:1280px;height:720px;overflow:hidden;background:#000}}
svg{{width:1280px;height:720px;display:block}}
.t{{font:900 170px Lato,sans-serif;fill:#fff;stroke:{INK};stroke-width:20px;paint-order:stroke}}
.tag{{font:900 40px Lato,sans-serif;fill:#fff}} .stamp{{font:900 66px Lato,sans-serif;fill:#fff}}
</style></head><body>{ghost_filter()}<svg viewBox="0 0 1920 1080">{svg}</svg>
<script>const tl=gsap.timeline({{paused:true}});
{chr(10).join(a.lines)}
tl.progress(1);</script></body></html>'''
(ROOT / "miniatura.html").write_text(html, encoding="utf-8")
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
await p.goto('file://'+process.argv[1]+'/miniatura.html');await p.waitForTimeout(500);await p.screenshot({path:process.argv[1]+'/miniatura.png'});await b.close();})();"""
subprocess.run(["node", "-e", js, str(ROOT)], check=True)
print("ok")
