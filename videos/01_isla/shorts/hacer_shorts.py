"""Corta 3 Shorts verticales (1080x1920) del video final: video al centro, fondo desenfocado,
gancho arriba y llamado al video completo abajo."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT.parent / "video1_isla_de_las_munecas.mp4"
FONT = "/usr/share/fonts/truetype/lato/Lato-Black.ttf"
SHORTS = [
    ("short1_gancho", 0.0, 40.6, "¿LA NIÑA", "EXISTIÓ?"),
    ("short2_2001", 238.3, 272.0, "LO ENCONTRARON", "EN EL MISMO LUGAR"),
    ("short3_sin_pruebas", 271.7, 309.6, "NO HAY NOMBRE.", "NO HAY FECHA."),
]


def dt(text, y, size, color="white", extra=""):
    t = text.replace(":", r"\:").replace("'", r"\'")
    return (f"drawtext=fontfile={FONT}:text='{t}':fontsize={size}:fontcolor={color}:borderw={max(6, size // 9)}:"
            f"bordercolor=black:x=(w-text_w)/2:y={y}{extra}")


def fit(t):
    return min(110, int(960 / (len(t) * .64)))


for name, a, b, l1, l2 in SHORTS:
    d = b - a
    vf = (f"[0:v]split[bgsrc][fgsrc];"
          f"[bgsrc]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.18[bg];"
          f"[fgsrc]scale=1080:-2[fg];[bg][fg]overlay=0:620,"
          + dt(l1, 250, fit(l1)) + "," + dt(l2, 380, fit(l2), "0xFFC93C") + ","
          + "drawbox=x=90:y=1390:w=900:h=120:color=0xE63946@1:t=fill,"
          + dt("HISTORIA COMPLETA EN EL CANAL", 1422, 56) + ","
          + dt("¿QUÉ CREES TÚ? COMENTA", 1580, 64, "white", f":enable='gte(t,{d - 6:.1f})'")
          + f",fade=t=in:st=0:d=0.25,fade=t=out:st={d - .35:.2f}:d=0.35[v]")
    af = f"afade=t=in:st=0:d=0.2,afade=t=out:st={d - .5:.2f}:d=0.5"
    out = ROOT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(a), "-t", f"{d:.2f}", "-i", str(SRC),
                    "-filter_complex", vf, "-map", "[v]", "-map", "0:a", "-af", af, "-c:v", "libx264", "-crf", "19",
                    "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-r", "30", str(out)], check=True)
    print(out.name, f"{d:.1f}s")
