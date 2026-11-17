"""3 Shorts verticales (1080x1920) cortados del video 2, con gancho arriba y llamado al video completo."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT.parent / "video2_el_sismo_1985.mp4"
FONT = "/usr/share/fonts/truetype/lato/Lato-Black.ttf"
SHORTS = [
    ("short1_cual_cayo", 17.0, 38.5, "¿CUÁL CAYÓ?", "ADIVINA: A, B O C"),
    ("short2_resonancia", 73.3, 114.0, "¿POR QUÉ CAYÓ", "EL DE ALTURA MEDIA?"),
    ("short3_bebes", 129.5, 144.5, "14 BEBÉS RESCATADOS", "ENTRE LOS ESCOMBROS"),
]


def fit(t):
    return min(110, int(960 / (len(t) * .64)))


def dt(text, y, size, color="white", extra=""):
    t = text.replace(":", r"\:").replace("'", r"\'")
    return (f"drawtext=fontfile={FONT}:text='{t}':fontsize={size}:fontcolor={color}:borderw={max(6, size // 9)}:"
            f"bordercolor=black:x=(w-text_w)/2:y={y}{extra}")


for name, a, b, l1, l2 in SHORTS:
    d = b - a
    vf = ("[0:v]split[bgsrc][fgsrc];"
          "[bgsrc]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.18[bg];"
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
