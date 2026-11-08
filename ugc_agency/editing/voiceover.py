"""Limpieza de voces en off generadas por clonación/TTS.

Algunas herramientas de clonación insertan fragmentos sueltos sin sentido (típicamente
"ción" / "sión") en las pausas de comas y puntos, y dejan silencios demasiado largos.
Este módulo los detecta con la transcripción palabra por palabra y corta usando la
energía del audio, para no comerse el principio o el final de las palabras reales.
"""

from __future__ import annotations

import re
import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import analysis

# Fragmentos fantasma habituales: "ción", "sión", "sución", "susión"…
ARTEFACTO = re.compile(r"^(s?u?)?[sc]i[oó]n$", re.IGNORECASE)


@dataclass
class Corte:
    inicio: float
    fin: float
    motivo: str


def _pcm(path: Path, sr: int = 16000) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", str(sr),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def tramos_con_voz(x: np.ndarray, sr: int = 16000, umbral_db: float = -40.0, hueco: float = 0.06) -> list[tuple[float, float]]:
    """Tramos con energía por encima del umbral (ventanas de 10 ms), uniendo huecos cortos."""
    paso = sr // 100
    n = len(x) // paso
    db = 20 * np.log10(np.sqrt((x[: n * paso].reshape(n, paso) ** 2).mean(axis=1)) + 1e-9)
    activo = db > umbral_db
    tramos: list[list[float]] = []
    for i, a in enumerate(activo):
        t = i / 100
        if a:
            if tramos and t - tramos[-1][1] <= hueco:
                tramos[-1][1] = t + 0.01
            else:
                tramos.append([t, t + 0.01])
    return [(a, b) for a, b in tramos]


def _norm(t: str) -> str:
    return re.sub(r"[^\wáéíóúñ]", "", t.lower())


def planificar(path: Path, pausa_max: float = 0.38, pausa_obj: float = 0.28,
               whisper_model: str = "small", language: str = "es") -> tuple[list[Corte], float, list[str]]:
    x = _pcm(path)
    dur = len(x) / 16000
    voz = tramos_con_voz(x)
    palabras = [w for s in analysis.transcribe(path, whisper_model, language) for w in s.words]
    reales = [w for w in palabras if not ARTEFACTO.match(_norm(w.text))]
    cortes: list[Corte] = []

    # 1) Fragmentos fantasma: se quita el tramo de energía que los contiene y el silencio alrededor,
    #    dejando una pausa natural entre la palabra real anterior y la siguiente.
    for w in palabras:
        if not ARTEFACTO.match(_norm(w.text)):
            continue
        centro = (w.start + w.end) / 2
        tramo = min(voz, key=lambda v: 0 if v[0] <= centro <= v[1] else min(abs(v[0] - centro), abs(v[1] - centro)))
        prev_fin = max((v[1] for v in voz if v[1] <= tramo[0] + 1e-3), default=0.0)
        sig_ini = min((v[0] for v in voz if v[0] >= tramo[1] - 1e-3), default=dur)
        a = 0.0 if prev_fin == 0.0 else prev_fin + pausa_obj * 0.45
        b = sig_ini - (0.04 if prev_fin == 0.0 else pausa_obj * 0.55)
        if b > a:
            cortes.append(Corte(a, b, f"fragmento '{w.text}'"))

    # 2) Silencios demasiado largos entre tramos de voz (fuera de los cortes anteriores)
    def cubierto(t: float) -> bool:
        return any(c.inicio - 0.05 <= t <= c.fin + 0.05 for c in cortes)

    for (_, fin_a), (ini_b, _) in zip(voz, voz[1:]):
        hueco = ini_b - fin_a
        if hueco > pausa_max and not cubierto((fin_a + ini_b) / 2):
            cortes.append(Corte(fin_a + pausa_obj * 0.45, ini_b - pausa_obj * 0.55, f"silencio de {hueco:.2f}s"))
    if voz and voz[0][0] > 0.15 and not cubierto(voz[0][0] / 2):
        cortes.append(Corte(0.0, voz[0][0] - 0.04, "silencio inicial"))
    if voz and dur - voz[-1][1] > 0.3:
        cortes.append(Corte(voz[-1][1] + 0.2, dur, "silencio final"))

    texto = [w.text for w in reales]
    return sorted(cortes, key=lambda c: c.inicio), dur, texto


def aplicar(src: Path, dst: Path, cortes: list[Corte], dur: float, fade: float = 0.012, sr_salida: int = 48000) -> float:
    keeps, cur = [], 0.0
    for c in sorted(cortes, key=lambda c: c.inicio):
        if c.inicio > cur:
            keeps.append((cur, c.inicio))
        cur = max(cur, c.fin)
    if cur < dur:
        keeps.append((cur, dur))
    keeps = [(a, b) for a, b in keeps if b - a > 0.03]
    parts = [f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={fade},afade=t=out:st={b - a - fade:.3f}:d={fade}[k{i}]"
             for i, (a, b) in enumerate(keeps)]
    parts.append("".join(f"[k{i}]" for i in range(len(keeps))) + f"concat=n={len(keeps)}:v=0:a=1[out]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-filter_complex", ";".join(parts),
                    "-map", "[out]", "-ar", str(sr_salida), str(dst)], check=True)
    return sum(b - a for a, b in keeps)


def limpiar_voz(src: Path, dst: Path, **kw) -> tuple[list[Corte], float, float]:
    cortes, dur, _ = planificar(src, **kw)
    final = aplicar(src, dst, cortes, dur)
    return cortes, dur, final
