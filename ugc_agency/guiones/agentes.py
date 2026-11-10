"""Los dos especialistas: el Guionista y el Revisor de guiones."""

from __future__ import annotations

from ..agents.base import Agent, to_json
from .modelos import Guion, GuionBrief, Hallazgo, Revision
from .reglas import CRITERIOS, REGLAS_ESCRITOR, REGLAS_REVISOR


class Guionista(Agent[Guion]):
    """Escribe guiones hablados en español, por tomas, con etiquetas de emoción para la voz."""

    name = "guionista"
    role = "Guionista de video corto en español, especialista en voz hablada y en retención."
    instructions = """\
Escribe el guion del brief. Entrega exactamente `n_tomas` tomas, cada una con:
- `voz`: lo que se dice, sin etiquetas. Cabe en `toma_max_s` segundos (16-19 palabras para 8 s; menos con pausas).
- `voz_con_emociones`: el mismo texto con [etiquetas] de emoción, energía y pausa.
- `intencion`, `energia` y, si aplica, `en_pantalla`.
Usa SOLO los datos confirmados del brief. Lo que falta va en `pendientes` y la frase se escribe para que funcione sin ello.
Si recibes notas de revisión o hallazgos automáticos, corrige TODOS y conserva lo que ya funcionaba."""
    output_model = Guion

    @property
    def system_prompt(self) -> str:       # no usa la biblia de UGC en inglés: tiene la suya
        return f"{REGLAS_ESCRITOR}\n\nTU ROL: {self.role}\n\n{self.instructions}"

    def escribir(self, brief: GuionBrief, previo: Guion | None = None, notas: list[str] | None = None,
                 hallazgos: list[Hallazgo] | None = None) -> Guion:
        prompt = f"BRIEF:\n{to_json(brief)}"
        if previo is not None:
            prompt += f"\n\nBORRADOR ANTERIOR:\n{to_json(previo)}"
        if notas:
            prompt += "\n\nNOTAS DEL REVISOR (aplícalas todas):\n" + "\n".join(f"- {n}" for n in notas)
        if hallazgos:
            prompt += "\n\nHALLAZGOS AUTOMÁTICOS (corrige los errores y avisos):\n" + "\n".join(
                f"- [{h.nivel}] {h.donde}: {h.mensaje}" for h in hallazgos if h.nivel != "info")
        return self.run(prompt)


class RevisorGuiones(Agent[Revision]):
    """Evalúa un guion contra el brief y devuelve cambios concretos, no opiniones vagas."""

    name = "revisor_guiones"
    role = "Editor de guiones exigente: lees en voz alta, mides y propones cambios exactos."
    output_model = Revision

    @property
    def instructions(self) -> str:        # type: ignore[override]
        crit = "\n".join(f"- {k}: {v}" for k, v in CRITERIOS.items())
        return f"""\
Califica el guion del 1 al 10 en cada criterio y justifica con una cita breve del propio guion:
{crit}
Reglas de tu trabajo:
- `aprobado` solo si TODOS los criterios son >= 7 y no hay problemas de cumplimiento.
- Cada problema debe nombrar la toma. Cada reescritura debe ser concreta ("Toma 2: cambia 'X' por 'Y' porque…"),
  nunca "mejorar el ritmo".
- Lee cada toma como si la dijera una persona: marca lo que se traba, lo que suena a folleto y lo ambiguo.
- No pidas añadir datos que no están en el brief."""

    @property
    def system_prompt(self) -> str:
        return f"{REGLAS_REVISOR}\n\nTU ROL: {self.role}\n\n{self.instructions}"

    def revisar(self, brief: GuionBrief, guion: Guion, hallazgos: list[Hallazgo] | None = None) -> Revision:
        prompt = f"BRIEF:\n{to_json(brief)}\n\nGUION:\n{to_json(guion)}"
        if hallazgos:
            prompt += "\n\nHALLAZGOS AUTOMÁTICOS (ya medidos; tenlos en cuenta):\n" + "\n".join(
                f"- [{h.nivel}] {h.donde}: {h.mensaje}" for h in hallazgos)
        return self.run(prompt)
