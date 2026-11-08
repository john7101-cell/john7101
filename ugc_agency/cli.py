"""Línea de comandos de la agencia.

    python -m ugc_agency run examples/heatless_curler.json --concepts 5 --out output/curler
    python -m ugc_agency voice output/curler --voice-id <ELEVENLABS_VOICE_ID>
    python -m ugc_agency edit mi_video.mp4            # o un enlace de Drive/Dropbox
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


def cmd_edit(args: argparse.Namespace) -> int:
    from .editing import EditOptions, edit_video
    from .editing.media import download

    src = args.input
    if src.startswith(("http://", "https://")):
        print("Descargando video...")
        src_path = download(src, Path(args.download_dir))
    else:
        src_path = Path(src)
    out = Path(args.out) if args.out else src_path.with_name(src_path.stem + "_editado.mp4")
    opts = EditOptions(
        max_pause=args.max_pause, remove_fillers=not args.keep_fillers,
        remove_retakes=not args.keep_retakes, fix_visual_glitches=not args.no_visual_fixes,
        vertical=not args.keep_aspect, captions=not args.no_captions,
        whisper_model=args.whisper_model, language=args.language,
        repair_motion=not args.no_repair, join_fade=args.join_fade, transition=args.transition,
    )
    report = edit_video(src_path, out, opts)
    print(f"\n✔ {report.original_duration:.1f}s → {report.final_duration:.1f}s  ({out})")
    for reason, secs in sorted(report.summary_by_reason().items(), key=lambda x: -x[1]):
        print(f"  - {reason}: {secs:.1f}s")
    for r in report.repairs:
        print(f"  ✚ {r}")
    for w in report.warnings:
        print(f"  ⚠ {w}")
    return 0


def cmd_compose(args: argparse.Namespace) -> int:
    from .editing.compose import compose

    report = compose([Path(c) for c in args.clips], Path(args.graphics), Path(args.out),
                     whisper_model=args.whisper_model, language=args.language, transition=args.transition)
    print(f"\n✔ {report['output']} ({report['duration']:.1f}s, {report['loudness_lufs']:.1f} LUFS)")
    for r in report["repairs"]:
        print(f"  ✚ {r}")
    for g in report["graphics"]:
        print(f"  ▣ {g['image']}: {g['start']:.2f}s → {g['end']:.2f}s")
    return 0


def cmd_limpiar_voz(args: argparse.Namespace) -> int:
    from .editing.voiceover import limpiar_voz

    src = Path(args.audio)
    dst = Path(args.out) if args.out else src.with_name(src.stem + "_limpio.wav")
    cortes, dur, final = limpiar_voz(src, dst, pausa_max=args.pausa_max, language=args.language)
    for c in cortes:
        print(f"  ✂ {c.inicio:6.2f}-{c.fin:6.2f}s  {c.motivo}")
    print(f"\n✔ {dur:.1f}s → {final:.1f}s  ({dst})")
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

    edit = sub.add_parser("edit", help="Edita un video: quita pausas, muletillas, retakes y fallos visuales")
    edit.add_argument("input", help="Ruta del video o enlace (Google Drive, Dropbox o descarga directa)")
    edit.add_argument("--out", default=None)
    edit.add_argument("--max-pause", type=float, default=0.45, help="Pausa máxima permitida en segundos")
    edit.add_argument("--keep-fillers", action="store_true", help="No quitar muletillas (um, uh...)")
    edit.add_argument("--keep-retakes", action="store_true", help="No quitar tomas repetidas")
    edit.add_argument("--no-visual-fixes", action="store_true", help="No cortar cuadros negros/congelados/destellos")
    edit.add_argument("--keep-aspect", action="store_true", help="No convertir a 1080x1920")
    edit.add_argument("--no-captions", action="store_true", help="No quemar subtítulos")
    edit.add_argument("--whisper-model", default="small", help="tiny, base, small, medium, large-v3")
    edit.add_argument("--language", default=None, help="Idioma del audio (en, es...). Auto si se omite")
    edit.add_argument("--no-repair", action="store_true",
                      help="No quitar tirones (cuadros repetidos) ni suavizar saltos entre clips")
    edit.add_argument("--transition", choices=["punch", "fade"], default="punch",
                      help="Uniones entre clips: corte con cambio de encuadre (punch) o fundido (fade)")
    edit.add_argument("--join-fade", type=float, default=0.25, help="Duración del fundido en uniones (s)")
    edit.add_argument("--download-dir", default="input_videos")
    edit.set_defaults(func=cmd_edit)

    comp = sub.add_parser("compose", help="Arma un reel con clips limpios + gráficos anclados a frases de la voz")
    comp.add_argument("clips", nargs="+", help="Clips en orden")
    comp.add_argument("--graphics", required=True, help="JSON con los gráficos (ver examples/graficos_ejemplo.json)")
    comp.add_argument("--out", required=True)
    comp.add_argument("--transition", choices=["punch", "fade"], default="punch")
    comp.add_argument("--whisper-model", default="small")
    comp.add_argument("--language", default=None)
    comp.set_defaults(func=cmd_compose)

    lv = sub.add_parser("limpiar-voz", help="Quita fragmentos fantasma ('ción') y silencios largos de una voz clonada/TTS")
    lv.add_argument("audio")
    lv.add_argument("--out", default=None)
    lv.add_argument("--pausa-max", type=float, default=0.38, help="Pausas más largas que esto se acortan (s)")
    lv.add_argument("--language", default="es")
    lv.set_defaults(func=cmd_limpiar_voz)

    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
