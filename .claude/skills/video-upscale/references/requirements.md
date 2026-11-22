# Requirements: video-upscale

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
unverified; SeedVR2 3B/7B, tiled - 16-24 GB+ (estimate)

## Node types

### workflows/seedvr2_video_upscale.api.json
| class_type | node pack |
|---|---|
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SeedVR2Conditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SeedVR2PostProcessing | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SeedVR2Preprocess | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/seedvr2_image_upscale.api.json
| class_type | node pack |
|---|---|
| JoinImageWithAlpha | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SeedVR2Conditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SeedVR2PostProcessing | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SeedVR2Preprocess | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/seedvr2_video_upscale.api.json
| file | license |
|---|---|
| seedvr2_3b_int8_convrot.safetensors | SeedVR2 (ByteDance): Apache-2.0 per upstream repo (UNVERIFIED for these weights) |
| seedvr2_ema_vae_fp16.safetensors | SeedVR2 (ByteDance): Apache-2.0 per upstream repo (UNVERIFIED for these weights) |

### workflows/seedvr2_image_upscale.api.json
| file | license |
|---|---|
| seedvr2_3b_int8_convrot.safetensors | SeedVR2 (ByteDance): Apache-2.0 per upstream repo (UNVERIFIED for these weights) |
| seedvr2_ema_vae_fp16.safetensors | SeedVR2 (ByteDance): Apache-2.0 per upstream repo (UNVERIFIED for these weights) |
