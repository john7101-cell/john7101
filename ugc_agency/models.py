"""Esquemas de datos que intercambian los agentes.

Cada agente devuelve uno de estos modelos (validado con structured outputs),
así el orquestador puede pasar el trabajo de uno al siguiente sin parsear texto libre.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Entrada
# ---------------------------------------------------------------------------


class ProductInput(BaseModel):
    """Lo que el cliente de la agencia nos entrega sobre su producto."""

    name: str
    category: str
    price_usd: float | None = None
    description: str = ""
    key_features: list[str] = Field(default_factory=list)
    verified_claims: list[str] = Field(
        default_factory=list,
        description="Afirmaciones que la marca puede respaldar (estudios, certificaciones). "
        "Son las ÚNICAS afirmaciones de resultado que los guiones pueden usar.",
    )
    target_audience_hint: str = ""
    tiktok_shop_url: str = ""
    brand_notes: str = Field(default="", description="Tono, cosas prohibidas, promociones activas.")


# ---------------------------------------------------------------------------
# 1. Analista de producto
# ---------------------------------------------------------------------------


class AudienceSegment(BaseModel):
    name: str
    who_they_are: str
    daily_life_moments: list[str] = Field(description="Momentos concretos del día donde el producto encaja.")
    real_frustrations: list[str]
    how_they_talk: str


class ProductBrief(BaseModel):
    product_summary_plain_english: str
    audiences: list[AudienceSegment]
    natural_usage_moments: list[str]
    benefits_in_everyday_words: list[str]
    safe_claims: list[str] = Field(description="Afirmaciones permitidas (descriptivas o verificadas).")
    claims_to_avoid: list[str]
    price_framing: str


# ---------------------------------------------------------------------------
# 2. Estratega de tendencias
# ---------------------------------------------------------------------------


class ContentFormat(BaseModel):
    name: str
    description: str
    why_it_feels_native: str
    example_hook: str


class TrendInsights(BaseModel):
    formats: list[ContentFormat]
    hook_patterns: list[str]
    pacing_notes: str
    audio_vibe: str
    clichés_to_avoid: list[str]


# ---------------------------------------------------------------------------
# 3. Director de casting
# ---------------------------------------------------------------------------


class Persona(BaseModel):
    id: str = Field(description="Identificador corto, p.ej. 'p1'.")
    first_name: str
    age: int
    hometown: str = Field(description="Tipo de lugar en EE.UU., p.ej. 'suburb outside Columbus, OH'.")
    occupation: str
    household: str
    personality: str
    speaking_style: str
    verbal_habits: list[str] = Field(description="Muletillas y formas de hablar reales.")
    filming_spots: list[str] = Field(description="Dónde graba: carro, cocina, baño, etc.")
    look_description: str = Field(
        description="Apariencia genérica para generar el personaje con IA. Nunca parecido a personas reales."
    )
    connection_to_product: str


class PersonaRoster(BaseModel):
    personas: list[Persona]


# ---------------------------------------------------------------------------
# 4. Creativo de historias
# ---------------------------------------------------------------------------


class StoryConcept(BaseModel):
    id: str = Field(description="Identificador corto, p.ej. 'c1'.")
    persona_id: str
    title: str
    format_name: str
    everyday_situation: str
    emotional_arc: str
    product_moment: str = Field(description="Cómo aparece el producto de forma natural dentro de la historia.")
    hook: str
    why_it_feels_real: str


class ConceptBoard(BaseModel):
    concepts: list[StoryConcept]


# ---------------------------------------------------------------------------
# 5. Guionista
# ---------------------------------------------------------------------------


class ScriptBeat(BaseModel):
    time_range: str = Field(description="p.ej. '0-3s'")
    visual: str
    spoken_line: str
    on_screen_text: str = ""
    delivery_note: str = ""


class Script(BaseModel):
    concept_id: str
    persona_id: str
    title: str
    duration_seconds: int
    beats: list[ScriptBeat]
    soft_cta: str
    full_voiceover: str = Field(description="Todo lo que dice el personaje, en orden, listo para TTS.")


# ---------------------------------------------------------------------------
# 6. Editor de autenticidad / 7. Cumplimiento
# ---------------------------------------------------------------------------


class AuthenticityReview(BaseModel):
    naturalness_score: int = Field(ge=1, le=10)
    ad_speak_flags: list[str]
    what_feels_real: list[str]
    rewrite_notes: list[str]
    verdict: Literal["approve", "revise"]


class ComplianceIssue(BaseModel):
    severity: Literal["blocker", "warning"]
    excerpt: str
    problem: str
    fix: str


class ComplianceReview(BaseModel):
    passed: bool
    issues: list[ComplianceIssue]
    required_disclosures: list[str]


# ---------------------------------------------------------------------------
# 8. Director de escena / 9. Productor de video / 10. Copy
# ---------------------------------------------------------------------------


class Shot(BaseModel):
    number: int
    duration_seconds: float
    framing: str
    action: str
    camera: str = Field(description="Handheld, selfie, apoyado en el tablero, etc.")
    location_and_light: str
    audio: str
    spoken_line: str = ""


class ShotList(BaseModel):
    concept_id: str
    aspect_ratio: Literal["9:16"] = "9:16"
    overall_look: str
    shots: list[Shot]
    editing_notes: list[str]


class ScenePrompt(BaseModel):
    shot_number: int
    duration_seconds: float
    video_prompt: str
    negative_prompt: str
    voice_line: str = ""


class VoiceDirection(BaseModel):
    description: str
    pace: str
    emotion: str
    stability: float = Field(ge=0, le=1, description="Más bajo = más expresivo/variable.")
    style: float = Field(ge=0, le=1)


class VideoProductionPack(BaseModel):
    concept_id: str
    character_reference_prompt: str
    scenes: list[ScenePrompt]
    voice: VoiceDirection
    caption_style: str
    post_production_steps: list[str]


class PostPackage(BaseModel):
    concept_id: str
    caption: str
    hashtags: list[str]
    pinned_comment: str
    disclosure_text: str
    best_posting_window_et: str


# ---------------------------------------------------------------------------
# Resultado final de una pieza y de la campaña
# ---------------------------------------------------------------------------


class ContentPiece(BaseModel):
    concept: StoryConcept
    persona: Persona
    script: Script
    authenticity: AuthenticityReview
    compliance: ComplianceReview
    shot_list: ShotList
    production: VideoProductionPack
    post: PostPackage
    revision_rounds: int
    voiceover_file: str | None = None


class CampaignResult(BaseModel):
    product: ProductInput
    brief: ProductBrief
    trends: TrendInsights
    personas: PersonaRoster
    concepts: ConceptBoard
    pieces: list[ContentPiece]
    rejected: list[str] = Field(default_factory=list, description="Conceptos que no pasaron QA y por qué.")
