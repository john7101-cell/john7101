"""Pruebas de la editorial de ebooks (sin llamar a la API)."""

from __future__ import annotations

import json
import shutil
import zipfile
from pathlib import Path

import pytest

from ugc_agency.ebooks import (
    Capitulo, Criterio, EbookBrief, EstudioEbook, FichaVenta, PlanCapitulo, PlanEditorial, RevisionCapitulo,
    contar_palabras, fernandez_huerta, leer_manuscrito, maquetar, revisar_texto,
)

EJEMPLO = Path(__file__).parent.parent / "examples" / "manuscrito_muestra.md"
BRIEF = EbookBrief(tema="Finanzas para freelancers", autor="Ana Ejemplo", palabras_objetivo=3000, n_capitulos=3,
                   prohibido=["hazte rico"])


def mensajes(hs, nivel):
    return " ".join(h.mensaje for h in hs if h.nivel == nivel)


# ------------------------------------------------------------------ corrector
def test_cliches_promesas_y_prohibidos():
    t = "En el mundo actual es importante destacar que este método está garantizado. Hazte rico con él."
    hs = revisar_texto(t, prohibido=["hazte rico"], ortografia=False)
    assert "en el mundo actual" in mensajes(hs, "aviso")
    assert "garantizado" in mensajes(hs, "error")
    assert "prohibido" in mensajes(hs, "error")


def test_extension_y_encabezado_principal():
    hs = revisar_texto("# Título\n\nPoco texto aquí.", palabras_objetivo=1000, ortografia=False)
    err = mensajes(hs, "error")
    assert "Corto" in err and "'#'" in err


def test_frase_larga_y_legibilidad():
    larga = " ".join(["palabra"] * 45) + "."
    hs = revisar_texto(larga, ortografia=False)
    assert "Frase de 45 palabras" in mensajes(hs, "aviso")
    facil = "El gato come. El perro duerme. La casa es grande. " * 20
    assert fernandez_huerta(facil) > 70


def test_conteo_ignora_markdown_y_tablas():
    assert contar_palabras("## Hola\n\n- uno **dos**\n\n| a | b |\n|---|---|\n| c | d |") == 3


# ------------------------------------------------------------------ estudio con un LLM simulado
class LLMFalso:
    def __init__(self):
        self.llamadas = []
        self.revisiones = 0

    def generate(self, *, system, prompt, output_model):
        self.llamadas.append(output_model.__name__)
        if output_model is PlanEditorial:
            caps = [PlanCapitulo(numero=i, titulo=f"Capítulo {i}", objetivo="o", gancho="g", puntos=["a", "b"],
                                 palabras=60) for i in (1, 2, 3)]
            return PlanEditorial(titulo="Dinero en orden", subtitulo="Para freelancers", alternativas_titulo=["X"],
                                 promesa="p", lector_ideal="l", angulo="a", voz="tú", introduccion="i",
                                 capitulos=caps, cierre="c")
        if output_model is Capitulo:
            texto = "Abre tres cuentas hoy. Separa el dinero del cliente del tuyo. " * 50
            return Capitulo(numero=1, titulo="x", contenido=texto, resumen="r", ideas_clave=["i"])
        if output_model is RevisionCapitulo:
            self.revisiones += 1
            ok = self.revisiones % 2 == 0          # aprueba en la segunda ronda
            return RevisionCapitulo(criterios=[Criterio(nombre="voz", puntaje=9 if ok else 6, comentario="c")],
                                    aprobado=ok, resumen="r", reescrituras=[] if ok else ["cambia X por Y"])
        if output_model is FichaVenta:
            return FichaVenta(descripcion_html="<p>d</p>", contraportada="c", palabras_clave=["k"] * 7,
                              categorias=["a"], bio_autor="[PENDIENTE]", texto_portada="t", precio_sugerido="4,99",
                              llamada_resena="Si te sirvió, deja una reseña honesta.")
        raise AssertionError(output_model)


def test_estudio_completo_y_reanudable(tmp_path):
    llm = LLMFalso()
    libro = EstudioEbook(llm, tmp_path, umbral=8, max_rondas=3).run(BRIEF)
    assert len(libro.capitulos) == 5                       # intro + 3 + conclusión
    assert all(r.rondas == 2 and r.aprobado for r in libro.capitulos)
    ms = (tmp_path / "manuscrito.md").read_text(encoding="utf-8")
    assert ms.startswith("---") and "# Introducción {.unnumbered}" in ms and "# Capítulo 2" in ms
    assert (tmp_path / "informe.md").exists() and (tmp_path / "plan.md").exists()
    # relanzar no vuelve a gastar API
    n = len(llm.llamadas)
    EstudioEbook(llm, tmp_path).run(BRIEF)
    assert len(llm.llamadas) == n
    # reescribir solo un capítulo
    EstudioEbook(llm, tmp_path).run(BRIEF, solo={2})
    assert llm.llamadas[n:].count("Capitulo") >= 1 and "PlanEditorial" not in llm.llamadas[n:]


# ------------------------------------------------------------------ maquetación
def test_leer_manuscrito():
    ms = leer_manuscrito(EJEMPLO)
    assert ms.titulo == "Dinero en orden" and ms.autor == "Ana Ejemplo"
    assert [s.numerada for s in ms.secciones] == [False, True, True, False]


@pytest.mark.skipif(shutil.which("pandoc") is None, reason="requiere pandoc")
def test_maquetar_epub_y_pdf(tmp_path):
    pytest.importorskip("typst")
    rep = maquetar(EJEMPLO, tmp_path)
    assert rep["epub_valido"], rep["epubcheck"]
    with zipfile.ZipFile(rep["epub"]) as z:
        nombres = z.namelist()
        assert nombres[0] == "mimetype" and any(n.endswith(".css") for n in nombres)
    assert Path(rep["pdf"]).read_bytes()[:4] == b"%PDF" and rep["paginas"] >= 8
    assert Path(rep["portada"]).exists()
    assert json.loads((tmp_path / "maquetacion.json").read_text(encoding="utf-8"))["titulo"] == "Dinero en orden"
