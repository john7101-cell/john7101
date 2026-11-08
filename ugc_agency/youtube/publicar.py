"""Subida a YouTube: video, miniatura y subtítulos.

Por seguridad la subida es siempre explícita (`confirmar=True`) y, por defecto, el video queda
PRIVADO o programado: el dueño del canal lo revisa antes de que sea público.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .seo import Metadatos


def cuerpo(meta: Metadatos, privacidad: str = "private", publicar_en: datetime | None = None) -> dict:
    status = {
        "privacyStatus": "private" if publicar_en else privacidad,
        "selfDeclaredMadeForKids": meta.para_ninos,
        "containsSyntheticMedia": meta.contenido_sintetico,
        "embeddable": True,
    }
    if publicar_en:
        status["publishAt"] = publicar_en.isoformat()
    return {
        "snippet": {
            "title": meta.titulo, "description": meta.descripcion_final(), "tags": meta.etiquetas,
            "categoryId": meta.categoria, "defaultLanguage": meta.idioma, "defaultAudioLanguage": meta.idioma,
        },
        "status": status,
    }


def subir(video: Path, meta: Metadatos, miniatura: Path | None = None, subtitulos: Path | None = None,
          privacidad: str = "private", publicar_en: datetime | None = None, confirmar: bool = False,
          log=print) -> dict:
    problemas = [p for p in meta.validar() if not p.startswith("Aviso")]
    if problemas:
        raise ValueError("Metadatos inválidos:\n- " + "\n- ".join(problemas))
    body = cuerpo(meta, privacidad, publicar_en)
    if not confirmar:
        log("SIMULACIÓN (no se subió nada). Usa confirmar=True / --confirmar para subir.")
        return {"simulacion": True, "body": body, "video": str(video), "miniatura": str(miniatura) if miniatura else None}

    from googleapiclient.http import MediaFileUpload

    from .auth import youtube

    yt = youtube()
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(str(video), chunksize=8 * 1024 * 1024, resumable=True))
    resp = None
    while resp is None:
        estado, resp = req.next_chunk()
        if estado:
            log(f"  subiendo… {int(estado.progress() * 100)}%")
    vid = resp["id"]
    log(f"  ✔ video subido: https://youtu.be/{vid} ({body['status']['privacyStatus']})")
    if miniatura:
        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(miniatura), mimetype="image/jpeg")).execute()
        log("  ✔ miniatura aplicada")
    if subtitulos:
        yt.captions().insert(part="snippet", body={"snippet": {"videoId": vid, "language": meta.idioma, "name": "Español"}},
                             media_body=MediaFileUpload(str(subtitulos), mimetype="application/octet-stream")).execute()
        log("  ✔ subtítulos cargados")
    return {"id": vid, "url": f"https://youtu.be/{vid}", "privacidad": body["status"]["privacyStatus"]}


def hacer_publico(video_id: str, confirmar: bool = False) -> None:
    if not confirmar:
        raise ValueError("Para hacer público un video hace falta confirmar=True.")
    from .auth import youtube

    yt = youtube()
    actual = yt.videos().list(part="status", id=video_id).execute()["items"][0]["status"]
    actual["privacyStatus"] = "public"
    actual.pop("publishAt", None)
    yt.videos().update(part="status", body={"id": video_id, "status": actual}).execute()
