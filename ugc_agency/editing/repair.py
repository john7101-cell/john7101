"""Reparación de movimiento para videos generados con IA.

Arregla dos defectos muy comunes al unir clips de avatares y exportar:

1. Tirones periódicos (judder): el video se generó a 24/25 fps y se exportó a 30
   duplicando un cuadro cada N. Se detecta el patrón y se eliminan los duplicados.
2. Saltos de postura entre clips: el avatar cambia de posición de golpe en cada
   unión, a veces con unos pocos cuadros "intrusos" de otra toma. Se reemplazan
   por un fundido corto que NO cambia la duración, así el audio queda sincronizado.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .media import run


@dataclass
class Join:
    end_a: int     # primer cuadro que ya no pertenece al clip anterior
    start_b: int   # primer cuadro del clip siguiente (> end_a si hay cuadros intrusos)

    @property
    def gap(self) -> int:
        return self.start_b - self.end_a


@dataclass
class RepairPlan:
    fps: float
    frames: int
    pulldown_cycle: int | None = None
    joins: list[Join] = field(default_factory=list)

    @property
    def needed(self) -> bool:
        return bool(self.pulldown_cycle or self.joins)


# ---------------------------------------------------------------------------
# Análisis
# ---------------------------------------------------------------------------


def frame_motion(path: Path) -> tuple[float, np.ndarray]:
    """Diferencia media entre cuadros consecutivos (zona central, baja resolución)."""
    import cv2

    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    diffs, prev = [], None
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(cv2.resize(frame, (160, 284)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        h, w = g.shape
        g = g[int(h * 0.08):int(h * 0.65), int(w * 0.12):int(w * 0.88)]  # donde suele estar la persona
        diffs.append(float(np.mean(np.abs(g - prev))) if prev is not None else 0.0)
        prev = g
    cap.release()
    return fps, np.array(diffs)


def detect_pulldown(diffs: np.ndarray, min_share: float = 0.6) -> int | None:
    """Devuelve N si casi exactamente un cuadro de cada N es un duplicado."""
    if len(diffs) < 30:
        return None
    med = float(np.median(diffs[1:]))
    if med <= 0:
        return None
    dups = np.where(diffs[1:] < 0.3 * med)[0] + 1
    if len(dups) < 6:
        return None
    gaps = Counter(np.diff(dups).tolist())
    cycle, count = gaps.most_common(1)[0]
    if cycle < 3 or cycle > 8:
        return None
    expected = len(diffs) / cycle
    if count >= min_share * (len(dups) - 1) and len(dups) >= 0.6 * expected:
        return int(cycle)
    return None


def detect_joins(diffs: np.ndarray, fps: float, factor: float = 6.0, min_jump: float = 6.0,
                 max_intruder: int = 4) -> list[Join]:
    """Saltos bruscos de imagen = uniones entre clips. Dos saltos muy seguidos indican
    cuadros intrusos (una transición mal generada) entre ellos."""
    med = float(np.median(diffs[1:])) if len(diffs) > 1 else 0.0
    threshold = max(min_jump, factor * med)
    margin = int(fps * 0.3)
    jumps = [i for i in range(1, len(diffs)) if diffs[i] > threshold and margin < i < len(diffs) - margin]
    joins: list[Join] = []
    i = 0
    while i < len(jumps):
        start = jumps[i]
        end = start
        while i + 1 < len(jumps) and jumps[i + 1] - end <= max_intruder:
            i += 1
            end = jumps[i]
        joins.append(Join(start, end))
        i += 1
    # uniones demasiado juntas no dejan sitio para el fundido
    min_len = int(fps * 0.6)
    cleaned: list[Join] = []
    for j in joins:
        if cleaned and j.end_a - cleaned[-1].start_b < min_len:
            continue
        cleaned.append(j)
    return cleaned


def plan_repair(path: Path) -> RepairPlan:
    fps, diffs = frame_motion(path)
    plan = RepairPlan(fps=fps, frames=len(diffs))
    plan.pulldown_cycle = detect_pulldown(diffs)
    if plan.pulldown_cycle is None:
        plan.joins = detect_joins(diffs, fps)
    return plan


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------


def dejudder(src: Path, dst: Path, cycle: int) -> None:
    run(["ffmpeg", "-hide_banner", "-y", "-i", str(src), "-vf", f"decimate=cycle={cycle}",
         "-map", "0:v", "-map", "0:a?", "-c:v", "libx264", "-crf", "12", "-preset", "fast",
         "-c:a", "copy", str(dst)])


def join_graph(frames: int, fps: float, joins: list[Join], fade_frames: int) -> tuple[list[str], int]:
    """Filtro que reemplaza cada unión por un fundido manteniendo la duración total.

    Cada clip se alarga con copias de su último/primer cuadro (h1 + h2 = fundido + cuadros
    intrusos) y se encadena con xfade: lo que dura el resultado es igual al original."""
    bounds = [0]
    for j in joins:
        bounds += [j.end_a, j.start_b]
    bounds.append(frames)
    segs = [(bounds[k], bounds[k + 1]) for k in range(0, len(bounds), 2)]
    holds_in = [0] * len(segs)
    holds_out = [0] * len(segs)
    for k, j in enumerate(joins):
        total = fade_frames + j.gap
        holds_out[k] = total // 2
        holds_in[k + 1] = total - total // 2

    g, lens = [], []
    for k, (a, b) in enumerate(segs):
        pads = []
        if holds_in[k]:
            pads.append(f"start_mode=clone:start_duration={holds_in[k] / fps:.6f}")
        if holds_out[k]:
            pads.append(f"stop_mode=clone:stop_duration={holds_out[k] / fps:.6f}")
        pad = f",tpad={':'.join(pads)}" if pads else ""
        g.append(f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS{pad},fps={fps:.6f}[s{k}]")
        lens.append(b - a + holds_in[k] + holds_out[k])
    cur, cur_len = "[s0]", lens[0]
    for k in range(1, len(segs)):
        offset = (cur_len - fade_frames) / fps
        g.append(f"{cur}[s{k}]xfade=transition=fade:duration={fade_frames / fps:.6f}:offset={offset:.6f}[x{k}]")
        cur, cur_len = f"[x{k}]", cur_len + lens[k] - fade_frames
    g.append(f"{cur}format=yuv420p[vout]")
    return g, cur_len


def smooth_joins(src: Path, dst: Path, fps: float, frames: int, joins: list[Join], fade: float = 0.25) -> None:
    fade_frames = max(2, round(fade * fps))
    graph, _ = join_graph(frames, fps, joins, fade_frames)
    script = dst.with_suffix(".joins.txt")
    script.write_text(";\n".join(graph), encoding="utf-8")
    try:
        run(["ffmpeg", "-hide_banner", "-y", "-i", str(src), "-filter_complex_script", str(script),
             "-map", "[vout]", "-map", "0:a?", "-c:v", "libx264", "-crf", "12", "-preset", "fast",
             "-c:a", "copy", str(dst)])
    finally:
        script.unlink(missing_ok=True)


def face_anchor(path: Path, frame_index: int) -> tuple[float, float]:
    """Centro de la cara (0-1) en un cuadro; si no se detecta, un encuadre típico de busto."""
    import cv2

    cap = cv2.VideoCapture(str(path))
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ok, frame = cap.read()
    cap.release()
    if not ok:
        return 0.5, 0.35
    h, w = frame.shape[:2]
    gray = cv2.cvtColor(cv2.resize(frame, (w // 2, h // 2)), cv2.COLOR_BGR2GRAY)
    if not hasattr(cv2, "CascadeClassifier"):  # OpenCV 5 movió el detector clásico a contrib
        return 0.5, 0.35
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(40, 40))
    if len(faces) == 0:
        return 0.5, 0.35
    x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])
    return (x + fw / 2) * 2 / w, (y + fh / 2) * 2 / h


def punch_crop(width: int, height: int, zoom: float, anchor: tuple[float, float]) -> str:
    """Recorte para el plano cerrado: la cara queda a la misma altura relativa que en el abierto."""
    cw, ch = round(width / zoom / 2) * 2, round(height / zoom / 2) * 2
    ax, ay = anchor
    x = min(max(0, round(ax * width - cw / 2)), width - cw)
    y = min(max(0, round(ay * height - ay * ch)), height - ch)
    return f"crop={cw}:{ch}:{x}:{y},scale={width}:{height}:flags=lanczos"


def punch_cuts(src: Path, dst: Path, fps: float, frames: int, joins: list[Join], zoom: float = 1.12) -> None:
    """Corte limpio en cada unión, alternando plano abierto / cerrado (punch-in).

    No mezcla imágenes (sin efecto fantasma). Los cuadros intrusos se quitan junto con el
    mismo tramo de audio, que suele caer en una pausa."""
    from .media import probe

    info = probe(src)
    bounds = [0]
    for j in joins:
        bounds += [j.end_a, j.start_b]
    bounds.append(frames)
    segs = [(bounds[k], bounds[k + 1]) for k in range(0, len(bounds), 2)]
    g, labels = [], []
    for k, (a, b) in enumerate(segs):
        chain = f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS"
        if k % 2 == 1:
            chain += "," + punch_crop(info.width, info.height, zoom, face_anchor(src, (a + b) // 2))
        g.append(chain + f",setsar=1[v{k}]")
        labels.append(f"[v{k}]")
    g.append(f"{''.join(labels)}concat=n={len(segs)}:v=1:a=0,format=yuv420p[vout]")
    gaps = [(j.end_a / fps, j.start_b / fps) for j in joins if j.gap]
    if info.has_audio and gaps:
        expr = "+".join(f"between(t,{a:.4f},{b - 0.0005:.4f})" for a, b in gaps)
        g.append(f"[0:a]aselect='not({expr})',asetpts=N/SR/TB[aout]")
        amap = ["-map", "[aout]", "-c:a", "pcm_s16le"]
    else:
        amap = ["-map", "0:a?", "-c:a", "copy"]
    script = dst.with_suffix(".punch.txt")
    script.write_text(";\n".join(g), encoding="utf-8")
    try:
        run(["ffmpeg", "-hide_banner", "-y", "-i", str(src), "-filter_complex_script", str(script),
             "-map", "[vout]", *amap, "-c:v", "libx264", "-crf", "12", "-preset", "fast",
             str(dst.with_suffix(".mov"))])
        dst.with_suffix(".mov").replace(dst)
    finally:
        script.unlink(missing_ok=True)


def repair_motion(src: Path, work_dir: Path, fade: float = 0.25, transition: str = "punch",
                  zoom: float = 1.12) -> tuple[Path, list[str]]:
    """Devuelve el video reparado (o el original si no hacía falta) y notas para el reporte."""
    notes: list[str] = []
    work_dir.mkdir(parents=True, exist_ok=True)
    current = src
    plan = plan_repair(current)
    if plan.pulldown_cycle:
        fixed = work_dir / "dejudder.mp4"
        dejudder(current, fixed, plan.pulldown_cycle)
        new_fps = plan.fps * (plan.pulldown_cycle - 1) / plan.pulldown_cycle
        notes.append(f"Tirones: había 1 cuadro repetido de cada {plan.pulldown_cycle}; "
                     f"se eliminaron ({plan.fps:.0f} → {new_fps:.0f} fps reales).")
        current = fixed
        plan = plan_repair(current)
    if plan.joins:
        fixed = work_dir / "joins.mp4"
        if transition == "fade":
            smooth_joins(current, fixed, plan.fps, plan.frames, plan.joins, fade)
            how = "suavizado con fundido"
        else:
            punch_cuts(current, fixed, plan.fps, plan.frames, plan.joins, zoom)
            how = "convertido en corte con cambio de encuadre"
        for j in plan.joins:
            t = j.end_a / plan.fps
            extra = f" (se quitaron {j.gap} cuadros intrusos)" if j.gap else ""
            notes.append(f"Salto entre clips en {int(t // 60)}:{t % 60:05.2f} {how}{extra}.")
        current = fixed
    return current, notes
