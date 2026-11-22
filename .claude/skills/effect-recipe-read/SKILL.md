---
name: effect-recipe-read
description: Reverse-engineer a video effect into a reusable JSON recipe: a local Qwen3-VL 8B reads START/MIDDLE/END frames of a reference clip and writes the end-frame and motion prompts, then an open LTX-2 + Qwen edit graph applies the recipe to the user's photo (forkfield). Use for "make this effect with my photo" from a reference clip.
---

# effect-recipe-read

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX-2 license, which is **not** an OSI-approved open-source license.

This is the **forkfield** design (MIT): read an effect off three frames, write it down as a recipe, and apply the recipe to a new photo.

## 1. Read
1. Grab three frames and tile them side by side:
   `ffmpeg -i ref.mp4 -vf "select='eq(n,0)+eq(n,N/2)+eq(n,N-1)',scale=-1:512,tile=3x1" -frames:v 1 -vsync 0 strip.png`
   Set N to the frame count from ffprobe.
2. Upload the strip and set `1.image`. Run `forkfield_read_effect.api.json`. The graph is LoadImage → CLIPLoader (`qwen3vl_8b_int8_convrot`) → `TextGenerate` → `PreviewAny`.
3. Collect the text from the `texts` field of the JSON that `comfy_client.py run` prints.
4. Save it as `recipe.json`: `{"source": "ref.mp4", "endframe_prompt": …, "motion_prompt": …, "seed": …}`. If the model wrapped the text in prose, edit it by hand.

## 2. Apply
`forkfield_apply_open_ltx.api.json` (local graph: Qwen-Image-Edit makes the end frame, then LTX-2 runs first-to-last frame) takes these placeholders: `{{PHOTO}}` (node 1), `{{ENDFRAME_PROMPT}}` (17), `{{MOTION_PROMPT}}` (45) and `{{SEED}}` (22, 54). Every one must be set.

Not bundled: `forkfield_flf2v.api.json`. It uses `LtxApi25ImageToVideo` and `Flux3ImageNode`, which are **hosted API nodes**, and this collection is open weights only.

## Rules
- The recipe is a description and does not copy anyone's footage. Only fork clips the user has the rights to use as a reference.
- Judge the generated end frame with `still-qa` before you spend on video (stills first).
- The Qwen3-VL weights are Apache-2.0 (unverified for this int8 build). LTX uses the Lightricks license (not OSI).
