"""Exporta la campaña: JSON completo, un brief legible por pieza y el pack de prompts de video."""

from __future__ import annotations

import json
import re
from pathlib import Path

from ..models import CampaignResult, ContentPiece


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "item"


def piece_markdown(piece: ContentPiece) -> str:
    c, p, s = piece.concept, piece.persona, piece.script
    lines = [
        f"# {s.title}",
        "",
        f"**Personaje:** {p.first_name}, {p.age} — {p.occupation} ({p.hometown})  ",
        f"**Formato:** {c.format_name}  ",
        f"**Situación cotidiana:** {c.everyday_situation}  ",
        f"**Momento del producto:** {c.product_moment}  ",
        f"**Naturalidad:** {piece.authenticity.naturalness_score}/10 · "
        f"**Revisiones:** {piece.revision_rounds} · "
        f"**Cumplimiento:** {'aprobado' if piece.compliance.passed else 'pendiente'}",
        "",
        "## Guion",
        "",
        "| Tiempo | Visual | Lo que dice | Texto en pantalla |",
        "|---|---|---|---|",
    ]
    for b in s.beats:
        cell = lambda t: (t or "").replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {b.time_range} | {cell(b.visual)} | {cell(b.spoken_line)} | {cell(b.on_screen_text)} |")
    lines += ["", f"**CTA:** {s.soft_cta}", "", "### Voz en off (TTS)", "", f"> {s.full_voiceover}", ""]

    lines += ["## Shot list", ""]
    for sh in piece.shot_list.shots:
        lines.append(f"{sh.number}. **{sh.duration_seconds:g}s · {sh.framing}** — {sh.action} "
                     f"_(cámara: {sh.camera}; {sh.location_and_light}; audio: {sh.audio})_")
    lines += ["", "**Edición:** " + "; ".join(piece.shot_list.editing_notes), ""]

    pr = piece.production
    lines += ["## Producción IA", "", "**Referencia del personaje:**", "", f"```\n{pr.character_reference_prompt}\n```", ""]
    for sc in pr.scenes:
        lines += [f"**Escena {sc.shot_number} ({sc.duration_seconds:g}s)**", "",
                  f"```\n{sc.video_prompt}\n```", f"_Negative:_ {sc.negative_prompt}", ""]
    lines += [f"**Voz:** {pr.voice.description} · ritmo {pr.voice.pace} · emoción {pr.voice.emotion}", ""]

    post = piece.post
    lines += ["## Publicación", "", f"**Caption:** {post.caption} {' '.join(post.hashtags)}", "",
              f"**Comentario fijado:** {post.pinned_comment}", "",
              f"**Divulgación:** {post.disclosure_text}", "",
              f"**Horario sugerido (ET):** {post.best_posting_window_et}", "",
              "**Divulgaciones obligatorias:** " + "; ".join(piece.compliance.required_disclosures), ""]
    if piece.compliance.issues:
        lines += ["**Advertencias de cumplimiento:**", ""]
        lines += [f"- ({i.severity}) {i.problem} → {i.fix}" for i in piece.compliance.issues]
    return "\n".join(lines) + "\n"


def export_campaign(result: CampaignResult, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "campaign.json").write_text(result.model_dump_json(indent=2), encoding="utf-8")

    summary = [f"# Campaña UGC — {result.product.name}", "",
               f"Piezas aprobadas: **{len(result.pieces)}** · Rechazadas: **{len(result.rejected)}**", "",
               "## Personajes", ""]
    summary += [f"- **{p.first_name}** ({p.age}), {p.occupation} — {p.hometown}" for p in result.personas.personas]
    summary += ["", "## Piezas", ""]

    for piece in result.pieces:
        folder = out_dir / f"{piece.concept.id}-{slugify(piece.script.title)}"
        folder.mkdir(exist_ok=True)
        (folder / "brief.md").write_text(piece_markdown(piece), encoding="utf-8")
        (folder / "video_prompts.json").write_text(piece.production.model_dump_json(indent=2), encoding="utf-8")
        (folder / "voiceover.txt").write_text(piece.script.full_voiceover + "\n", encoding="utf-8")
        summary.append(f"- [{piece.script.title}]({folder.name}/brief.md) — "
                       f"{piece.persona.first_name}, naturalidad {piece.authenticity.naturalness_score}/10")
    if result.rejected:
        summary += ["", "## Rechazadas", ""] + [f"- {r}" for r in result.rejected]
    (out_dir / "README.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    return out_dir


def load_campaign(path: Path) -> CampaignResult:
    return CampaignResult.model_validate(json.loads(path.read_text(encoding="utf-8")))
