"""Pruebas del estudio de guiones (sin llamar a la API)."""

from __future__ import annotations

from ugc_agency.guiones import (
    Criterio, EstudioGuiones, Guion, GuionBrief, Revision, Toma, estimar_segundos, exportar, revisar_tomas,
)

BRIEF = GuionBrief(
    tema="Taller Volver a mí", genero_neutro=True, n_tomas=4, toma_max_s=8, duracion_s=30,
    datos_confirmados=["fecha: 29 de noviembre", "lugar: Club Nativos, Envigado"],
    en_pantalla=["WhatsApp: 315 322 8900"], prohibido=["última oportunidad"],
)


def niveles(hs, nivel):
    return [h for h in hs if h.nivel == nivel]


def test_duracion_estimada_cerca_de_los_clips_reales():
    # clips reales medidos en el proyecto: 7.9 s (19 palabras con pausas) y 7.5 s (18 palabras)
    t2 = "Esperas su respuesta. Buscas su aprobación. Callas para que no se vaya… y poco a poco, te quedas sin ti."
    t4 = "Se llama… Volver a mí. Te espero el veintinueve de noviembre, en Club Nativos, Envigado. Escríbeme por WhatsApp."
    assert abs(estimar_segundos(t2) - 7.9) < 0.8
    assert abs(estimar_segundos(t4) - 7.5) < 0.8


def test_toma_demasiado_larga_es_error():
    largo = "Escríbeme por WhatsApp para más información y cupos, ya que serán limitados y se agotan rápido en cada edición."
    hs = revisar_tomas([(1, largo + " " + largo)], BRIEF)
    assert any("máximo" in h.mensaje for h in niveles(hs, "error"))


def test_telefono_en_la_voz_y_dato_de_pantalla():
    hs = revisar_tomas([(1, "Escríbeme al 315 322 8900.")], BRIEF)
    msgs = " ".join(h.mensaje for h in niveles(hs, "error"))
    assert "teléfono" in msgs and "dato de pantalla" in msgs


def test_promesas_y_diagnosticos():
    hs = revisar_tomas([(1, "Tu ansiedad se cura, garantizado, resultados 100% seguros.")], BRIEF)
    assert len(niveles(hs, "error")) >= 3


def test_genero_marcado_solo_si_el_brief_pide_neutralidad():
    texto = "Un espacio solo para mujeres, para todas."
    assert any("género" in h.mensaje for h in revisar_tomas([(1, texto)], BRIEF))
    abierto = BRIEF.model_copy(update={"genero_neutro": False})
    assert not any("género" in h.mensaje for h in revisar_tomas([(1, texto)], abierto))


def test_solo_como_adverbio_no_es_genero():
    hs = revisar_tomas([(1, "Solo ven cómo funciona.")], BRIEF)
    assert not any("género" in h.mensaje for h in hs)


def test_datos_no_confirmados_y_prohibidos():
    hs = revisar_tomas([(1, "El 15 de diciembre es la última oportunidad."), ], BRIEF)
    msgs = " ".join(h.mensaje for h in hs)
    assert "diciembre" in msgs and "prohibido" in msgs and "15" in msgs


def test_confirmados_no_generan_aviso():
    hs = revisar_tomas([(1, "Será el 29 de noviembre, en Club Nativos, Envigado.")], BRIEF)
    assert not any("no aparece" in h.mensaje or "datos confirmados" in h.mensaje for h in hs)


def test_repeticion_entre_tomas():
    hs = revisar_tomas([(1, "Te espero el veintinueve de noviembre en Club Nativos."),
                        (2, "Recuerda: te espero el veintinueve de noviembre en Club Nativos.")], BRIEF)
    assert any("repite" in h.mensaje for h in hs)


def test_etiquetas_no_cuentan_como_palabras():
    con = "[intrigante, voz baja y cercana] ¿Y si no amas demasiado… [pausa] sino que te olvidaste de ti?"
    sin = "¿Y si no amas demasiado… sino que te olvidaste de ti?"
    assert estimar_segundos(con) >= estimar_segundos(sin) - 0.01      # la pausa suma; las etiquetas no
    assert estimar_segundos(con) < estimar_segundos(sin) + 0.5


# ---------------------------------------------------------------- bucle del estudio con LLM falso
class FakeLLM:
    """Primer borrador con una toma de 31 palabras y teléfono en la voz; el segundo ya cumple."""

    def __init__(self) -> None:
        self.escritos = 0
        self.revisiones = 0

    def generate(self, *, system, prompt, output_model):
        if output_model is Guion:
            self.escritos += 1
            if self.escritos == 1:
                voces = ["¿Y si no amas demasiado… sino que te olvidaste de ti?",
                         "Esperas su respuesta. Buscas su aprobación. Callas para que no se vaya.",
                         "Un taller para ti.",
                         "Se llama Volver a mí. Será el veintinueve de noviembre en Club Nativos, Envigado, escríbeme por WhatsApp al 315 322 8900 "
                         "para más información sobre cupos, horarios, precios y todo lo demás que necesites saber."]
            else:
                assert "NOTAS DEL REVISOR" in prompt and "HALLAZGOS AUTOMÁTICOS" in prompt
                voces = ["¿Y si no amas demasiado… sino que te olvidaste de ti?",
                         "Esperas su respuesta. Buscas su aprobación. Callas para que no se vaya.",
                         "Por eso preparé un taller para ti.",
                         "Se llama Volver a mí. Será el 29 de noviembre en Club Nativos, Envigado. Escríbeme por WhatsApp."]
            return Guion(titulo="Volver a mí", gancho=voces[0], arco="gancho, dolor, giro, invitación",
                         tomas=[Toma(numero=i + 1, intencion="x", voz=v, voz_con_emociones=f"[cálida] {v}") for i, v in enumerate(voces)],
                         pendientes=["hora de inicio"])
        if output_model is Revision:
            self.revisiones += 1
            ok = self.revisiones > 1
            return Revision(
                criterios=[Criterio(nombre="gancho", puntaje=8 if ok else 6, comentario="c")], aprobado=ok, resumen="ok" if ok else "ajustar",
                problemas=[] if ok else ["Toma 4: demasiado larga"], reescrituras=[] if ok else ["Toma 4: quita el teléfono y los cupos"])
        raise AssertionError(output_model)


def test_estudio_reescribe_hasta_aprobar_y_exporta(tmp_path):
    llm = FakeLLM()
    res = EstudioGuiones(llm, max_rondas=3).run(BRIEF)
    assert res.rondas == 2 and res.aprobado
    assert llm.escritos == 2 and llm.revisiones == 2
    out = exportar(res, tmp_path / "g")
    assert "APROBADO" in (out / "guion.md").read_text(encoding="utf-8")
    assert (out / "voz_con_emociones.txt").read_text(encoding="utf-8").startswith("[cálida]")
    plano = (out / "voz_sin_etiquetas.txt").read_text(encoding="utf-8")
    assert "[" not in plano and "Volver a mí" in plano
    assert (out / "toma4_voz.txt").exists() and (out / "guion.json").exists()


def test_estudio_se_detiene_en_max_rondas():
    class SiempreMal(FakeLLM):
        def generate(self, *, system, prompt, output_model):
            if output_model is Revision:
                return Revision(criterios=[Criterio(nombre="gancho", puntaje=3, comentario="c")], aprobado=False,
                                resumen="mal", problemas=["x"], reescrituras=["y"])
            self.escritos = 0                      # siempre el primer borrador defectuoso (super lo sube a 1)
            return super().generate(system=system, prompt=prompt, output_model=output_model)

    res = EstudioGuiones(SiempreMal(), max_rondas=2).run(BRIEF)
    assert res.rondas == 2 and not res.aprobado
