# Requirements: previs-control-passes

## Software
- [navarisun1982/comfyui-motion-previs-studio](https://github.com/navarisun1982/comfyui-motion-previs-studio) (MIT): a local WebGL/Electron app, installed by the user from its README.
- `scripts/binding_apply.py`: Python 3 standard library only.

## VRAM
The previs app runs in WebGL and has no GPU VRAM figure. The downstream render VRAM is set by `control-to-video` or `camera-control`.

## Not bundled
- The studio's LTX-2.5 template needs the Stubelius Ultimate LTX 2.5 node pack (stuubszzz/Stubelius-Ultimate-LTX2.5, **GPL-3.0**, checked with the GitHub API on 2026-10-30). It is excluded from this repo.
- Its weights (LTX-2.5 22B distilled INT8, Gemma encoder, VAEs, spatial upscaler) are under the Lightricks LTX-2 Community License (not OSI-approved); the Gemma licence is unverified.
