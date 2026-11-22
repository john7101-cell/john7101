---
name: comfyui-preflight
description: Check, before submitting, that a ComfyUI server has every node type and model weight file a workflow needs. Reads /object_info only; submits nothing. Use before the first run of any workflow on a new or changed server (local, Google Colab, or hosted).
---

# comfyui-preflight

`python scripts/preflight.py --url $COMFY_URL workflows/*.api.json`

To check fully offline, save `/object_info` once and run `--object-info saved.json`.

The output is one JSON report per workflow: `ready`, `missing_node_types`, `missing_weight_files` (node, input, file) and `weights_found`. The exit code is 1 if anything is missing.

## What it checks
1. Every `class_type` in the graph exists in the server's `/object_info`.
2. Every input value that looks like a weight file (`.safetensors .sft .ckpt .pt .pth .bin .gguf .onnx`) is one of the combo options the server lists for that input. If it isn't, the file isn't in the right `models/` folder.

## Fixing what it finds
- **Missing node type:** look up the pack in the skill's `references/requirements.md` and install it with ComfyUI-Manager or `git clone` into `custom_nodes/`. Restart and re-run preflight.
- **Missing weight:** download the exact filename into the folder named by the loader (for example `models/diffusion_models`, `models/text_encoders`, `models/vae`, `models/loras`). Use the source link in the workflow's notes or on the model card. Check the weight license first.
- Never "fix" a graph by renaming a file input to a different model unless the user agrees.
- Some loaders take free-text paths. The script can't check those, so they show up under `weights_found` and still need checking by eye.
