"""Estado del canal y progreso hacia el Programa de Socios de YouTube (YPP)."""

from __future__ import annotations

from datetime import date, timedelta

from .auth import analytics, youtube

# Umbrales públicos del YPP con anuncios (verifícalos en YouTube Studio > Ganar dinero):
UMBRAL_SUSCRIPTORES = 1000
UMBRAL_HORAS_365 = 4000
UMBRAL_VISTAS_SHORTS_90 = 10_000_000


def estado() -> dict:
    yt = youtube()
    canal = yt.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()["items"][0]
    stats = canal["statistics"]
    hoy = date.today()
    rep = analytics().reports().query(
        ids="channel==MINE", startDate=str(hoy - timedelta(days=365)), endDate=str(hoy),
        metrics="estimatedMinutesWatched,views",
    ).execute()
    minutos, vistas_365 = (rep.get("rows") or [[0, 0]])[0]
    subs = int(stats.get("subscriberCount", 0))
    horas = minutos / 60
    return {
        "canal": canal["snippet"]["title"],
        "suscriptores": subs,
        "videos": int(stats.get("videoCount", 0)),
        "vistas_totales": int(stats.get("viewCount", 0)),
        "horas_vistas_365d": round(horas, 1),
        "progreso_suscriptores": f"{subs}/{UMBRAL_SUSCRIPTORES} ({min(100, subs / UMBRAL_SUSCRIPTORES * 100):.0f}%)",
        "progreso_horas": f"{horas:.0f}/{UMBRAL_HORAS_365} ({min(100, horas / UMBRAL_HORAS_365 * 100):.0f}%)",
        "uploads_playlist": canal["contentDetails"]["relatedPlaylists"]["uploads"],
    }
