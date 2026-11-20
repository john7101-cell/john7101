"""Sube los 3 Shorts de mitos y leyendas como públicos, con miniatura y SEO.
Uso: python shorts_mitos/subir_mitos.py --confirmar
"""
import json, sys
from pathlib import Path
from googleapiclient.http import MediaFileUpload
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ugc_agency.youtube.seo import Metadatos
from ugc_agency.youtube.publicar import subir
from ugc_agency.youtube.auth import youtube
if "--confirmar" not in sys.argv:
    sys.exit("Falta --confirmar: este script publica en YouTube.")
D = Path(__file__).parent
G = json.loads((D / "guiones.json").read_text())
DESC = {
 "llorona": "Según la tradición mexicana, La Llorona busca a sus hijos junto a los canales de noche. ¿La escucharías? Escribe tu respuesta en los comentarios.\n\nMás mitos y leyendas de Latinoamérica en el canal.",
 "cadejo": "En Centroamérica, El Cadejo es un perro negro de ojos rojos: para unos, un protector; para otros, un mal presagio. ¿Qué crees tú? Escríbelo en los comentarios.\n\nMás mitos y leyendas de Latinoamérica en el canal.",
 "patasola": "Según la leyenda colombiana, La Patasola es una mujer con una sola pierna que atrae a los viajeros al bosque. ¿Te perderías por seguir una voz? Cuéntanos en los comentarios.\n\nMás mitos y leyendas de Latinoamérica en el canal.",
}
HT = ["MitosYLeyendas", "LatinoAmerica", "Shorts"]
res = []
yt = youtube()
for s in G["shorts"]:
    sid = s["id"]
    m = Metadatos(titulo=s["titulo"], descripcion=DESC[sid] + "\n\nFuentes: " + "; ".join(s["fuentes"]),
                  etiquetas=s["etiquetas"], hashtags=HT, categoria="27", idioma="es", contenido_sintetico=False)
    print(sid, "validar:", m.validar() or "OK")
    r = subir(D / sid / f"short_{sid}.mp4", m, None, None, privacidad="public", confirmar=True)
    try:
        yt.thumbnails().set(videoId=r["id"], media_body=MediaFileUpload(str(D / sid / "miniatura.jpg"), mimetype="image/jpeg")).execute()
        print("miniatura OK")
    except Exception as e:
        print("miniatura NO:", str(e)[:120])
    res.append({"id": sid, "url": r["url"]})
(D / "publicados.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
print(res)
