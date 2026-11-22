---
name: video-upscale
description: Upscale and restore generated video or stills with open-weights SeedVR2 in ComfyUI (one-step diffusion restoration). Use after shots are approved and before film-assembly, or to sharpen a keyframe.
---

# video-upscale

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are listed in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX license, which is **not** an OSI-approved open-source license.

| Need | Workflow | Set |
|---|---|---|
| Upscale a video clip | `seedvr2_video_upscale.api.json` | `1.file`, `109.seed`. Read the target size from the SeedVR2 preprocess node, and see `references/rosesfield-upscale-video-README.md` |
| Upscale a still | `seedvr2_image_upscale.api.json` | `1.image`, `54.seed` |

## Rules
- Only upscale the **approved** take, as the last step on each shot. Never upscale before `still-qa` or `continuity-check`.
- Upscale every shot in a sequence the same way, so the grain and sharpness match across cuts.
- The graph uses tiled VAE encode/decode, so reduce the tile size if you run out of memory. The SeedVR2 weight license is **unverified**.
