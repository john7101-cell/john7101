"""Línea de comandos de la agencia.

    python -m ugc_agency run examples/heatless_curler.json --concepts 5 --out output/curler
    python -m ugc_agency voice output/curler --voice-id <ELEVENLABS_VOICE_ID>
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from .models import ProductInput


def cmd_run(args: argparse.Namespace) -> int:
    from .llm import ClaudeLLM
    from .orchestrator import CampaignSettings, UGCAgency
    from .production.export import export_campaign, slugify

    product = ProductInput.model_validate(json.loads(Path(args.product).read_text(encoding="utf-8")))
    settings = CampaignSettings(
        personas=args.personas, concepts=args.concepts,
        authenticity_threshold=args.threshold, max_revisions=args.max_revisions,
        parallel_pieces=args.parallel,
    )
    agency = UGCAgency(ClaudeLLM(model=args.model, effort=args.effort), settings, on_step=print)
    result = agency.run(product)

    out = Path(args.out or f"output/{slugify(product.name)}-{datetime.now():%Y%m%d-%H%M%S}")
    export_campaign(result, out)
    print(f"\n✔ {len(result.pieces)} piezas aprobadas, {len(result.rejected)} rechazadas → {out}/README.md")
    for r in result.rejected:
        print(f"  ✘ {r}")
    return 0 if result.pieces else 1


def cmd_voice(args: argparse.Namespace) -> int:
    from .production.export import load_campaign, slugify
    from .production.voice import ElevenLabsVoice

    out = Path(args.campaign_dir)
    result = load_campaign(out / "campaign.json")
    tts = ElevenLabsVoice()
    voice_map = dict(v.split("=", 1) for v in args.persona_voice or [])
    for piece in result.pieces:
        voice_id = voice_map.get(piece.persona.id, args.voice_id)
        if not voice_id:
            print(f"  · {piece.concept.id}: sin voice_id para {piece.persona.id}, se omite")
            continue
        path = out / f"{piece.concept.id}-{slugify(piece.script.title)}" / "voiceover.mp3"
        tts.synthesize(piece, voice_id, path)
        print(f"  ✔ {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ugc-agency", description="Agencia UGC con agentes de IA para TikTok Shop USA")
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Genera una campaña completa a partir de un producto (JSON)")
    run.add_argument("product", help="Ruta al JSON del producto (ver examples/)")
    run.add_argument("--personas", type=int, default=3)
    run.add_argument("--concepts", type=int, default=5)
    run.add_argument("--threshold", type=int, default=8, help="Naturalidad mínima (1-10) para aprobar")
    run.add_argument("--max-revisions", type=int, default=3)
    run.add_argument("--parallel", type=int, default=3, help="Piezas producidas en paralelo")
    run.add_argument("--model", default=None)
    run.add_argument("--effort", default=None, choices=["low", "medium", "high", "xhigh", "max"])
    run.add_argument("--out", default=None)
    run.set_defaults(func=cmd_run)

    voice = sub.add_parser("voice", help="Genera las voces en off con ElevenLabs para una campaña ya creada")
    voice.add_argument("campaign_dir")
    voice.add_argument("--voice-id", default=None, help="Voz por defecto para todos los personajes")
    voice.add_argument("--persona-voice", action="append", metavar="PERSONA_ID=VOICE_ID",
                       help="Voz específica por personaje, p.ej. p1=abc123 (repetible)")
    voice.set_defaults(func=cmd_voice)

    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
