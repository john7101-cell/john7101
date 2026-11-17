"""Narración con Kokoro (local). Una frase a la vez: sabemos la duración exacta de cada línea."""
import json
from pathlib import Path
import numpy as np, soundfile as sf
from kokoro import KPipeline

ROOT = Path(__file__).parent
SR = 24000
G = json.loads((ROOT / "guion.json").read_text())
pipe = KPipeline(lang_code="e")
audio, segs, t = [], [], 0.0

def silencio(s):
    global t
    audio.append(np.zeros(int(s * SR), dtype=np.float32)); t += s

for esc in G["escenas"]:
    for ln in esc["lineas"]:
        chunks = [a for _, _, a in pipe(ln, voice="em_alex", speed=0.92)]
        wav = np.concatenate([np.asarray(c, dtype=np.float32) for c in chunks])
        segs.append({"escena": esc["id"], "mood": esc["mood"], "texto": ln,
                     "ini": round(t, 3), "fin": round(t + len(wav) / SR, 3)})
        audio.append(wav); t += len(wav) / SR
        silencio(.45)
    silencio(.35)
    print(esc["id"], f"t={t:.1f}s", flush=True)

sf.write(ROOT / "assets/narracion.wav", np.concatenate(audio), SR)
(ROOT / "assets/segmentos.json").write_text(json.dumps(segs, ensure_ascii=False, indent=1))
print("total", round(t, 1), "s,", len(segs), "líneas")
