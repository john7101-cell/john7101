"""3 Shorts verticales (1080x1920) del video 4, con gancho arriba y enlace al video largo."""
import subprocess
from pathlib import Path
ROOT = Path(__file__).parent
SRC = ROOT.parent / "video4_chapo_tunel.mp4"
FONT = "/usr/share/fonts/truetype/lato/Lato-Black.ttf"
SHORTS = [
    ("short1_cuanto_tardo", 15.0, 41.7, "¿CUÁNTO TARDÓ?", "ADIVINA ANTES DE VER"),
    ("short2_tunel", 42.0, 76.7, "UN TÚNEL DE 1,5 KM", "BAJO UNA PRISIÓN"),
    ("short3_meses", 77.0, 103.7, "¿CUÁNTOS MESES?", "LA RESPUESTA TE SORPRENDE"),
]
def fit(t): return min(110, int(960 / (len(t) * .64)))
def dt(text, y, size, color="white", extra=""):
    t = text.replace(":", r"\:").replace("'", r"\'")
    return (f"drawtext=fontfile={FONT}:text='{t}':fontsize={size}:fontcolor={color}:borderw={max(6, size // 9)}:"
            f"bordercolor=black:x=(w-text_w)/2:y={y}{extra}")
for name, a, b, l1, l2 in SHORTS:
    d = b - a
    vf = ("[0:v]split[bgsrc][fgsrc];[bgsrc]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.18[bg];"
          "[fgsrc]scale=1080:-2[fg];[bg][fg]overlay=0:660,"
          + dt(l1, 250, fit(l1)) + "," + dt(l2, 380, fit(l2), "0xFFC93C") + ","
          + "drawbox=x=90:y=1390:w=900:h=120:color=0xE63946@1:t=fill,"
          + dt("HISTORIA COMPLETA EN EL CANAL", 1422, 56) + ","
          + dt("VIDEO COMPLETO: ENLACE EN LA DESCRIPCIÓN", 1580, 46, "white", f":enable='gte(t,{d - 6:.1f})'")
          + f",fade=t=in:st=0:d=0.25,fade=t=out:st={d - .35:.2f}:d=0.35[v]")
    af = f"afade=t=in:st=0:d=0.2,afade=t=out:st={d - .5:.2f}:d=0.5"
    out = ROOT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(a), "-t", f"{d:.2f}", "-i", str(SRC),
                    "-filter_complex", vf, "-map", "[v]", "-map", "0:a", "-af", af, "-c:v", "libx264", "-crf", "19",
                    "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-r", "30", str(out)], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{d * .5:.2f}", "-i", str(out), "-frames:v", "1",
                    str(ROOT / f"{name}_miniatura.jpg")], check=True)
    print(out.name, f"{d:.1f}s")
