---
name: ltx-iclora-utils
description: LTX-2.3/2.5 IC-LoRA and LoRA utility graphs: motion transfer from a reference clip, motion-guided i2v, LTX-2.5 effects, plus official templates for subtitle and watermark removal, archival restoration, style transitions, generic IC-LoRA and ID-LoRA (identity). Use for clip-in, clip-out repair and effects on LTX.
---

# ltx-iclora-utils

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX-2 license, which is **not** an OSI-approved open-source license.

**What is not here (to avoid duplicates):**
- depth-restyle IC-LoRA is in `restyle`
- LTX-2.3 object removal is in `video-inpaint-remove`
- LTX-2.3 reframe and outpaint is in `reframe-aspect`
- the LipDub IC-LoRA is in `lip-sync`
- the motion swap is in `character-swap-h3`

The Comfy-Org `template_ltx2_3_lora_video_outpainting` and `…obscura…remove_object` templates were skipped because they duplicate `reframe-aspect` and `video-inpaint-remove`.

| graph | format | use |
|---|---|---|
| `ltx23_ic_lora_motion.api.json` | API (rosesfield) | transfer motion from `199.file` (clip) onto `200.image` (photo) |
| `ltx23_ic_lora_motion_guide.api.json` | API (rosesfield) | the same, with motion-guide conditioning (see its README) |
| `ltx25_effects.api.json` | API (rosesfield) | LTX-2.5 effect from photo `395.image`. Two-stage graph with base 640×352 and 241 frames (8n+1) |
| `ui/ltx23_remove_subtitles.ui.json`, `ui/ltx23_remove_watermark.ui.json` | UI (Comfy-Org) | clean burned-in text. Only use this on footage you have the rights to |
| `ui/ltx23_restore_archival.ui.json` | UI | restore old or damaged footage |
| `ui/ltx23_style_transition.ui.json` | UI | style morph across a clip |
| `ui/ltx23_ic_lora.ui.json` | UI | generic IC-LoRA (load any LTX-2.3 IC-LoRA) |
| `ui/ltx23_id_lora.ui.json` | UI | ID-LoRA identity conditioning |

`workflows/ui/*.ui.json` are official Comfy-Org templates (MIT) in **UI format**, and most contain subgraphs. `comfy_client.py` refuses UI format. To use one: open it in ComfyUI, install the missing nodes and models that ComfyUI lists (they are also in `requirements.md`), then use **Workflow → Export (API)** to save it as `workflows/<name>.api.json`. Run `preflight.py` on the export and read off the node ids for `--set`. Node ids change when you export, so do not reuse ids from another graph.

## Rules
- Frames must be 8n+1, and base sizes multiples of 32. Stage 1 strength is 1.0 for static shots and 0.7 otherwise. Stage 2 is 1.0 (see `video-director/references/quality-playbook.md`).
- The negative prompts that ship in these graphs do nothing at CFG 1. Leave them alone.
- All LTX weights and IC-LoRAs are under the Lightricks LTX-2 license (not OSI).
