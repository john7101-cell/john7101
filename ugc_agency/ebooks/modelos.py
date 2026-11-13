"""Modelos de datos de la editorial de ebooks."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class EbookBrief(BaseModel):
    """Lo que quiere el autor/editor. Lo que no esté aquí (datos, cifras, casos) NO se puede inventar."""

    tema: str = Field(description="Tema del libro, p. ej. 'finanzas personales para freelancers'")
    autor: str = Field(default="", description="Nombre que firma el libro (seudónimo permitido)")
    lector: str = Field(default="", description="Quién es el lector ideal y qué le pasa hoy")
    transformacion: str = Field(default="", description="Qué podrá hacer el lector al terminar el libro")
    idioma: str = Field(default="español latino neutro")
    tono: str = Field(default="cercano, claro y práctico, sin relleno")
    genero: Literal["guía práctica", "divulgación", "autoayuda", "negocios", "manual técnico", "recetario",
                    "memorias", "otro"] = "guía práctica"
    palabras_objetivo: int = Field(default=20000, ge=3000, le=150000, description="Extensión total aproximada")
    n_capitulos: int = Field(default=10, ge=3, le=40)
    mercado: str = Field(default="Amazon KDP en español", description="Dónde se venderá (afecta metadatos y formato)")
    precio_usd: float | None = Field(default=None, description="Precio previsto, si ya se decidió")
    competidores: list[str] = Field(default_factory=list, description="Libros que compiten (título — autor)")
    datos_confirmados: list[str] = Field(
        default_factory=list, description="Hechos, cifras, casos y fuentes verificados que el libro puede usar"
    )
    prohibido: list[str] = Field(default_factory=list, description="Promesas, temas o frases que no se pueden usar")
    material: str = Field(default="", description="Apuntes, transcripciones o borradores del autor")
    notas: str = Field(default="")


# ------------------------------------------------------------------ plan editorial
class PlanCapitulo(BaseModel):
    numero: int
    titulo: str = Field(description="Título comercial y concreto (promete un resultado o despierta curiosidad)")
    objetivo: str = Field(description="Qué sabrá o podrá hacer el lector al terminar el capítulo")
    gancho: str = Field(description="Cómo abre: escena, pregunta, dato confirmado o error común")
    puntos: list[str] = Field(description="Secciones/ideas en orden (4-8)")
    herramienta: str = Field(default="", description="Ejercicio, plantilla, checklist o paso a paso que incluye")
    palabras: int = Field(description="Extensión objetivo del capítulo")


class PlanEditorial(BaseModel):
    titulo: str = Field(description="Título corto y memorable (2-6 palabras)")
    subtitulo: str = Field(description="Promesa concreta + para quién (lo que se busca en Amazon)")
    alternativas_titulo: list[str] = Field(description="3-5 títulos alternativos")
    promesa: str = Field(description="La transformación en una frase")
    lector_ideal: str = Field(description="Retrato del lector: situación, dolor, deseo, objeciones")
    angulo: str = Field(description="Qué hace distinto a este libro frente a la competencia")
    voz: str = Field(description="Guía de voz del autor: persona gramatical, registro, ritmo, qué evitar")
    introduccion: str = Field(description="Qué debe lograr la introducción (gancho, promesa, cómo usar el libro)")
    capitulos: list[PlanCapitulo]
    cierre: str = Field(description="Qué debe lograr la conclusión (síntesis, siguiente paso, llamada a reseñar)")
    pendientes: list[str] = Field(default_factory=list, description="Datos que faltan y el autor debe aportar")


# ------------------------------------------------------------------ escritura y revisión
class Capitulo(BaseModel):
    numero: int = Field(description="0 = introducción; 99 = conclusión")
    titulo: str
    contenido: str = Field(
        description="Texto completo en Markdown. Empieza en el primer párrafo (sin repetir el título como '#'). "
        "Secciones con '##', recuadros con '> **Clave:** …', listas y tablas cuando ayuden."
    )
    resumen: str = Field(description="Resumen de 3-5 frases para dar continuidad a los capítulos siguientes")
    ideas_clave: list[str] = Field(description="3-6 ideas que el lector se lleva")
    pendientes: list[str] = Field(default_factory=list, description="Datos que faltan, marcados en el texto como [PENDIENTE: …]")


class Criterio(BaseModel):
    nombre: str
    puntaje: int = Field(ge=1, le=10)
    comentario: str


class RevisionCapitulo(BaseModel):
    criterios: list[Criterio]
    aprobado: bool
    resumen: str
    problemas: list[str] = Field(default_factory=list, description="Problemas concretos, citando el pasaje")
    reescrituras: list[str] = Field(default_factory=list, description="Cambios exactos: 'cambia X por Y porque…'")


class Hallazgo(BaseModel):
    nivel: Literal["error", "aviso", "info"]
    donde: str
    mensaje: str


# ------------------------------------------------------------------ venta
class FichaVenta(BaseModel):
    descripcion_html: str = Field(description="Descripción de Amazon en HTML simple (<p>, <b>, <i>, <ul>, <li>, <h2>), ≤ 4000 caracteres")
    contraportada: str = Field(description="Texto de contraportada, 120-180 palabras")
    palabras_clave: list[str] = Field(description="Exactamente 7 frases de búsqueda (≤ 50 caracteres cada una), sin repetir el título")
    categorias: list[str] = Field(description="3 rutas de categoría BISAC/Amazon sugeridas")
    bio_autor: str = Field(description="Biografía breve; si no hay datos del autor, deja [PENDIENTE]")
    texto_portada: str = Field(description="Frase corta para la portada (≤ 8 palabras), opcional pero recomendable")
    precio_sugerido: str = Field(description="Rango de precio y razón (regalías KDP 70 % entre 2,99 y 9,99 USD)")
    llamada_resena: str = Field(description="Párrafo final pidiendo una reseña, sin incentivos (cumple política de Amazon)")
