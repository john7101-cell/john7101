---
name: yt-politicas-ia
description: Revisa que un canal o video de YouTube cumpla las políticas de monetización y de contenido con IA antes de publicar - contenido no auténtico/repetitivo, reutilizado, divulgación de contenido sintético, derechos de autor, contenido para niños y afiliados. Úsala antes de solicitar el YPP, antes de publicar un lote automatizado o cuando la monetización sea rechazada.
---

# Políticas de YouTube para canales automatizados con IA

Las políticas cambian: confirma en la ayuda de YouTube (Políticas de monetización de canales) antes de dar un veredicto final.

## Riesgos que hacen rechazar el YPP en canales automatizados
- **Contenido no auténtico** (antes "repetitivo"): videos producidos en masa con la misma plantilla y cambios mínimos, slideshows con TTS sin aporte, listas genéricas. Solución: guion original con punto de vista, investigación propia, variedad real de formato y edición.
- **Contenido reutilizado**: clips, películas, música, videos de otros canales o compilaciones sin comentario/transformación significativa.
- **Derechos de autor**: solo música/imágenes con licencia (Biblioteca de audio de YouTube, stock con licencia, generación propia). Guarda las licencias.

## Obligaciones
- **Contenido alterado o sintético**: marcar en Studio (y `"contenido_sintetico": true` en `meta.json`) cuando hay voz clonada, personas realistas generadas, o escenas realistas que no ocurrieron. No hace falta para guiones, subtítulos o efectos claramente irreales.
- **Voz clonada**: solo de la propia persona o con permiso por escrito.
- **Para niños (COPPA)**: declararlo con honestidad; si es para niños se pierden comentarios y anuncios personalizados.
- **Afiliados/patrocinios**: casilla "Incluye promoción pagada" + mención verbal/escrita.
- **Claims**: nada de promesas de salud, dinero rápido garantizado o datos inventados (atenta contra las normas de anunciantes y la confianza).

## Checklist antes de publicar / solicitar YPP
- [ ] Cada video aporta algo propio (análisis, explicación, historia) que no estaría sin el creador.
- [ ] Los últimos videos no comparten plantilla idéntica con solo el tema cambiado.
- [ ] Toda música, imagen y clip tiene licencia o es original.
- [ ] Contenido sintético declarado donde corresponde.
- [ ] Título y miniatura cumplen lo que el video entrega.
- [ ] Sin advertencias de normas de la comunidad activas; 2FA activada.
Devuelve: veredicto (OK / corregir / alto riesgo), cada problema con el video y minuto, y el cambio concreto.
