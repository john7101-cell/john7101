"""Alinea cada línea del guion con su tiempo en la narración (transcripción palabra por palabra)."""
import json, re, unicodedata, subprocess
from pathlib import Path
import soundfile as sf
from faster_whisper import WhisperModel
ROOT = Path(__file__).parent
G = json.loads((ROOT / "guion.json").read_text())
tmp = ROOT / "assets/_n16.wav"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(ROOT / "assets/narracion.wav"), "-ar", "16000", "-ac", "1", str(tmp)], check=True)
a, _ = sf.read(tmp, dtype="float32")
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, language="es", word_timestamps=True, vad_filter=False)
words = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
def norm(t): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", t.lower()).encode("ascii", "ignore").decode())
W = [(norm(w), s, e) for w, s, e in words if norm(w)]
pos = 0; out = []
for esc in G["escenas"]:
    for ln in esc["lineas"]:
        toks = [norm(t) for t in ln.split() if norm(t)]
        key = toks[:3]
        found = None
        for i in range(pos, len(W) - 2):
            if [W[i][0], W[i + 1][0], W[i + 2][0]] == key:
                found = i; break
        if found is None:
            for i in range(pos, len(W)):
                if W[i][0] == key[0]:
                    found = i; break
        if found is None:
            found = min(pos, len(W) - 1)
        ini = W[found][1]
        last = min(len(W) - 1, found + len(toks) - 1)
        fin = W[last][2]
        out.append({"escena": esc["id"], "mood": esc["mood"], "texto": ln, "ini": round(ini, 3), "fin": round(max(fin, ini + .8), 3)})
        pos = min(last + 1, len(W) - 1)
(ROOT / "assets/segmentos.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
tmp.unlink()
print(len(out), "líneas; total", out[-1]["fin"], "s")
for o in out: print(f'{o["ini"]:7.2f} {o["fin"]:7.2f} {o["escena"]:12} {o["texto"][:50]}')
