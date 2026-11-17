"""Paquete de publicación del video 1: metadatos SEO, subtítulos SRT y miniatura JPG."""
import json, re
from pathlib import Path
from PIL import Image
from build import NUM, SEGS, S
import sys; sys.path.insert(0, str(Path(__file__).parents[2]))
from ugc_agency.youtube.seo import Metadatos

ROOT = Path(__file__).parent

desc = """La Isla de las Muñecas de Xochimilco es famosa por una leyenda: un hombre que pasó 50 años colgando muñecas para calmar el espíritu de una niña ahogada. Pero ¿esa niña existió? Separamos lo COMPROBADO de la LEYENDA.

En este video: quién fue Julián Santana Barrera, por qué se fue a vivir solo a una chinampa del lago de Teshuilo, qué pasó en 2001, qué dice su propia familia y por qué la verdadera historia es más triste… y más humana que la versión de terror.

👉 Próximo video: los 2 minutos que cambiaron la Ciudad de México para siempre (19 de septiembre de 1985). Suscríbete para no perderlo.

Fuentes consultadas:
• Infobae (2024): ¿Quién es el dueño de la Isla de las Muñecas en Xochimilco?
• AFP / BioBioChile (2019): La oscura historia de la Isla de las Muñecas
• Wikipedia: Island of the Dolls
• UNESCO: Centro histórico de México y Xochimilco (1987)

Animación y narración producidas con herramientas digitales. Las escenas son ilustraciones, no imágenes reales."""

capitulos = [(0, "El hombre de las muñecas"), (S(9) - .2, "Xochimilco: el lugar"), (S(18) - .2, "¿Quién era Julián Santana?"),
             (S(29) - .2, "La leyenda de la niña"), (S(40) - .2, "Medio siglo de muñecas"), (S(50) - .2, "2001"),
             (S(58) - .2, "Lo que no te contaron"), (S(70) - .2, "La isla hoy"), (S(73) - .2, "La verdadera historia")]

meta = Metadatos(
    titulo="La VERDADERA historia de la Isla de las Muñecas: ¿y la niña?",
    descripcion=desc,
    etiquetas=["isla de las muñecas", "la isla de las muñecas", "isla de las muñecas historia", "isla de las muñecas xochimilco",
               "historia real isla de las muñecas", "julián santana barrera", "xochimilco", "leyendas de méxico",
               "misterios de méxico", "historia de méxico", "leyendas mexicanas", "lugares embrujados de méxico",
               "documental en español", "historias de terror reales", "chinampas", "isla de las muñecas explicada"],
    hashtags=["IslaDeLasMuñecas", "Xochimilco", "MisteriosDeMéxico"],
    capitulos=[(round(t), n) for t, n in capitulos],
    categoria="27", idioma="es", contenido_sintetico=False, para_ninos=False,
)
print("\n".join(meta.validar()) or "metadatos OK", "| título", len(meta.titulo), "car.")
meta.guardar(ROOT / "metadatos.json")

def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02}:{int(m):02}:{s:06.3f}".replace(".", ",")

cues = []
for s in SEGS:
    txt = s["texto"]
    for k, v in NUM.items():
        txt = txt.replace(k, v)
    words = txt.split()
    parts, cur = [], []
    for w in words:
        cur.append(w)
        if len(" ".join(cur)) > 38 and re.search(r"[,.:?!…]$", w) or len(" ".join(cur)) > 55:
            parts.append(cur); cur = []
    if cur: parts.append(cur)
    tot = sum(len(" ".join(p)) for p in parts); acc = 0; d = s["fin"] - s["ini"]
    for p in parts:
        l = len(" ".join(p))
        cues.append((s["ini"] + d * acc / tot, s["ini"] + d * (acc + l) / tot, " ".join(p))); acc += l
srt = "\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1))
(ROOT / "subtitulos_es.srt").write_text(srt, encoding="utf-8")
Image.open(ROOT / "miniatura.png").convert("RGB").save(ROOT / "miniatura.jpg", quality=92)
print(len(cues), "subtítulos ·", (ROOT / "miniatura.jpg").stat().st_size // 1024, "KB miniatura")
print(meta.descripcion_final()[-420:])
