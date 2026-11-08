"""Autenticación OAuth con la API de YouTube.

Las credenciales se leen de variables de entorno que el dueño del canal configura en los
ajustes del entorno (nunca en el chat ni en el código):

    YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
"""

from __future__ import annotations

import os

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


class FaltanCredenciales(RuntimeError):
    pass


def credenciales():
    from google.oauth2.credentials import Credentials

    faltan = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.getenv(k)]
    if faltan:
        raise FaltanCredenciales(
            "Faltan variables de entorno: " + ", ".join(faltan)
            + ". Agrégalas en los ajustes del entorno (no en el chat). Guía: docs/youtube_conexion.md"
        )
    return Credentials(
        token=None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )


def youtube():
    from googleapiclient.discovery import build

    return build("youtube", "v3", credentials=credenciales(), cache_discovery=False)


def analytics():
    from googleapiclient.discovery import build

    return build("youtubeAnalytics", "v2", credentials=credenciales(), cache_discovery=False)
