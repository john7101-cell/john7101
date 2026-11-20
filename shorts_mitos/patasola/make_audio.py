"""Música original (video 2) (sintetizada, libre de derechos) + pista de efectos del video 1.

- assets/musica.wav: fondo de misterio en La menor con caja de música; sección "ligera" en Do mayor
  para el contexto (mapa, chinampas, UNESCO, fiesta) y la isla hoy; latido en los momentos tensos.
  Baja automáticamente (ducking) cuando habla el narrador.
- assets/sfx.wav: los efectos de assets/sfx_events.json (biblioteca Pixabay de HyperFrames).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).parent
SR = 44100
SFX_DIR = Path("/root/.claude/skills/media-use/audio/assets/sfx")
SEGS = json.loads((ROOT / "assets/segmentos.json").read_text())
DUR = SEGS[-1]["fin"] + 2.0
N = int(DUR * SR)
rng = np.random.default_rng(7)

def _rangos(mood):
    out, cur = [], None
    for x in SEGS:
        if x.get("mood") == mood:
            if cur and x["ini"] - cur[1] < 3:
                cur[1] = x["fin"]
            else:
                cur = [x["ini"], x["fin"]]; out.append(cur)
    return [tuple(r) for r in out]


LIGERO = _rangos("ligero")
TENSO = _rangos("tenso")
BEAT = 60 / 70  # 70 bpm


def hz(midi: float) -> float:
    return 440 * 2 ** ((midi - 69) / 12)


def env(n: int, a: float, r: float) -> np.ndarray:
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-3)) * np.exp(-t / r)


def add(buf: np.ndarray, t0: float, sig: np.ndarray, gain: float = 1.0) -> None:
    i = int(t0 * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def pad_note(m: float, dur: float) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * hz(m) * (1 + d) * t + p) for d, p in ((0, 0), (.004, 1.1), (-.005, 2.3)))
    s += .3 * np.sin(2 * np.pi * hz(m) * 2 * t)
    a = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2).clip(0)
    return s * a / 3


def bell(m: float, dur: float = 2.2) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * hz(m) * t) + .35 * np.sin(2 * np.pi * hz(m) * 2.76 * t) * np.exp(-t * 6)
    return s * env(n, .005, .55)


def marimba(m: float) -> np.ndarray:
    n = int(.6 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * hz(m) * t) + .25 * np.sin(2 * np.pi * hz(m) * 4 * t) * np.exp(-t * 20)) * env(n, .003, .16)


def bass(m: float, dur: float) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * hz(m) * t) * np.minimum(1, t / .05) * np.exp(-t / (dur * .8))


def heartbeat() -> np.ndarray:
    n = int(.25 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 52 * t) * np.exp(-t * 18)


def track(chords: list[list[int]], arp_div: int, voice, arp_gain: float, seed: int) -> np.ndarray:
    r = np.random.default_rng(seed)
    buf = np.zeros(N, dtype=np.float64)
    bar = 4 * BEAT
    t, ci = 0.0, 0
    while t < DUR:
        ch = chords[ci % len(chords)]
        for m in ch:
            add(buf, t, pad_note(m, bar * 2 + 1.2), .10)
        add(buf, t, bass(ch[0] - 12, bar * 2), .22)
        step = BEAT / arp_div
        k = 0
        while k * step < bar * 2:
            if r.random() < .78:
                m = ch[r.integers(len(ch))] + 12 * int(r.integers(1, 3))
                add(buf, t + k * step, voice(m), arp_gain * (.7 + .3 * r.random()))
            k += 1
        t += bar * 2
        ci += 1
    return buf


def mask(ranges, fade: float = 2.0) -> np.ndarray:
    t = np.arange(N) / SR
    m = np.zeros(N)
    for a, b in ranges:
        m = np.maximum(m, np.clip(np.minimum((t - a) / fade + 1, (b - t) / fade + 1), 0, 1))
    return m


def musica() -> np.ndarray:
    # misterio: Am - F - Dm - E
    mist = track([[57, 60, 64], [53, 57, 60], [50, 53, 57], [52, 56, 59]], 2, bell, .16, 1)
    # ligero: C - G - Am - F, marimba en semicorcheas
    lig = track([[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]], 4, marimba, .14, 2)
    ml = mask(LIGERO)
    out = mist * (1 - ml) + lig * ml
    # tensión: latido + drone grave
    mt = mask(TENSO, .8)
    hb = np.zeros(N)
    t = 0.0
    while t < DUR:
        add(hb, t, heartbeat(), .9)
        add(hb, t + .28, heartbeat(), .6)
        t += .9
    tt = np.arange(N) / SR
    drone = .25 * np.sin(2 * np.pi * 55 * tt) * (1 + .3 * np.sin(2 * np.pi * .2 * tt))
    out = out * (1 - .6 * mt) + (hb + drone) * mt
    # ducking bajo la voz
    voz = np.zeros(N)
    for s in SEGS:
        voz[int(s["ini"] * SR): int(s["fin"] * SR)] = 1
    k = int(.4 * SR)
    voz = np.convolve(voz, np.ones(k) / k, mode="same")
    out *= 1 - .55 * voz
    # entrada y salida
    out *= np.minimum(1, tt / 1.5) * np.clip((DUR - tt) / 3, 0, 1)
    rms = np.sqrt(np.mean(out ** 2))
    return out * (10 ** (-33 / 20) / rms)  # ~ -33 dBFS RMS, por debajo de la voz


def load_sfx(name: str) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(SFX_DIR / f"{name}.mp3"), "-f", "f32le",
                          "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def efectos() -> np.ndarray:
    ev = json.loads((ROOT / "assets/sfx_events.json").read_text())
    cache: dict[str, np.ndarray] = {}
    buf = np.zeros(N)
    for name, t, vol in ev:
        if name not in cache:
            cache[name] = load_sfx(name)
        add(buf, t, cache[name], vol)
    return buf


def guardar(name: str, x: np.ndarray) -> None:
    peak = np.abs(x).max()
    if peak > .98:
        x = x * (.98 / peak)
    sf.write(ROOT / "assets" / name, x.astype(np.float32), SR)
    print(name, f"{len(x) / SR:.1f}s pico {20 * np.log10(np.abs(x).max() + 1e-9):.1f} dBFS")


if __name__ == "__main__":
    guardar("musica.wav", musica())
    guardar("sfx.wav", efectos())
