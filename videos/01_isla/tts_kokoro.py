"""Borrador de narración con Kokoro (local, gratis). Escribe assets/narracion.wav y assets/segmentos.json."""
import json, re, sys
from pathlib import Path
import numpy as np, soundfile as sf
from kokoro import KPipeline

ROOT = Path(__file__).parent
SR = 24000
PAUSA = {"short pause": .35, "long pause": .9}
VOZ = sys.argv[1] if len(sys.argv) > 1 else "em_alex"

md = (ROOT.parent.parent / "guiones/youtube/01_isla_voz_elevenlabs.md").read_text()
partes = [p.split("\n", 1)[1].split("\n---")[0].strip() for p in md.split("## Parte")[1:]]

pipe = KPipeline(lang_code="e")
audio, segs, t = [], [], 0.0

def silencio(s):
    global t
    audio.append(np.zeros(int(s * SR), dtype=np.float32)); t += s

for pi, parte in enumerate(partes):
    for par in [p for p in parte.split("\n\n") if p.strip()]:
        piezas = re.split(r"\[([^\]]+)\]", par)
        for i, pz in enumerate(piezas):
            if i % 2 == 1:
                if pz in PAUSA: silencio(PAUSA[pz])
                continue
            txt = " ".join(pz.split())
            if not txt: continue
            chunks = [a for _, _, a in pipe(txt, voice=VOZ, speed=0.92)]
            wav = np.concatenate([np.asarray(c, dtype=np.float32) for c in chunks])
            segs.append({"parte": pi + 1, "texto": txt, "ini": round(t, 3), "fin": round(t + len(wav) / SR, 3)})
            audio.append(wav); t += len(wav) / SR
        silencio(.45)
    print(f"parte {pi+1} lista, t={t:.1f}s", flush=True)

sf.write(ROOT / "assets/narracion.wav", np.concatenate(audio), SR)
(ROOT / "assets/segmentos.json").write_text(json.dumps(segs, ensure_ascii=False, indent=1))
print("total", round(t, 1), "s,", len(segs), "segmentos")
