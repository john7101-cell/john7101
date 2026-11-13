"""Línea de comandos de la agencia.

    python -m ugc_agency run examples/heatless_curler.json --concepts 5 --out output/curler
    python -m ugc_agency voice output/curler --voice-id <ELEVENLABS_VOICE_ID>
    python -m ugc_agency edit mi_video.mp4            # o un enlace de Drive/Dropbox
    python -m ugc_agency metricas examples/metricas_ejemplo.json   # diagnóstico de métricas (TikTok/Shop/Meta)
    python -m ugc_agency guion taller.docx --duracion 30 --tomas 4 --neutro --dato "fecha: 29 de noviembre"
    python -m ugc_agency ebook examples/ebook_brief.json --out output/mi-libro --solo-plan   # índice para aprobar
    python -m ugc_agency ebook examples/ebook_brief.json --out output/mi-libro --maquetar    # escribe y maqueta
    python -m ugc_agency ebook-maquetar manuscrito.md --out output/maqueta                  # EPUB + PDF + portadas
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


def _brief_desde_args(args: argparse.Namespace):
    from .guiones import GuionBrief, leer_material

    if args.brief.lower().endswith(".json"):
        brief = GuionBrief.model_validate(json.loads(Path(args.brief).read_text(encoding="utf-8")))
    else:
        material = leer_material(args.brief)
        brief = GuionBrief(tema=args.tema or Path(args.brief).stem, material=material)
    for campo in ("objetivo", "audiencia", "tono", "formato", "voz"):
        if getattr(args, campo, None):
            setattr(brief, campo, getattr(args, campo))
    if args.duracion:
        brief.duracion_s = args.duracion
    if args.tomas:
        brief.n_tomas = args.tomas
    if args.toma_max:
        brief.toma_max_s = args.toma_max
    if args.neutro:
        brief.genero_neutro = True
    brief.datos_confirmados += args.dato or []
    brief.en_pantalla += args.pantalla or []
    brief.prohibido += args.prohibido or []
    return brief


def cmd_guion(args: argparse.Namespace) -> int:
    from .guiones import EstudioGuiones, exportar, resumen
    from .llm import ClaudeLLM

    brief = _brief_desde_args(args)
    res = EstudioGuiones(ClaudeLLM(model=args.model, effort=args.effort), umbral=args.umbral,
                         max_rondas=args.rondas, on_step=print).run(brief)
    out = exportar(res, args.out or f"output/guion-{datetime.now():%Y%m%d-%H%M%S}")
    print(f"\n{'✔ APROBADO' if res.aprobado else '! CON OBSERVACIONES'} en {res.rondas} ronda(s) → {out}/guion.md")
    print(resumen(res.hallazgos))
    return 0 if res.aprobado else 1


def cmd_guion_revisar(args: argparse.Namespace) -> int:
    from .guiones import EstudioGuiones, resumen, revisar_tomas
    from .guiones.estudio import exportar

    brief = _brief_desde_args(args)
    texto = Path(args.guion).read_text(encoding="utf-8")
    tomas = [t.strip() for t in texto.split("\n\n") if t.strip()]
    print(f"{len(tomas)} toma(s) detectadas (una por párrafo).")
    hallazgos = revisar_tomas(list(enumerate(tomas, 1)), brief)
    print(resumen(hallazgos))
    if args.sin_llm:
        return 1 if any(h.nivel == "error" for h in hallazgos) else 0
    from .llm import ClaudeLLM
    res = EstudioGuiones(ClaudeLLM(model=args.model, effort=args.effort)).revisar_existente(brief, tomas)
    out = exportar(res, args.out or "output/revision-guion")
    print(f"\nRevisión completa → {out}/guion.md")
    return 0 if res.aprobado else 1


def cmd_metricas(args: argparse.Namespace) -> int:
    from .mercado_us import reporte_desde_dict

    data = json.loads(Path(args.archivo).read_text(encoding="utf-8"))
    rep = reporte_desde_dict(data)
    if args.json:
        print(json.dumps(rep.a_dict(), ensure_ascii=False, indent=2))
        return 0
    print(f"Plataforma: {data.get('plataforma', '—')} · Periodo: {data.get('periodo', '—')}")
    if rep.economia:
        e = rep.economia
        print(f"Margen por pedido: ${e['margen_usd']} ({e['margen_pct']:.0%}) · ROAS de equilibrio: {e['roas_equilibrio']} · CPA máximo: ${e['cpa_maximo_usd']}")
    iconos = {"verde": "🟢", "ámbar": "🟡", "rojo": "🔴", "sin dato": "⚪", "inconcluso": "⚪"}
    for h in rep.hallazgos:
        print(f"  {iconos.get(h.semaforo, '·')} {h.metrica:<11} {h.valor if h.valor is not None else '—':<8} {h.mensaje}")
    if rep.cuello_de_botella:
        print(f"\nPrimer cuello de botella: {rep.cuello_de_botella} (arréglalo antes de tocar lo que sigue)")
    for d in rep.datos_pendientes:
        print(f"  · pendiente: {d}")
    print("\nRangos orientativos (terceros), ver docs/tiktok_us/metricas.md. Para el análisis completo usa el agente `analista-tiktok-us`.")
    return 0


def cmd_yt_estado(args: argparse.Namespace) -> int:
    from .youtube.canal import estado

    for k, v in estado().items():
        print(f"  {k:22s} {v}")
    return 0


def cmd_yt_ideas(args: argparse.Namespace) -> int:
    from .youtube.ideas import investigar

    for v in investigar(args.tema, dias=args.dias, region=args.region)[: args.n]:
        print(f"  {v['vistas_dia']:>8}/día  {v['vistas']:>9} vistas  {v['titulo'][:70]}  ({v['canal']})")
    return 0


def cmd_yt_miniatura(args: argparse.Namespace) -> int:
    from .youtube.miniatura import crear, cuadro_de_video

    fondo = Path(args.fondo)
    if fondo.suffix.lower() in (".mp4", ".mov", ".webm"):
        fondo = cuadro_de_video(fondo, args.segundo, Path(args.out).with_suffix(".fondo.png"))
    out = crear(fondo, args.linea, Path(args.out), acento=args.acento, lado=args.lado, etiqueta=args.etiqueta)
    print(f"✔ {out} ({out.stat().st_size // 1024} KB)")
    return 0


def cmd_yt_publicar(args: argparse.Namespace) -> int:
    from datetime import datetime

    from .youtube.publicar import subir
    from .youtube.seo import Metadatos

    meta = Metadatos.cargar(Path(args.meta))
    for p in meta.validar():
        print(f"  ⚠ {p}")
    cuando = datetime.fromisoformat(args.programar) if args.programar else None
    r = subir(Path(args.video), meta, Path(args.miniatura) if args.miniatura else None,
              Path(args.subtitulos) if args.subtitulos else None, publicar_en=cuando, confirmar=args.confirmar)
    print(json.dumps(r, indent=2, ensure_ascii=False, default=str))
    return 0


# ------------------------------------------------------------------ ebooks
def _ebook_brief(args: argparse.Namespace):
    from .ebooks import EbookBrief
    from .guiones import leer_material

    if args.brief.lower().endswith(".json"):
        brief = EbookBrief.model_validate(json.loads(Path(args.brief).read_text(encoding="utf-8")))
    elif Path(args.brief).exists():
        brief = EbookBrief(tema=args.tema or Path(args.brief).stem, material=leer_material(args.brief))
    else:
        brief = EbookBrief(tema=args.brief)
    for campo in ("autor", "lector", "tono"):
        if getattr(args, campo, None):
            setattr(brief, campo, getattr(args, campo))
    if args.palabras:
        brief.palabras_objetivo = args.palabras
    if args.capitulos:
        brief.n_capitulos = args.capitulos
    return brief


def cmd_ebook(args: argparse.Namespace) -> int:
    from .ebooks import EstudioEbook, maquetar, resumen_maquetacion
    from .llm import ClaudeLLM

    brief = _ebook_brief(args)
    out = Path(args.out or f"output/ebook-{datetime.now():%Y%m%d-%H%M%S}")
    # capítulos largos: más margen de salida (por debajo del límite de peticiones no-streaming)
    llm = ClaudeLLM(model=args.model, effort=args.effort, max_tokens=21000)
    estudio = EstudioEbook(llm, out, umbral=args.umbral, max_rondas=args.rondas, on_step=print)
    if args.solo_plan:
        estudio.planificar(brief, args.notas or "", rehacer=args.replanificar)
        print(f"\nPlan listo → {out}/plan.md  (revísalo; edita plan.json si quieres y vuelve a lanzar sin --solo-plan)")
        return 0
    libro = estudio.run(brief, args.notas or "", replanificar=args.replanificar,
                        solo=set(args.capitulo) if args.capitulo else None)
    pendientes = [r for r in libro.capitulos if not r.aprobado]
    print(f"\n{'✔' if not pendientes else '!'} Manuscrito → {out}/manuscrito.md · informe → {out}/informe.md")
    if args.maquetar:
        rep = maquetar(out / "manuscrito.md", out / "maqueta", paleta=args.paleta,
                       frase=libro.ficha.texto_portada if libro.ficha else "",
                       contraportada=libro.ficha.contraportada if libro.ficha else "")
        print(resumen_maquetacion(rep))
    return 0 if not pendientes else 1


def cmd_ebook_maquetar(args: argparse.Namespace) -> int:
    from .ebooks import maquetar, resumen_maquetacion

    contra = Path(args.contraportada).read_text(encoding="utf-8") if args.contraportada else ""
    rep = maquetar(args.manuscrito, args.out or "output/maqueta", portada=args.portada, tamano=args.tamano,
                   paleta=args.paleta, frase=args.frase or "", imagen=args.imagen, contraportada=contra,
                   formatos=tuple(args.formatos.split(",")), incrustar_fuentes=args.incrustar_fuentes)
    print(resumen_maquetacion(rep))
    return 0 if rep.get("epub_valido", True) else 1


def cmd_ebook_revisar(args: argparse.Namespace) -> int:
    from .ebooks import contar_palabras, fernandez_huerta, leer_manuscrito, resumen, revisar_texto

    ms = leer_manuscrito(args.archivo)
    hs = []
    for s in ms.secciones:
        hs += revisar_texto(s.cuerpo, s.titulo or "preliminares", args.palabras, args.prohibido or [],
                            ortografia=not args.sin_ortografia)
    texto = "\n\n".join(s.cuerpo for s in ms.secciones)
    print(f"«{ms.titulo}»: {contar_palabras(texto)} palabras, legibilidad Fernández-Huerta {fernandez_huerta(texto)}\n")
    print(resumen(hs))
    return 1 if any(h.nivel == "error" for h in hs) else 0


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

    def _opts_brief(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("brief", help="Brief: .json (GuionBrief) o un documento (.md .txt .docx .pdf .pptx .xlsx)")
        sp.add_argument("--tema", default=None, help="Nombre del tema si el brief es un documento")
        sp.add_argument("--objetivo", default=None)
        sp.add_argument("--audiencia", default=None)
        sp.add_argument("--tono", default=None)
        sp.add_argument("--formato", default=None, help="reel, teaser, historia dramática, anuncio, YouTube…")
        sp.add_argument("--voz", choices=["clonada", "generada", "sin definir"], default=None)
        sp.add_argument("--duracion", type=int, default=None, help="Segundos totales objetivo")
        sp.add_argument("--tomas", type=int, default=None, help="Cantidad de tomas/clips")
        sp.add_argument("--toma-max", type=float, default=None, help="Duración máxima por toma (s)")
        sp.add_argument("--neutro", action="store_true", help="Sin énfasis ni formas de género")
        sp.add_argument("--dato", action="append", help="Dato confirmado, p.ej. 'fecha: 29 de noviembre' (repetible)")
        sp.add_argument("--pantalla", action="append", help="Dato solo para pantalla, p.ej. 'WhatsApp: 315 322 8900'")
        sp.add_argument("--prohibido", action="append", help="Frase o promesa que no se puede usar")
        sp.add_argument("--model", default=None)
        sp.add_argument("--effort", default=None)
        sp.add_argument("--out", default=None)

    gu = sub.add_parser("guion", help="Estudio de guiones: escribe, mide, revisa y reescribe hasta aprobar")
    _opts_brief(gu)
    gu.add_argument("--rondas", type=int, default=3)
    gu.add_argument("--umbral", type=int, default=7, help="Puntaje mínimo (1-10) en cada criterio")
    gu.set_defaults(func=cmd_guion)
    gr = sub.add_parser("guion-revisar", help="Revisa un guion que ya existe (un párrafo por toma): medidas + revisor")
    _opts_brief(gr)
    gr.add_argument("guion", help="Archivo de texto con el guion: un párrafo por toma")
    gr.add_argument("--sin-llm", action="store_true", help="Solo revisión automática (no usa la API)")
    gr.set_defaults(func=cmd_guion_revisar)

    mt = sub.add_parser("metricas", help="Diagnóstico de métricas (TikTok/Shop/Meta): semáforo, ROAS de equilibrio y cuello de botella")
    mt.add_argument("archivo", help="JSON con 'metricas' y 'economia' (ver examples/metricas_ejemplo.json)")
    mt.add_argument("--json", action="store_true", help="Salida en JSON")
    mt.set_defaults(func=cmd_metricas)

    ye = sub.add_parser("yt-estado", help="Estado del canal y progreso hacia la monetización")
    ye.set_defaults(func=cmd_yt_estado)
    yi = sub.add_parser("yt-ideas", help="Videos del tema que más vistas por día están sumando")
    yi.add_argument("tema")
    yi.add_argument("--dias", type=int, default=90)
    yi.add_argument("--region", default="MX")
    yi.add_argument("-n", type=int, default=15)
    yi.set_defaults(func=cmd_yt_ideas)
    ym = sub.add_parser("yt-miniatura", help="Crea una miniatura 1280x720 (fondo = imagen o video)")
    ym.add_argument("fondo")
    ym.add_argument("--linea", action="append", required=True, help="Línea de texto (repetible, máx. 3; *así* = acento)")
    ym.add_argument("--out", required=True)
    ym.add_argument("--segundo", type=float, default=1.0, help="Si el fondo es un video, segundo del cuadro")
    ym.add_argument("--acento", default="#F8CB12")
    ym.add_argument("--lado", choices=["izquierda", "derecha"], default="izquierda")
    ym.add_argument("--etiqueta", default=None)
    ym.set_defaults(func=cmd_yt_miniatura)
    yp = sub.add_parser("yt-publicar", help="Sube video + miniatura + subtítulos (privado o programado)")
    yp.add_argument("video")
    yp.add_argument("--meta", required=True, help="JSON de metadatos (título, descripción, etiquetas…)")
    yp.add_argument("--miniatura", default=None)
    yp.add_argument("--subtitulos", default=None)
    yp.add_argument("--programar", default=None, help="Fecha ISO con zona, p.ej. 2026-11-12T18:00:00-05:00")
    yp.add_argument("--confirmar", action="store_true", help="Sin esto solo se simula la subida")
    yp.set_defaults(func=cmd_yt_publicar)

    eb = sub.add_parser("ebook", help="Editorial de ebooks: plan, capítulos revisados, ficha de venta y (opcional) maqueta")
    eb.add_argument("brief", help="JSON con EbookBrief (ver examples/ebook_brief.json), un documento con apuntes o el tema entre comillas")
    eb.add_argument("--tema", default=None)
    eb.add_argument("--autor", default=None)
    eb.add_argument("--lector", default=None)
    eb.add_argument("--tono", default=None)
    eb.add_argument("--palabras", type=int, default=None, help="Extensión total objetivo")
    eb.add_argument("--capitulos", type=int, default=None)
    eb.add_argument("--solo-plan", action="store_true", help="Solo el plan editorial (título, índice) para aprobarlo antes")
    eb.add_argument("--replanificar", action="store_true", help="Rehace el plan aunque ya exista")
    eb.add_argument("--notas", default=None, help="Indicaciones para el estratega (p. ej. 'más casos prácticos')")
    eb.add_argument("--capitulo", type=int, action="append", help="Reescribe solo este capítulo (0 = intro, 99 = conclusión)")
    eb.add_argument("--rondas", type=int, default=3)
    eb.add_argument("--umbral", type=int, default=8, help="Puntaje mínimo (1-10) en cada criterio del editor")
    eb.add_argument("--maquetar", action="store_true", help="Al terminar, genera EPUB, PDF y portadas")
    eb.add_argument("--paleta", default="noche", help="noche, bosque, terracota, papel, vino")
    eb.add_argument("--model", default=None)
    eb.add_argument("--effort", default=None)
    eb.add_argument("--out", default=None)
    eb.set_defaults(func=cmd_ebook)

    em = sub.add_parser("ebook-maquetar", help="Manuscrito Markdown → EPUB validado, PDF de imprenta, portada y cubierta KDP")
    em.add_argument("manuscrito", help="Markdown con front matter (title, subtitle, author); cada '# ' es un capítulo")
    em.add_argument("--out", default=None)
    em.add_argument("--portada", default=None, help="Imagen de portada propia (si no, se diseña una)")
    em.add_argument("--imagen", default=None, help="Foto/ilustración de fondo para la portada diseñada")
    em.add_argument("--frase", default=None, help="Frase corta para la portada")
    em.add_argument("--paleta", default="noche", help="noche, bosque, terracota, papel, vino")
    em.add_argument("--tamano", default="6x9", choices=["6x9", "5.5x8.5", "5x8", "8.5x11"])
    em.add_argument("--contraportada", default=None, help="Archivo de texto para la contraportada")
    em.add_argument("--formatos", default="epub,pdf")
    em.add_argument("--incrustar-fuentes", action="store_true", help="Incrusta EB Garamond en el EPUB")
    em.set_defaults(func=cmd_ebook_maquetar)

    er = sub.add_parser("ebook-revisar", help="Corrector automático de un manuscrito (sin API): ritmo, clichés, promesas, ortografía")
    er.add_argument("archivo")
    er.add_argument("--palabras", type=int, default=None, help="Extensión objetivo por capítulo")
    er.add_argument("--prohibido", action="append")
    er.add_argument("--sin-ortografia", action="store_true")
    er.set_defaults(func=cmd_ebook_revisar)

    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
