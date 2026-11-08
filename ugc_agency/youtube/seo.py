"""Metadatos SEO para YouTube con las reglas de la plataforma validadas antes de subir."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

CATEGORIAS = {"educacion": "27", "ciencia_tecnologia": "28", "gente_blogs": "22", "como_hacer": "26", "negocios": "27"}


@dataclass
class Metadatos:
    titulo: str
    descripcion: str
    etiquetas: list[str] = field(default_factory=list)
    hashtags: list[str] = field(default_factory=list)
    capitulos: list[tuple[float, str]] = field(default_factory=list)
    categoria: str = "27"
    idioma: str = "es"
    contenido_sintetico: bool = True   # declarar voces/caras realistas generadas con IA
    para_ninos: bool = False

    def descripcion_final(self) -> str:
        partes = [self.descripcion.strip()]
        if self.capitulos:
            partes.append("Capítulos:\n" + "\n".join(f"{_ts(t)} {n}" for t, n in self.capitulos))
        if self.hashtags:
            partes.append(" ".join(h if h.startswith("#") else f"#{h}" for h in self.hashtags))
        return "\n\n".join(partes)

    def validar(self) -> list[str]:
        """Devuelve problemas que harían fallar la subida o empeorarían el SEO."""
        p = []
        if not self.titulo or len(self.titulo) > 100:
            p.append(f"El título debe tener 1-100 caracteres (tiene {len(self.titulo)}).")
        elif len(self.titulo) > 70:
            p.append(f"Aviso: el título tiene {len(self.titulo)} caracteres; en móvil se corta cerca de 60-70.")
        if "<" in self.titulo or ">" in self.titulo:
            p.append("El título no puede contener < ni >.")
        desc = self.descripcion_final()
        if len(desc.encode("utf-8")) > 5000:
            p.append("La descripción supera 5000 bytes.")
        if sum(len(e) + 1 for e in self.etiquetas) > 500:
            p.append("Las etiquetas suman más de 500 caracteres.")
        if self.capitulos:
            if self.capitulos[0][0] != 0:
                p.append("El primer capítulo debe empezar en 0:00.")
            if len(self.capitulos) < 3:
                p.append("YouTube necesita al menos 3 capítulos para mostrarlos.")
            for (a, _), (b, _) in zip(self.capitulos, self.capitulos[1:]):
                if b - a < 10:
                    p.append("Cada capítulo debe durar al menos 10 s.")
                    break
        if len(self.hashtags) > 15:
            p.append("Más de 15 hashtags: YouTube ignora todos.")
        return p

    def guardar(self, ruta: Path) -> None:
        ruta.write_text(json.dumps(asdict(self), indent=2, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def cargar(cls, ruta: Path) -> "Metadatos":
        d = json.loads(ruta.read_text(encoding="utf-8"))
        d["capitulos"] = [tuple(c) for c in d.get("capitulos", [])]
        return cls(**d)


def _ts(t: float) -> str:
    t = int(t)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02}:{s:02}" if h else f"{m}:{s:02}"
