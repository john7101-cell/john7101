"""Sube el video 4 (público, con miniatura, subtítulos y SEO) y después sus 3 Shorts enlazados.
Ejecutar desde la raíz del repo, con confirmación explícita: python videos/04_chapo/subir_todo.py --confirmar
"""
import json, sys
from pathlib import Path
from googleapiclient.http import MediaFileUpload
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ugc_agency.youtube.seo import Metadatos
from ugc_agency.youtube.publicar import subir, hacer_publico
from ugc_agency.youtube.auth import youtube

V = Path(__file__).parent
S = V / "shorts"
if "--confirmar" not in sys.argv:
    sys.exit("Falta --confirmar: este script publica en YouTube.")

meta = Metadatos.cargar(V / "metadatos.json")
r = subir(V / "video4_chapo_tunel.mp4", meta, None, None, privacidad="private", confirmar=True)
vid = r["id"]; URL = f"https://youtu.be/{vid}"; print("video largo:", URL)
yt = youtube()
yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(V / "miniatura.jpg"), mimetype="image/jpeg")).execute()
yt.captions().insert(part="snippet", body={"snippet": {"videoId": vid, "language": "es", "name": "Español"}},
    media_body=MediaFileUpload(str(V / "subtitulos_es.srt"), mimetype="application/octet-stream")).execute()
hacer_publico(vid, confirmar=True)
print("video largo público")

tags = ["fuga del chapo", "túnel del chapo", "ingeniería del túnel", "historia real", "altiplano fuga"]
items = [
 ("short1_cuanto_tardo.mp4", "short1_cuanto_tardo_miniatura.jpg", "¿Cuánto tardó el túnel del Chapo? 🤔",
  "Un túnel de 1,5 km bajo una prisión de máxima seguridad. ¿Cuánto tiempo crees que tomó? Escribe tu respuesta en los comentarios."),
 ("short2_tunel.mp4", "short2_tunel_miniatura.jpg", "Un túnel de 1,5 km bajo una prisión | Fuga del Chapo",
  "La ingeniería detrás de la fuga de 2015: luz, ventilación y tierra que nadie vio salir."),
 ("short3_meses.mp4", "short3_meses_miniatura.jpg", "¿Cuántos meses tomó? La respuesta te sorprende",
  "Los expertos estiman entre 12 y 24 meses de obra. Así lo calcularon."),
]
res = [{"video_largo": URL, "id": vid}]
for vf, mf, t, d in items:
    m = Metadatos(titulo=t, descripcion=f"{d}\n\n▶ Historia completa: {URL}\n\nSuscríbete para más historias reales.",
                  etiquetas=tags, hashtags=["Shorts", "HistoriaReal"], categoria="27", idioma="es", contenido_sintetico=False)
    rs = subir(S / vf, m, None, None, privacidad="public", confirmar=True)
    try:
        yt.thumbnails().set(videoId=rs["id"], media_body=MediaFileUpload(str(S / mf), mimetype="image/jpeg")).execute()
    except Exception as e:
        print("miniatura del short NO:", str(e)[:120])
    print(t, "→", rs["url"])
    res.append({"titulo": t, "url": rs["url"], "id": rs["id"]})
(V / "publicados.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
print("listo")
