"""Corrector automático: mide el texto sin gastar API (extensión, ritmo, legibilidad, clichés, promesas, ortografía)."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from collections import Counter

from .modelos import Hallazgo
from .reglas import CLICHES, COMODINES, PROMESAS_RIESGO

_FRASE = re.compile(r"(?<=[.!?…])\s+(?=[¿¡«\"A-ZÁÉÍÓÚÑ0-9])")
_PALABRA = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:-[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*")
_VOCALES = re.compile(r"[aeiouáéíóúü]+", re.I)
_PASIVA = re.compile(r"\b(?:fue|fueron|es|son|será|serán|ha sido|han sido|había sido)\s+\w+(?:ado|ada|ados|adas|ido|ida|idos|idas)\b", re.I)

# palabras vacías que no cuentan como repeticiones
_VACIAS = set("""a al algo algún alguna algunas alguno algunos ante antes aquí así aun aún bien cada como con contra
cual cuando de del desde donde dos el él ella ellas ellos en entre era eres es esa esas ese eso esos esta está están
estas este esto estos fue fueron ha han hasta hay la las le les lo los más me mi mis mucho muy nada ni no nos o otra
otras otro otros para pero poco por porque que qué se sea según ser si sí sin sino sobre son su sus también tan te
tiene tienen todo todos tu tú tus un una unas uno unos vez y ya yo puede pueden hace hacer cómo eso ese""".split())


def palabras(texto: str) -> list[str]:
    return _PALABRA.findall(_limpiar_md(texto))


def contar_palabras(texto: str) -> int:
    return len(palabras(texto))


def _limpiar_md(texto: str) -> str:
    t = re.sub(r"```.*?```", " ", texto, flags=re.S)
    t = re.sub(r"^\s*\|.*$", " ", t, flags=re.M)          # tablas
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"^\s{0,3}(#{1,6}|>|[-*+]|\d+\.)\s*", "", t, flags=re.M)
    t = re.sub(r"[*_`|]", " ", t)
    return t


def _parrafos(texto: str) -> list[str]:
    bloques = [b.strip() for b in re.split(r"\n\s*\n", texto)]
    return [b for b in bloques if b and not re.match(r"^(#|>|[-*+] |\d+\. |\||```)", b)]


def frases(texto: str) -> list[str]:
    out: list[str] = []
    for p in _parrafos(texto):
        out += [f.strip() for f in _FRASE.split(_limpiar_md(p).replace("\n", " ")) if f.strip()]
    return out


def _silabas(palabra: str) -> int:
    return max(1, len(_VOCALES.findall(palabra)))


def fernandez_huerta(texto: str) -> float:
    """Legibilidad en español (0-100; 60-70 = normal, >70 = fácil, <50 = difícil)."""
    ps = palabras(texto)
    fs = frases(texto) or [texto]
    if not ps:
        return 0.0
    silabas_100 = 100 * sum(_silabas(p) for p in ps) / len(ps)
    frases_100 = 100 * len(fs) / len(ps)
    return round(206.84 - 0.60 * silabas_100 - 1.02 * frases_100, 1)


def _ortografia(texto: str) -> list[str]:
    """Palabras que Hunspell no reconoce (diccionario RAE; variante en EBOOK_DICCIONARIO, p. ej. es_MX)."""
    if not shutil.which("hunspell"):
        return []
    dic = os.getenv("EBOOK_DICCIONARIO", "es_ES")
    candidatas = "\n".join(p for p in palabras(texto) if p.islower() and len(p) > 3)
    r = subprocess.run(["hunspell", "-d", dic, "-l"], input=candidatas, capture_output=True, text=True)
    if r.returncode != 0:
        return []
    return sorted({w for w in r.stdout.split() if len(w) > 3})


def revisar_texto(texto: str, donde: str = "texto", palabras_objetivo: int | None = None,
                  prohibido: list[str] | None = None, ortografia: bool = True) -> list[Hallazgo]:
    hs: list[Hallazgo] = []
    low = texto.lower()
    n = contar_palabras(texto)

    # extensión
    if palabras_objetivo:
        desvio = (n - palabras_objetivo) / palabras_objetivo
        if desvio < -0.30:
            hs.append(Hallazgo(nivel="error", donde=donde, mensaje=f"Corto: {n} palabras de {palabras_objetivo} objetivo ({desvio:+.0%})."))
        elif desvio < -0.15 or desvio > 0.35:
            hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"Extensión {n} palabras frente a {palabras_objetivo} objetivo ({desvio:+.0%})."))

    # estructura Markdown
    if re.search(r"^# ", texto, flags=re.M):
        hs.append(Hallazgo(nivel="error", donde=donde, mensaje="Usa '#' dentro del capítulo; los subtítulos van con '##'."))
    if n > 1200 and not re.search(r"^## ", texto, flags=re.M):
        hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje="Más de 1200 palabras sin subtítulos '##': el lector se pierde."))

    # ritmo
    fs = frases(texto)
    largas = [f for f in fs if len(_PALABRA.findall(f)) > 40]
    for f in largas[:5]:
        hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"Frase de {len(_PALABRA.findall(f))} palabras: «{f[:90]}…»"))
    if fs:
        media = sum(len(_PALABRA.findall(f)) for f in fs) / len(fs)
        if media > 26:
            hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"Frases largas de media ({media:.0f} palabras); objetivo 12-22."))
    for p in _parrafos(texto):
        np_ = len(_PALABRA.findall(p))
        if np_ > 170:
            hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"Párrafo de {np_} palabras: divídelo. «{p[:70]}…»"))

    # legibilidad
    if n >= 150:
        fh = fernandez_huerta(texto)
        if fh < 50:
            hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"Legibilidad Fernández-Huerta {fh} (difícil). Apunta a 60-75."))
        else:
            hs.append(Hallazgo(nivel="info", donde=donde, mensaje=f"Legibilidad Fernández-Huerta {fh}."))

    # clichés y tono de IA
    for c in CLICHES:
        k = low.count(c)
        if k:
            hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"Cliché/tono de IA «{c}» ×{k}."))
    por_mil = max(1.0, n / 1000)
    for c in COMODINES:
        k = len(re.findall(rf"\b{re.escape(c)}\b", low))
        if k / por_mil > 2:
            hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"Palabra comodín «{c}» ×{k}: varía o elimina."))
    mente = len(re.findall(r"\b\w{4,}mente\b", low))
    if mente / por_mil > 8:
        hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"{mente} adverbios en -mente ({mente / por_mil:.0f} por 1000 palabras)."))
    pasivas = len(_PASIVA.findall(texto))
    if pasivas / por_mil > 6:
        hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"{pasivas} construcciones pasivas: prefiere la voz activa."))

    # repeticiones cercanas (misma palabra con contenido ≥ 3 veces en 60 palabras)
    ps = [p.lower() for p in palabras(texto)]
    vistos: set[str] = set()
    for i in range(0, max(1, len(ps) - 60), 30):
        ventana = Counter(p for p in ps[i:i + 60] if len(p) > 4 and p not in _VACIAS)
        for w, k in ventana.items():
            if k >= 3 and w not in vistos:
                vistos.add(w)
                hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"Repetición cercana: «{w}» ×{k} en pocas líneas."))

    # veracidad y cumplimiento
    for pr in PROMESAS_RIESGO:
        if pr in low:
            hs.append(Hallazgo(nivel="error", donde=donde, mensaje=f"Promesa/afirmación de riesgo «{pr.strip()}»: respáldala con un dato confirmado o elimínala."))
    for pr in prohibido or []:
        if pr and pr.lower() in low:
            hs.append(Hallazgo(nivel="error", donde=donde, mensaje=f"Usa algo prohibido por el brief: «{pr}»."))
    pend = re.findall(r"\[PENDIENTE[^\]]*\]", texto)
    if pend:
        hs.append(Hallazgo(nivel="info", donde=donde, mensaje=f"{len(pend)} marca(s) [PENDIENTE] por completar."))
    if re.search(r"https?://", texto):
        hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje="Contiene enlaces: verifica que existan (no inventar URL)."))
    if re.search(r"[\U0001F300-\U0001FAFF]", texto):
        hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje="Contiene emojis: no van en un libro."))

    # ortografía
    if ortografia:
        desconocidas = _ortografia(texto)
        if desconocidas:
            hs.append(Hallazgo(nivel="info", donde=donde, mensaje="Revisa ortografía: " + ", ".join(desconocidas[:25])))
    return hs


def resumen(hs: list[Hallazgo]) -> str:
    if not hs:
        return "Sin hallazgos."
    orden = {"error": 0, "aviso": 1, "info": 2}
    marca = {"error": "✖", "aviso": "!", "info": "·"}
    return "\n".join(f"{marca[h.nivel]} [{h.donde}] {h.mensaje}" for h in sorted(hs, key=lambda h: orden[h.nivel]))
