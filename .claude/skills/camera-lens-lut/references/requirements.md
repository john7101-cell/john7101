# Requirements: camera-lens-lut

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
CPU/GPU-light post nodes; graph VRAM depends on its loaders (unverified)

## Node types

### workflows/backlot_direct.api.json
| class_type | node pack |
|---|---|
| BacklotCameraRig | bundled: assets/comfyui-backlot (Trenchplanet/mogfield, Apache-2.0) |
| BacklotGradeLUT | bundled: assets/comfyui-backlot (Trenchplanet/mogfield, Apache-2.0) |
| BacklotLensKit | bundled: assets/comfyui-backlot (Trenchplanet/mogfield, Apache-2.0) |
| BacklotLetterbox | bundled: assets/comfyui-backlot (Trenchplanet/mogfield, Apache-2.0) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DepthAnythingV2Preprocessor | https://github.com/Fannovel16/comfyui_controlnet_aux |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/backlot_direct.api.json
| file | license |
|---|---|
| depth_anything_v2_vitl.pth | Depth Anything: license varies by size (V2-Small Apache-2.0; larger V2/V3 checkpoints CC-BY-NC-4.0) - UNVERIFIED for this file |
