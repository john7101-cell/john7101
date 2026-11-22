# Requirements: subtitles-captions

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
Whisper large-v3-turbo ~1.6 GB VRAM (node tooltip); burn-in is CPU (ffmpeg)

## Node types

### workflows/whisper_asr_segments.api.json
| class_type | node pack |
|---|---|
| CJWhisperASR | bundled: assets/cj_whisper_asr (xk44/adrift, MIT) |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewAny | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/whisper_asr_segments.api.json
| file | license |
|---|---|
| (none named) | |
