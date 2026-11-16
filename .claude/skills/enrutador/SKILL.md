---
name: enrutador
description: Decide qué agente, habilidad o comando de la agencia UGC debe atender un pedido y lo despacha. Úsala cuando el usuario escriba /enrutador, o cuando un pedido sea ambiguo o mezcle varias tareas (guion, revisión, métricas, reel, voz, edición, YouTube) y haya que repartirlo entre el equipo en el orden correcto.
---

# Enrutador

Recibe un pedido, lo clasifica y lo manda al recurso adecuado. No hace el trabajo de fondo él mismo: decide, despacha y junta los resultados.

## 1. Clasifica el pedido

Lee el pedido (y los archivos o pantallazos adjuntos) y asígnale una o varias intenciones de esta tabla:

| Intención | Señales en el pedido | Destino |
|---|---|---|
| Escribir guion | "escribe", "guion", "reel", "teaser", "drama", tomas, voz clonada | Agente `guionista` |
| Revisar guion existente | Pega un guion ya escrito, "revisa", "mejora", "¿está bien?" | Agente `revisor-de-guiones` |
| Analizar canal / pauta | Pantallazos o números de TikTok, TikTok Shop o Meta Ads; "qué escalo", "qué pauso", ROAS, CTR | Agente `analista-tiktok-us` |
| Video animado vertical hecho con código | "hazme el reel", "TikTok animado", subtítulos, portada | Habilidad `becario-reels` |
| Campaña UGC desde ficha de producto | JSON de producto, "campaña", "ideas UGC" | `python -m ugc_agency run <producto.json>` |
| Voces en off | "genera las voces", ElevenLabs, voice_id | `python -m ugc_agency voice` (o herramientas ElevenLabs) |
| Editar un video grabado | Quitar pausas, muletillas, retakes | `python -m ugc_agency edit` |
| Armar reel con clips + gráficos | Clips limpios y gráficos anclados a frases | `python -m ugc_agency compose` |
| Limpiar voz clonada/TTS | Fragmentos fantasma, silencios largos | `python -m ugc_agency limpiar-voz` |
| Diagnóstico rápido de métricas en CSV/JSON | Archivo de métricas, semáforo, ROAS de equilibrio | `python -m ugc_agency metricas` |
| YouTube | Estado del canal, ideas, miniatura, publicar | `python -m ugc_agency yt-estado / yt-ideas / yt-miniatura / yt-publicar` |
| Ninguna de las anteriores | — | Resuélvelo tú directamente, sin despachar |

Antes de usar un comando, revisa sus opciones con `python -m ugc_agency <comando> --help`.

## 2. Ordena el flujo

Si hay varias intenciones, encadénalas en este orden y pasa la salida de cada paso al siguiente:

1. Análisis (`analista-tiktok-us`) — define qué conviene crear.
2. Guion (`guionista`).
3. Revisión (`revisor-de-guiones`). Si el puntaje no aprueba, devuelve los cambios al `guionista` una vez más como máximo y vuelve a revisar.
4. Producción: voz, edición, `compose` o `becario-reels`.
5. Publicación (YouTube) solo si el usuario lo pidió explícitamente.

Pasos independientes (por ejemplo, analizar dos cuentas distintas) pueden ir en paralelo.

## 3. Pregunta solo si hace falta

Pregunta al usuario únicamente cuando falte algo que cambia el destino o el resultado: no está claro si quiere escribir o revisar, falta el producto, la plataforma o la duración. Si hay un valor por defecto razonable, úsalo y dilo.

Pide confirmación antes de cualquier acción que gaste créditos (generar voces o video) o que publique algo hacia afuera (subir a YouTube, cambiar pauta).

## 4. Entrega

Responde en español con:

- **Ruta elegida**: qué agente, habilidad o comando atendió cada parte y por qué, en una línea cada uno.
- **Resultado**: lo que entregó cada paso (guion, diagnóstico, rutas de archivos generados).
- **Siguiente paso sugerido**, si lo hay.
