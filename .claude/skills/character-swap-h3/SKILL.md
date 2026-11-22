---
name: character-swap-h3
description: Swap a person, face or object in an existing clip for a reference image using open-weights MiniMax H3 (local weights) with D3voz's one-click swap nodes, or an open LTX-2.3 motion-swap fallback. Use for recasting, outfit/product swaps and face fixes.
---

# character-swap-h3

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are listed in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX license, which is **not** an OSI-approved open-source license.

**About H3:** these graphs load MiniMax H3 weights *locally*, from Comfy-Org's Hugging Face repos. They do not call a hosted MiniMax API, so this is an open-weights path. The H3 weight license is **unverified**, so check it before commercial use. If H3 weights aren't available, or their license doesn't fit, use the LTX fallback.

## Install (once)
- Copy `assets/comfyui-h3-oneclick-swap/` into `ComfyUI/custom_nodes/`. It is MIT, from D3voz.
- The other packs (KJNodes, VideoHelperSuite, H3-FaceRefine, MiniMaxH3-Context-Loop, Fantastic PromptBuilder) are listed in `references/requirements.md`.
- H3-FaceRefine needs **insightface**. Its default `buffalo_l` face models are commonly distributed for non-commercial research use (unverified), so check them before commercial work.

| Need | Workflow | Set |
|---|---|---|
| Swap a person (whole body) | `h3_swap_simple.api.json` | `5.video` clip, `2.image` reference, `11.seed`, `11.resolution` (`736p`) |
| Swap a face only | `h3_swap_face.api.json` | `1.video`, `2.image`, `24.noise_seed` |
| Swap an object, outfit or product | `h3_swap_object.api.json` | `5.video`, `2.image`, `18.text` (what to replace), `7.seed` |
| **Open fallback** (LTX-2.3 masked motion swap) | `ltx23_motion_swap_open_fallback.api.json` | `1.file`, `2.image`, `3.text` (who to replace), `5.noise_seed` |

## Rules
- The reference should match the source framing: same body coverage, similar light.
- Run `continuity-check` with the reference as `--ref` on the first, middle and last frames.
- Only swap a real person's face with their consent. Never use it to impersonate someone.
