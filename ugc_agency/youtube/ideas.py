"""Investigación de ideas: qué videos de un tema están funcionando ahora mismo."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .auth import youtube


def investigar(tema: str, dias: int = 90, region: str = "MX", idioma: str = "es", n: int = 25) -> list[dict]:
    """Busca videos recientes del tema y los ordena por vistas por día (cuesta ~101 unidades de cuota)."""
    yt = youtube()
    desde = (datetime.now(timezone.utc) - timedelta(days=dias)).isoformat().replace("+00:00", "Z")
    res = yt.search().list(part="id", q=tema, type="video", order="viewCount", publishedAfter=desde,
                           regionCode=region, relevanceLanguage=idioma, maxResults=min(n, 50)).execute()
    ids = [i["id"]["videoId"] for i in res.get("items", [])]
    if not ids:
        return []
    vids = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids)).execute()["items"]
    ahora = datetime.now(timezone.utc)
    out = []
    for v in vids:
        pub = datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
        edad = max(1.0, (ahora - pub).total_seconds() / 86400)
        vistas = int(v["statistics"].get("viewCount", 0))
        out.append({
            "titulo": v["snippet"]["title"], "canal": v["snippet"]["channelTitle"], "id": v["id"],
            "vistas": vistas, "vistas_dia": round(vistas / edad), "duracion": v["contentDetails"]["duration"],
            "likes": int(v["statistics"].get("likeCount", 0)), "comentarios": int(v["statistics"].get("commentCount", 0)),
            "publicado": pub.date().isoformat(),
        })
    return sorted(out, key=lambda x: -x["vistas_dia"])
