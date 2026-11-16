# VOLVER A MÍ — Animar fotos reales del sitio en Flow

## Cómo hacerlo en Flow
1. Crea un proyecto y elige **Frames to Video** (o «Imagen a video»).
2. Sube la foto del sitio como **primer fotograma** (First frame). Déjala sin último fotograma.
3. Formato **9:16**. Si la foto es horizontal, Flow la recorta: centra lo importante o pide el recorte vertical antes.
4. Pega el prompt de abajo según el tipo de foto + el bloque de **realismo**.
5. Genera 2 tomas y quédate con la que menos «invente» cosas.

## Bloque de realismo (pégalo al final de TODOS)
```
Keep the place exactly as in the photo: same architecture, furniture, colors and layout. Do not add or remove buildings, objects, signs or text. Realistic, natural motion only, as if filmed with a real camera on a gimbal. Photorealistic, 4K, natural light, no distortion, no morphing. Ambient sound only.
```

## Reglas para que se vea real
- **Un solo movimiento de cámara** lento por clip (empuje, paneo o subida). Nada de giros bruscos.
- Anima lo que se movería de verdad: hojas, niebla, nubes, agua, cortinas, velas, luz.
- Si añades personas, que sean pocas, de espaldas o a lo lejos: las caras y manos son lo que más delata la IA.
- No pidas cambiar la hora del día ni el clima: eso deforma la foto.

## Prompts por tipo de foto

**Fachada / entrada del hotel**
```
Slow, smooth dolly-in towards the entrance of this boutique hotel. Leaves and flowers sway gently in the breeze, soft clouds drift in the sky, warm afternoon sunlight.
```

**Vista aérea o panorámica de montañas (Santa Elena)**
```
Slow aerial drone-style forward glide over the landscape. Light mist moves through the valleys, clouds drift slowly, pine trees sway slightly. Calm and majestic.
```

**Jardín / sendero**
```
Slow gimbal walk forward along the garden path. Plants and flowers move softly with the wind, sunlight flickers through the leaves, a butterfly crosses the frame.
```

**Salón donde será el encuentro (vacío)**
```
Slow lateral slide across the room. Soft sunlight moves across the floor, curtains move gently, candles flicker, dust particles float in the warm light. Cozy and welcoming atmosphere.
```

**Salón con mujeres (añadir personas)**
```
Slow push-in. A small group of women sit in a circle in this room, seen from behind and in soft focus, talking calmly and listening. Warm light, intimate atmosphere. Keep the room exactly as in the photo.
```

**Terraza / balcón con vista**
```
Slow push-in towards the view. Clouds and mist drift over the mountains, plants on the terrace sway gently, warm golden-hour light.
```

**Habitación / detalle de decoración (cojines, tazas, flores, velas)**
```
Very slow macro push-in. Candle flames flicker, steam rises from the coffee cup, petals move slightly, soft bokeh in the background.
```

**Chimenea / zona de fogata**
```
Static camera with a very slow push-in. The fire crackles and the flames move naturally, warm light flickers on the wood and walls.
```

## Dónde va cada clip en las historias
| Historia | Foto recomendada |
|---|---|
| 5 – La propuesta | fachada/entrada (llegada) + salón con o sin mujeres |
| 6 – La cita contigo | panorámica de montañas + fachada (con los datos encima) |
| 7 – Vuelve a ti | jardín/sendero o terraza al atardecer (espacio abajo para el sticker de reserva) |

---

# Prompts para las fotos reales del sitio

Formato recomendado en Flow: **16:9** (las fotos son horizontales; en 9:16 Flow recortaría o inventaría los lados).
Yo monto el clip en vertical para la historia, con fondo desenfocado y los textos arriba y abajo.

## Foto 1 · Patio colonial de noche (`fotos/patio-original.jpg`)

**1A · Sin personas (historia 6: «tienes una cita contigo» + datos)**
```
Very slow, smooth dolly-in towards the central stone fountain of this colonial courtyard at blue hour. Water flows gently from the fountain, soft ripples and warm light reflections shimmer on the wet tiled floor, palm fronds and hanging plants sway slightly in a light breeze, warm interior lights glow through the arched green stained-glass windows, a few clouds drift slowly in the deep blue sky. Keep the place exactly as in the photo: same architecture, colors, furniture and layout. Do not add or remove objects, signs or text. Realistic camera on a gimbal, photorealistic, natural motion only, no morphing. Ambient sound of water and night insects.
```

**1B · Con mujeres llegando (historia 7: «esta vez, vuelve a ti»)**
```
Static camera with a very slow push-in on this colonial courtyard at blue hour. Two women walk slowly from the left side towards the arched entrance, seen from behind, relaxed and smiling to each other, their reflections on the wet tiled floor. The fountain water flows gently, palms sway slightly, warm lights glow from the windows. Keep the place exactly as in the photo. Photorealistic, natural motion only, no morphing. Ambient sound.
```

## Foto 2 · Salón con vista al bosque (`fotos/salon-sin-logo.jpg`)
Usa la versión **sin logo** (le recorté el muñequito de la esquina; si no, Flow lo anima).

**2A · Sin personas (historia 5: «Volver a mí… un encuentro para ti»)**
```
Slow lateral camera slide from left to right along the cushioned window bench of this cozy rustic lounge. The warm fairy lights twinkle softly among the hanging vines, pine trees outside the large windows sway gently with light mist drifting through the forest, soft daylight comes in. Keep the room exactly as in the photo: same wooden chairs, tables, beams, cushions and stone floor. Do not add or remove objects or text. Realistic gimbal shot, photorealistic, natural motion only, no morphing. Ambient sound of soft wind and birds.
```

**2B · Con el grupo de mujeres (historia 5: «reconocer tus necesidades… fortalecer tu identidad»)**
```
Slow push-in into this cozy rustic lounge. A small group of five women of different ages sit together at the long wooden table by the window, seen mostly from behind and in profile, talking softly, one woman speaks while the others listen and nod, cups of coffee on the table. Fairy lights twinkle among the vines, pine trees sway outside with light mist. Keep the room exactly as in the photo. Photorealistic, natural motion, no morphing, no distorted faces or hands. Ambient sound of soft conversation.
```
