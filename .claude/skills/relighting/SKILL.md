---
name: relighting
description: Relight a still (change light direction, colour, time of day, or match a plate) with open-weights models: Qwen-Image-Edit 2509 relight, FLUX.2 Klein + normal-map lights (motionfield), or the Comfy-Org portrait relighting template. Stills only; animate afterwards with image-to-video. Use before video when lighting must match across shots.
---

# relighting

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX-2 license, which is **not** an OSI-approved open-source license.

**Stills only.** No open, permissive video-relighting graph was found, so relight the keyframe and then animate it with `ltx25-image-to-video`. To keep light consistent across a cut, relight both keyframes to the same description.

| graph | format | how |
|---|---|---|
| `image-edit/workflows/qwen_edit_2509_relight.api.json` (route `fix.relight`) | API (rosesfield) | instruction relight. This is the default |
| `klein_relight_normals.api.json` | API (motionfield) | Depth Anything 3 normals feed `OF_Relight` (`{{LIGHTS}}` JSON lights, `{{STRENGTH}}`), then FLUX.2 Klein re-renders with the relit reference. Physically placed lights |
| `normals_from_da3.api.json` | API (motionfield) | normals pass only |
| `ui/qwen_edit_2509_relight.ui.json` | UI (Comfy-Org) | official relight template |
| `ui/character_portrait_relighting.ui.json` | UI | portrait relight |

The motionfield graphs (MIT) use `{{PLACEHOLDER}}` strings. **Every** placeholder must be replaced with `--set` before you submit (`grep -o '{{[A-Z_]*}}' workflows/<file>` lists them). Pass numbers as JSON (`--set 9.width=832`). Their `OF_*` nodes are bundled in `assets/motionfield_nodes` (MIT; `dwpose_onnx` is Apache-2.0), and they need numpy, torch, opencv and onnxruntime on the **server**. Copy the folder to `ComfyUI/custom_nodes/`.

`workflows/ui/*.ui.json` are official Comfy-Org templates (MIT) in **UI format**, and most contain subgraphs. `comfy_client.py` refuses UI format. To use one: open it in ComfyUI, install the missing nodes and models that ComfyUI lists (they are also in `requirements.md`), then use **Workflow → Export (API)** to save it as `workflows/<name>.api.json`. Run `preflight.py` on the export and read off the node ids for `--set`. Node ids change when you export, so do not reuse ids from another graph.

## IC-Light
lllyasviel/IC-Light code is Apache-2.0, but it is a standalone Gradio app and not a ComfyUI graph. **The IC-Light weights license is unverified.** It is not bundled and not routed. Use it only after you have checked the model card.

## Rules
- Prompt the relight as an end state ("warm low sunset key from frame left, cool blue fill"). Keep identity, pose and composition unchanged.
- Run `still-qa` after relighting. Relight passes can shift faces, so fall back to `fix.edit` with the reference if they do.
- Depth Anything 3 checkpoints may be CC-BY-NC. Check them per file in `requirements.md`.
