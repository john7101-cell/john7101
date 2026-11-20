"""Descarga el audio de una respuesta de Speko guardada en un archivo JSON (sin cargar el base64)."""
import json, sys, urllib.request
src, dst = sys.argv[1], sys.argv[2]
arr = json.loads(open(src).read())
for item in arr:
    t = item.get("text", "")
    if t.startswith("{"):
        d = json.loads(t)
        url, dur = d["url"], d.get("duration_seconds")
        urllib.request.urlretrieve(url, dst)
        print("ok", dst, "duración", dur, "s")
        break
