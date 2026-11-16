---
name: yt-analitica
description: Analiza el rendimiento de un canal o video de YouTube (CTR, retención, vistas, suscriptores, horas hacia el YPP) y decide qué repetir, corregir o dejar. Úsala cuando compartan métricas o capturas de YouTube Studio, pregunten por qué un video no funciona o pidan el reporte semanal del canal.
---

# Analítica de YouTube

1. **Datos**: `python -m ugc_agency yt-estado` para el progreso al YPP; si la persona comparte capturas de Studio, extrae los números. Si está conectado Windsor.ai (`youtube`), se puede leer datos por video. No inventes números: marca lo que falta.
2. **Diagnóstico por embudo** (compara contra la media del propio canal, no contra promedios genéricos):
   - Impresiones bajas → tema/título sin demanda o poca coherencia de nicho.
   - CTR bajo (<4% en long-form suele indicar problema) → miniatura y título; probar variantes A/B.
   - Retención baja en los primeros 30 s → gancho no cumple la promesa del título; reescribir intro.
   - Caídas a mitad → bloques lentos; cortar, añadir cambios visuales y loops abiertos.
   - Buena retención pero pocos subs → falta de serie/CTA hacia el siguiente video.
3. **Decisión**: por cada video: *duplicar* (hacer secuela/variante del formato), *corregir* (cambiar miniatura/título, ya que se puede hacer después de publicar), o *abandonar* el formato.
4. **Reporte semanal**: tabla de videos (impresiones, CTR, duración media vista, % visto, subs), progreso subs/horas con ritmo necesario por semana para llegar al YPP en la fecha objetivo, 3 acciones para la próxima semana.
5. Para canales de TikTok/Meta usa el subagente `analista-tiktok-us`.
