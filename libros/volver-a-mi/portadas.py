"""Portada y contraportada de «Volver a mí» con la identidad visual de Paola Velásquez (rosa, dorado, retrato circular).

    python libros/volver-a-mi/portadas.py
"""

from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = Path(__file__).parent
W, H = 1800, 2700
ROSA_CLARO, ROSA, FUCSIA, DORADO, CIRUELA = "#FFF3F7", "#F9CFDF", "#B5487E", "#B8913C", "#3A1F2B"
F = "/usr/share/fonts/truetype"


def fuente(nombre: str, tam: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(f"{F}/{nombre}", tam)


def fondo() -> Image.Image:
    grad = Image.linear_gradient("L").resize((W, H))
    return Image.composite(Image.new("RGB", (W, H), ROSA), Image.new("RGB", (W, H), ROSA_CLARO), grad)


def centrado(d: ImageDraw.ImageDraw, y: int, texto: str, f, color, tracking: int = 0) -> int:
    if tracking:
        anchos = [d.textlength(c, font=f) + tracking for c in texto]
        x = (W - sum(anchos) + tracking) / 2
        for c, a in zip(texto, anchos):
            d.text((x, y), c, font=f, fill=color)
            x += a
    else:
        d.text(((W - d.textlength(texto, font=f)) / 2, y), texto, font=f, fill=color)
    return y + f.size


def envolver(d, texto, f, ancho):
    out, linea = [], ""
    for p in texto.split():
        prueba = f"{linea} {p}".strip()
        if d.textlength(prueba, font=f) <= ancho:
            linea = prueba
        else:
            out.append(linea)
            linea = p
    return out + [linea]


def puntos(img: Image.Image, cx: int, cy: int, r: int, n: int = 140) -> None:
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    rnd = random.Random(7)
    for _ in range(n):
        ang = rnd.uniform(0, 6.283)
        dist = r + rnd.uniform(10, 110) * rnd.random()
        import math
        x, y = cx + dist * math.cos(ang), cy + dist * math.sin(ang)
        s = rnd.uniform(3, 13)
        alfa = rnd.randint(70, 200)
        color = (232, 120, 168, alfa) if rnd.random() < 0.8 else (184, 145, 60, alfa)
        d.ellipse((x - s, y - s, x + s, y + s), fill=color)
    img.paste(capa, (0, 0), capa)


def retrato(img: Image.Image, cx: int, cy: int, r: int) -> None:
    foto = Image.open(AQUI / "img" / "retrato.jpg").convert("RGB")
    lado = min(foto.size)
    foto = foto.crop(((foto.width - lado) // 2, 0, (foto.width - lado) // 2 + lado, lado)).resize((2 * r, 2 * r))
    mascara = Image.new("L", (2 * r, 2 * r), 0)
    ImageDraw.Draw(mascara).ellipse((0, 0, 2 * r, 2 * r), fill=255)
    sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).ellipse((cx - r - 10, cy - r + 14, cx + r + 10, cy + r + 34), fill=(120, 40, 80, 70))
    sombra = sombra.filter(ImageFilter.GaussianBlur(22))
    img.paste(sombra, (0, 0), sombra)
    img.paste(foto, (cx - r, cy - r), mascara)
    d = ImageDraw.Draw(img)
    d.ellipse((cx - r - 22, cy - r - 22, cx + r + 22, cy + r + 22), outline=DORADO, width=16)
    d.ellipse((cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4), outline="#FFFFFF", width=8)


def logo(img: Image.Image, cy: int, alto: int) -> None:
    lg = Image.open(AQUI / "img" / "logo.png").convert("RGBA")
    lg = lg.resize((int(lg.width * alto / lg.height), alto))
    img.paste(lg, ((W - lg.width) // 2, cy), lg)


def portada(salida: Path) -> Path:
    img = fondo()
    d = ImageDraw.Draw(img)
    centrado(d, 200, "VOLVER A MÍ", fuente("ebgaramond/EBGaramond12-Regular.ttf", 205), FUCSIA, tracking=10)
    centrado(d, 470, "Dios quiere restaurar tu corazón", fuente("ebgaramond/EBGaramond12-Italic.ttf", 104), DORADO)
    cx, cy, r = W // 2, 1180, 400
    puntos(img, cx, cy, r + 40)
    retrato(img, cx, cy, r)
    d = ImageDraw.Draw(img)
    y = 1740
    for linea in envolver(d, "Cómo dejar de perderte en tus relaciones y recuperar tu valor, tu voz y tu fe",
                          fuente("lato/Lato-Regular.ttf", 66), 1300):
        y = centrado(d, y, linea, fuente("lato/Lato-Regular.ttf", 66), CIRUELA) + 22
    y += 40
    centrado(d, y, "PSICOLOGÍA  ·  IDENTIDAD  ·  FE", fuente("lato/Lato-Bold.ttf", 40), FUCSIA, tracking=8)
    d.line((300, 2170, W - 300, 2170), fill=FUCSIA, width=4)
    centrado(d, 2215, "PAOLA VELÁSQUEZ", fuente("lato/Lato-Regular.ttf", 64), CIRUELA, tracking=14)
    logo(img, 2350, 260)
    img.save(salida, quality=93)
    return salida


def contraportada(salida: Path) -> Path:
    img = fondo().transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    d = ImageDraw.Draw(img)
    m = 190
    d.line((m, 230, m + 160, 230), fill=DORADO, width=10)
    d.text((m, 280), "VOLVER A MÍ", font=fuente("ebgaramond/EBGaramond12-Regular.ttf", 120), fill=FUCSIA)
    y = 470
    frase = fuente("ebgaramond/EBGaramond12-Italic.ttf", 82)
    for linea in envolver(d, "«No tengo que perderme para demostrar que amo.»", frase, W - 2 * m):
        d.text((m, y), linea, font=frase, fill=DORADO)
        y += 96
    y += 50
    cuerpo = fuente("lato/Lato-Regular.ttf", 50)
    texto = (AQUI / "contraportada.txt").read_text(encoding="utf-8").split("\n")
    for p in [t for t in texto if t.strip()]:
        for linea in envolver(d, p, cuerpo, W - 2 * m):
            d.text((m, y), linea, font=cuerpo, fill=CIRUELA)
            y += 70
        y += 40
    d.line((m, H - 470, W - m, H - 470), fill=FUCSIA, width=3)
    foto = Image.open(AQUI / "img" / "retrato.jpg").convert("RGB").resize((230, 230))
    mascara = Image.new("L", (230, 230), 0)
    ImageDraw.Draw(mascara).ellipse((0, 0, 230, 230), fill=255)
    img.paste(foto, (m, H - 410), mascara)
    d.ellipse((m - 8, H - 418, m + 238, H - 172), outline=DORADO, width=8)
    d.text((m + 290, H - 390), "PAOLA VELÁSQUEZ", font=fuente("lato/Lato-Bold.ttf", 58), fill=CIRUELA)
    d.text((m + 290, H - 315), "Psicóloga · Creadora del Programa Mujer de Fortaleza",
           font=fuente("lato/Lato-Regular.ttf", 40), fill=CIRUELA)
    d.text((m + 290, H - 245), "paolavelasquez.com  ·  @terapeutacristianapaola",
           font=fuente("lato/Lato-Regular.ttf", 40), fill=FUCSIA)
    img.save(salida, quality=93)
    return salida


if __name__ == "__main__":
    (AQUI / "portadas").mkdir(exist_ok=True)
    print(portada(AQUI / "portadas" / "portada.jpg"))
    print(contraportada(AQUI / "portadas" / "contraportada.jpg"))
