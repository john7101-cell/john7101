"""Genera las fotos de producto de la maqueta con la API de imágenes de OpenAI.

Uso:  python tools/generar_fotos.py [id_producto ...]
Sin argumentos genera todas las que falten en public/img/. Necesita OPENAI_API_KEY.
"""
import base64, io, json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

OUT = os.path.join(os.path.dirname(__file__), '..', 'public', 'img')
MODEL = os.environ.get('OPENAI_IMAGE_MODEL', 'gpt-image-2')

STYLE = ("Professional high-end e-commerce product photograph, square composition, product centered and fully visible, "
         "soft natural window light from the left, warm cream beige seamless studio background, gentle soft shadow, "
         "one or two fresh green tropical leaves as a subtle accent at the edge, photorealistic, crisp detail, "
         "minimalist premium aesthetic. Any packaging text must be short, spelled exactly as given, and legible. "
         "No watermark, no extra text, no people.")

PRODUCTS = {
    'cafe-huila': "A kraft paper stand-up coffee bag with a white label that reads 'Café Altamira' and 'COLOMBIAN COFFEE', a few roasted coffee beans and a small wooden bowl of beans beside it.",
    'serum-sacha': "An amber glass dropper bottle of facial serum with a black dropper cap and a cream label that reads 'Selva Botánica' and 'BOTANICAL SERUM', a few small sacha inchi seeds beside it.",
    'crema-cacao': "A short wide frosted glass jar of whipped moisturizer cream with a wooden lid, the lid off showing the white cream texture, label reads 'Tierra Maya', a piece of raw cacao pod beside it.",
    'jabon-romero': "A round green solid shampoo bar on a small wooden soap dish, a recycled paper box with label 'Raíz Pura' behind it, sprigs of fresh rosemary.",
    'maca': "A white matte supplement pouch with a dark green label that reads 'Inti Wasi' and 'MACA', a small ceramic bowl of beige maca powder with a wooden spoon.",
    'moringa': "A white supplement bottle with a green cap and a green label that reads 'Verde Vivo' and 'MORINGA', a few green capsules spilled beside it and fresh moringa leaves.",
    'yerba': "A green and kraft paper package of yerba mate that reads 'Campo Guaraní' and 'YERBA MATE', next to a traditional calabash mate gourd with a metal bombilla straw.",
    'chifles': "A golden-yellow snack bag of plantain chips that reads 'Costa Dorada' and 'CHIFLES', a small white bowl of thin crispy plantain chips beside it.",
    'chocolate': "A dark brown and gold wrapped artisan chocolate bar that reads 'Nacional' and '70% CACAO', partially unwrapped showing dark chocolate squares, a split cacao pod beside it.",
    'dulce-leche': "A glass jar of dulce de leche with a gingham fabric-covered lid and kraft label that reads 'La Estancia', a spoon with glossy caramel dripping.",
    'dog-treats': "A terracotta-orange resealable pouch of dog treats that reads 'Patitas' and 'DOG TREATS', a few dehydrated sweet potato chews on a small plate.",
    'pet-hammock': "A colorful hand-woven Guatemalan cotton cat hammock with red, blue and yellow traditional patterns, neatly displayed on a simple wooden frame, no animals.",
    'alpaca-beanie': "A soft heather grey baby alpaca knit beanie with a ribbed cuff and a small leather tag, neatly folded on a stack of knitted fabric.",
    'guayabera': "A neatly folded off-white linen guayabera shirt showing its pleats, four pockets and buttons, on a flat surface.",
    'tote': "A handmade Wayuu mochila crochet bag with vibrant teal, yellow, red and white geometric patterns and a long braided strap, standing upright.",
    'hero': "A curated group of Latin American artisan products arranged together: a kraft coffee bag labeled 'COLOMBIAN COFFEE', an amber dropper bottle of serum, a small jar of natural moisturizer, a dark chocolate bar, roasted coffee beans and green leaves. Wide inviting composition with empty space on the left.",
}

def generate(pid):
    path = os.path.join(OUT, f'{pid}.jpg')
    if os.path.exists(path) and pid not in sys.argv[1:]:
        return f'{pid}: ya existe'
    body = json.dumps({'model': MODEL, 'prompt': f"{PRODUCTS[pid]} {STYLE}", 'size': '1536x1024' if pid == 'hero' else '1024x1024',
                       'quality': 'medium', 'n': 1}).encode()
    req = urllib.request.Request('https://api.openai.com/v1/images/generations', data=body, headers={
        'Authorization': f"Bearer {os.environ.get('OPENAI_API_KEY', 'sk-proxy')}", 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    img = Image.open(io.BytesIO(base64.b64decode(data['data'][0]['b64_json']))).convert('RGB')
    img.thumbnail((1200, 800) if pid == 'hero' else (800, 800), Image.LANCZOS)
    img.save(path, 'JPEG', quality=82, optimize=True, progressive=True)
    return f'{pid}: {os.path.getsize(path) // 1024} KB'

def _safe(pid):
    try:
        return generate(pid)
    except Exception as e:  # noqa: BLE001
        detail = e.read().decode()[:300] if hasattr(e, 'read') else ''
        return f'{pid}: ERROR {e} {detail}'


def write_manifest():
    ids = sorted(f[:-4] for f in os.listdir(OUT) if f.endswith('.jpg'))
    with open(os.path.join(OUT, 'photos.js'), 'w') as fh:
        fh.write("// IDs de productos que tienen foto en esta carpeta (img/<id>.jpg). 'hero' = foto de portada.\n"
                 "// tools/generar_fotos.py actualiza esta lista; si agregas fotos a mano, añade aquí su id.\n"
                 f"window.PRODUCT_PHOTOS = {json.dumps(ids)};\n")


if __name__ == '__main__':
    ids = sys.argv[1:] or list(PRODUCTS)
    with ThreadPoolExecutor(max_workers=6) as ex:
        for res in ex.map(lambda p: _safe(p), ids):
            print(res, flush=True)
    write_manifest()
