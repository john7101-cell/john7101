"""Maquetador: manuscrito Markdown → EPUB 3 (Kindle/Apple/Kobo), PDF de imprenta (KDP tapa blanda) y portadas.

Herramientas: Pandoc (EPUB y conversión a Typst), Typst (PDF tipográfico), Pillow (portada ebook)
y EPUBCheck (validación, si está instalado). Ver scripts/instalar_ebooks.sh.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import textwrap
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

PLANTILLAS = Path(__file__).with_name("plantillas")

# Tamaños de corte habituales de KDP (pulgadas) y grosor de página para el lomo
TAMANOS = {"6x9": (6.0, 9.0), "5.5x8.5": (5.5, 8.5), "5x8": (5.0, 8.0), "8.5x11": (8.5, 11.0)}
GROSOR_PAGINA = {"blanco": 0.002252, "crema": 0.0025}


@dataclass
class Seccion:
    titulo: str
    cuerpo: str
    numerada: bool = True


@dataclass
class Manuscrito:
    titulo: str
    subtitulo: str = ""
    autor: str = ""
    idioma: str = "es"
    meta: dict = field(default_factory=dict)
    secciones: list[Seccion] = field(default_factory=list)


def leer_manuscrito(ruta: str | Path) -> Manuscrito:
    """Lee un Markdown con front matter YAML; cada '# Título' es un capítulo ('{.unnumbered}' = sin número)."""
    texto = Path(ruta).read_text(encoding="utf-8")
    meta: dict = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", texto, flags=re.S)
    if m:
        import yaml
        meta = yaml.safe_load(m.group(1)) or {}
        texto = texto[m.end():]
    secciones: list[Seccion] = []
    partes = re.split(r"^# (.+)$", texto, flags=re.M)
    if partes[0].strip():
        secciones.append(Seccion("", partes[0].strip(), numerada=False))
    for i in range(1, len(partes), 2):
        tit = partes[i].strip()
        numerada = not re.search(r"\{[^}]*(\.unnumbered|-)[^}]*\}\s*$", tit)
        tit = re.sub(r"\s*\{[^}]*\}\s*$", "", tit)
        secciones.append(Seccion(tit, partes[i + 1].strip(), numerada))
    return Manuscrito(titulo=str(meta.get("title", Path(ruta).stem)), subtitulo=str(meta.get("subtitle", "") or ""),
                      autor=str(meta.get("author", "") or ""), idioma=str(meta.get("lang", "es")), meta=meta,
                      secciones=secciones)


def _pandoc(args: list[str], entrada: str | None = None) -> str:
    if not shutil.which("pandoc"):
        raise RuntimeError("Falta Pandoc. Ejecuta scripts/instalar_ebooks.sh (o apt-get install pandoc).")
    r = subprocess.run(["pandoc", *args], input=entrada, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Pandoc falló: {r.stderr}")
    return r.stdout


# ------------------------------------------------------------------ EPUB
def _pagina_creditos(ms: Manuscrito) -> str:
    anio = ms.meta.get("year", date.today().year)
    lineas = [f"© {anio} {ms.autor or '[PENDIENTE: autor]'}. Todos los derechos reservados.", "",
              "Ninguna parte de esta publicación puede reproducirse, almacenarse o transmitirse por ningún medio "
              "sin el permiso previo y por escrito del autor, salvo citas breves en reseñas.", ""]
    if ms.meta.get("isbn"):
        lineas += [f"ISBN: {ms.meta['isbn']}", ""]
    lineas += [str(ms.meta.get("disclaimer") or
               "Este libro tiene fines informativos y educativos. No sustituye el consejo de un profesional "
               "cualificado. El autor no se hace responsable del uso que se haga de la información."), ""]
    return "\n".join(lineas)


def construir_epub(ms: Manuscrito, ruta_md: Path, salida: Path, portada: Path | None = None,
                   css: Path | None = None, incrustar_fuentes: bool = False) -> Path:
    css = css or PLANTILLAS / "epub.css"
    cuerpo = ["# Créditos {.unnumbered .unlisted .creditos}", "", _pagina_creditos(ms), ""]
    n = 0
    for s in ms.secciones:
        if not s.titulo:
            cuerpo += [s.cuerpo, ""]
            continue
        if s.numerada:
            n += 1
            cuerpo += [f"# {s.titulo} {{.capitulo data-numero=\"{n}\"}}", ""]
        else:
            cuerpo += [f"# {s.titulo} {{.unnumbered}}", ""]
        cuerpo += [s.cuerpo, ""]
    meta = {"title": ms.titulo, "subtitle": ms.subtitulo, "author": ms.autor, "lang": ms.idioma,
            "rights": f"© {ms.meta.get('year', date.today().year)} {ms.autor}",
            "date": str(ms.meta.get("date", date.today().isoformat())),
            "description": ms.meta.get("description") or ms.subtitulo}
    meta = {k: v for k, v in meta.items() if v}      # EPUBCheck rechaza metadatos vacíos
    if ms.meta.get("isbn"):
        meta["identifier"] = [{"scheme": "ISBN", "text": str(ms.meta["isbn"])}]
    tmp = salida.with_suffix(".tmp.md")
    tmp.write_text("---\n" + json.dumps(meta, ensure_ascii=False) + "\n---\n\n" + "\n".join(cuerpo), encoding="utf-8")
    args = [str(tmp), "-f", "markdown+smart-citations", "-t", "epub3", "-o", str(salida), "--toc", "--toc-depth=1",
            "--split-level=1", f"--css={css}", f"--resource-path={ruta_md.parent}",
            "--metadata", "toc-title=Índice"]
    if portada:
        args.append(f"--epub-cover-image={portada}")
    if incrustar_fuentes:
        for f in ("EBGaramond12-Regular", "EBGaramond12-Italic", "EBGaramond12-Bold"):
            p = Path(f"/usr/share/fonts/opentype/ebgaramond/{f}.otf")
            if p.exists():
                args.append(f"--epub-embed-font={p}")
    try:
        _pandoc(args)
    finally:
        tmp.unlink(missing_ok=True)
    return salida


def validar_epub(ruta: Path) -> tuple[bool, str]:
    """Valida con EPUBCheck (el mismo validador que usan Apple, Kobo y Google). Devuelve (ok, informe)."""
    cmd = ["epubcheck"] if shutil.which("epubcheck") else None
    if cmd is None:
        return True, "EPUBCheck no está instalado: validación omitida (scripts/instalar_ebooks.sh)."
    r = subprocess.run([*cmd, str(ruta), "-q"], capture_output=True, text=True)
    salida = "\n".join(l for l in (r.stdout + r.stderr).splitlines() if not l.startswith("Picked up JAVA"))
    return r.returncode == 0, salida.strip() or "EPUBCheck: sin errores ni avisos."


# ------------------------------------------------------------------ PDF (Typst)
def _a_typst(md: str) -> str:
    return _pandoc(["-f", "markdown+smart-citations", "-t", "typst", "--wrap=none"], md)


def _esc_typst(s: str) -> str:
    return re.sub(r"([\\#\[\]*_`$<>@])", r"\\\1", s)


def construir_pdf(ms: Manuscrito, salida: Path, tamano: str = "6x9", fuente: str = "EB Garamond",
                  cuerpo_pt: float = 11.0, sangrado: bool = False) -> Path:
    try:
        import typst
    except ImportError as e:
        raise RuntimeError("Falta Typst: pip install typst") from e
    ancho, alto = TAMANOS[tamano]
    caps = []
    n = 0
    for s in ms.secciones:
        if not s.titulo:
            continue
        cuerpo = _a_typst(s.cuerpo)
        if s.numerada:
            n += 1
            caps.append(f"#capitulo(numero: {n}, titulo: [{_esc_typst(s.titulo)}])\n\n{cuerpo}")
        else:
            caps.append(f"#capitulo(titulo: [{_esc_typst(s.titulo)}])\n\n{cuerpo}")
    plantilla = (PLANTILLAS / "libro.typ").read_text(encoding="utf-8")
    datos = {
        "titulo": ms.titulo, "subtitulo": ms.subtitulo, "autor": ms.autor or "[PENDIENTE: autor]",
        "creditos": _pagina_creditos(ms), "ancho": f"{ancho + (0.125 if sangrado else 0)}in",
        "alto": f"{alto + (0.25 if sangrado else 0)}in", "fuente": fuente, "cuerpo": f"{cuerpo_pt}pt",
        "idioma": ms.idioma[:2],
    }
    for k, v in datos.items():
        plantilla = plantilla.replace("{{" + k + "}}", _esc_typst(v) if k in ("titulo", "subtitulo", "autor", "creditos") else v)
    fuente_typ = salida.with_suffix(".typ")
    fuente_typ.write_text(plantilla + "\n\n" + "\n\n".join(caps) + "\n", encoding="utf-8")
    typst.compile(str(fuente_typ), output=str(salida), root=str(salida.parent))
    return salida


def contar_paginas_pdf(ruta: Path) -> int:
    datos = ruta.read_bytes()
    m = re.findall(rb"/Type\s*/Pages\b[^>]*?/Count\s+(\d+)", datos)
    return max((int(x) for x in m), default=0) or len(re.findall(rb"/Type\s*/Page\b", datos))


# ------------------------------------------------------------------ portadas
def _fuente(nombre: str, tam: int):
    from PIL import ImageFont
    rutas = {
        "titulo": ["/usr/share/fonts/truetype/lato/Lato-Black.ttf", "/usr/share/fonts/opentype/inter/Inter-Black.otf"],
        "texto": ["/usr/share/fonts/truetype/lato/Lato-Regular.ttf", "/usr/share/fonts/opentype/inter/Inter-Regular.otf"],
        "serif": ["/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Italic.ttf"],
    }
    for r in rutas[nombre]:
        if Path(r).exists():
            return ImageFont.truetype(r, tam)
    return ImageFont.load_default(tam)


def _envolver(draw, texto: str, fuente, ancho_max: int) -> list[str]:
    palabras, lineas, actual = texto.split(), [], ""
    for p in palabras:
        prueba = f"{actual} {p}".strip()
        if draw.textlength(prueba, font=fuente) <= ancho_max:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas


PALETAS = {
    "noche": ("#0F1B2D", "#1F3A5F", "#F4C95D", "#FFFFFF"),
    "bosque": ("#0E2A22", "#1E5245", "#E9C46A", "#FFFFFF"),
    "terracota": ("#5A2A1B", "#B5562F", "#F6E7CB", "#FFFFFF"),
    "papel": ("#F3EEE4", "#E4DACA", "#C0392B", "#1B1B1B"),
    "vino": ("#3B0D1C", "#6E1B33", "#F2D0A4", "#FFFFFF"),
}


def portada_ebook(titulo: str, subtitulo: str, autor: str, salida: Path, paleta: str = "noche",
                  frase: str = "", imagen: Path | None = None) -> Path:
    """Portada 1600×2560 (proporción 1:1.6 recomendada por KDP). Legible en miniatura: título grande y alto contraste."""
    from PIL import Image, ImageDraw, ImageFilter

    W, H = 1600, 2560
    fondo, fondo2, acento, tinta = PALETAS.get(paleta, PALETAS["noche"])
    img = Image.new("RGB", (W, H), fondo)
    if imagen:
        foto = Image.open(imagen).convert("RGB")
        r = max(W / foto.width, H / foto.height)
        foto = foto.resize((int(foto.width * r) + 1, int(foto.height * r) + 1))
        foto = foto.crop(((foto.width - W) // 2, (foto.height - H) // 2, (foto.width - W) // 2 + W, (foto.height - H) // 2 + H))
        img.paste(foto)
        velo = Image.new("RGB", (W, H), fondo)
        mascara = Image.linear_gradient("L").resize((W, H)).point(lambda v: int(60 + v * 0.65))
        img = Image.composite(velo, img, mascara.transpose(Image.Transpose.FLIP_TOP_BOTTOM))
    else:
        grad = Image.linear_gradient("L").resize((W, H))
        img = Image.composite(Image.new("RGB", (W, H), fondo2), img, grad)
        deco = Image.new("L", (W, H), 0)
        ImageDraw.Draw(deco).ellipse((W * 0.35, -H * 0.12, W * 1.45, H * 0.45), fill=70)
        img = Image.composite(Image.new("RGB", (W, H), acento), img, deco.filter(ImageFilter.GaussianBlur(40)))

    d = ImageDraw.Draw(img)
    margen = 130
    y = int(H * 0.40)
    d.rectangle((margen, y - 70, margen + 180, y - 52), fill=acento)
    tam = 230 if len(titulo) < 18 else 190 if len(titulo) < 32 else 150
    ft = _fuente("titulo", tam)
    for linea in _envolver(d, titulo.upper(), ft, W - 2 * margen):
        d.text((margen, y), linea, font=ft, fill=tinta)
        y += int(tam * 1.02)
    if subtitulo:
        y += 50
        fs = _fuente("texto", 68)
        for linea in _envolver(d, subtitulo, fs, W - 2 * margen)[:5]:
            d.text((margen, y), linea, font=fs, fill=tinta)
            y += 88
    if frase:
        fq = _fuente("serif", 66)
        d.text((margen, H - 430), frase, font=fq, fill=acento)
    fa = _fuente("texto", 80)
    d.text((margen, H - 250), (autor or "").upper(), font=fa, fill=tinta)
    salida.parent.mkdir(parents=True, exist_ok=True)
    img.save(salida, quality=92)
    return salida


def portada_tapa_blanda(portada: Path, contraportada: str, titulo: str, autor: str, paginas: int, salida: Path,
                        tamano: str = "6x9", papel: str = "blanco", paleta: str = "noche") -> tuple[Path, float]:
    """Cubierta completa para KDP tapa blanda (contra + lomo + portada, 0.125 in de sangrado) a 300 ppp."""
    from PIL import Image, ImageDraw

    ancho, alto = TAMANOS[tamano]
    lomo = paginas * GROSOR_PAGINA[papel]
    dpi = 300
    W = round((ancho * 2 + lomo + 0.25) * dpi)
    H = round((alto + 0.25) * dpi)
    fondo, _, acento, tinta = PALETAS.get(paleta, PALETAS["noche"])
    lienzo = Image.new("RGB", (W, H), fondo)
    frente_w = round((ancho + 0.125) * dpi)
    frente = Image.open(portada).convert("RGB").resize((frente_w, H))
    lienzo.paste(frente, (W - frente_w, 0))
    d = ImageDraw.Draw(lienzo)
    # contraportada
    m = round(0.6 * dpi)
    ft = _fuente("texto", 44)
    y = m + 80
    for parrafo in contraportada.split("\n"):
        for linea in _envolver(d, parrafo, ft, round(ancho * dpi) - 2 * m):
            d.text((m + round(0.125 * dpi), y), linea, font=ft, fill=tinta)
            y += 64
        y += 30
    d.rectangle((W - frente_w - round(lomo * dpi) - round(2.2 * dpi), H - round(1.6 * dpi),
                 W - frente_w - round(lomo * dpi) - round(0.4 * dpi), H - round(0.4 * dpi)), outline=acento, width=4)
    # lomo (solo con texto si hay > 79 páginas, regla de KDP)
    if paginas > 79:
        lomo_px = round(lomo * dpi)
        tira = Image.new("RGB", (H, lomo_px), fondo)
        dl = ImageDraw.Draw(tira)
        tam = max(20, int(lomo_px * 0.45))
        fl = _fuente("titulo", tam)
        texto = f"{titulo.upper()}   ·   {autor.upper()}"
        tw = dl.textlength(texto, font=fl)
        dl.text(((H - tw) / 2, (lomo_px - tam) / 2 - tam * 0.15), texto, font=fl, fill=tinta)
        lienzo.paste(tira.rotate(-90, expand=True), (W - frente_w - lomo_px, 0))
    lienzo.save(salida, "PDF", resolution=dpi)
    return salida, lomo


# ------------------------------------------------------------------ todo junto
def maquetar(ruta_md: str | Path, salida: str | Path, portada: str | Path | None = None, tamano: str = "6x9",
             paleta: str = "noche", frase: str = "", imagen: str | Path | None = None, contraportada: str = "",
             formatos: tuple[str, ...] = ("epub", "pdf"), incrustar_fuentes: bool = False) -> dict:
    ruta_md = Path(ruta_md)
    out = Path(salida)
    out.mkdir(parents=True, exist_ok=True)
    ms = leer_manuscrito(ruta_md)
    base = re.sub(r"[^a-z0-9]+", "-", ms.titulo.lower()).strip("-")[:60] or "libro"
    rep: dict = {"titulo": ms.titulo, "capitulos": sum(1 for s in ms.secciones if s.titulo)}

    p_portada = Path(portada) if portada else portada_ebook(ms.titulo, ms.subtitulo, ms.autor, out / "portada.jpg",
                                                              paleta, frase, Path(imagen) if imagen else None)
    rep["portada"] = str(p_portada)
    if "epub" in formatos:
        epub = construir_epub(ms, ruta_md, out / f"{base}.epub", p_portada, incrustar_fuentes=incrustar_fuentes)
        ok, informe = validar_epub(epub)
        rep.update(epub=str(epub), epub_valido=ok, epubcheck=informe)
    if "pdf" in formatos:
        pdf = construir_pdf(ms, out / f"{base}-interior-{tamano}.pdf", tamano)
        paginas = contar_paginas_pdf(pdf)
        rep.update(pdf=str(pdf), paginas=paginas)
        if paginas >= 24:      # mínimo de KDP para tapa blanda
            texto = contraportada or ms.meta.get("description", "") or ms.subtitulo
            cub, lomo = portada_tapa_blanda(p_portada, texto, ms.titulo, ms.autor, paginas,
                                            out / f"{base}-cubierta-{tamano}.pdf", tamano, paleta=paleta)
            rep.update(cubierta=str(cub), lomo_in=round(lomo, 3))
        else:
            rep["cubierta"] = f"No generada: {paginas} páginas (KDP pide mínimo 24 para tapa blanda)."
    (out / "maquetacion.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    return rep


def resumen_maquetacion(rep: dict) -> str:
    l = [f"«{rep['titulo']}» — {rep['capitulos']} capítulos", f"  Portada: {rep['portada']}"]
    if "epub" in rep:
        l.append(f"  EPUB:    {rep['epub']}  ({'válido' if rep['epub_valido'] else 'CON ERRORES'})")
        if not rep["epub_valido"]:
            l.append(textwrap.indent(rep["epubcheck"][:2000], "    "))
    if "pdf" in rep:
        l.append(f"  PDF:     {rep['pdf']}  ({rep['paginas']} páginas)")
        l.append(f"  Cubierta: {rep['cubierta']}" + (f"  (lomo {rep['lomo_in']} in)" if "lomo_in" in rep else ""))
    return "\n".join(l)
