---
name: lip-sync
description: Make a character speak or sing to an audio track with open weights in ComfyUI - talking shot from a photo + audio (LTX-2.3), re-dub an existing video (LTX-2.3 IC-LoRA lipdub), or low-VRAM singing/talking (Wan 2.1 + InfiniteTalk). Use for dialogue, presenters and music-video performance.
---

# lip-sync

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are listed in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX license, which is **not** an OSI-approved open-source license.

| Need | Workflow | Set |
|---|---|---|
| Photo + speech to a talking shot | `ltx23_lipsync_photo.api.json` | `269.image`, `276.audio`, prompt in `900.string_a`, `302.width/height/length` |
| Re-dub an existing clip to new audio | `ltx23_ic_lora_lipdub_video.api.json` | `7.file` ref video, `11.text`, `14.*` size and length |
| Singing, or a lower-VRAM path (Wan 2.1 + InfiniteTalk, GGUF + block swap) | `wan21_infinitetalk_single.api.json` | `1.image`, `6.audio`, `13.positive_prompt`, `15.seed` |

## Rules
- Render the audio first (`voiceover` or `music-sfx`), then set the clip length from it: frames = 8n+1 at or above audio_seconds × fps for LTX. Wan runs at 25 fps.
- Use a frontal or 3/4 face, mouth visible, no hands near the face.
- **Lip-sync scoring:** OneShotMV's `fv/syncnet` code is MIT/Apache, but the SyncNet weights are research-use only (Oxford VGG, CC-BY research). They are **not bundled**. Judge sync with `still-qa` on frames plus a listen-through.
- Only clone or re-dub a real person's voice or face with their consent.
