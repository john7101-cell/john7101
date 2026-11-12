"""Pruebas de la calculadora de métricas del mercado EE. UU. (sin red)."""

from __future__ import annotations

import json
from pathlib import Path

from ugc_agency.mercado_us import Economia, Metricas, calcular, diagnosticar, margen_contribucion, reporte_desde_dict


def sem(rep, nombre):
    return next(h.semaforo for h in rep.hallazgos if h.metrica == nombre)


def test_margen_y_roas_de_equilibrio():
    m = margen_contribucion(Economia(precio=30, cogs=8, envio=4, comision_plataforma_pct=6, comision_afiliado_pct=10, devoluciones_pct=5))
    # 30 - 8 - 4 - 4.8 (16 %) - 1.5 (5 %) = 11.7
    assert m["margen_usd"] == 11.7
    assert m["roas_equilibrio"] == round(1 / (11.7 / 30), 2)


def test_margen_no_positivo_no_da_roas_de_equilibrio():
    m = margen_contribucion(Economia(precio=20, cogs=18, envio=4))
    assert m["roas_equilibrio"] is None and m["cpa_maximo_usd"] is None


def test_derivadas():
    d = calcular(Metricas(impresiones=10000, vistas_3s=3000, thruplays=900, clics=150, gasto=100, compras=5, ingresos=250))
    assert d["hook_rate"] == 0.3 and d["hold_rate"] == 0.3 and d["ctr"] == 0.015
    assert d["cpa"] == 20.0 and d["roas"] == 2.5 and d["aov"] == 50.0


def test_hook_bajo_es_el_cuello_de_botella():
    rep = diagnosticar(Metricas(impresiones=50000, vistas_3s=7500, thruplays=3000, clics=600, compras=30, visitas_ficha=500))
    assert sem(rep, "hook_rate") == "rojo"          # 15 %
    assert rep.cuello_de_botella == "hook_rate"


def test_muestra_chica_es_inconcluso():
    rep = diagnosticar(Metricas(impresiones=300, vistas_3s=40, clics=3, compras=1, visitas_ficha=10))
    assert sem(rep, "hook_rate") == "inconcluso"
    assert sem(rep, "cvr") == "inconcluso"
    assert rep.cuello_de_botella is None


def test_roas_bajo_el_equilibrio_es_rojo():
    rep = diagnosticar(Metricas(gasto=500, ingresos=600),
                       Economia(precio=30, cogs=8, envio=4, comision_plataforma_pct=6))
    assert sem(rep, "roas") == "rojo"


def test_roas_sin_economia_pide_datos():
    rep = diagnosticar(Metricas(gasto=100, ingresos=300))
    assert sem(rep, "roas") == "sin dato"
    assert any("COGS" in d for d in rep.datos_pendientes)


def test_margen_negativo_se_marca():
    rep = diagnosticar(Metricas(), Economia(precio=20, cogs=18, envio=4))
    assert sem(rep, "margen") == "rojo"


def test_ejemplo_del_repo_funciona():
    data = json.loads((Path(__file__).parent.parent / "examples" / "metricas_ejemplo.json").read_text(encoding="utf-8"))
    rep = reporte_desde_dict(data)
    assert rep.cuello_de_botella == "hook_rate" and rep.economia["roas_equilibrio"] > 1
