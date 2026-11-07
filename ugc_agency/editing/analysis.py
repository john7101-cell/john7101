"""Detección de lo que hace que un video se vea poco atractivo.

- Pausas largas y silencios (transcripción palabra por palabra + silencedetect)
- Muletillas ("um", "uh"...) y tomas repetidas (retakes)
- Cuadros negros, imágenes congeladas y destellos/transiciones rotas típicas de video generado con IA
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

from .media import run

FILLERS = {"um", "uh", "uhm", "umm", "uhh", "erm", "er", "ah", "hmm", "mm", "eh", "este", "ehm"}

_SILENCE_RE = re.compile(r"silence_(start|end): (-?[\d.]+)")
_BLACK_RE = re.compile(r"black_start:([\d.]+) black_end:([\d.]+)")
_FREEZE_RE = re.compile(r"lavfi\.freezedetect\.freeze_(start|end): ([\d.]+)")


@dataclass
class Word:
    start: float
    end: float
    text: str
    probability: float = 1.0

    @property
    def clean(self) -> str:
        return re.sub(r"[^\w']", "", self.text.lower())


@dataclass
class Segment:
    start: float
    end: float
    text: str
    words: list[Word]


# ---------------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------------


def detect_silences(path: Path, noise_db: float = -35, min_duration: float = 0.35) -> list[tuple[float, float]]:
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vn",
               "-af", f"silencedetect=noise={noise_db}dB:d={min_duration}", "-f", "null", "-"]).stderr
    result, start = [], None
    for kind, value in _SILENCE_RE.findall(out):
        if kind == "start":
            start = max(0.0, float(value))
        elif start is not None:
            result.append((start, float(value)))
            start = None
    if start is not None:
        result.append((start, float("inf")))
    return result


def transcribe(path: Path, model_size: str = "small", language: str | None = None) -> list[Segment]:
    from faster_whisper import WhisperModel  # import perezoso: es pesado

    import numpy as np

    # Decodificamos con ffmpeg (16 kHz mono) en vez de PyAV: funciona con cualquier formato
    # que ffmpeg entienda y evita incompatibilidades de versiones.
    raw = subprocess.run(
        ["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000",
         "-f", "s16le", "-"], capture_output=True, check=True,
    ).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(
        audio, language=language, word_timestamps=True, vad_filter=True,
        # Sin esto Whisper tiende a "limpiar" las muletillas y no podríamos encontrarlas.
        initial_prompt="Umm, so, uh, like... you know, I mean, hmm.",
    )
    result = []
    for seg in segments:
        words = [Word(w.start, w.end, w.word.strip(), w.probability) for w in (seg.words or [])]
        result.append(Segment(seg.start, seg.end, seg.text.strip(), words))
    return result


def find_fillers(segments: list[Segment]) -> list[Word]:
    return [w for seg in segments for w in seg.words if w.clean in FILLERS]


def _norm(text: str) -> str:
    return " ".join(re.sub(r"[^\w\s']", " ", text.lower()).split())


def find_retakes(segments: list[Segment], similarity: float = 0.72) -> list[Segment]:
    """Frases que se dijeron y luego se repitieron (se conserva la última toma)."""
    retakes = []
    for current, nxt in zip(segments, segments[1:]):
        a, b = _norm(current.text), _norm(nxt.text)
        if len(a.split()) < 3:
            continue
        head = " ".join(b.split()[: len(a.split()) + 2])
        if SequenceMatcher(None, a, head).ratio() >= similarity:
            retakes.append(current)
    return retakes


# ---------------------------------------------------------------------------
# Video
# ---------------------------------------------------------------------------


def detect_black(path: Path, min_duration: float = 0.1) -> list[tuple[float, float]]:
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-an",
               "-vf", f"blackdetect=d={min_duration}:pix_th=0.10", "-f", "null", "-"]).stderr
    return [(float(s), float(e)) for s, e in _BLACK_RE.findall(out)]


def detect_freezes(path: Path, min_duration: float = 0.5) -> list[tuple[float, float]]:
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-an",
               "-vf", f"freezedetect=n=-55dB:d={min_duration}", "-f", "null", "-"]).stderr
    result, start = [], None
    for kind, value in _FREEZE_RE.findall(out):
        if kind == "start":
            start = float(value)
        elif start is not None:
            result.append((start, float(value)))
            start = None
    if start is not None:
        result.append((start, float("inf")))
    return result


def detect_scenes(path: Path, threshold: float = 27.0) -> list[tuple[float, float]]:
    from scenedetect import ContentDetector, detect

    scenes = detect(str(path), ContentDetector(threshold=threshold, min_scene_len=2))
    return [(s.get_seconds(), e.get_seconds()) for s, e in scenes]


def find_glitch_shots(scenes: list[tuple[float, float]], max_len: float = 0.3) -> list[tuple[float, float]]:
    """Planos de unos pocos cuadros entre dos cortes: destellos y transiciones mal generadas."""
    return [(s, e) for i, (s, e) in enumerate(scenes) if 0 < i < len(scenes) - 1 and e - s <= max_len]
