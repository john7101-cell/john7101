"""Revisiones automáticas de un guion (sin IA): duración, repeticiones, datos inventados, promesas, género."""

from __future__ import annotations

import re
import unicodedata

from .modelos import GuionBrief, Hallazgo

PALABRAS_POR_S = 2.8        # ritmo oral con voz cálida; las pausas se suman aparte
PAUSA_FRASE_S = 0.2         # cierre de frase
PAUSA_DRAMATICA_S = 0.3     # "…" o [pausa]
MAX_PALABRAS_TOMA = 20
MAX_PALABRAS_GANCHO = 16
MAX_PALABRAS_FRASE = 22
TOLERANCIA_S = 0.4          # la estimación es aproximada: error solo si se pasa por más de esto

MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "setiembre", "octubre", "noviembre", "diciembre")

PROMESAS = [
    r"\bcura(r|rte|rse|rá|rás|mos)?\b", r"\bsana(r|rte|rse|rá|rás)\b", r"garantiz\w+", r"\b100\s?%",
    r"te aseguro", r"resultados? (inmediatos?|garantizados?|seguros?)", r"\bdiagn[oó]stic\w+",
    r"\bsuperar[aá]s\b", r"\bdejar[aá]s de (sufrir|depender)\b", r"\belimin\w+ (la |tu )?(ansiedad|depresi[oó]n|dependencia)",
    r"\btratamiento\b", r"\bterapia (te|que) (cura|sana)\b",
]
GENERO_MARCADO = [
    r"\bmujer(es)?\b", r"\bhombres?\b", r"\bellas?\b", r"\bellos?\b", r"\bsolas\b", r"\bsolos\b",
    r"\bbienvenid[ao]s?\b", r"\btod[ao]s\b", r"\bamig[ao]s\b", r"\bse[ñn]oras?\b", r"\bchic[ao]s\b",
    r"\bcansad[ao]s?\b", r"\bcompletas?\b", r"\bperdid[ao]s?\b",
]


def _sin_etiquetas(texto: str) -> str:
    return re.sub(r"\[[^\]]*\]", " ", texto)


def _norm(t: str) -> str:
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def _palabras(texto: str) -> list[str]:
    return re.findall(r"[\wáéíóúüñÁÉÍÓÚÜÑ]+(?:[-'][\wáéíóúüñ]+)*", _sin_etiquetas(texto))


def estimar_segundos(voz: str) -> float:
    """Estimación de lo que dura una toma hablada (calibrada con clips reales de ~7-8 s)."""
    limpio = _sin_etiquetas(voz)
    n = len(_palabras(limpio))
    frases = len(re.findall(r"[.?!]+(?=\s|$)", limpio))
    dramaticas = limpio.count("…") + limpio.count("...") + len(re.findall(r"\[\s*pausa", voz, re.I))
    return n / PALABRAS_POR_S + frases * PAUSA_FRASE_S + dramaticas * PAUSA_DRAMATICA_S


def revisar_tomas(tomas: list[tuple[int, str]], brief: GuionBrief | None = None) -> list[Hallazgo]:
    """`tomas` = [(numero, texto_de_voz)]. Devuelve hallazgos ordenados por gravedad."""
    brief = brief or GuionBrief(tema="(sin brief)")
    hs: list[Hallazgo] = []
    total = 0.0
    todo_norm = []
    for num, voz in tomas:
        limpio = _sin_etiquetas(voz)
        pal = _palabras(limpio)
        seg = estimar_segundos(voz)
        total += seg
        donde = f"toma {num}"
        if seg > brief.toma_max_s + TOLERANCIA_S:
            hs.append(Hallazgo(nivel="error", donde=donde,
                               mensaje=f"Dura ~{seg:.1f} s y el máximo es {brief.toma_max_s:g} s ({len(pal)} palabras). Recorta o divide."))
        elif seg > brief.toma_max_s - 0.5:
            hs.append(Hallazgo(nivel="aviso", donde=donde,
                               mensaje=f"Dura ~{seg:.1f} s, casi el límite de {brief.toma_max_s:g} s; si el clip sale largo habrá que acelerar la voz."))
        if len(pal) > MAX_PALABRAS_TOMA:
            hs.append(Hallazgo(nivel="error", donde=donde, mensaje=f"{len(pal)} palabras; en un clip de 8 s no deben pasar de {MAX_PALABRAS_TOMA}."))
        for frase in re.split(r"(?<=[.?!…])\s+", limpio.strip()):
            n = len(_palabras(frase))
            if n > MAX_PALABRAS_FRASE:
                hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"Frase de {n} palabras; en voz alta se pierde. Pártela."))
        if len(_sin_etiquetas(voz).strip()) and not re.search(r"[.?!…]\s*$", limpio.strip()):
            hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje="La toma no termina en una frase redonda (. ? ! …): riesgo de corte a mitad de idea."))
        if re.search(r"\b\d[\d\s.\-]{6,}\d\b", limpio):
            hs.append(Hallazgo(nivel="error", donde=donde, mensaje="Hay un teléfono/número largo en la voz. Va en pantalla; la voz solo dice la acción."))
        if re.search(r"https?://|www\.|\.com\b|@\w+", limpio):
            hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje="URL o usuario en la voz: mejor en pantalla."))
        for pat in PROMESAS:
            m = re.search(pat, _norm(limpio))
            if m:
                hs.append(Hallazgo(nivel="error", donde=donde, mensaje=f"Posible promesa o diagnóstico: «{m.group(0)}». Reformula como invitación."))
        if brief.genero_neutro:
            for pat in GENERO_MARCADO:
                m = re.search(pat, _norm(limpio))
                if m:
                    hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"Forma de género marcada «{m.group(0)}» y el brief pide neutralidad."))
        for pat in brief.prohibido:
            if pat and _norm(pat) in _norm(limpio):
                hs.append(Hallazgo(nivel="error", donde=donde, mensaje=f"Usa algo prohibido por el brief: «{pat}»."))
        for d in brief.en_pantalla:
            valor = d.split(":", 1)[-1].strip()
            solo_digitos = re.sub(r"\D", "", valor)
            if (len(solo_digitos) >= 7 and solo_digitos in re.sub(r"\D", "", limpio)) or (valor and len(valor) > 6 and _norm(valor) in _norm(limpio)):
                hs.append(Hallazgo(nivel="error", donde=donde, mensaje=f"«{valor}» está marcado como dato de pantalla pero se dice en voz."))
        # datos no confirmados: cifras y meses que no aparecen en el brief
        conocido = _norm(" ".join(brief.datos_confirmados + brief.en_pantalla + [brief.material, brief.notas, brief.tema]))
        numeros_conocidos = set(re.findall(r"\b\d+\b", conocido))       # números completos, no subcadenas ("15" no está en "315")
        for m in re.finditer(r"\b\d+\b", limpio):
            if m.group(0) not in numeros_conocidos:
                hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"La cifra «{m.group(0)}» no aparece en el brief confirmado."))
        for mes in MESES:
            if re.search(rf"\b{mes}\b", _norm(limpio)) and mes not in conocido:
                hs.append(Hallazgo(nivel="aviso", donde=donde, mensaje=f"Menciona «{mes}» y ese mes no está en los datos confirmados."))
        todo_norm.append((num, _norm(limpio)))
    if tomas:
        g = len(_palabras(tomas[0][1]))
        if g > MAX_PALABRAS_GANCHO:
            hs.append(Hallazgo(nivel="aviso", donde="gancho", mensaje=f"El gancho tiene {g} palabras; por encima de {MAX_PALABRAS_GANCHO} pierde fuerza."))
    # repeticiones entre tomas (n-gramas de 4 palabras)
    vistos: dict[str, int] = {}
    for num, t in todo_norm:
        pal = t.split()
        for k in range(len(pal) - 3):
            ng = " ".join(pal[k:k + 4])
            if ng in vistos and vistos[ng] != num:
                hs.append(Hallazgo(nivel="aviso", donde=f"tomas {vistos[ng]} y {num}", mensaje=f"Se repite «{ng}…»: no repitas información entre tomas."))
                break
            vistos.setdefault(ng, num)
    # duración total frente al objetivo
    if abs(total - brief.duracion_s) > max(3, 0.12 * brief.duracion_s):
        nivel = "aviso"
        hs.append(Hallazgo(nivel=nivel, donde="total", mensaje=f"Duración estimada {total:.0f} s frente a un objetivo de {brief.duracion_s} s."))
    if len(tomas) != brief.n_tomas:
        hs.append(Hallazgo(nivel="info", donde="total", mensaje=f"Hay {len(tomas)} tomas y el brief pedía {brief.n_tomas}."))
    orden = {"error": 0, "aviso": 1, "info": 2}
    return sorted(hs, key=lambda h: orden[h.nivel])


def resumen(hs: list[Hallazgo]) -> str:
    if not hs:
        return "✔ Sin hallazgos automáticos."
    ico = {"error": "✘", "aviso": "!", "info": "·"}
    return "\n".join(f"  {ico[h.nivel]} [{h.donde}] {h.mensaje}" for h in hs)
