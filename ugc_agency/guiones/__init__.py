"""Estudio de guiones: un Guionista y un Revisor especializados en voz hablada, retención y cumplimiento."""

from .agentes import Guionista, RevisorGuiones
from .estudio import EstudioGuiones, ResultadoGuion, exportar, leer_material
from .lint import estimar_segundos, resumen, revisar_tomas
from .modelos import Criterio, Guion, GuionBrief, Hallazgo, Revision, Toma

__all__ = [
    "Criterio", "EstudioGuiones", "Guion", "GuionBrief", "Guionista", "Hallazgo", "ResultadoGuion",
    "Revision", "RevisorGuiones", "Toma", "estimar_segundos", "exportar", "leer_material", "resumen", "revisar_tomas",
]
