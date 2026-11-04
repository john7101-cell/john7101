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
