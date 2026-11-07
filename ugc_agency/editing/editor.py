"""Editor automático: decide los cortes, renderiza y deja un reporte de lo que hizo."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

from . import analysis
from .media import MediaInfo, probe, require_ffmpeg, run
from .timeline import Cut, Interval, keep_segments, map_time, overlaps


@dataclass
class EditOptions:
    max_pause: float = 0.45          # pausas más largas que esto se acortan
    keep_pause: float = 0.12         # aire que se deja antes/después de cada frase
    remove_fillers: bool = True
    remove_retakes: bool = True
    fix_visual_glitches: bool = True
    repair_motion: bool = True       # quitar tirones (cuadros duplicados) y suavizar saltos entre clips
    join_fade: float = 0.25          # duración del fundido (solo con transition="fade")
    transition: str = "punch"        # "punch": corte con cambio de encuadre; "fade": fundido
    freeze_min: float = 0.2          # congeladas más largas que esto se cortan si no hay voz
    vertical: bool = True            # salida 1080x1920 para TikTok
    captions: bool = True
    loudness_lufs: float = -14.0     # nivel típico de TikTok/Reels
    whisper_model: str = "small"
    language: str | None = None


@dataclass
class EditReport:
    input: str
    output: str
    original_duration: float
    final_duration: float
    cuts: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    repairs: list[str] = field(default_factory=list)
    transcript: str = ""

    def summary_by_reason(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        for c in self.cuts:
            totals[c["reason"]] = totals.get(c["reason"], 0.0) + c["end"] - c["start"]
        return totals


def _fmt(t: float) -> str:
    m, s = divmod(t, 60)
    return f"{int(m)}:{s:05.2f}"


def plan_cuts(path: Path, info: MediaInfo, opts: EditOptions, log: Callable[[str], None],
              patches: list[Interval] | None = None) -> tuple[list[Cut], list[analysis.Segment], list[str]]:
    """Decide los cortes. Los destellos que caen sobre la voz se agregan a `patches`
    (se tapan con el cuadro anterior sin tocar el audio)."""
    patches = patches if patches is not None else []
    cuts: list[Cut] = []
    warnings: list[str] = []
    segments: list[analysis.Segment] = []
    dur = info.duration

    if info.has_audio:
        log("Transcribiendo audio palabra por palabra...")
        segments = analysis.transcribe(path, opts.whisper_model, opts.language)
        words = [w for s in segments for w in s.words]

        if words:
            # Pausas: inicio, huecos entre palabras y final.
            points = [(0.0, 0.0)] + [(w.start, w.end) for w in words] + [(dur, dur)]
            for (_, prev_end), (next_start, _) in zip(points, points[1:]):
                gap = next_start - prev_end
                if gap > opts.max_pause:
                    lead = 0.0 if prev_end == 0.0 else opts.keep_pause
                    tail = 0.0 if next_start == dur else opts.keep_pause
                    cuts.append(Cut(prev_end + lead, next_start - tail, "pausa"))
            if opts.remove_fillers:
                for w in analysis.find_fillers(segments):
                    cuts.append(Cut(w.start, w.end, f"muletilla '{w.text}'"))
            if opts.remove_retakes:
                for seg in analysis.find_retakes(segments):
                    cuts.append(Cut(seg.start, seg.end, f"toma repetida: \"{seg.text[:50]}\""))
        else:
            log("No se detectó voz; se usan los silencios del audio.")
            for s, e in analysis.detect_silences(path, min_duration=opts.max_pause):
                cuts.append(Cut(s + opts.keep_pause, min(e, dur) - opts.keep_pause, "silencio"))

    if opts.fix_visual_glitches:
        log("Buscando cuadros negros, imágenes congeladas y transiciones rotas...")
        speech = [(w.start, w.end) for s in segments for w in s.words]

        def talks(iv: Interval) -> bool:
            return any(overlaps(iv, sp) for sp in speech)

        for s, e in analysis.detect_black(path):
            if talks((s, e)):
                warnings.append(f"Cuadro negro con voz en {_fmt(s)}-{_fmt(e)}: no se cortó para no perder diálogo.")
            else:
                cuts.append(Cut(s, e, "cuadro negro"))
        for s, e in analysis.detect_freezes(path, opts.freeze_min):
            e = min(e, dur)
            if talks((s, e)):
                warnings.append(f"Imagen congelada con voz en {_fmt(s)}-{_fmt(e)}: conviene regenerar esa escena.")
            else:
                cuts.append(Cut(s, e, "imagen congelada"))
        for s, e in analysis.find_glitch_shots(analysis.detect_scenes(path)):
            if talks((s, e)):
                patches.append((s, e))
            else:
                cuts.append(Cut(s, e, "destello / transición mal generada"))

    cuts = [c for c in cuts if c.end - c.start > 0.03]
    return sorted(cuts, key=lambda c: c.start), segments, warnings


def _chunks(words: list[analysis.Word], keeps: list[Interval], max_words: int = 3):
    """Agrupa palabras conservadas en bloques cortos para subtítulos estilo TikTok."""
    mapped = []
    for w in words:
        s, e = map_time(w.start, keeps), map_time(w.end, keeps)
        if s is not None and e is not None and w.clean not in analysis.FILLERS:
            mapped.append((s, e, w.text))
    group: list[tuple[float, float, str]] = []
    for item in mapped:
        group.append(item)
        if len(group) == max_words or item[2].rstrip().endswith((".", "?", "!", ",")):
            yield group[0][0], group[-1][1], " ".join(t for *_, t in group)
            group = []
    if group:
        yield group[0][0], group[-1][1], " ".join(t for *_, t in group)


def write_srt(path: Path, segments: list[analysis.Segment], keeps: list[Interval]) -> int:
    def ts(t: float) -> str:
        ms = int(round(t * 1000))
        h, ms = divmod(ms, 3_600_000)
        m, ms = divmod(ms, 60_000)
        s, ms = divmod(ms, 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    words = [w for s in segments for w in s.words]
    lines, n = [], 0
    for n, (s, e, text) in enumerate(_chunks(words, keeps), 1):
        lines += [str(n), f"{ts(s)} --> {ts(max(e, s + 0.2))}", text.upper(), ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return n


def render(src: Path, dst: Path, info: MediaInfo, keeps: list[Interval], opts: EditOptions,
           srt: Path | None, patches: list[Interval] | None = None) -> None:
    fade = 0.012  # micro-fundido de audio en cada corte para evitar "clics"
    parts, labels = [], []
    # Destellos sobre la voz: se reemplazan esos cuadros por el cuadro anterior.
    vin = "[0:v]"
    for j, (s, e) in enumerate(patches or []):
        first = max(1, int(round(s * info.fps)))
        last = max(first, int(round(e * info.fps)) - 1)
        parts.append(f"{vin}split[pa{j}][pb{j}]")
        parts.append(f"[pa{j}][pb{j}]freezeframes=first={first}:last={last}:replace={first - 1}[pv{j}]")
        vin = f"[pv{j}]"
    n_keeps = len(keeps)
    if n_keeps > 1:
        parts.append(f"{vin}split={n_keeps}" + "".join(f"[src{i}]" for i in range(n_keeps)))
        sources = [f"[src{i}]" for i in range(n_keeps)]
    else:
        sources = [vin]
    for i, (s, e) in enumerate(keeps):
        parts.append(f"{sources[i]}trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS[v{i}]")
        label = f"[v{i}]"
        if info.has_audio:
            d = e - s
            parts.append(
                f"[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS,"
                f"afade=t=in:d={fade},afade=t=out:st={max(0.0, d - fade):.3f}:d={fade}[a{i}]"
            )
            label += f"[a{i}]"
        labels.append(label)
    a_out = 1 if info.has_audio else 0
    parts.append(f"{''.join(labels)}concat=n={len(keeps)}:v=1:a={a_out}[vc]" + ("[ac]" if a_out else ""))

    fps = min(60, max(24, round(info.fps))) if math.isfinite(info.fps) else 30
    video_chain = []
    if opts.vertical:
        video_chain += ["scale=1080:1920:force_original_aspect_ratio=increase", "crop=1080:1920"]
    video_chain += [f"fps={fps}", "eq=contrast=1.03:saturation=1.06", "unsharp=5:5:0.35", "setsar=1"]
    if srt is not None:
        style = ("FontName=DejaVu Sans,Bold=1,FontSize=13,PrimaryColour=&H00FFFFFF,"
                 "OutlineColour=&H00000000,BorderStyle=1,Outline=2.2,Shadow=0,Alignment=2,MarginV=70")
        escaped = str(srt).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
        video_chain.append(f"subtitles='{escaped}':force_style='{style}'")
    parts.append(f"[vc]{','.join(video_chain)},format=yuv420p[vout]")
    if a_out:
        parts.append(f"[ac]highpass=f=70,loudnorm=I={opts.loudness_lufs}:TP=-1.5:LRA=11,aresample=48000[aout]")

    script = dst.with_suffix(".filtergraph.txt")
    script.write_text(";\n".join(parts), encoding="utf-8")
    cmd = ["ffmpeg", "-hide_banner", "-y", "-i", str(src), "-filter_complex_script", str(script),
           "-map", "[vout]"]
    if a_out:
        cmd += ["-map", "[aout]", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-movflags", "+faststart", str(dst)]
    try:
        run(cmd)
    finally:
        script.unlink(missing_ok=True)


def measure_lufs(path: Path) -> float | None:
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vn", "-af", "ebur128", "-f", "null", "-"]).stderr
    values = [line.split("I:")[1].split()[0] for line in out.splitlines() if line.strip().startswith("I:")]
    try:
        return float(values[-1])
    except (IndexError, ValueError):
        return None


def fix_loudness(path: Path, target: float, tolerance: float = 0.7) -> float | None:
    """Ajuste fino de volumen: loudnorm de una pasada se queda corto en clips de pocos segundos."""
    measured = measure_lufs(path)
    if measured is None or measured < -60 or abs(measured - target) <= tolerance:
        return measured
    tmp = path.with_name(path.stem + ".gain" + path.suffix)
    run(["ffmpeg", "-hide_banner", "-y", "-i", str(path), "-c:v", "copy",
         "-af", f"volume={target - measured:.2f}dB,alimiter=limit=0.84:level=false",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(tmp)])
    tmp.replace(path)
    return measure_lufs(path)


def edit_video(src: Path, dst: Path, opts: EditOptions | None = None,
               log: Callable[[str], None] = print) -> EditReport:
    require_ffmpeg()
    opts = opts or EditOptions()
    original = src
    repairs: list[str] = []
    work_dir = dst.parent / f".{dst.stem}_work"
    if opts.repair_motion:
        from .repair import repair_motion

        log("Revisando el movimiento cuadro por cuadro (tirones y saltos entre clips)...")
        src, repairs = repair_motion(src, work_dir, opts.join_fade, opts.transition)
        for note in repairs:
            log(f"  · {note}")
    info = probe(src)
    log(f"Video: {info.width}x{info.height}, {info.duration:.1f}s, {info.fps:.0f} fps, "
        f"audio={'sí' if info.has_audio else 'no'}")

    patches: list[Interval] = []
    cuts, segments, warnings = plan_cuts(src, info, opts, log, patches)
    keeps = keep_segments(info.duration, cuts)
    if not keeps:
        raise RuntimeError("Los cortes eliminarían todo el video; revisa los parámetros.")
    final = sum(e - s for s, e in keeps)
    log(f"{len(cuts)} cortes → {info.duration:.1f}s pasa a {final:.1f}s. Renderizando...")

    dst.parent.mkdir(parents=True, exist_ok=True)
    srt = None
    if opts.captions and segments:
        srt = dst.with_suffix(".srt")
        if not write_srt(srt, segments, keeps):
            srt = None
    render(src, dst, info, keeps, opts, srt, patches)
    if info.has_audio:
        lufs = fix_loudness(dst, opts.loudness_lufs)
        if lufs is not None:
            log(f"Volumen final: {lufs:.1f} LUFS")

    if work_dir.exists():
        import shutil

        shutil.rmtree(work_dir, ignore_errors=True)

    report = EditReport(
        input=str(original), output=str(dst), original_duration=round(info.duration, 2),
        final_duration=round(final, 2),
        cuts=[{"start": round(c.start, 2), "end": round(c.end, 2), "reason": c.reason} for c in cuts],
        warnings=warnings + [f"Destello tapado con el cuadro anterior en {_fmt(s)}-{_fmt(e)} (había voz)."
                             for s, e in patches],
        repairs=repairs,
        transcript=" ".join(s.text for s in segments),
    )
    dst.with_suffix(".report.json").write_text(json.dumps(asdict(report), indent=2, ensure_ascii=False),
                                              encoding="utf-8")
    return report
