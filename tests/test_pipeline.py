"""Prueba el pipeline completo sin llamar a la API, con un LLM falso."""

from __future__ import annotations

import types
import typing
from pathlib import Path

from pydantic import BaseModel

from ugc_agency.models import (
    AuthenticityReview,
    ConceptBoard,
    PersonaRoster,
    ProductInput,
)
from ugc_agency.orchestrator import CampaignSettings, UGCAgency
from ugc_agency.production.export import export_campaign, load_campaign


def build(tp, name: str = "x"):
    """Construye un valor mínimo válido para cualquier anotación de tipo."""
    origin = typing.get_origin(tp)
    args = typing.get_args(tp)
    if origin is typing.Literal:
        return args[0]
    if origin in (typing.Union, types.UnionType):
        return build(next(a for a in args if a is not type(None)), name)
    if origin is list:
        return [build(args[0], name)]
    if isinstance(tp, type) and issubclass(tp, BaseModel):
        return tp(**{n: build(f.annotation, n) for n, f in tp.model_fields.items()})
    if tp is int:
        return 8
    if tp is float:
        return 0.5
    if tp is bool:
        return True
    return f"{name}-value"


class FakeLLM:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.authenticity_calls = 0

    def generate(self, *, system, prompt, output_model):
        self.calls.append(output_model.__name__)
        if output_model is PersonaRoster:
            p = build(PersonaRoster).personas[0]
            return PersonaRoster(personas=[p.model_copy(update={"id": "p1", "first_name": "Dana"})])
        if output_model is ConceptBoard:
            c = build(ConceptBoard).concepts[0]
            return ConceptBoard(concepts=[
                c.model_copy(update={"id": "c1", "persona_id": "p1", "title": "Car talk before shift"}),
                c.model_copy(update={"id": "c2", "persona_id": "p1", "title": "Sunday reset"}),
            ])
        if output_model is AuthenticityReview:
            self.authenticity_calls += 1
            # La primera revisión pide cambios para ejercitar el bucle de revisión.
            if self.authenticity_calls == 1:
                return AuthenticityReview(naturalness_score=5, ad_speak_flags=["game-changer"],
                                          what_feels_real=[], rewrite_notes=["less salesy"], verdict="revise")
            return AuthenticityReview(naturalness_score=9, ad_speak_flags=[], what_feels_real=["specific"],
                                      rewrite_notes=[], verdict="approve")
        return build(output_model)


def test_full_campaign(tmp_path: Path) -> None:
    llm = FakeLLM()
    agency = UGCAgency(llm, CampaignSettings(personas=1, concepts=2, parallel_pieces=1), on_step=lambda _: None)
    product = ProductInput(name="Test Tumbler", category="Drinkware")

    result = agency.run(product)

    assert len(result.pieces) == 2
    assert result.rejected == []
    assert sum(p.revision_rounds for p in result.pieces) == 1
    for agent in ["ProductBrief", "TrendInsights", "PersonaRoster", "ConceptBoard", "Script",
                  "ComplianceReview", "ShotList", "VideoProductionPack", "PostPackage"]:
        assert agent in llm.calls

    out = export_campaign(result, tmp_path / "campaign")
    assert (out / "README.md").exists()
    briefs = list(out.glob("c*/brief.md"))
    assert len(briefs) == 2
    assert "## Guion" in briefs[0].read_text()
    assert load_campaign(out / "campaign.json").product.name == "Test Tumbler"


def test_piece_rejected_after_max_revisions() -> None:
    class AlwaysAd(FakeLLM):
        def generate(self, *, system, prompt, output_model):
            if output_model is AuthenticityReview:
                return AuthenticityReview(naturalness_score=3, ad_speak_flags=["must-have"],
                                          what_feels_real=[], rewrite_notes=["rewrite"], verdict="revise")
            return super().generate(system=system, prompt=prompt, output_model=output_model)

    agency = UGCAgency(AlwaysAd(), CampaignSettings(personas=1, concepts=2, max_revisions=1),
                       on_step=lambda _: None)
    result = agency.run(ProductInput(name="X", category="Y"))
    assert result.pieces == []
    assert len(result.rejected) == 2


def test_system_prompts_include_rules() -> None:
    agency = UGCAgency(FakeLLM(), on_step=lambda _: None)
    for agent in [agency.writer, agency.editor, agency.compliance, agency.producer]:
        assert "AUTHENTICITY RULES" in agent.system_prompt
        assert "AIGC" in agent.system_prompt
