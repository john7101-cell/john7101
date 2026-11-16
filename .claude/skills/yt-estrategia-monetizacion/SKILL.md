---
name: yt-estrategia-monetizacion
description: Plan para monetizar un canal de YouTube desde cero lo más rápido posible - elegir nicho por RPM y demanda, ruta al Programa de Socios (YPP), calendario semanal y fuentes de ingreso antes de los 1000 suscriptores. Úsala cuando pidan crear/arrancar un canal, elegir nicho, "cómo monetizar", plan de crecimiento o revisar el progreso hacia la monetización.
---

# Estrategia de monetización de YouTube (canal desde cero)

## 1. Diagnóstico inicial
- Si hay credenciales (`YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`), corre `python -m ugc_agency yt-estado` y parte de esos números. Si no, guía con `docs/youtube_conexion.md`. Nunca pidas claves en el chat.
- Pregunta solo lo imprescindible: idioma/mercado, si la persona sale en cámara o el canal es "faceless", horas por semana y presupuesto.

## 2. Requisitos del YPP (verificar siempre en YouTube Studio > Ganar dinero; cambian)
| Nivel | Requisitos | Desbloquea |
|---|---|---|
| Ampliado (países elegibles) | 500 subs + 3 subidas públicas en 90 días + (3000 h de visualización en 365 días **o** 3M vistas de Shorts en 90 días) | Membresías, Super Thanks/Chat, Shopping |
| Completo | 1000 subs + (4000 h en 365 días **o** 10M vistas de Shorts en 90 días) | Ingresos por anuncios (long-form y Shorts) |
Además: 2FA activada, cuenta de AdSense, sin advertencias activas, y cumplir las políticas de monetización (ver skill `yt-politicas-ia`).

## 3. Elegir nicho (la decisión que más acelera)
Puntúa 1-5 cada candidato y elige el mayor total:
- **RPM**: finanzas, inversión, software/IA, negocios, seguros, bienes raíces, salud (cuidado con claims) > tecnología/educación > entretenimiento, gaming, vlogs, humor.
- **Demanda comprobada**: `python -m ugc_agency yt-ideas "<tema>" --region <país>`; busca canales pequeños (<10k subs) con videos que superan 5-10x sus suscriptores = hueco.
- **Capacidad de producir 3-5 videos/semana** con el pipeline del repo (guion → voz → edición → miniatura).
- **Riesgo de política**: evita compilaciones, reuploads, contenido de terceros, "noticias" leídas por TTS sin aporte.
Idioma: español tiene RPM menor que inglés pero menos competencia; para EE. UU. hispano el RPM suele ser mayor que LATAM.

## 4. Ruta más rápida recomendada (modelo híbrido)
- **Long-form 8-15 min** (2-3/semana): suma horas de visualización y es donde está el RPM. Series con el mismo formato para que el algoritmo aprenda a quién mostrarlo.
- **Shorts** (1/día): suman suscriptores rápido; cada Short apunta a un video largo (función "video relacionado").
- Las 4000 h equivalen a ~24.000 vistas de 10 min con 50% de retención: planifica desde ahí.
- Un video largo "pilar" por semana orientado a búsqueda (evergreen) + uno orientado a navegación/tendencia.

## 5. Ingresos antes del YPP (día 1)
Afiliados (Amazon, software con comisiones recurrentes), producto digital propio, patrocinios pequeños, lead magnet → email. Siempre con divulgación ("Incluye contenido pagado" en Studio + mención en el video).

## 6. Entregable
Devuelve: nicho elegido con puntuación, 3 formatos de serie, 20 títulos iniciales, calendario de 4 semanas (día, formato, título, objetivo: búsqueda/navegación), metas semanales (subs, horas) y los hitos de revisión. Luego ofrece pasar a la skill `yt-produccion-video`.
