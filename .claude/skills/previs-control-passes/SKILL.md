---
name: previs-control-passes
description: Block a shot in 3D and export deterministic control passes (OpenPose skeleton MP4, depth MP4, subject alpha, 4x4 camera matrices, 24 fps previs) from ComfyUI Motion Previs Studio, then feed them to control-to-video or camera-control. Also applies its verified template-binding format to ComfyUI API graphs. Use when blocking and camera must be designed before generation.
---

# previs-control-passes

**navarisun1982/comfyui-motion-previs-studio** (MIT) is a local WebGL/Electron app. The user installs and runs it from its README. This skill does not install or run it. Its architecture and template docs are copied in `references/` (MIT).

## Flow
1. Block the shot in the studio: actors, motion presets, camera, lens, aspect.
2. Use **Previs Render & Export** to export a 24 fps composite MP4, a clean beauty pass, an **OpenPose 18-joint** MP4, a **normalized depth** MP4, a subject alpha mask, and a bundle with the `4×4` camera matrices and the compiled prompt.
3. Route the passes:
   - OpenPose or depth go to `control-to-video` (Wan VACE pose, LTX-2 depth or pose).
   - Camera matrices go to `camera-control` (ATI or Fun Camera) or are kept for continuity.
   - The alpha mask goes to `background-matte` or `video-inpaint-remove`.
4. Record the pass files on the shot in the video-director manifest (`shot.extra[].params`).

## Template bindings (`scripts/binding_apply.py`)
The studio pairs each API graph with a `<id>.binding.json` that maps fields (prompt, seed, frames and so on) to `{node, input}` and **verifies** them before queueing. The studio's own binding files live in its repo under `workflows/templates/`. `scripts/binding_apply.py` (stdlib, original) implements the same contract for any graph:
`python scripts/binding_apply.py check <graph.api.json> <binding.json>` checks that each node exists, the class_type matches and the input exists. Then `python scripts/binding_apply.py apply <graph> <binding> prompt="..." seed=5 --out filled.json`. Fields marked `fixed` are always forced to their value. Fields with a studio-specific `patch` (for example `timeline`) are refused, so edit those inputs by hand.

## Studio LTX-2.5 template (not bundled)
The studio also ships an LTX-2.5 22B INT8 template that needs the **Stubelius Ultimate LTX 2.5** node pack ([stuubszzz/Stubelius-Ultimate-LTX2.5](https://github.com/stuubszzz/Stubelius-Ultimate-LTX2.5)). That pack is **GPL-3.0**, so the template and its binding are not included in this MIT/Apache/BSD pack. To use it anyway, install the pack and the template from their own repos under their own licences. Otherwise, the recommended open path is to send the exported passes to `control-to-video` or `camera-control`.
- LTX-2.5 weights are under the Lightricks LTX-2 Community License (not OSI-approved).
- The studio's MiniMax H3 and Seedance paths are not used here. Seedance is a hosted API, and the H3 weight license is unverified.
