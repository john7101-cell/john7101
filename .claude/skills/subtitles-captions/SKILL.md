---
name: subtitles-captions
description: Make captions and subtitles - SRT/ASS from the shot plan's narration timing or from Whisper ASR (open weights, local ComfyUI node), then burn them in or ship a sidecar with ffmpeg. Use for every film with speech or lyrics, and for accessibility deliveries.
---

# subtitles-captions

Use one of two sources for the timing:
1. **From the plan (preferred, no model).** Narration lines and shot start times are already in the production manifest. Run `python scripts/make_srt.py --manifest manifest.json --out captions.srt`.
2. **From audio (ASR).** Install `assets/cj_whisper_asr/` into `ComfyUI/custom_nodes/` (MIT, from xk44/adrift) and put a Hugging Face-format Whisper model under `models/stt/whisper/` (for example large-v3-turbo; the node never downloads one). Upload the audio, then run `python scripts/comfy_client.py run workflows/whisper_asr_segments.api.json --set 1.audio=<name>`. The `texts` result is the segments JSON. Then run `python scripts/make_srt.py --segments segments.json --out captions.srt`.

Burn the captions in, or keep them as a sidecar:
- Burn in: `python scripts/make_srt.py ... --burn film.mp4 --burned film_captioned.mp4`. This prints the ffmpeg command; add `--run` to execute it.
- Styled ASS captions and lyric cues: `scripts/captions.py` (Apache-2.0, from hodgemann/mondo-music-video) has `to_srt`, `to_ass` and `cues`. Import it from Python.

## Rules
- Keep each caption to at most 2 lines and about 42 characters per line, on screen for 1-7 s.
- Keep captions in the bottom 15% of the frame. For 9:16, raise them above the platform UI (about 20% up).
- Deliver the SRT sidecar even when captions are burned in.
- Whisper uses about 1.6 GB of VRAM. Its weights are MIT (unverified for your build).

## Web-safe output
Every H.264 encode uses `-pix_fmt yuv420p -profile:v high -movflags +faststart`. ffmpeg keeps 4:4:4 (High 4:4:4 Predictive) when the input is RGB, for example PNG stills or title cards, and browsers, GitHub and Discord cannot play that, and it shows no thumbnail. 4:2:0 High profile plays everywhere, and `+faststart` puts the index at the front so the file starts streaming at once. Keep these flags in any encode you add.
