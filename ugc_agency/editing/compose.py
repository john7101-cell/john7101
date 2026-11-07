"""Compositor: arma un reel a partir de clips limpios + gráficos sincronizados con la voz.

Los gráficos se anclan a frases de la narración (no a segundos fijos), así siempre
aparecen en el momento exacto en que se mencionan, aunque cambie la edición.

Especificación (JSON):

    {
      "graphics": [
        {"image": "calendario.png", "x": 784, "y": 24,
         "start": {"phrase": "31 de diciembre"},
         "end":   {"phrase": "vence el plazo", "edge": "end"}},
        {"image": "tarjeta.png", "x": 784, "y": 1422,
         "start": {"phrase": "escríbenos", "offset": -0.1}, "end": "video_end"}
      ]
    }

- "phrase": palabras dichas en el video (sin importar mayúsculas, acentos ni puntuación).
- "edge": "start" (por defecto en "start") o "end" (por defecto en "end") de la frase.
- "offset": segundos a sumar (negativo = antes).
- "occurrence": 1 por defecto; usa 2 para la segunda vez que se dice la frase.
"""

from __future__ import annotations

import json
import re
import shutil
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from . import analysis
from .editor import fix_loudness
from .media import probe, require_ffmpeg, run
from .repair import repair_motion


@dataclass
class PlacedGraphic:
    image: Path
    x: int
    y: int
    start: float
    end: float
    label: str


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^\w]", "", text)


def find_phrase(words: list[analysis.Word], phrase: str, occurrence: int = 1) -> tuple[float, float]:
    target = [t for t in (_norm(p) for p in phrase.split()) if t]
    tokens = [_norm(w.text) for w in words]
    found = 0
    for i in range(len(tokens) - len(target) + 1):
        if tokens[i:i + len(target)] == target:
            found += 1
            if found == occurrence:
                return words[i].start, words[i + len(target) - 1].end
    raise ValueError(f"No encontré la frase \"{phrase}\" en la narración.")


def resolve_cue(cue, words: list[analysis.Word], duration: float, default_edge: str) -> float:
    if cue == "video_end":
        return duration
    if cue == "video_start":
        return 0.0
    if isinstance(cue, (int, float)):
        return float(cue)
    start, end = find_phrase(words, cue["phrase"], cue.get("occurrence", 1))
    t = start if cue.get("edge", default_edge) == "start" else end
    return max(0.0, min(duration, t + float(cue.get("offset", 0.0))))


def concat_clips(clips: list[Path], dst: Path, width: int = 1080, height: int = 1920, fps: int = 30) -> None:
    parts, labels = [], []
    for i, _ in enumerate(clips):
        parts.append(f"[{i}:v]fps={fps},scale={width}:{height}:force_original_aspect_ratio=increase:flags=lanczos,"
                     f"crop={width}:{height},setsar=1[v{i}]")
        parts.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}]")
        labels.append(f"[v{i}][a{i}]")
    parts.append(f"{''.join(labels)}concat=n={len(clips)}:v=1:a=1[v][a]")
    cmd = ["ffmpeg", "-hide_banner", "-y"]
    for c in clips:
        cmd += ["-i", str(c)]
    cmd += ["-filter_complex", ";".join(parts), "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-c:a", "pcm_s16le", str(dst.with_suffix(".mov"))]
    run(cmd)
    dst.with_suffix(".mov").replace(dst)


def compose(clips: list[Path], spec_path: Path, dst: Path, fade: float = 0.15,
            whisper_model: str = "small", language: str | None = None,
            loudness: float = -14.0, log: Callable[[str], None] = print) -> dict:
    require_ffmpeg()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    work = dst.parent / f".{dst.stem}_work"
    work.mkdir(parents=True, exist_ok=True)
    try:
        log(f"Uniendo {len(clips)} clips en 1080x1920...")
        joined = work / "joined.mov"
        concat_clips(clips, joined)

        log("Reparando movimiento (tirones y saltos entre clips)...")
        base, repairs = repair_motion(joined, work)
        for r in repairs:
            log(f"  · {r}")

        log("Transcribiendo para sincronizar los gráficos con la voz...")
        segments = analysis.transcribe(base, whisper_model, language)
        words = [w for s in segments for w in s.words]
        duration = probe(base).duration

        placed: list[PlacedGraphic] = []
        for g in spec["graphics"]:
            image = (spec_path.parent / g["image"]).resolve()
            start = resolve_cue(g["start"], words, duration, "start")
            end = resolve_cue(g.get("end", "video_end"), words, duration, "end")
            if end <= start:
                raise ValueError(f"{g['image']}: termina antes de empezar ({start:.2f}-{end:.2f}s)")
            placed.append(PlacedGraphic(image, int(g["x"]), int(g["y"]), start, end, g.get("label", image.stem)))
            log(f"  {image.stem:18s} {start:6.2f}s → {end:6.2f}s")

        cmd = ["ffmpeg", "-hide_banner", "-y", "-i", str(base)]
        for p in placed:
            cmd += ["-loop", "1", "-i", str(p.image)]
        chain, cur = [], "[0:v]"
        for k, p in enumerate(placed, 1):
            d = p.end - p.start
            f = min(fade, d / 3)
            chain.append(f"[{k}:v]format=rgba,fade=t=in:st={p.start:.3f}:d={f:.3f}:alpha=1,"
                         f"fade=t=out:st={p.end - f:.3f}:d={f:.3f}:alpha=1[g{k}]")
            chain.append(f"{cur}[g{k}]overlay={p.x}:{p.y}:enable='between(t,{p.start:.3f},{p.end:.3f})'"
                         f":shortest=1[o{k}]")
            cur = f"[o{k}]"
        chain.append(f"{cur}format=yuv420p[vout]")
        chain.append(f"[0:a]highpass=f=60,loudnorm=I={loudness}:TP=-1.5:LRA=9,aresample=48000[aout]")
        script = work / "graph.txt"
        script.write_text(";\n".join(chain), encoding="utf-8")
        dst.parent.mkdir(parents=True, exist_ok=True)
        run(cmd + ["-filter_complex_script", str(script), "-map", "[vout]", "-map", "[aout]",
                   "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-c:a", "aac", "-b:a", "192k",
                   "-movflags", "+faststart", str(dst)])
        lufs = fix_loudness(dst, loudness)

        report = {
            "output": str(dst), "duration": round(duration, 2), "loudness_lufs": lufs,
            "repairs": repairs,
            "graphics": [{"image": p.image.name, "start": round(p.start, 2), "end": round(p.end, 2)}
                         for p in placed],
            "transcript": " ".join(s.text for s in segments),
        }
        dst.with_suffix(".report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                                  encoding="utf-8")
        return report
    finally:
        shutil.rmtree(work, ignore_errors=True)
