"""Miniatura del video 4 (1280x720): ¿CUÁNTO TARDÓ? + túnel de 1,5 km."""
import importlib.util, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parents[0] / "01_isla"))
from rig_lib import INK, RED, YEL, Anim, rig
spec = importlib.util.spec_from_file_location("b4", ROOT / "build.py")
b4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(b4)
DET = dict(shirt="#a47148", pants="#3d405b", hat="fedora")
a = Anim(); a.face("dm", 0, "o", (-28, 28), (-16, -2)); a.pose("dm", 0, .01, uaR=-150, faR=-40, head=-6)
svg = f'''<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff3d6"/><stop offset="1" stop-color="#ffb703"/></linearGradient></defs>
<rect width="1920" height="1080" fill="url(#bg)"/>
<rect x="0" y="560" width="1920" height="520" fill="#8d5524" stroke="{INK}" stroke-width="10"/>
<path d="M200 640 L1720 640 L1720 690 L200 690 Z" fill="#3a3a3a" stroke="{INK}" stroke-width="8"/>
<line x1="200" y1="700" x2="1720" y2="700" stroke="#adb5bd" stroke-width="12"/>
{rig("dm", 1560, 880, 1.7, **DET)}
{b4.pill("tt", 980, 300, 660, "1,5 KM BAJO TIERRA", RED, "tag")}'''
html = f'''<!doctype html><html><head><meta charset="utf-8"><script src="./gsap.min.js"></script><style>
html,body{{margin:0;width:1280px;height:720px;overflow:hidden;background:#000}}
svg{{width:1280px;height:720px;display:block}}
.t{{font:900 200px Lato,sans-serif;fill:#fff;stroke:{INK};stroke-width:22px;paint-order:stroke}}
.t.y{{fill:{YEL}}} .tag{{font:900 44px Lato,sans-serif;fill:#fff}}
</style></head><body><svg viewBox="0 0 1920 1080">{svg}
<text x="60" y="230" class="t">¿CUÁNTO</text><text x="60" y="400" class="t y">TARDÓ?</text>
</svg><script>const tl=gsap.timeline({{paused:true}});{chr(10).join(a.lines)} tl.progress(1);</script></body></html>'''
(ROOT / "miniatura.html").write_text(html, encoding="utf-8")
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
await p.goto('file://'+process.argv[1]+'/miniatura.html');await p.waitForTimeout(400);await p.screenshot({path:process.argv[1]+'/miniatura.png'});await b.close();})();"""
subprocess.run(["node", "-e", js, str(ROOT)], check=True)
from PIL import Image
Image.open(ROOT / "miniatura.png").convert("RGB").save(ROOT / "miniatura.jpg", quality=92)
print("ok")
