"""Ayudantes de ffmpeg/ffprobe y descarga de videos por enlace."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


class MediaError(RuntimeError):
    pass


def require_ffmpeg() -> None:
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise MediaError(f"No se encontró {tool}. Instálalo (p.ej. `apt-get install ffmpeg`).")


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise MediaError(f"Falló: {' '.join(cmd[:6])}...\n{proc.stderr[-2000:]}")
    return proc


@dataclass
class MediaInfo:
    duration: float
    width: int
    height: int
    fps: float
    has_audio: bool

    @property
    def is_vertical(self) -> bool:
        return self.height > self.width


def probe(path: Path) -> MediaInfo:
    out = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)])
    data = json.loads(out.stdout)
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    if video is None:
        raise MediaError("El archivo no tiene pista de video.")
    num, _, den = video.get("avg_frame_rate", "30/1").partition("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 30.0
    width, height = int(video["width"]), int(video["height"])
    rotation = abs(int(video.get("tags", {}).get("rotate", 0) or 0))
    for sd in video.get("side_data_list", []):
        rotation = abs(int(sd.get("rotation", rotation) or rotation))
    if rotation in (90, 270):
        width, height = height, width
    return MediaInfo(
        duration=float(data["format"]["duration"]),
        width=width,
        height=height,
        fps=fps or 30.0,
        has_audio=any(s["codec_type"] == "audio" for s in data["streams"]),
    )


# ---------------------------------------------------------------------------
# Descarga por enlace (Google Drive, Dropbox o enlace directo)
# ---------------------------------------------------------------------------


def direct_download_url(url: str) -> str:
    """Convierte enlaces para compartir de Drive/Dropbox en enlaces de descarga directa."""
    m = re.search(r"drive\.google\.com/(?:file/d/|open\?id=|uc\?.*id=)([\w-]+)", url)
    if m:
        return f"https://drive.usercontent.google.com/download?id={m.group(1)}&export=download&confirm=t"
    if "dropbox.com" in url:
        parts = urllib.parse.urlsplit(url)
        query = dict(urllib.parse.parse_qsl(parts.query))
        query["dl"] = "1"
        return urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(query)))
    return url


def download(url: str, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(direct_download_url(url), headers={"User-Agent": "ugc-agency-editor"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        ctype = resp.headers.get("Content-Type", "")
        if "text/html" in ctype:
            raise MediaError(
                "El enlace devolvió una página web, no un video. Comparte el archivo como "
                "'Cualquier persona con el enlace' o usa un enlace de descarga directa."
            )
        name = "input"
        disp = resp.headers.get("Content-Disposition", "")
        m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)', disp)
        if m:
            name = Path(urllib.parse.unquote(m.group(1))).name
        if not Path(name).suffix:
            name += ".mp4"
        path = dest_dir / name
        with path.open("wb") as f:
            shutil.copyfileobj(resp, f, length=1 << 20)
    return path
