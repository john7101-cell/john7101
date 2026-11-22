---
name: flux3-klein-stills
description: Generate stills and keyframes with open-weights FLUX Klein (distilled FLUX 3 Klein, FLUX 3 Klein base with prompt upsampling, or FLUX.2 Klein 4B/9B) through ComfyUI. Use for shot keyframes, character references and any text-to-image still.
---

# flux3-klein-stills

Run every graph with the bundled client: `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`. Upload input files first with `python scripts/comfy_client.py upload <file>`. Before the first run on a server, check it with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses for this skill are in `references/requirements.md`. Use open-weights models only, and never swap in a hosted or closed model.

## Pick a graph
| Need | Workflow | Set |
|---|---|---|
| **Default.** Distilled FLUX 3 Klein, 16 steps at CFG 1 | `flux3_klein_distilled_t2i.api.json` | `4.text`=prompt, `7.seed`, `6.width/height` |
| FLUX 3 Klein **base** with a Qwen prompt upsampler (50 steps, CFG 3.5; slower, and a negative prompt does work at this CFG) | `flux3_klein_t2i.api.json` | `18:17.value`=prompt, `18:7.seed`. The bbox/layout nodes only feed a PreviewAny, so they do **not** steer the sampler |
| The same base graph as a clean template | `flux3_klein_t2i_template.api.json` | `18:17.value`, `18:7.seed` |
| FLUX.2 Klein 9B | `flux2_klein_9b_t2i.api.json` | `6.text`, `14.noise_seed`, and width/height on nodes `5` and `13` (keep them equal) |
| Lean drafts (FLUX.2 Klein 4B) | `flux2_klein_t2i_lean.api.json` | `74.text`, `73.noise_seed`, and width/height on nodes `62` and `66` |

For detailed prompt rules, see `video-director/references/quality-playbook.md`.

## Prompting
- Write one paragraph covering subject, action, setting, lens and framing, light, and style. Take the style and cast descriptors word for word from the story bible.
- Keyframes for video: frame the start pose of the motion, and use the target video aspect (for example 1280x720 or 768x1344).
- Fix the seed for each shot and log it. To get variations, change only the seed.
- Hand every result to `still-qa` before it goes to video.
- **License warning:** FLUX.2 Klein 9B is believed to be non-commercial (unverified), and the FLUX 3 Klein license is unverified. Tell the user before any commercial use.
