"""Modelos de datos del estudio de guiones."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class GuionBrief(BaseModel):
    """Lo que el cliente o la agencia quiere comunicar. Todo lo que no esté aquí NO se puede inventar."""

    tema: str = Field(description="De qué trata el video (p. ej. 'Taller Volver a mí')")
    objetivo: str = Field(default="", description="Qué debe lograr: expectativa, venta, seguidores, reconocimiento")
    audiencia: str = Field(default="", description="A quién le habla")
    tono: str = Field(default="cercano y cálido", description="Tono general de la voz")
    formato: str = Field(default="reel", description="reel, teaser, historia dramática, anuncio, video de YouTube…")
    duracion_s: int = Field(default=30, ge=5, le=900, description="Duración total objetivo en segundos")
    n_tomas: int = Field(default=4, ge=1, le=60, description="Cantidad de tomas/clips")
    toma_max_s: float = Field(default=8.0, gt=1, le=60, description="Duración máxima de cada toma")
    voz: Literal["clonada", "generada", "sin definir"] = "clonada"
    idioma: str = Field(default="español latino neutro")
    genero_neutro: bool = Field(default=False, description="Si es True no se dirige a un género ni usa formas marcadas")
    datos_confirmados: list[str] = Field(
        default_factory=list, description="Hechos verificados: 'fecha: 29 de noviembre', 'lugar: Club Nativos, Envigado'…"
    )
    en_pantalla: list[str] = Field(
        default_factory=list, description="Datos que irán SOLO en pantalla (teléfono, precio, URL) y no deben decirse en voz"
    )
    prohibido: list[str] = Field(default_factory=list, description="Frases, promesas o temas que no se pueden usar")
    material: str = Field(default="", description="Documento de apoyo del cliente (texto completo o resumen)")
    notas: str = Field(default="", description="Cualquier otra indicación")


class Toma(BaseModel):
    numero: int
    intencion: str = Field(description="Qué hace esta toma en el arco (gancho, dolor, giro, invitación…)")
    voz: str = Field(description="Texto exacto que se dice, SIN etiquetas")
    voz_con_emociones: str = Field(description="El mismo texto con [etiquetas de emoción y pausa] para ElevenLabs v3")
    energia: Literal["muy baja", "baja", "media", "alta", "muy alta"] = "media"
    en_pantalla: list[str] = Field(default_factory=list, description="Gráficos o datos que aparecen en esta toma")
    prompt_video: str = Field(default="", description="Opcional: prompt para el generador de video de esta toma")


class Guion(BaseModel):
    titulo: str
    gancho: str = Field(description="La frase de gancho, tal como se dice")
    arco: str = Field(description="Resumen del arco emocional en 1-2 frases")
    tomas: list[Toma]
    pendientes: list[str] = Field(default_factory=list, description="Datos que faltan y cómo se resolvió su ausencia")
    texto_publicacion: str = Field(default="", description="Descripción sugerida para publicar (sin promesas)")

    def voz_completa(self) -> str:
        return " ".join(t.voz.strip() for t in self.tomas)


class Criterio(BaseModel):
    nombre: str
    puntaje: int = Field(ge=1, le=10)
    comentario: str


class Revision(BaseModel):
    criterios: list[Criterio]
    aprobado: bool
    resumen: str
    problemas: list[str] = Field(default_factory=list, description="Problemas concretos, con la toma a que se refieren")
    reescrituras: list[str] = Field(
        default_factory=list, description="Cambios concretos a aplicar: 'Toma 2: cambia X por Y porque…'"
    )


class Hallazgo(BaseModel):
    """Resultado de una revisión automática (sin IA)."""

    nivel: Literal["error", "aviso", "info"]
    donde: str
    mensaje: str
