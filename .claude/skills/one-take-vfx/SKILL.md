---
name: one-take-vfx
description: Add a stylised VFX effect to an existing clip in one pass (set-on-fire, disintegrate, time-freeze, hologram, portal, rain-stop, levitate, aurora trails, liquid chrome, neon wireframe, particle bloom, slow-mo debris) with open-weights LTX IC-LoRA union control and Kainotomic's preset node. Use for hero moments and title beats.
---

# one-take-vfx

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are listed in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX license, which is **not** an OSI-approved open-source license.

## Install (once)
Copy `assets/onetake_vfx/` into `ComfyUI/custom_nodes/onetake_vfx/`. It is MIT, from Kainotomic/one-take-vfx, and provides OneTakeGuideMotion and OneTakeVFXPreset.

| Need | Workflow | Set |
|---|---|---|
| A preset effect | `one_take_vfx_preset_node.api.json` | `load_video.video`, `preset.preset` (a name from `references/presets/`), `noise.noise_seed` |
| A custom effect prompt | `one_take_vfx.api.json` | `load_video.video`, `positive.text`, `empty_latent.length` (8n+1), `noise.noise_seed` |

## Rules
- Read the preset JSON before you change the prompt. It holds the tested prompt and strengths.
- Apply the effect to one hero shot, not every shot, and check continuity on the join into the next shot.
- The default working size is 768×448. Upscale afterwards with `video-upscale`.
