"""Operaciones con intervalos de tiempo: qué se corta, qué se conserva y cómo se reubica."""

from __future__ import annotations

from dataclasses import dataclass

Interval = tuple[float, float]


@dataclass
class Cut:
    start: float
    end: float
    reason: str

    @property
    def duration(self) -> float:
        return self.end - self.start


def merge(intervals: list[Interval], gap: float = 0.0) -> list[Interval]:
    out: list[list[float]] = []
    for s, e in sorted(i for i in intervals if i[1] > i[0]):
        if out and s <= out[-1][1] + gap:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [(s, e) for s, e in out]


def keep_segments(duration: float, cuts: list[Cut], min_keep: float = 0.12) -> list[Interval]:
    """Lo que queda del video después de quitar los cortes (descarta trocitos minúsculos)."""
    removed = merge([(max(0.0, c.start), min(duration, c.end)) for c in cuts])
    keeps: list[Interval] = []
    cursor = 0.0
    for s, e in removed:
        if s > cursor:
            keeps.append((cursor, s))
        cursor = max(cursor, e)
    if cursor < duration:
        keeps.append((cursor, duration))
    return [(s, e) for s, e in keeps if e - s >= min_keep]


def map_time(t: float, keeps: list[Interval]) -> float | None:
    """Convierte un instante del video original al tiempo del video editado (None si fue cortado)."""
    offset = 0.0
    for s, e in keeps:
        if s <= t <= e:
            return offset + (t - s)
        offset += e - s
    return None


def overlaps(a: Interval, b: Interval) -> bool:
    return a[0] < b[1] and b[0] < a[1]
