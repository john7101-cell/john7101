---
name: background-matte
description: Remove or replace backgrounds and pull mattes with open-weights BiRefNet in ComfyUI (stills to transparent or solid colour, video background removal), plus PlateLock plate compositing (difference matte, temporal stabilise, fidelity report) to put a generated element back onto a real plate. Use for product shots, compositing and green-screen style work.
---

# background-matte

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are listed in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX license, which is **not** an OSI-approved open-source license.

| Need | Workflow | Set |
|---|---|---|
| Still to transparent PNG | `birefnet_image_transparent.api.json` | `1.image` |
| Still on a solid colour | `birefnet_image_solid.api.json` | `1.image` (the colour is a node input; read the graph) |
| Video background removal | `birefnet_video_background.api.json` | `1.file` |
| Composite a generated element onto the real plate | `platelock_comp.api.json` | `1.file` plate, `3.file` generated clip, `8.seed` |

## Install PlateLock (once)
Copy `assets/comfyui-platelock/` into `ComfyUI/custom_nodes/`. It is MIT, from TusharTechs/platelock. Use its fidelity report node to check that the untouched plate pixels really are unchanged.

## Rules
- Hair and motion blur are the weak spots. Check them at 100% on 3 frames.
- For product spots, matte the product still first, then build the scene around it with `image-edit`.
