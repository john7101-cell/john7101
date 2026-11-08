"""Pruebas del módulo de YouTube sin conexión (no llaman a la API)."""

from pathlib import Path

import pytest
from PIL import Image

from ugc_agency.youtube.miniatura import ALTO, ANCHO, crear
from ugc_agency.youtube.publicar import cuerpo, subir
from ugc_agency.youtube.seo import Metadatos


def _meta(**kw):
    base = dict(titulo="Cómo vender en México", descripcion="Guía rápida.", etiquetas=["importar", "méxico"],
                hashtags=["comercioexterior"], capitulos=[(0, "Intro"), (15, "Paso 1"), (40, "Paso 2")])
    base.update(kw)
    return Metadatos(**base)


def test_metadatos_validos_y_descripcion_con_capitulos():
    m = _meta()
    assert m.validar() == []
    d = m.descripcion_final()
    assert "0:00 Intro" in d and "0:40 Paso 2" in d and "#comercioexterior" in d


@pytest.mark.parametrize("kw,fragmento", [
    ({"titulo": "x" * 101}, "1-100"),
    ({"capitulos": [(5, "a"), (20, "b"), (40, "c")]}, "0:00"),
    ({"capitulos": [(0, "a"), (5, "b"), (40, "c")]}, "10 s"),
    ({"etiquetas": ["e" * 60] * 10}, "500"),
])
def test_validacion_detecta_problemas(kw, fragmento):
    assert any(fragmento in p for p in _meta(**kw).validar())


def test_programado_queda_privado_y_declara_ia():
    from datetime import datetime, timedelta, timezone

    b = cuerpo(_meta(), publicar_en=datetime(2030, 1, 1, tzinfo=timezone(timedelta(hours=-5))))
    assert b["status"]["privacyStatus"] == "private" and "publishAt" in b["status"]
    assert b["status"]["containsSyntheticMedia"] is True


def test_sin_confirmar_no_sube(tmp_path: Path):
    r = subir(tmp_path / "v.mp4", _meta(), confirmar=False, log=lambda _: None)
    assert r["simulacion"] is True


def test_miniatura_tamano_y_peso(tmp_path: Path):
    fondo = tmp_path / "f.png"
    Image.new("RGB", (720, 1280), (90, 120, 160)).save(fondo)
    out = crear(fondo, ["Vende en", "*México*"], tmp_path / "m.jpg", etiqueta="Guía")
    im = Image.open(out)
    assert im.size == (ANCHO, ALTO) and out.stat().st_size < 2 * 1024 * 1024
