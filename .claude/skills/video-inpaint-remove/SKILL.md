---
name: video-inpaint-remove
description: Remove or replace an object in a video using a mask, with open-weights Wan 2.1 VACE or LTX-2.3 in-painting in ComfyUI (tracked mask, feathering, original pixels kept outside the mask). Use to clean props, logos, rigs or artifacts from a take.
---

# video-inpaint-remove

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are listed in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX license, which is **not** an OSI-approved open-source license.

## Install the node pack (once)
Copy `assets/openframe-nodes/` into `ComfyUI/custom_nodes/openframe/`. It provides OpenFrameVideoInput, SaveVideo, GreenFill and PadForRefinement, and is MIT, from satianurag/openframe. Mask tracking uses SAM 2, so its weight license applies.

| Need | Workflow | Set |
|---|---|---|
| Light and fast (Wan VACE 1.3B) | `wan_vace_inpaint_remove.api.json` | `source.filename`, `source.mask_filename` (a white = remove mask on the first frame), `positive.text` = what should be there instead, `sample.seed` |
| Higher quality (LTX-2.3) | `ltx23_inpaint_remove.api.json` | `source.filename`, `source.mask_filename`, `positive.text`, `noise.noise_seed` |

## Rules
- Describe the clean result ("an empty marble table in sunlight"), not the removal itself.
- Keep `preserve_outside_mask` set to true so untouched pixels stay identical to the source.
- Check the result with `still-qa` on 3 frames. The method notes are in `references/openframe-workflows-README.md`.
