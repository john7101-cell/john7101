"""El equipo editorial: Estratega, Escritor, Editor de desarrollo y Editor comercial."""

from __future__ import annotations

from ..agents.base import Agent, to_json
from .modelos import Capitulo, EbookBrief, FichaVenta, Hallazgo, PlanCapitulo, PlanEditorial, RevisionCapitulo
from .reglas import CRITERIOS, REGLAS_OFICIO


class _Editorial(Agent):
    @property
    def system_prompt(self) -> str:       # usa el oficio editorial, no la biblia de UGC
        return f"{REGLAS_OFICIO}\n\nTU ROL: {self.role}\n\n{self.instructions}".strip()


class EstrategaEditorial(_Editorial):
    name = "estratega_editorial"
    role = ("Editor de adquisiciones y estratega de mercado de ebooks: conoces lo que se vende en Amazon, "
            "cómo se posiciona un título y cómo se estructura un libro que se lee entero.")
    instructions = """\
Diseña el plan editorial del brief:
- Título corto y memorable + subtítulo con la promesa concreta y las palabras que el lector buscaría.
- Ángulo diferencial frente a los competidores del brief (si no hay, frente a lo típico del tema).
- Guía de voz precisa para que todos los capítulos suenen al mismo autor.
- Exactamente `n_capitulos` capítulos en progresión lógica (de diagnóstico a método a aplicación),
  sin solapamientos. Reparte `palabras_objetivo` entre ellos (introducción y conclusión aparte, ~6 % cada una).
- Cada capítulo con objetivo medible, gancho, 4-8 puntos y una herramienta práctica.
- Lista en `pendientes` los datos que harían el libro más creíble y que el autor debe aportar."""
    output_model = PlanEditorial

    def planificar(self, brief: EbookBrief, notas: str = "") -> PlanEditorial:
        prompt = f"BRIEF:\n{to_json(brief)}"
        if notas:
            prompt += f"\n\nINDICACIONES DEL EDITOR:\n{notas}"
        return self.run(prompt)


class Escritor(_Editorial):
    name = "escritor"
    role = ("Escritor profesional de no ficción comercial (ghostwriter senior). Escribes capítulos completos, "
            "publicables, con la voz del autor y sin relleno.")
    instructions = """\
Escribe el capítulo indicado COMPLETO, en Markdown, con la extensión pedida (±10 %).
- Sigue la guía de voz y el plan; conecta con lo que ya se contó (resúmenes previos) sin repetirlo.
- No repitas el título del capítulo como encabezado: empieza directamente con el gancho.
- Incluye la herramienta práctica del plan en formato usable (pasos numerados, checklist o plantilla).
- Cierra con '## Ideas clave' (3-6 viñetas) y una frase puente al siguiente capítulo (si lo hay).
- Si recibes notas del editor o hallazgos del corrector, corrígelos TODOS y conserva lo que funcionaba."""
    output_model = Capitulo

    def escribir(self, brief: EbookBrief, plan: PlanEditorial, cap: PlanCapitulo, resumenes: list[str],
                 previo: Capitulo | None = None, notas: list[str] | None = None,
                 hallazgos: list[Hallazgo] | None = None) -> Capitulo:
        datos = {
            "tema": brief.tema, "idioma": brief.idioma, "tono": brief.tono, "lector": plan.lector_ideal,
            "promesa_libro": plan.promesa, "voz": plan.voz, "datos_confirmados": brief.datos_confirmados,
            "prohibido": brief.prohibido, "material_autor": brief.material[:30000],
        }
        indice = "\n".join(f"{c.numero}. {c.titulo} — {c.objetivo}" for c in plan.capitulos)
        prompt = (f"CONTEXTO DEL LIBRO:\n{to_json(datos)}\n\nTÍTULO: {plan.titulo}: {plan.subtitulo}\n\n"
                  f"ÍNDICE:\n{indice}\n\nCAPÍTULO A ESCRIBIR:\n{to_json(cap)}")
        if resumenes:
            prompt += "\n\nLO QUE YA SE CONTÓ (resúmenes de capítulos anteriores):\n" + "\n".join(f"- {r}" for r in resumenes)
        if previo is not None:
            prompt += f"\n\nBORRADOR ANTERIOR (reescríbelo):\n{previo.contenido}"
        if notas:
            prompt += "\n\nNOTAS DEL EDITOR (aplícalas todas):\n" + "\n".join(f"- {n}" for n in notas)
        if hallazgos:
            prompt += "\n\nHALLAZGOS DEL CORRECTOR AUTOMÁTICO:\n" + "\n".join(
                f"- [{h.nivel}] {h.mensaje}" for h in hallazgos if h.nivel != "info")
        return self.run(prompt)


class EditorDesarrollo(_Editorial):
    name = "editor_desarrollo"
    role = "Editor de desarrollo y de estilo exigente: lees como el lector que pagó y como el editor que firma la calidad."
    output_model = RevisionCapitulo

    @property
    def instructions(self) -> str:        # type: ignore[override]
        crit = "\n".join(f"- {k}: {v}" for k, v in CRITERIOS.items())
        return f"""\
Califica el capítulo del 1 al 10 en cada criterio, con una cita breve del propio texto:
{crit}
- `aprobado` solo si TODOS los criterios son >= 8 y no hay datos inventados ni promesas indebidas.
- Cada problema cita el pasaje. Cada reescritura es exacta ("cambia 'X' por 'Y' porque…", "corta el párrafo que
  empieza por '…'", "añade un ejemplo de … en la sección '…'"), nunca "mejora el ritmo".
- Marca como problema cualquier cifra, estudio, cita o caso que no esté en los datos confirmados.
- Ten en cuenta los hallazgos del corrector automático, pero juzga tú si de verdad molestan al lector."""

    def revisar(self, brief: EbookBrief, plan: PlanEditorial, cap: PlanCapitulo, escrito: Capitulo,
                hallazgos: list[Hallazgo]) -> RevisionCapitulo:
        prompt = (f"PROMESA DEL LIBRO: {plan.promesa}\nGUÍA DE VOZ: {plan.voz}\n"
                  f"DATOS CONFIRMADOS:\n{to_json(brief.datos_confirmados)}\nPROHIBIDO: {to_json(brief.prohibido)}\n\n"
                  f"PLAN DEL CAPÍTULO:\n{to_json(cap)}\n\nTEXTO:\n{escrito.contenido}\n\n"
                  "HALLAZGOS AUTOMÁTICOS:\n" + ("\n".join(f"- [{h.nivel}] {h.mensaje}" for h in hallazgos) or "(ninguno)"))
        return self.run(prompt)


class EditorComercial(_Editorial):
    name = "editor_comercial"
    role = "Especialista en lanzamientos de Amazon KDP: descripción, palabras clave, categorías y precio."
    instructions = """\
Prepara la ficha de venta del libro terminado.
- Descripción: abre con el dolor/deseo del lector, la promesa, 4-6 viñetas de lo que aprenderá (concretas,
  tomadas de los capítulos), para quién es y una llamada a la acción. HTML simple permitido por KDP.
- 7 palabras clave: frases que la gente escribe en Amazon (long tail), sin marcas ajenas, sin "gratis",
  sin repetir palabras del título, ≤ 50 caracteres.
- Nada de promesas indebidas, superlativos sin respaldo ni reseñas inventadas."""
    output_model = FichaVenta

    def ficha(self, brief: EbookBrief, plan: PlanEditorial, capitulos: list[Capitulo]) -> FichaVenta:
        datos = {"titulo": plan.titulo, "subtitulo": plan.subtitulo, "promesa": plan.promesa, "lector": plan.lector_ideal,
                 "angulo": plan.angulo, "autor": brief.autor, "mercado": brief.mercado, "precio_usd": brief.precio_usd,
                 "competidores": brief.competidores,
                 "capitulos": [{"titulo": c.titulo, "ideas_clave": c.ideas_clave} for c in capitulos]}
        return self.run(f"LIBRO:\n{to_json(datos)}")
