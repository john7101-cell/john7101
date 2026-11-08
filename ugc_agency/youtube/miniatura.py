"""Miniaturas 1280x720 legibles en móvil: imagen de fondo, texto grande con contorno y acento de color."""

from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ANCHO, ALTO = 1280, 720
FUENTES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf",
]


def _fuente(tam: int, preferida: str | None = None) -> ImageFont.FreeTypeFont:
    for f in ([preferida] if preferida else []) + FUENTES:
        if f and Path(f).exists():
            return ImageFont.truetype(f, tam)
    return ImageFont.load_default()


def cuadro_de_video(video: Path, segundo: float, salida: Path) -> Path:
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(segundo), "-i", str(video), "-frames:v", "1", str(salida)], check=True)
    return salida


def _cubrir(im: Image.Image, foco_y: float = 0.22) -> Image.Image:
    """Recorta a 16:9. En imágenes verticales prioriza la parte alta (donde suele estar la cara)."""
    escala = max(ANCHO / im.width, ALTO / im.height)
    im = im.resize((round(im.width * escala), round(im.height * escala)), Image.LANCZOS)
    x, y = (im.width - ANCHO) // 2, int((im.height - ALTO) * foco_y)
    return im.crop((x, y, x + ANCHO, y + ALTO))


def crear(fondo: Path, lineas: list[str], salida: Path, acento: str = "#F8CB12", color_texto: str = "#FFFFFF",
          lado: str = "izquierda", etiqueta: str | None = None, fuente: str | None = None,
          foco_y: float = 0.22) -> Path:
    """`lineas`: 1-3 líneas cortas (≤14 letras). La línea con *asteriscos* sale en el color de acento."""
    if not 1 <= len(lineas) <= 3:
        raise ValueError("Usa entre 1 y 3 líneas de texto: en una miniatura se lee poco texto.")
    fuente_img = Image.open(fondo).convert("RGB")
    if fuente_img.height > fuente_img.width:
        # Fuente vertical (reel): fondo desenfocado + retrato nítido de alto completo en el lado opuesto al texto
        base = _cubrir(fuente_img, 0.3).filter(ImageFilter.GaussianBlur(28))
        base = Image.blend(base, Image.new("RGB", base.size, (5, 8, 20)), 0.35)
        h = ALTO
        w = round(fuente_img.width * h / fuente_img.height)
        retrato = fuente_img.resize((w, h), Image.LANCZOS)
        base.paste(retrato, (ANCHO - w if lado == "izquierda" else 0, 0))
    else:
        base = _cubrir(fuente_img, foco_y)
    # Degradado oscuro del lado del texto para garantizar contraste
    grad = Image.new("L", (ANCHO, ALTO))
    gd = ImageDraw.Draw(grad)
    for x in range(ANCHO):
        frac = x / ANCHO if lado == "derecha" else 1 - x / ANCHO
        gd.line([(x, 0), (x, ALTO)], fill=int(215 * max(0.0, frac - 0.15) / 0.85))
    negro = Image.new("RGB", (ANCHO, ALTO), (5, 8, 20))
    img = Image.composite(negro, base, grad)
    d = ImageDraw.Draw(img)
    margen = 60
    zona = ANCHO * 0.58
    y = ALTO // 2 - (len(lineas) * 150) // 2
    for linea in lineas:
        destacada = linea.startswith("*") and linea.endswith("*")
        txt = linea.strip("*").upper()
        tam = 170
        while tam > 60 and d.textlength(txt, font=_fuente(tam, fuente)) > zona:
            tam -= 6
        f = _fuente(tam, fuente)
        w = d.textlength(txt, font=f)
        x = margen if lado == "izquierda" else ANCHO - margen - w
        if destacada:
            alto = f.getbbox(txt)[3]
            d.rounded_rectangle([x - 18, y - 4, x + w + 18, y + alto + 18], radius=18, fill=acento)
            d.text((x, y), txt, font=f, fill="#0B1B33")
        else:
            d.text((x, y), txt, font=f, fill=color_texto, stroke_width=max(4, tam // 22), stroke_fill="#000000")
        y += int(tam * 1.08)
    if etiqueta:
        f = _fuente(44, fuente)
        w = d.textlength(etiqueta.upper(), font=f)
        x = ANCHO - margen - w - 30 if lado == "izquierda" else margen
        d.rounded_rectangle([x, 40, x + w + 40, 112], radius=16, fill=acento)
        d.text((x + 20, 50), etiqueta.upper(), font=f, fill="#0B1B33")
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=60))
    salida.parent.mkdir(parents=True, exist_ok=True)
    calidad = 92
    while True:
        img.save(salida, "JPEG", quality=calidad, optimize=True)
        if salida.stat().st_size < 2 * 1024 * 1024 or calidad < 60:  # límite de YouTube: 2 MB
            break
        calidad -= 6
    return salida


def crear_con_personaje(pose: Path, lineas: list[str], salida: Path, fondo=(17, 22, 58), fondo2=(30, 40, 100),
                        acento: str = "#FFC23C", etiqueta: str | None = None, fuente: str | None = None) -> Path:
    """Miniatura de marca: personaje recortado (PNG con transparencia) a la derecha y texto grande a la izquierda."""
    if not 1 <= len(lineas) <= 3:
        raise ValueError("Usa entre 1 y 3 líneas de texto.")
    img = Image.new("RGB", (ANCHO, ALTO), fondo)
    d = ImageDraw.Draw(img)
    for r in range(900, 0, -6):  # halo detrás del personaje para separarlo del fondo
        t = 1 - r / 900
        d.ellipse([ANCHO * 0.74 - r, ALTO * 0.55 - r, ANCHO * 0.74 + r, ALTO * 0.55 + r],
                  fill=tuple(int(fondo[i] + (fondo2[i] - fondo[i]) * t) for i in range(3)))
    p = Image.open(pose).convert("RGBA")
    alto = int(ALTO * 1.02)
    p = p.resize((int(p.width * alto / p.height), alto), Image.LANCZOS)
    x = ANCHO - p.width + int(p.width * 0.08)
    borde = Image.new("RGBA", p.size, (255, 255, 255, 0))
    borde.putalpha(p.split()[3].point(lambda v: 255 if v > 10 else 0).filter(ImageFilter.MaxFilter(13)))
    blanco = Image.new("RGBA", p.size, (255, 255, 255, 255))
    blanco.putalpha(borde.split()[3])
    img.paste(blanco, (x, ALTO - p.height + 10), blanco)          # contorno blanco tipo sticker
    img.paste(p, (x, ALTO - p.height + 10), p)
    d = ImageDraw.Draw(img)
    zona = ANCHO * 0.56
    y = ALTO // 2 - (len(lineas) * 165) // 2
    for linea in lineas:
        destacada = linea.startswith("*") and linea.endswith("*")
        txt = linea.strip("*").upper()
        tam = 180
        while tam > 60 and d.textlength(txt, font=_fuente(tam, fuente)) > zona:
            tam -= 6
        f = _fuente(tam, fuente)
        w = d.textlength(txt, font=f)
        if destacada:
            alto_t = f.getbbox(txt)[3]
            d.rounded_rectangle([46, y - 4, 46 + w + 36, y + alto_t + 20], radius=20, fill=acento)
            d.text((64, y), txt, font=f, fill=fondo)
        else:
            d.text((60, y), txt, font=f, fill="#FFFFFF", stroke_width=max(4, tam // 24), stroke_fill="#000000")
        y += int(tam * 1.1)
    if etiqueta:
        f = _fuente(46, fuente)
        w = d.textlength(etiqueta.upper(), font=f)
        d.rounded_rectangle([50, 40, 50 + w + 40, 112], radius=16, fill="#FF3B3B")
        d.text((70, 50), etiqueta.upper(), font=f, fill="#FFFFFF")
    salida.parent.mkdir(parents=True, exist_ok=True)
    img.save(salida, "JPEG", quality=92, optimize=True)
    return salida
