# Agencia UGC con IA para TikTok Shop USA

Una agencia de contenido UGC formada por **10 agentes de IA especializados** (Claude) que, a partir de la ficha de un producto, entregan guiones e ideas listos para producir, además de paquetes de producción de video. Todo está pensado para que parezca grabado por **gente común contando su día a día**, con el producto apareciendo de forma natural dentro de la historia.

El contenido final (guiones, voces y captions) sale en **inglés americano casual**, porque va para TikTok Shop USA. La interfaz y los briefs internos están en español.

## El equipo

| # | Agente | Qué hace | Entrega |
|---|---|---|---|
| 1 | **Analista de producto** | Traduce el producto a lenguaje cotidiano, detecta audiencias y los momentos del día en que el producto ayuda, y separa las afirmaciones permitidas de las prohibidas | `ProductBrief` |
| 2 | **Estratega de tendencias** | Elige formatos nativos de TikTok (day in my life, car talk, GRWM, reset with me, POV…), patrones de hook, ritmo y clichés que hay que evitar | `TrendInsights` |
| 3 | **Director de casting** | Crea personajes ficticios comunes (enfermera, papá en el *school pickup*, estudiante, abuela…) con vida, muletillas y lugares donde graban | `PersonaRoster` |
| 4 | **Creativo de historias** | Propone historias de la vida cotidiana donde el producto resuelve un momento real | `ConceptBoard` |
| 5 | **Guionista** | Escribe el guion de 20 a 45 s tal como habla la gente: hook, beats, voz en off y un CTA suave | `Script` |
| 6 | **Editor de autenticidad** | Califica la naturalidad del 1 al 10, marca el lenguaje de anuncio y pide reescrituras | `AuthenticityReview` |
| 7 | **Revisor de cumplimiento** | Revisa las políticas de TikTok Shop US y de la FTC: afirmaciones, salud, urgencia falsa y divulgaciones | `ComplianceReview` |
| 8 | **Director de escena** | Arma un shot list vertical 9:16 con estética de celular (selfie, tablero del carro, B-roll a mano) | `ShotList` |
| 9 | **Productor de video IA** | Escribe el prompt de referencia del personaje, un prompt por escena para generadores de video y la dirección de voz | `VideoProductionPack` |
| 10 | **Copywriter social** | Escribe el caption con la voz del personaje, los hashtags, el comentario fijado, la divulgación y el horario | `PostPackage` |

El **productor ejecutivo** (`orchestrator.py`) coordina todo:

```
Analista → Estratega → Casting → Creativo
                                    │
          ┌─────── por cada historia (en paralelo) ───────┐
          │  Guionista ⇄ Editor de autenticidad            │
          │           ⇄ Revisor de cumplimiento            │  ← bucle hasta aprobar
          │  → Director de escena → Productor de video IA  │     (o descartar)
          │  → Copywriter social                           │
          └────────────────────────────────────────────────┘
```

Una pieza solo se aprueba si la naturalidad llega al umbral (8/10 por defecto) **y** no tiene bloqueos de cumplimiento. Si no lo logra tras N revisiones, se descarta y queda registrada con el motivo.

## Instalación

```bash
pip install -e ".[dev]"
cp .env.example .env   # agrega tu ANTHROPIC_API_KEY (o usa `ant auth login`)
```

## Uso

1. Describe el producto en un JSON (hay ejemplos en `examples/`):

```json
{
  "name": "TrailMate 40oz Insulated Tumbler",
  "category": "Home & Kitchen / Drinkware",
  "price_usd": 24.99,
  "key_features": ["Fits most car cup holders", "Leak-resistant straw lid"],
  "verified_claims": ["Keeps drinks cold up to 24 hours (internal lab testing)"],
  "target_audience_hint": "Busy workers, nurses, parents",
  "brand_notes": "Avoid saying 'spill-proof'."
}
```

> `verified_claims` es importante: son las **únicas** afirmaciones de resultado que los guiones pueden usar.

2. Genera la campaña:

```bash
python -m ugc_agency run examples/insulated_tumbler.json --personas 3 --concepts 6 --out output/tumbler
```

Opciones: `--threshold` (naturalidad mínima), `--max-revisions`, `--parallel`, `--model` y `--effort`.

3. (Opcional) Genera las voces en off con ElevenLabs:

```bash
export ELEVENLABS_API_KEY=...
python -m ugc_agency voice output/tumbler --persona-voice p1=<voice_id> --persona-voice p2=<voice_id>
```

### Qué se genera

```
output/tumbler/
├── README.md                 # resumen: personajes y piezas aprobadas/rechazadas
├── campaign.json             # todo lo que produjo cada agente
└── c1-car-talk-before-my-shift/
    ├── brief.md              # guion, shot list, prompts de escena y publicación
    ├── video_prompts.json    # pack para el generador de video (referencia + escenas + voz)
    ├── voiceover.txt         # texto para TTS
    └── voiceover.mp3         # si usaste el comando `voice`
```

## Del guion al video

El **Productor de video IA** entrega prompts independientes de la herramienta, compatibles con Veo, Kling, Sora, Runway, Hailuo, etc.:

1. Genera la imagen de referencia del personaje con `character_reference_prompt` para mantener la misma cara y ropa en todas las escenas.
2. Genera cada escena (image-to-video) con su `video_prompt` y su `negative_prompt`.
3. Genera la voz (`voice` o ElevenLabs) y haz lip-sync si la escena es a cámara.
4. Monta en CapCut o Descript siguiendo `editing_notes`: captions automáticos, jump cuts y texto nativo.
5. Al publicar, **activa la etiqueta de contenido generado por IA** de TikTok y pon la divulgación (#ad / comisión).

La integración directa con APIs de generación de video no está incluida. Cada proveedor tiene su propia API y precios, y se puede agregar como un adaptador nuevo en `ugc_agency/production/`.

## Editor automático de video

Si ya tienes un video (grabado o generado con IA), el editor lo pule para que se vea profesional sin perder la naturalidad del UGC:

| Problema | Cómo lo detecta | Qué hace |
|---|---|---|
| Tirones / "paradas" cada fracción de segundo | Patrón de cuadros duplicados (video de 24/25 fps exportado a 30) | Elimina los duplicados y recupera los fps reales: el movimiento vuelve a ser fluido |
| Saltos de postura entre clips del avatar | Saltos bruscos de imagen cuadro a cuadro | Corte limpio alternando plano abierto / cerrado (punch-in de 12 %), como un cambio de cámara intencional. Con `--transition fade` usa un fundido |
| Cuadros "intrusos" de otra toma en una unión | Dos saltos separados por 1-4 cuadros | Los quita dentro del fundido |
| Pausas largas e inicio/final muertos | Transcripción palabra por palabra (Whisper) | Las acorta y deja unos 0.12 s de aire |
| Muletillas ("um", "uh", "hmm") | Transcripción | Las corta |
| Tomas repetidas (retakes) | Frases consecutivas casi iguales | Conserva solo la última toma |
| Cuadros negros | `blackdetect` | Los corta si no hay voz encima |
| Imágenes congeladas (típico de video IA) | `freezedetect` | Las corta si no hay voz; si la hay, lo avisa para regenerar esa escena |
| Destellos y transiciones mal generadas | Detección de escenas (planos de menos de 0.3 s) | Los corta, o los tapa con el cuadro anterior si hay voz |
| Formato y acabado | — | 1080x1920 (9:16), volumen a -14 LUFS, ligero contraste y nitidez, micro-fundidos de audio en cada corte |
| Subtítulos | Transcripción | Subtítulos estilo TikTok (2-3 palabras, mayúsculas, con contorno) quemados en el video y además un `.srt` |

```bash
pip install -e ".[editing]"     # también necesitas ffmpeg instalado
python -m ugc_agency edit mi_video.mp4
python -m ugc_agency edit "https://drive.google.com/file/d/XXXX/view"   # también Dropbox
```

> **Imágenes emergentes fuera de tiempo**: si las imágenes o gráficos vienen "quemados" en el video, el editor no puede moverlos automáticamente. Lo mejor es corregir su tiempo en el proyecto original (CapCut, Canva, etc.) usando la transcripción del reporte, que trae el segundo exacto de cada frase.

Se generan `mi_video_editado.mp4`, `mi_video_editado.srt` y `mi_video_editado.report.json` (cada corte con su motivo, avisos y transcripción).

Opciones útiles: `--no-repair` (no tocar tirones ni uniones), `--join-fade 0.2`, `--max-pause 0.6` (más relajado), `--keep-fillers`, `--keep-retakes`, `--no-captions`, `--keep-aspect`, `--language en` y `--whisper-model medium` (más preciso, más lento).

### Armar un reel con gráficos sincronizados

Si tienes los clips del avatar **sin gráficos** y las imágenes sueltas, el compositor arma el reel completo: une los clips (1080x1920), repara el movimiento, transcribe y coloca cada gráfico **anclado a la frase que lo menciona**. Así aparece en el momento exacto aunque cambie la edición.

```bash
python -m ugc_agency compose clip1.mp4 clip2.mp4 clip3.mp4 --graphics graficos.json --out reel.mp4
```

Para quitar frases de la narración agrega `"remove": [{"phrase": "en el horizonte"}]`: se cortan audio y video dejando una pausa natural, y los gráficos se reacomodan solos.

Cada gráfico define su imagen, su posición en píxeles y en qué frase entra y sale (ver `examples/graficos_ejemplo.json`). Las frases ignoran mayúsculas, acentos y puntuación; `offset` adelanta o atrasa en segundos y `"end": "video_end"` lo deja hasta el final.

## Reglas de la agencia

Están en `ugc_agency/guidelines.py` y se inyectan en todos los agentes:

- **Autenticidad**: personajes comunes, situaciones cotidianas, lenguaje hablado real con muletillas y autocorrecciones, imperfecciones y CTA suave. Está prohibido el *ad-speak* ("game-changer", "must-have", "you NEED this"…).
- **Cumplimiento**: solo afirmaciones verificadas; nada de salud ni antes/después; nada de urgencia falsa; nada de imitar a personas reales. **Etiqueta AIGC obligatoria** y divulgación de afiliado, porque los personajes son ficticios y generados con IA, y nunca se presentan como clientes reales.

Edita ese archivo para ajustar el estilo de tu agencia.

## Desarrollo

```bash
pytest   # prueba el pipeline completo con un LLM falso (no gasta créditos)
```

Por defecto usa el modelo `claude-opus-5-5` con esfuerzo `high` (configurable con `UGC_MODEL` / `UGC_EFFORT`). Cada agente responde con *structured outputs* validados con Pydantic, y las peticiones que rechace un clasificador de seguridad se reintentan automáticamente en otro modelo (`fallbacks: "default"`).
