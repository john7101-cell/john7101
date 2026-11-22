# Requirements: voiceover

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
~6 GB (estimate, unverified)

## Node types

### workflows/voice_chatterbox_multilingual.api.json
| class_type | node pack |
|---|---|
| FL_ChatterboxMultilingualTTS | https://github.com/filliptm/ComfyUI_Fill-ChatterBox |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveAudioMP3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TrimAudioDuration | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/voice_change_chatterbox.api.json
| class_type | node pack |
|---|---|
| FL_ChatterboxVC | https://github.com/filliptm/ComfyUI_Fill-ChatterBox |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveAudioMP3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TrimAudioDuration | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/voice_chatterbox_multilingual.api.json
| file | license |
|---|---|
| (none named) | |

### workflows/voice_change_chatterbox.api.json
| file | license |
|---|---|
| (none named) | |
