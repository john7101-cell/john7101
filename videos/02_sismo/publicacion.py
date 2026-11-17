"""Paquete de publicación del video 2: metadatos SEO, capítulos, subtítulos SRT y miniatura JPG."""
import json, re, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ugc_agency.youtube.seo import Metadatos

ROOT = Path(__file__).parent
SEG = json.loads((ROOT / "assets/segmentos.json").read_text())
G = json.loads((ROOT / "guion.json").read_text())
FIRST = {}
for s in SEG:
    FIRST.setdefault(s["escena"], s["ini"])

CAP = [("gancho", "El minuto que cambió la ciudad"), ("quiz", "¿Cuál crees que cayó?"), ("suelo", "El suelo de la ciudad"),
       ("resonancia", "La ciencia: resonancia"), ("hospital", "Hospital Juárez"), ("bebes", "Los bebés rescatados"),
       ("topos", "Los Topos"), ("cifras", "¿Cuántos murieron?"), ("consejo", "Qué hacer en un sismo"),
       ("cierre", "La respuesta")]
capitulos = [(0 if i == 0 else round(FIRST[e] - .2), n) for i, (e, n) in enumerate(CAP)]

fuentes = "\n".join(f"• {f}" for f in G["fuentes"])
desc = f"""¿Por qué cayó ESE edificio en el terremoto de 1985 y el de al lado se quedó de pie? La respuesta no es la suerte: es la ciencia.

El 19 de septiembre de 1985, poco después de las 7:19 de la mañana, la Ciudad de México se sacudió. Aquí explicamos qué pasó, por qué el suelo del antiguo lago amplificó el movimiento y qué es la resonancia que derrumbó edificios de altura intermedia.

También contamos la historia del Hospital Juárez, de los bebés rescatados y de los Topos, y por qué todavía no hay una cifra exacta de víctimas.

👉 Si te gustó la Isla de las Muñecas, aquí está la primera historia del canal: https://youtu.be/Op0bC0i-fQw

Fuentes consultadas:
{fuentes}

Las animaciones son ilustraciones, no imágenes reales de los hechos. Las cifras se presentan como rangos porque las fuentes no coinciden."""

meta = Metadatos(
    titulo="¿Por qué cayó ESE edificio en el terremoto del 85? La ciencia",
    descripcion=desc,
    etiquetas=["terremoto 1985", "sismo 1985", "terremoto 1985 méxico", "19 de septiembre 1985", "sismo 19 septiembre 1985",
               "ciudad de méxico terremoto", "hospital juárez 1985", "topos rescate 1985", "resonancia sísmica",
               "edificios terremoto", "historia de méxico", "terremoto explicado", "documental en español", "sismo cdmx"],
    hashtags=["Terremoto1985", "CDMX", "HistoriaDeMéxico"],
    capitulos=capitulos, categoria="27", idioma="es", contenido_sintetico=False, para_ninos=False,
)
print("\n".join(meta.validar()) or "metadatos OK", "| título", len(meta.titulo), "car.")
meta.guardar(ROOT / "metadatos.json")


def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02}:{int(m):02}:{s:06.3f}".replace(".", ",")


NUM = {"mil novecientos ochenta y cinco": "1985", "siete y diecinueve": "7:19", "cuatrocientos kilómetros": "400 km",
       "ocho punto uno": "8.1", "doce pisos": "12 pisos", "catorce": "14", "diez mil": "10,000"}
cues = []
for s in SEG:
    txt = s["texto"]
    for k, v in NUM.items():
        txt = txt.replace(k, v)
    words = txt.split()
    parts, cur = [], []
    for w in words:
        cur.append(w)
        if len(" ".join(cur)) > 42 and re.search(r"[,.:?!…]$", w) or len(" ".join(cur)) > 58:
            parts.append(cur); cur = []
    if cur: parts.append(cur)
    tot = sum(len(" ".join(p)) for p in parts); acc = 0; d = s["fin"] - s["ini"]
    for p in parts:
        l = len(" ".join(p))
        cues.append((s["ini"] + d * acc / tot, s["ini"] + d * (acc + l) / tot, " ".join(p))); acc += l
srt = "\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1))
(ROOT / "subtitulos_es.srt").write_text(srt, encoding="utf-8")
print(len(cues), "subtítulos")
