---
name: yt-seo-metadatos
description: Escribe título, descripción, capítulos, etiquetas y hashtags de un video de YouTube y genera el meta.json que valida y usa yt-publicar. Úsala para SEO de YouTube, títulos con alto CTR, descripciones, capítulos o cuando haya que preparar metadatos antes de subir.
---

# SEO y metadatos de YouTube

## Título (lo más importante después de la miniatura)
- 40-60 caracteres; palabra clave principal en las primeras 3-4 palabras si el video es de búsqueda.
- Una promesa concreta + curiosidad: número, resultado, contraste o error ("Dejé de hacer X y pasó esto").
- Sin clickbait que el video no cumple (destruye la retención y el algoritmo lo castiga). Sin MAYÚSCULAS completas.
- Entrega 5 opciones y recomienda una; las otras sirven para la prueba de títulos de Studio.

## Descripción
- Primeras 2 líneas (lo que se ve sin expandir): resumen con la palabra clave y un gancho.
- Luego: qué aprenderá, enlaces (afiliados con divulgación), videos relacionados, capítulos y 3-5 hashtags.
- Máx. 5000 bytes.

## Capítulos
Empiezan en 0:00, mínimo 3, cada uno ≥10 s, con nombres que contengan términos buscables.

## Etiquetas y hashtags
Etiquetas: pocas y relevantes (marca del canal, palabra clave, variantes con errores comunes); total ≤500 caracteres. Hashtags: 3-5 (más de 15 = YouTube los ignora).

## Formato de salida (`meta.json`, lo lee `ugc_agency/youtube/seo.py`)
```json
{
  "titulo": "…",
  "descripcion": "…",
  "etiquetas": ["…"],
  "hashtags": ["#…"],
  "capitulos": [[0, "Introducción"], [45, "…"], [180, "…"]],
  "categoria": "27",
  "idioma": "es",
  "contenido_sintetico": true,
  "para_ninos": false
}
```
`contenido_sintetico` debe ser `true` si hay voz clonada o personas/escenas realistas generadas con IA. Valida con `Metadatos.cargar(ruta).validar()` y corrige todo lo que devuelva antes de subir.
