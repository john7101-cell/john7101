# Requirements: frame-interpolation

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
FILM ~0.1 GB of weights (per rosesfield README); low VRAM

## Node types

### workflows/film_frame_interpolation.api.json
| class_type | node pack |
|---|---|
| ComfyMathExpression | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfySwitchNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FrameInterpolate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FrameInterpolationModelLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetImageSize | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveBoolean | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/film_frame_interpolation.api.json
| file | license |
|---|---|
| film_net_fp16.safetensors | FILM frame interpolation (Google): Apache-2.0 (unverified for this file) |
