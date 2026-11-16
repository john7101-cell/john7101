---
name: yt-produccion-video
description: Pipeline completo para producir y publicar un video de YouTube con las herramientas del repo - idea, guion, voz, edición, miniatura, metadatos y subida (privada o programada). Úsala cuando pidan "haz un video", "produce el episodio", "sube el video", automatizar la producción o procesar un lote de videos.
---

# Producción y publicación de videos (pipeline del repo)

Sigue los pasos en orden; no te saltes revisiones. Guarda todo en `salidas/<slug>/`.

1. **Idea validada**: `python -m ugc_agency yt-ideas "<tema>" --dias 90 --region <país>`. Elige un ángulo con prueba de demanda; anota el video de referencia y por qué funcionó.
2. **Guion**: usa el subagente `guionista` (o `python -m ugc_agency guion ...`). Estructura long-form: gancho 0-30 s que repite la promesa del título/miniatura → contexto mínimo → bloques con "loops" abiertos → payoff → CTA a otro video (no "suscríbete" al inicio). Revisión con `revisor-de-guiones` / `guion-revisar` hasta aprobar.
3. **Voz**: `python -m ugc_agency voice ...` (ElevenLabs) y después `python -m ugc_agency limpiar-voz <audio>`.
4. **Edición**: `python -m ugc_agency edit ...` (quita pausas, muletillas, retakes) y `compose` para gráficos anclados a frases. Cambio visual cada 3-6 s en long-form, cada 1-2 s en Shorts.
5. **Miniatura**: `python -m ugc_agency yt-miniatura <fondo> --linea "Texto" --linea "*acento*" --out salidas/<slug>/mini.jpg`. Máx. 3-4 palabras, una cara/objeto grande, contraste alto; no repitas el título. Haz 2-3 variantes para la prueba A/B de Studio ("Probar y comparar").
6. **Metadatos**: skill `yt-seo-metadatos` → `salidas/<slug>/meta.json`.
7. **Subtítulos**: genera `.srt` desde el guion/transcripción (mejora accesibilidad y búsqueda).
8. **Publicación**: primero simula
   `python -m ugc_agency yt-publicar video.mp4 --meta meta.json --miniatura mini.jpg --subtitulos subs.srt --programar 2026-11-20T18:00:00-05:00`
   y solo con confirmación explícita de la persona añade `--confirmar`. Sube siempre privado o programado, nunca público directo.
9. **Post-publicación**: comentario fijado con pregunta, pantalla final hacia el siguiente video, añadir a lista de reproducción de la serie. A las 48 h pasa a la skill `yt-analitica`.

## Lotes (automatización)
Para varios videos, crea una carpeta por slug y un `plan.json` con título, fecha y estado de cada paso; avanza paso a paso y marca el estado. Programa las subidas espaciadas (mismo horario, días fijos). No publiques en masa contenido casi idéntico (ver `yt-politicas-ia`).
