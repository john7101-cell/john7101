"""Estudio de guiones: escribe, mide, revisa y reescribe hasta aprobar (o agotar las rondas)."""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from ..llm import LLM
from .agentes import Guionista, RevisorGuiones
from .lint import estimar_segundos, resumen, revisar_tomas
from .modelos import Guion, GuionBrief, Hallazgo, Revision


@dataclass
class ResultadoGuion:
    brief: GuionBrief
    guion: Guion
    revision: Revision
    hallazgos: list[Hallazgo]
    rondas: int
    historial: list[str] = field(default_factory=list)

    @property
    def aprobado(self) -> bool:
        return self.revision.aprobado and not any(h.nivel == "error" for h in self.hallazgos)


class EstudioGuiones:
    def __init__(self, llm: LLM, umbral: int = 7, max_rondas: int = 3,
                 on_step: Callable[[str], None] | None = None) -> None:
        self.guionista = Guionista(llm)
        self.revisor = RevisorGuiones(llm)
        self.umbral = umbral
        self.max_rondas = max_rondas
        self.log = on_step or (lambda s: None)

    def _medir(self, brief: GuionBrief, guion: Guion) -> list[Hallazgo]:
        return revisar_tomas([(t.numero, t.voz) for t in guion.tomas], brief)

    def _bajo_umbral(self, rev: Revision) -> bool:
        return (not rev.aprobado) or any(c.puntaje < self.umbral for c in rev.criterios)

    def run(self, brief: GuionBrief) -> ResultadoGuion:
        historial: list[str] = []
        self.log("Guionista: escribiendo el primer borrador…")
        guion = self.guionista.escribir(brief)
        hallazgos = self._medir(brief, guion)
        rev = self.revisor.revisar(brief, guion, hallazgos)
        ronda = 1
        historial.append(f"Ronda 1: {sum(c.puntaje for c in rev.criterios) / max(1, len(rev.criterios)):.1f}/10, "
                         f"{len([h for h in hallazgos if h.nivel == 'error'])} errores automáticos")
        while ronda < self.max_rondas and (self._bajo_umbral(rev) or any(h.nivel == "error" for h in hallazgos)):
            ronda += 1
            self.log(f"Ronda {ronda}: el revisor pide cambios, reescribiendo…")
            guion = self.guionista.escribir(brief, previo=guion, notas=rev.reescrituras + rev.problemas, hallazgos=hallazgos)
            hallazgos = self._medir(brief, guion)
            rev = self.revisor.revisar(brief, guion, hallazgos)
            historial.append(f"Ronda {ronda}: {sum(c.puntaje for c in rev.criterios) / max(1, len(rev.criterios)):.1f}/10, "
                             f"{len([h for h in hallazgos if h.nivel == 'error'])} errores automáticos")
        return ResultadoGuion(brief, guion, rev, hallazgos, ronda, historial)

    def revisar_existente(self, brief: GuionBrief, tomas: list[str]) -> ResultadoGuion:
        """Revisa un guion que ya existe (una cadena por toma) sin reescribirlo."""
        from .modelos import Toma
        guion = Guion(titulo=brief.tema, gancho=tomas[0].split(".")[0] if tomas else "", arco="(guion existente)",
                      tomas=[Toma(numero=i + 1, intencion="", voz=t, voz_con_emociones=t) for i, t in enumerate(tomas)])
        hallazgos = self._medir(brief, guion)
        rev = self.revisor.revisar(brief, guion, hallazgos)
        return ResultadoGuion(brief, guion, rev, hallazgos, 1, ["Revisión de un guion existente"])


# ---------------------------------------------------------------- entrada y salida
def leer_material(ruta: str | Path) -> str:
    """Texto de un documento del cliente: .md/.txt directo; .docx/.pdf/.pptx/.xlsx con MarkItDown."""
    p = Path(ruta)
    if p.suffix.lower() in (".md", ".txt"):
        return p.read_text(encoding="utf-8")
    try:
        r = subprocess.run(["markitdown", str(p)], capture_output=True, text=True, check=True)
    except FileNotFoundError as e:
        raise RuntimeError("Para leer .docx/.pdf/.pptx/.xlsx instala MarkItDown: pip install 'markitdown[pdf,docx,pptx,xlsx]'") from e
    return r.stdout


def exportar(res: ResultadoGuion, destino: str | Path) -> Path:
    out = Path(destino)
    out.mkdir(parents=True, exist_ok=True)
    g, rev = res.guion, res.revision
    filas = ["| Toma | Intención | Energía | ~s | Voz |", "|---|---|---|---|---|"]
    for t in g.tomas:
        filas.append(f"| {t.numero} | {t.intencion} | {t.energia} | {estimar_segundos(t.voz):.1f} | {t.voz} |")
    total = sum(estimar_segundos(t.voz) for t in g.tomas)
    md = [f"# {g.titulo}", "", f"**Gancho:** {g.gancho}", "", f"**Arco:** {g.arco}", "",
          f"**Duración estimada:** {total:.0f} s en {len(g.tomas)} tomas", "", *filas, ""]
    for t in g.tomas:
        md += [f"### Toma {t.numero} — {t.intencion}", "", "```", t.voz_con_emociones, "```"]
        if t.en_pantalla:
            md += ["", "En pantalla: " + " · ".join(t.en_pantalla)]
        if t.prompt_video:
            md += ["", "Prompt de video:", "", "```", t.prompt_video, "```"]
        md.append("")
    if g.pendientes:
        md += ["## Pendientes (datos que faltan)", "", *[f"- {p}" for p in g.pendientes], ""]
    if g.texto_publicacion:
        md += ["## Texto de publicación", "", g.texto_publicacion, ""]
    md += ["## Revisión", "", f"**{'APROBADO' if res.aprobado else 'CON OBSERVACIONES'}** tras {res.rondas} ronda(s). {rev.resumen}", "",
           "| Criterio | Puntaje | Comentario |", "|---|---|---|",
           *[f"| {c.nombre} | {c.puntaje}/10 | {c.comentario} |" for c in rev.criterios], ""]
    if rev.problemas:
        md += ["### Problemas", "", *[f"- {p}" for p in rev.problemas], ""]
    if rev.reescrituras:
        md += ["### Cambios sugeridos", "", *[f"- {p}" for p in rev.reescrituras], ""]
    md += ["### Revisión automática", "", "```", resumen(res.hallazgos), "```", "", "### Historial", "", *[f"- {h}" for h in res.historial], ""]
    (out / "guion.md").write_text("\n".join(md), encoding="utf-8")
    (out / "guion.json").write_text(json.dumps({"guion": g.model_dump(), "revision": rev.model_dump(),
                                                  "hallazgos": [h.model_dump() for h in res.hallazgos]}, ensure_ascii=False, indent=2), encoding="utf-8")
    # voz lista para pegar: con etiquetas (v3) y sin etiquetas (pausas con comas/puntos suspensivos)
    (out / "voz_con_emociones.txt").write_text("\n\n".join(t.voz_con_emociones for t in g.tomas), encoding="utf-8")
    plano = [re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", t.voz_con_emociones)).strip() for t in g.tomas]
    (out / "voz_sin_etiquetas.txt").write_text("\n\n".join(plano), encoding="utf-8")
    for t in g.tomas:
        (out / f"toma{t.numero}_voz.txt").write_text(t.voz_con_emociones, encoding="utf-8")
    return out
