"""Métricas y diagnóstico de campañas/canales (TikTok, TikTok Shop, Meta Ads).

Los rangos son REFERENCIAS orientativas tomadas de fuentes de terceros (ver docs/tiktok_us/metricas.md),
no reglas de TikTok ni de Meta. Todo es configurable. Cuando la muestra es chica el resultado es
"inconcluso" en lugar de inventar una conclusión.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Optional

VERDE, AMBAR, ROJO, SIN_DATO, INCONCLUSO = "verde", "ámbar", "rojo", "sin dato", "inconcluso"

# Referencias (verificar): hook rate = vistas de 3 s ÷ impresiones; hold rate = ThruPlays ÷ vistas de 3 s.
REFERENCIAS = {
    "hook_rate": {"rojo_bajo": 0.25, "verde_desde": 0.30},          # <25 % flojo; ≥30 % bueno; ≥40 % élite
    "hold_rate": {"rojo_bajo": 0.20, "verde_desde": 0.30},          # ThruPlays ÷ vistas 3 s (definición propia)
    "ctr": {"rojo_bajo": 0.008, "verde_desde": 0.012},              # CTR de enlace
    "cvr": {"rojo_bajo": 0.01, "verde_desde": 0.025},               # compras ÷ clics/visitas a ficha
    "frecuencia_max": 3.0,                                          # prospecting
}
MIN_IMPRESIONES_GANCHO = 1000
MIN_CLICS_CTR = 100
MIN_COMPRAS_CVR = 10


@dataclass
class Economia:
    precio: float
    cogs: float = 0.0
    envio: float = 0.0                       # costo de envío/logística asumido por el vendedor por pedido
    comision_plataforma_pct: float = 6.0     # referral fee: VERIFICAR en Seller Center (fuentes dicen 6 % u 8 %)
    comision_afiliado_pct: float = 0.0
    devoluciones_pct: float = 0.0            # % esperado de ventas devueltas


@dataclass
class Metricas:
    impresiones: Optional[float] = None
    vistas: Optional[float] = None           # vistas de video (orgánico)
    vistas_3s: Optional[float] = None
    thruplays: Optional[float] = None
    clics: Optional[float] = None            # clics en el enlace
    gasto: Optional[float] = None
    visitas_ficha: Optional[float] = None
    compras: Optional[float] = None
    ingresos: Optional[float] = None
    frecuencia: Optional[float] = None
    compartidos: Optional[float] = None
    guardados: Optional[float] = None


@dataclass
class Hallazgo:
    metrica: str
    valor: Optional[float]
    semaforo: str
    mensaje: str


@dataclass
class Reporte:
    derivadas: dict = field(default_factory=dict)
    economia: dict = field(default_factory=dict)
    hallazgos: list[Hallazgo] = field(default_factory=list)
    cuello_de_botella: Optional[str] = None
    datos_pendientes: list[str] = field(default_factory=list)

    def a_dict(self) -> dict:
        d = asdict(self)
        return d


def _div(a: Optional[float], b: Optional[float]) -> Optional[float]:
    if a is None or b in (None, 0):
        return None
    return a / b


def margen_contribucion(e: Economia) -> dict:
    """Margen por pedido y ROAS de equilibrio (1 ÷ margen %). Sin margen positivo no hay pauta rentable."""
    comisiones = e.precio * (e.comision_plataforma_pct + e.comision_afiliado_pct) / 100
    devol = e.precio * e.devoluciones_pct / 100
    margen = e.precio - e.cogs - e.envio - comisiones - devol
    pct = margen / e.precio if e.precio else 0.0
    return {
        "margen_usd": round(margen, 2),
        "margen_pct": round(pct, 4),
        "roas_equilibrio": round(1 / pct, 2) if pct > 0 else None,
        "cpa_maximo_usd": round(margen, 2) if margen > 0 else None,
    }


def calcular(m: Metricas) -> dict:
    """Métricas derivadas (solo las que se pueden calcular con los datos entregados)."""
    d = {
        "ctr": _div(m.clics, m.impresiones),
        "cpm": (_div(m.gasto, m.impresiones) or 0) * 1000 if m.gasto is not None and m.impresiones else None,
        "cpc": _div(m.gasto, m.clics),
        "hook_rate": _div(m.vistas_3s, m.impresiones if m.impresiones else m.vistas),
        "hold_rate": _div(m.thruplays, m.vistas_3s),
        "cvr": _div(m.compras, m.visitas_ficha if m.visitas_ficha else m.clics),
        "cpa": _div(m.gasto, m.compras),
        "roas": _div(m.ingresos, m.gasto),
        "aov": _div(m.ingresos, m.compras),
        "compartidos_guardados_por_vista": _div((m.compartidos or 0) + (m.guardados or 0),
                                                m.vistas or m.impresiones) if (m.compartidos or m.guardados) else None,
    }
    return {k: (round(v, 4) if v is not None else None) for k, v in d.items()}


def _semaforo(valor: float, ref: dict) -> str:
    if valor < ref["rojo_bajo"]:
        return ROJO
    return VERDE if valor >= ref["verde_desde"] else AMBAR


def diagnosticar(m: Metricas, e: Optional[Economia] = None) -> Reporte:
    """Semáforo por eslabón del embudo (de arriba hacia abajo) y primer cuello de botella."""
    rep = Reporte(derivadas=calcular(m))
    d = rep.derivadas
    eco = margen_contribucion(e) if e else {}
    rep.economia = eco
    h = rep.hallazgos

    def agregar(nombre, valor, semaforo, msg):
        h.append(Hallazgo(nombre, valor, semaforo, msg))

    base_gancho = m.impresiones or m.vistas
    if d["hook_rate"] is None:
        agregar("hook_rate", None, SIN_DATO, "Falta vistas de 3 s e impresiones/vistas.")
        rep.datos_pendientes.append("vistas de 3 s e impresiones (para el hook rate)")
    elif (base_gancho or 0) < MIN_IMPRESIONES_GANCHO:
        agregar("hook_rate", d["hook_rate"], INCONCLUSO, f"Menos de {MIN_IMPRESIONES_GANCHO} impresiones: muestra chica.")
    else:
        s = _semaforo(d["hook_rate"], REFERENCIAS["hook_rate"])
        msg = {ROJO: "El gancho no detiene el scroll: probar hooks nuevos antes de tocar lo demás.",
               AMBAR: "Gancho aceptable, mejorable con variantes del mismo ángulo.",
               VERDE: "El gancho funciona."}[s]
        agregar("hook_rate", d["hook_rate"], s, msg)

    if d["hold_rate"] is None:
        agregar("hold_rate", None, SIN_DATO, "Falta ThruPlays (o vistas completas) y vistas de 3 s.")
    elif (m.vistas_3s or 0) < MIN_IMPRESIONES_GANCHO / 4:
        agregar("hold_rate", d["hold_rate"], INCONCLUSO, "Muestra chica de vistas de 3 s.")
    else:
        s = _semaforo(d["hold_rate"], REFERENCIAS["hold_rate"])
        msg = {ROJO: "El cuerpo no cumple el gancho: recortar, reordenar la prueba y acelerar el ritmo.",
               AMBAR: "Retención media: probar abrir con el resultado y cortar relleno.",
               VERDE: "El cuerpo sostiene la atención."}[s]
        agregar("hold_rate", d["hold_rate"], s, msg)

    if d["ctr"] is None:
        agregar("ctr", None, SIN_DATO, "Falta clics en el enlace e impresiones.")
    elif (m.clics or 0) < MIN_CLICS_CTR and (m.impresiones or 0) < 5000:
        agregar("ctr", d["ctr"], INCONCLUSO, "Muestra chica de clics/impresiones.")
    else:
        s = _semaforo(d["ctr"], REFERENCIAS["ctr"])
        msg = {ROJO: "Poca intención de clic: la promesa/CTA o el ángulo no convence.",
               AMBAR: "CTR medio: reforzar la prueba y el CTA.", VERDE: "CTR sólido."}[s]
        agregar("ctr", d["ctr"], s, msg)

    if d["cvr"] is None:
        agregar("cvr", None, SIN_DATO, "Faltan compras y visitas a ficha o clics.")
        rep.datos_pendientes.append("compras y visitas a la ficha (para el CVR)")
    elif (m.compras or 0) < MIN_COMPRAS_CVR:
        agregar("cvr", d["cvr"], INCONCLUSO, f"Menos de {MIN_COMPRAS_CVR} compras: no se puede leer el CVR.")
    else:
        s = _semaforo(d["cvr"], REFERENCIAS["cvr"])
        msg = {ROJO: "El tráfico llega pero no compra: revisar precio, oferta, reseñas, envío y ficha.",
               AMBAR: "Conversión media: probar bundle, prueba social y garantía de compra.",
               VERDE: "Buena conversión."}[s]
        agregar("cvr", d["cvr"], s, msg)

    if m.frecuencia is not None and m.frecuencia > REFERENCIAS["frecuencia_max"]:
        agregar("frecuencia", m.frecuencia, AMBAR, "Frecuencia alta: riesgo de fatiga; refrescar creativos.")

    roas, eq = d["roas"], eco.get("roas_equilibrio") if eco else None
    if e and eco.get("margen_usd", 0) <= 0:
        agregar("margen", eco.get("margen_usd"), ROJO,
                "El margen de contribución es ≤ 0: no se puede pautar con ganancia. Ajustar precio, COGS, bundle o comisiones.")
    if roas is not None and eq:
        s = VERDE if roas >= eq * 1.2 else (AMBAR if roas >= eq else ROJO)
        msg = {VERDE: f"ROAS {roas} sobre el equilibrio ({eq}): hay utilidad.",
               AMBAR: f"ROAS {roas} apenas sobre el equilibrio ({eq}): sin colchón.",
               ROJO: f"ROAS {roas} bajo el equilibrio ({eq}): se pierde dinero."}[s]
        agregar("roas", roas, s, msg)
    elif roas is not None:
        agregar("roas", roas, SIN_DATO, "Hay ROAS pero falta la economía (precio/COGS/comisiones) para saber si deja utilidad.")
        rep.datos_pendientes.append("precio, COGS, envío y comisiones (para el ROAS de equilibrio)")

    for x in h:
        if x.semaforo in (ROJO, AMBAR):
            rep.cuello_de_botella = x.metrica
            break
    return rep


def reporte_desde_dict(data: dict) -> Reporte:
    """Arma el reporte desde un dict {"metricas": {...}, "economia": {...}}."""
    m = Metricas(**{k: v for k, v in (data.get("metricas") or {}).items() if k in Metricas.__dataclass_fields__})
    eco = data.get("economia")
    e = Economia(**{k: v for k, v in eco.items() if k in Economia.__dataclass_fields__}) if eco else None
    return diagnosticar(m, e)
