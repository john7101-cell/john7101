import json
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
a, sr = sf.read("/tmp/claude-0/-home-user-john7101/f3c6e0da-f1ba-5663-83e0-e6940d2d2cae/scratchpad/n16.wav", dtype="float32")
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, language="es", word_timestamps=True, vad_filter=False)
words = [{"w": w.word.strip(), "ini": round(w.start, 3), "fin": round(w.end, 3)} for s in segs for w in s.words]
json.dump(words, open("assets/palabras.json", "w"), ensure_ascii=False)
print(len(words), "palabras"); print(" ".join(x["w"] for x in words[:90]))
