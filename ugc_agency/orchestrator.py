"""Productor ejecutivo: coordina a los agentes de principio a fin."""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Callable

from .agents import (
    AuthenticityEditor,
    CastingDirector,
    ComplianceOfficer,
    ProductAnalyst,
    SceneDirector,
    Scriptwriter,
    SocialCopywriter,
    StoryCreative,
    TrendStrategist,
    VideoProducer,
)
from .llm import LLM
from .models import (
    AuthenticityReview,
    CampaignResult,
    ComplianceReview,
    ContentPiece,
    Persona,
    ProductBrief,
    ProductInput,
    Script,
    StoryConcept,
)

log = logging.getLogger("ugc_agency")


@dataclass
class CampaignSettings:
    personas: int = 3
    concepts: int = 5
    authenticity_threshold: int = 8
    max_revisions: int = 3
    parallel_pieces: int = 3


class UGCAgency:
    """Pipeline:

    Analista -> Estratega -> Casting -> Creativo -> por cada concepto (en paralelo):
        Guionista <-> Editor de autenticidad + Cumplimiento (bucle de revisión)
        -> Director de escena -> Productor de video -> Copywriter social
    """

    def __init__(self, llm: LLM, settings: CampaignSettings | None = None,
                 on_step: Callable[[str], None] | None = None) -> None:
        self.settings = settings or CampaignSettings()
        self.on_step = on_step or (lambda msg: log.info(msg))
        self.analyst = ProductAnalyst(llm)
        self.strategist = TrendStrategist(llm)
        self.casting = CastingDirector(llm)
        self.creative = StoryCreative(llm)
        self.writer = Scriptwriter(llm)
        self.editor = AuthenticityEditor(llm)
        self.compliance = ComplianceOfficer(llm)
        self.director = SceneDirector(llm)
        self.producer = VideoProducer(llm)
        self.copywriter = SocialCopywriter(llm)

    # ------------------------------------------------------------------
    def run(self, product: ProductInput) -> CampaignResult:
        s = self.settings
        self.on_step(f"[Analista de producto] estudiando '{product.name}'...")
        brief = self.analyst.analyze(product)

        self.on_step("[Estratega de tendencias] eligiendo formatos y hooks...")
        trends = self.strategist.research(brief)

        self.on_step(f"[Director de casting] creando {s.personas} personajes cotidianos...")
        roster = self.casting.cast(brief, s.personas)

        self.on_step(f"[Creativo de historias] proponiendo {s.concepts} historias de la vida diaria...")
        board = self.creative.pitch(brief, trends, roster, s.concepts)

        personas = {p.id: p for p in roster.personas}
        pieces: list[ContentPiece] = []
        rejected: list[str] = []

        def work(concept: StoryConcept) -> ContentPiece | str:
            persona = personas.get(concept.persona_id) or roster.personas[0]
            try:
                return self._produce_piece(concept, persona, product, brief)
            except Exception as e:  # una pieza fallida no tumba la campaña
                log.exception("Fallo en el concepto %s", concept.id)
                return f"{concept.id} ({concept.title}): error — {e}"

        with ThreadPoolExecutor(max_workers=max(1, s.parallel_pieces)) as pool:
            for result in pool.map(work, board.concepts):
                (pieces if isinstance(result, ContentPiece) else rejected).append(result)

        return CampaignResult(
            product=product, brief=brief, trends=trends, personas=roster,
            concepts=board, pieces=pieces, rejected=rejected,
        )

    # ------------------------------------------------------------------
    def _produce_piece(self, concept: StoryConcept, persona: Persona,
                       product: ProductInput, brief: ProductBrief) -> ContentPiece:
        s = self.settings
        tag = f"[{concept.id} · {persona.first_name}]"

        self.on_step(f"{tag} Guionista escribiendo '{concept.title}'...")
        script = self.writer.write(concept, persona, brief)

        rounds = 0
        while True:
            authenticity, compliance = self._review(script, persona, product, brief)
            approved = (
                authenticity.verdict == "approve"
                and authenticity.naturalness_score >= s.authenticity_threshold
                and compliance.passed
            )
            self.on_step(
                f"{tag} naturalidad {authenticity.naturalness_score}/10, "
                f"cumplimiento {'OK' if compliance.passed else 'con bloqueos'}"
            )
            if approved:
                break
            if rounds >= s.max_revisions:
                raise RuntimeError(
                    f"no aprobó tras {rounds} revisiones "
                    f"(naturalidad {authenticity.naturalness_score}, cumplimiento {compliance.passed})"
                )
            rounds += 1
            notes = list(authenticity.rewrite_notes) + [
                f"[COMPLIANCE {i.severity.upper()}] '{i.excerpt}': {i.problem} -> {i.fix}"
                for i in compliance.issues
            ]
            self.on_step(f"{tag} revisión #{rounds} con {len(notes)} notas...")
            script = self.writer.write(concept, persona, brief, revision_notes=notes, previous=script)

        self.on_step(f"{tag} Director de escena armando el shot list...")
        shot_list = self.director.plan(script, persona)
        self.on_step(f"{tag} Productor de video IA preparando prompts y voz...")
        production = self.producer.produce(shot_list, persona, product.name)
        self.on_step(f"{tag} Copywriter social escribiendo caption...")
        post = self.copywriter.write(script, persona, compliance)

        return ContentPiece(
            concept=concept, persona=persona, script=script, authenticity=authenticity,
            compliance=compliance, shot_list=shot_list, production=production, post=post,
            revision_rounds=rounds,
        )

    def _review(self, script: Script, persona: Persona, product: ProductInput,
                brief: ProductBrief) -> tuple[AuthenticityReview, ComplianceReview]:
        with ThreadPoolExecutor(max_workers=2) as pool:
            a = pool.submit(self.editor.review, script, persona, self.settings.authenticity_threshold)
            c = pool.submit(self.compliance.review, script, product, brief)
            return a.result(), c.result()
