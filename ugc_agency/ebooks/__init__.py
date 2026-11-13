"""Editorial de ebooks: estratega, escritor, editor y maquetador profesional (EPUB, PDF de imprenta y portadas)."""

from .agentes import EditorComercial, EditorDesarrollo, Escritor, EstrategaEditorial
from .estudio import EstudioEbook, Libro, ResultadoCapitulo, exportar, manuscrito, plan_markdown
from .lint import contar_palabras, fernandez_huerta, resumen, revisar_texto
from .maquetacion import leer_manuscrito, maquetar, portada_ebook, resumen_maquetacion, validar_epub
from .modelos import (
    Capitulo, Criterio, EbookBrief, FichaVenta, Hallazgo, PlanCapitulo, PlanEditorial, RevisionCapitulo,
)

__all__ = [
    "Capitulo", "Criterio", "EbookBrief", "EditorComercial", "EditorDesarrollo", "Escritor", "EstrategaEditorial",
    "EstudioEbook", "FichaVenta", "Hallazgo", "Libro", "PlanCapitulo", "PlanEditorial", "ResultadoCapitulo",
    "RevisionCapitulo", "contar_palabras", "exportar", "fernandez_huerta", "leer_manuscrito", "manuscrito", "maquetar",
    "plan_markdown", "portada_ebook", "resumen", "resumen_maquetacion", "revisar_texto", "validar_epub",
]
