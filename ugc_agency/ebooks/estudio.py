"""Estudio editorial: plan → capítulos (escribir ⇄ corregir ⇄ editar) → ficha de venta → manuscrito.

Todo se guarda en la carpeta del proyecto en cuanto se produce, así que si el proceso se corta
basta con volver a lanzarlo: retoma desde el último capítulo terminado.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from ..llm import LLM
from .agentes import EditorComercial, EditorDesarrollo, Escritor, EstrategaEditorial
from .lint import contar_palabras, resumen, revisar_texto
from .modelos import Capitulo, EbookBrief, FichaVenta, Hallazgo, PlanCapitulo, PlanEditorial, RevisionCapitulo


@dataclass
class ResultadoCapitulo:
    capitulo: Capitulo
    revision: RevisionCapitulo
    hallazgos: list[Hallazgo]
    rondas: int

    @property
    def aprobado(self) -> bool:
        return self.revision.aprobado and not any(h.nivel == "error" for h in self.hallazgos)


@dataclass
class Libro:
    brief: EbookBrief
    plan: PlanEditorial
    capitulos: list[ResultadoCapitulo] = field(default_factory=list)
    ficha: FichaVenta | None = None


def _guardar(ruta: Path, obj) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    data = obj.model_dump() if hasattr(obj, "model_dump") else obj
    ruta.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class EstudioEbook:
    def __init__(self, llm: LLM, carpeta: str | Path, umbral: int = 8, max_rondas: int = 3,
                 on_step: Callable[[str], None] | None = None) -> None:
        self.estratega = EstrategaEditorial(llm)
        self.escritor = Escritor(llm)
        self.editor = EditorDesarrollo(llm)
        self.comercial = EditorComercial(llm)
        self.dir = Path(carpeta)
        self.umbral = umbral
        self.max_rondas = max_rondas
        self.log = on_step or (lambda s: None)

    # ------------------------------------------------------------ plan
    def planificar(self, brief: EbookBrief, notas: str = "", rehacer: bool = False) -> PlanEditorial:
        ruta = self.dir / "plan.json"
        _guardar(self.dir / "brief.json", brief)
        if ruta.exists() and not rehacer:
            self.log("Plan editorial existente: lo reutilizo (usa --replanificar para rehacerlo).")
            return PlanEditorial.model_validate_json(ruta.read_text(encoding="utf-8"))
        self.log("Estratega editorial: posicionamiento, título e índice…")
        plan = self.estratega.planificar(brief, notas)
        _guardar(ruta, plan)
        (self.dir / "plan.md").write_text(plan_markdown(plan), encoding="utf-8")
        return plan

    # ------------------------------------------------------------ capítulos
    def _bajo_umbral(self, rev: RevisionCapitulo) -> bool:
        return (not rev.aprobado) or any(c.puntaje < self.umbral for c in rev.criterios)

    def escribir_capitulo(self, brief: EbookBrief, plan: PlanEditorial, cap: PlanCapitulo,
                          resumenes: list[str]) -> ResultadoCapitulo:
        donde = f"cap {cap.numero}"
        self.log(f"Escritor: «{cap.titulo}» (~{cap.palabras} palabras)…")
        escrito = self.escritor.escribir(brief, plan, cap, resumenes)
        hs = revisar_texto(escrito.contenido, donde, cap.palabras, brief.prohibido)
        rev = self.editor.revisar(brief, plan, cap, escrito, hs)
        ronda = 1
        while ronda < self.max_rondas and (self._bajo_umbral(rev) or any(h.nivel == "error" for h in hs)):
            ronda += 1
            media = sum(c.puntaje for c in rev.criterios) / max(1, len(rev.criterios))
            self.log(f"  Editor: {media:.1f}/10, pide cambios → ronda {ronda}")
            escrito = self.escritor.escribir(brief, plan, cap, resumenes, previo=escrito,
                                             notas=rev.reescrituras + rev.problemas, hallazgos=hs)
            hs = revisar_texto(escrito.contenido, donde, cap.palabras, brief.prohibido)
            rev = self.editor.revisar(brief, plan, cap, escrito, hs)
        escrito.numero, escrito.titulo = cap.numero, cap.titulo
        return ResultadoCapitulo(escrito, rev, hs, ronda)

    def _secciones(self, plan: PlanEditorial, brief: EbookBrief) -> list[PlanCapitulo]:
        extra = max(600, int(brief.palabras_objetivo * 0.06))
        intro = PlanCapitulo(numero=0, titulo="Introducción", objetivo=plan.introduccion, gancho="El dolor del lector y la promesa",
                             puntos=["Por qué este libro", "Qué conseguirás", "Cómo usar este libro"], palabras=extra)
        cierre = PlanCapitulo(numero=99, titulo="Conclusión", objetivo=plan.cierre, gancho="La transformación lograda",
                              puntos=["Lo esencial del método", "Tu siguiente paso", "Una petición"], palabras=extra)
        return [intro, *plan.capitulos, cierre]

    def run(self, brief: EbookBrief, notas_plan: str = "", replanificar: bool = False,
            solo: set[int] | None = None) -> Libro:
        plan = self.planificar(brief, notas_plan, replanificar)
        libro = Libro(brief, plan)
        resumenes: list[str] = []
        for cap in self._secciones(plan, brief):
            ruta = self.dir / "capitulos" / f"{cap.numero:02d}.json"
            if ruta.exists() and (solo is None or cap.numero not in solo):
                data = json.loads(ruta.read_text(encoding="utf-8"))
                res = ResultadoCapitulo(Capitulo.model_validate(data["capitulo"]),
                                        RevisionCapitulo.model_validate(data["revision"]),
                                        [Hallazgo.model_validate(h) for h in data["hallazgos"]], data["rondas"])
                self.log(f"✓ «{cap.titulo}» ya escrito, lo reutilizo.")
            else:
                res = self.escribir_capitulo(brief, plan, cap, resumenes)
                _guardar(ruta, {"capitulo": res.capitulo.model_dump(), "revision": res.revision.model_dump(),
                                "hallazgos": [h.model_dump() for h in res.hallazgos], "rondas": res.rondas})
                (ruta.with_suffix(".md")).write_text(res.capitulo.contenido, encoding="utf-8")
                self.log(f"{'✔' if res.aprobado else '!'} «{cap.titulo}»: {contar_palabras(res.capitulo.contenido)} palabras, "
                         f"{res.rondas} ronda(s)")
            libro.capitulos.append(res)
            resumenes.append(f"{cap.titulo}: {res.capitulo.resumen}")

        ruta_ficha = self.dir / "ficha_venta.json"
        if ruta_ficha.exists() and solo is None:
            libro.ficha = FichaVenta.model_validate_json(ruta_ficha.read_text(encoding="utf-8"))
        else:
            self.log("Editor comercial: descripción, palabras clave y categorías…")
            libro.ficha = self.comercial.ficha(brief, plan, [r.capitulo for r in libro.capitulos])
            _guardar(ruta_ficha, libro.ficha)
        exportar(libro, self.dir)
        return libro


# ------------------------------------------------------------ salida
def plan_markdown(plan: PlanEditorial) -> str:
    md = [f"# {plan.titulo}", f"## {plan.subtitulo}", "", f"**Promesa:** {plan.promesa}", "",
          f"**Lector ideal:** {plan.lector_ideal}", "", f"**Ángulo:** {plan.angulo}", "", f"**Voz:** {plan.voz}", "",
          "**Títulos alternativos:** " + " · ".join(plan.alternativas_titulo), "", "## Índice", ""]
    for c in plan.capitulos:
        md += [f"### {c.numero}. {c.titulo} (~{c.palabras} palabras)", "", f"*Objetivo:* {c.objetivo}", "",
               f"*Gancho:* {c.gancho}", "", *[f"- {p}" for p in c.puntos]]
        if c.herramienta:
            md += ["", f"*Herramienta:* {c.herramienta}"]
        md.append("")
    if plan.pendientes:
        md += ["## Datos que debe aportar el autor", "", *[f"- {p}" for p in plan.pendientes], ""]
    return "\n".join(md)


def manuscrito(libro: Libro) -> str:
    """Manuscrito único en Markdown con metadatos YAML, listo para `maquetar`."""
    p, b = libro.plan, libro.brief
    def esc(s: str) -> str:
        return s.replace('"', '\\"')
    md = ["---", f'title: "{esc(p.titulo)}"', f'subtitle: "{esc(p.subtitulo)}"', f'author: "{esc(b.autor or "[PENDIENTE: autor]")}"',
          "lang: es", "---", ""]
    for r in libro.capitulos:
        c = r.capitulo
        clase = " {.unnumbered}" if c.numero in (0, 99) else ""
        md += [f"# {c.titulo}{clase}", "", c.contenido.strip(), ""]
    if libro.ficha:
        md += ["# Una petición {.unnumbered}", "", libro.ficha.llamada_resena, ""]
        if libro.ficha.bio_autor and "PENDIENTE" not in libro.ficha.bio_autor:
            md += ["# Sobre el autor {.unnumbered}", "", libro.ficha.bio_autor, ""]
    return "\n".join(md)


def exportar(libro: Libro, carpeta: str | Path) -> Path:
    out = Path(carpeta)
    out.mkdir(parents=True, exist_ok=True)
    (out / "manuscrito.md").write_text(manuscrito(libro), encoding="utf-8")
    total = sum(contar_palabras(r.capitulo.contenido) for r in libro.capitulos)
    inf = [f"# Informe editorial — {libro.plan.titulo}", "", f"**Extensión:** {total} palabras "
           f"(objetivo {libro.brief.palabras_objetivo}) · ~{total // 250} páginas de 6×9 in", "",
           "| Capítulo | Palabras | Rondas | Media | Estado |", "|---|---|---|---|---|"]
    pendientes: list[str] = list(libro.plan.pendientes)
    for r in libro.capitulos:
        media = sum(c.puntaje for c in r.revision.criterios) / max(1, len(r.revision.criterios))
        inf.append(f"| {r.capitulo.titulo} | {contar_palabras(r.capitulo.contenido)} | {r.rondas} | {media:.1f} | "
                   f"{'aprobado' if r.aprobado else 'revisar'} |")
        pendientes += [f"{r.capitulo.titulo}: {x}" for x in r.capitulo.pendientes]
    inf.append("")
    for r in libro.capitulos:
        if not r.aprobado:
            inf += [f"## Revisar: {r.capitulo.titulo}", "", r.revision.resumen, "",
                    *[f"- {x}" for x in r.revision.problemas + r.revision.reescrituras], "",
                    "```", resumen([h for h in r.hallazgos if h.nivel != "info"]), "```", ""]
    if pendientes:
        inf += ["## Pendientes del autor", "", *[f"- {x}" for x in pendientes], ""]
    if libro.ficha:
        f = libro.ficha
        inf += ["## Ficha de venta", "", "**Palabras clave:** " + " · ".join(f.palabras_clave), "",
                "**Categorías:** " + " · ".join(f.categorias), "", f"**Precio:** {f.precio_sugerido}", "",
                "**Contraportada:**", "", f.contraportada, ""]
        (out / "descripcion_amazon.html").write_text(f.descripcion_html, encoding="utf-8")
    (out / "informe.md").write_text("\n".join(inf), encoding="utf-8")
    return out
