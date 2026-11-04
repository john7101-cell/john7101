"""Generación opcional de voz en off con ElevenLabs (API REST de text-to-speech)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from ..models import ContentPiece

API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"


class VoiceError(RuntimeError):
    pass


class ElevenLabsVoice:
    def __init__(self, api_key: str | None = None, model_id: str | None = None) -> None:
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY", "")
        self.model_id = model_id or os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2")
        if not self.api_key:
            raise VoiceError("Falta ELEVENLABS_API_KEY")

    def synthesize(self, piece: ContentPiece, voice_id: str, out_path: Path) -> Path:
        v = piece.production.voice
        body = {
            "text": piece.script.full_voiceover,
            "model_id": self.model_id,
            "voice_settings": {
                "stability": v.stability,
                "similarity_boost": 0.75,
                "style": v.style,
                "use_speaker_boost": True,
            },
        }
        req = urllib.request.Request(
            API_URL.format(voice_id=voice_id),
            data=json.dumps(body).encode(),
            headers={"xi-api-key": self.api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                audio = resp.read()
        except urllib.error.HTTPError as e:
            raise VoiceError(f"ElevenLabs respondió {e.code}: {e.read()[:300]!r}") from e
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(audio)
        return out_path
