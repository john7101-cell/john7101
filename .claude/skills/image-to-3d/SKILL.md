---
name: image-to-3d
description: Turn a still (or 4 views) into a GLB mesh with open-weights TRELLIS.2 or Pixal3D in ComfyUI. Use for previs props, set pieces and turnaround references.
---

# image-to-3d

Run every graph with the bundled client: `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`. Upload input files first with `python scripts/comfy_client.py upload <file>`. Before the first run on a server, check it with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses for this skill are in `references/requirements.md`. Use open-weights models only, and never swap in a hosted or closed model.

| Need | Workflow | Set |
|---|---|---|
| One image to a mesh (TRELLIS.2) | `trellis2_image_to_3d.api.json` | `1.image` |
| One image to a mesh (Pixal3D) | `pixal3d_image_to_3d.api.json` | `1.image` |
| Four views to a mesh | `pixal3d_multiview_to_3d.api.json` | `40`, `43`, `46`, `49` `.image` (front, right, back, left) |

## Notes
- The input should show one object on a plain background. The graph removes the background with BiRefNet.
- The output is a `.glb` (SaveGLB). Use it for blocking in a 3D tool, or render turnarounds as references for `image-edit`.
- The licenses of the DINOv3, MoGe and Pixal3D weights are unverified. Check them before commercial use.
