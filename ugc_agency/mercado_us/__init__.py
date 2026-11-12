"""Mercado EE. UU.: calculadora de métricas y diagnóstico para TikTok, TikTok Shop y Meta Ads."""

from .metricas import (
    Economia, Hallazgo, Metricas, Reporte, calcular, diagnosticar, margen_contribucion, reporte_desde_dict,
)

__all__ = [
    "Economia", "Hallazgo", "Metricas", "Reporte", "calcular", "diagnosticar", "margen_contribucion",
    "reporte_desde_dict",
]
