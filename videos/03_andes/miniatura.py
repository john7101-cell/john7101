"""Miniatura del video 3 (1280x720): LOS DIERON POR MUERTOS + 72 DÍAS."""
import importlib.util, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parents[0] / "01_isla"))
from rig_lib import INK, RED, YEL
spec = importlib.util.spec_from_file_location("b3", ROOT / "build.py")
b3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(b3)
svg = f'''<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1d3a"/><stop offset="1" stop-color="#3a5a80"/></linearGradient></defs>
<rect width="1920" height="1080" fill="url(#bg)"/>{b3.montanas("mt")}
{b3.avion("avt", 1380, 470, 1.1)}
<g transform="translate(60 230) rotate(-3)"><text x="0" y="0" class="t">LOS DIERON</text><text x="0" y="175" class="t y">POR MUERTOS</text></g>
{b3.stamp("st", 1420, 800, 760, "72 DÍAS", RED, -6)}'''
html = f'''<!doctype html><html><head><meta charset="utf-8"><script src="./gsap.min.js"></script><style>
html,body{{margin:0;width:1280px;height:720px;overflow:hidden;background:#000}}
svg{{width:1280px;height:720px;display:block}}
.t{{font:900 175px Lato,sans-serif;fill:#fff;stroke:{INK};stroke-width:22px;paint-order:stroke}}
.t.y{{fill:{YEL}}} .stamp{{font:900 100px Lato,sans-serif;fill:#fff}} .tag{{font:900 40px Lato,sans-serif;fill:#fff}}
.tiny{{font:900 40px Lato,sans-serif;fill:{INK}}}
</style></head><body>{b3.ghost_filter()}<svg viewBox="0 0 1920 1080">{svg}</svg></body></html>'''
(ROOT / "miniatura.html").write_text(html, encoding="utf-8")
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
await p.goto('file://'+process.argv[1]+'/miniatura.html');await p.waitForTimeout(400);await p.screenshot({path:process.argv[1]+'/miniatura.png'});await b.close();})();"""
subprocess.run(["node", "-e", js, str(ROOT)], check=True)
from PIL import Image
Image.open(ROOT / "miniatura.png").convert("RGB").save(ROOT / "miniatura.jpg", quality=92)
print("ok")
