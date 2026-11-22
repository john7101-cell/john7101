# Quality playbook

These are per-model prompting and graph rules that video-director applies. The sources are the collection's SKILL.md files, the copied workflows, and a static node-by-node comparison of the LTX and Klein graphs made during the source analysis (not included). Anything marked *unverified* has not been measured on a GPU.

## FLUX.2 Klein (stills: `still.klein`, `still.flux2_4b`, `still.flux2_9b`)
- **The distilled graph is the default.** It runs 16 steps (4B/9B distilled presets differ; see flux3-klein-stills) at **CFG 1**. The negative path is `ConditioningZeroOut`, and at CFG 1 the negative is never evaluated. **Do not write negative prompts. They are a no-op.** Put every constraint in the positive prompt as a statement about the end state: write "clean empty sky", not "no birds".
- **Write long, end-state prompts.** Kara's caption rules give the order: medium first ("Painterly 35mm film still."), then the shot size, then the subject with the full bible descriptor, then frame-relative placement ("at frame left", "lower third"), then lighting and palette, then the lens or depth of field. Aim for 100–350 words for hero shots. Put any visible text in double quotes (`sign reading "CHORUS"`).
- **Repeat the full cast descriptor in every shot.** Never write "same woman as before", because the model has no memory between shots. Identity drift goes to `fix.edit` with the reference image. It does not get a re-roll.
- **Base model (`still.klein_base`) is max tier only.** It runs 50 steps at CFG 3.5 and is about 3× slower. Kara's graphs use base. Do not copy 50/3.5 into a distilled graph.
- **Layout and bbox nodes do nothing.** In Kara's graph, `CreateBoundingBoxes` → `Flux3LayoutPrompt` feeds only `PreviewAny`, so it does not steer the sampler. Control composition through the prompt or an edit pass.
- Sizes are multiples of 64 at 16:9 (1024×576, 1280×704 is allowed when the still seeds LTX). Generate stills at the video's final aspect so the i2v start frame matches.

## LTX-2.x video (`video.i2v`, `video.i2v_se`, `video.t2v`, `vfx.swap_ltx`, `vfx.restyle`)
- **Frame counts must be 8n+1:** `frames = 8·ceil(dur·fps/8)+1`, so 5 s at 24 fps is 121 and 4 s is 97. `direct.py validate` rejects anything else.
- **Width and height must be multiples of 32** at the *base* (stage-1) size. The graph upsamples the latent ×2, so a 640×352 base gives a 1280×704 final (352 = 11·32). draft is 512×288, standard is 640×352, max is 768×448.
- **Two-stage graph:** stage 1 is a distilled low-res pass and stage 2 is a latent-upsample refine. Both run CFG 1 with euler_ancestral. Stage-1 sigmas are `1.0 … 0.909375, 0.725, 0.421875, 0`. Stage-2 sigmas are `0.85, 0.7250, 0.4219, 0`, which is what the Comfy-Org template and every open graph checked use. The Lightricks advanced example starts stage 2 at **0.909375**. Treat that as an opt-in A/B (it gives more detail or more drift). It is not a fix.
- **Guide (image-conditioning) strength:**
  - The brief's value of 0.7 is the stage-1 default (node 357) in leafreel and openfield.
  - **Comfyrizz raises stage 1 to 1.0 for static, locked-off or tripod shots** because it recorded first-frame drift at 0.7. direct.py does the same: `strength1 = 1.0` when the camera matches static, locked or tripod, and 0.7 otherwise.
  - **Stage 2 (node 349) always uses 1.0**, because it re-injects the image.
  - Never drop static shots back to 0.7. The cost of 1.0 is less motion, which is what a static shot wants anyway.
- **Video prompts describe motion only.** Give the camera move first, then what moves and how. The still already fixes the look. One action per shot.
- **Chaining:** `chain_from` starts shot N+1 on shot N's last frame. On the `video.i2v_se` (first and last frame) route, the approved still becomes the end target. Chain within a scene, and cut between scenes.
- VAE decode tiling is 512/64/64/16 by default. openfield's 768/64/4096/32 gives fewer seams but uses more VRAM, so it is max tier only.
- **License:** the LTX-2 weights are under the **Lightricks LTX-2 Community License**. That is **not an OSI-approved open-source license**: it has use and revenue conditions. Read `licenses/LTX-2-weights-LICENSE.reference.txt` before any commercial use. The graphs themselves are MIT/Apache.

## Wan-family graphs (`control.*`, `camera.fun`, `video.s2v`, `video.talk_music`)
- Use **16 fps** and **4n+1** frames (motionfield's catalog: `CAM_FRAMES = 16·duration + 1`). The camera rig renders at 832×480 for 16:9, 480×832 for 9:16 and 624×624 for 1:1. These come from the `workflows/*.defaults.json` sidecars, and `direct.py` applies them instead of the LTX rule.
- Every `{{PLACEHOLDER}}` has to be filled. `direct.py` refuses to submit if one is missing.
- Pose and canny control carry no identity, so feed the approved still as well. Use named camera moves (`MOVES`) from the catalog. Never invent names.
- The Wan 2.1, 2.2 and VACE weights are Apache-2.0 (unverified per file).

## Measurements (`qa.shot`)
Run shot-qc on every render. A freeze (at least 0.5 s, unless the shot is static) or black frames fail the attempt. When the VLM says a camera is "locked off" and shot-qc measured motion, trust the measurement (the agentY rule).

## Edits and fixes
- **Qwen-Image-Edit (`fix.edit`, `fix.tryon`, `fix.angle`, `fix.relight`, `fix.outpaint`):** write one instruction per pass, phrased as an imperative about the change only ("Replace the jacket with a red raincoat; keep face, pose, lighting"). Chain passes rather than stacking instructions. `fix.edit_fast` (Lightning LoRA, few steps) is for draft tier only.
- **still-qa judge:** a still passes when the mean is at least `caps.pass_mean` and the minimum is at least `caps.pass_min`. Issue tags drive the fix: identity goes to edit with the reference, composition goes to a re-prompt, and artifacts go to seed+1.

## Audio
- **ACE-Step (`audio.music`):** comma tags for genre, tempo in bpm, mood and instruments. Use `[instrumental]` for no vocals. Set the duration to the cut length plus 2 s.
- **Stable Audio Open (`audio.sfx`):** one sound per prompt, close-mic phrasing, 5 s or less. Its weights are under the Stability AI Community License, which is not OSI. Check it before commercial use.
- **Chatterbox (`audio.voice`, voice change):** short sentences, about 15 words per narration line, and one line per shot. Keep `exaggeration` low for narration. The weights are MIT. Voice cloning needs consent from the speaker.
- **Lip-sync (`video.lipsync*`):** the input must be a frontal or ¾ face that is at least 25% of the frame height, with clean vocals (stems if possible). SyncNet scoring is *not* bundled, because the Oxford VGG weights are research-only.

## Post
- **SeedVR2 upscale (`post.upscale`):** max tier only, run once on the final cut or per hero shot. It never fixes composition.
- **FILM interpolation (`post.interp`):** use it to reach 48 or 60 fps or for slow-motion. Do not interpolate across cuts.
- **Reframe (`post.reframe`):** subject-aware crop for 9:16 and 1:1 deliverables. Plan 9:16 safe areas at the still stage.

## Budget and caps (enforced by direct.py)
| rule | value |
|---|---|
| retries per still | `caps.still_retries` (draft 1, standard 2, max 3) |
| video retries per shot | `caps.video_retries` (0 / 1 / 2) |
| continuity regens per join | `caps.continuity_regens` (0 / 1 / 2) |
| hard render ceiling | `caps.max_renders`. When it is hit, the run logs `cap_hit` and stops rendering. It never silently continues |
| GPU-minute ceiling | `target.budget.max_gpu_minutes`. Preflight downgrades the tier if the estimate exceeds it |
| spend gate | `gates.spend: human` stops before the first paid render (Google Colab compute units, Comfy Cloud credits) |
| still before video | no video job runs without `still.approved` |

The rates in direct.py (seconds per render) are **unverified placeholders**. Replace them with measured values in `cost.rates_s_per_render`.

## Open weights only
Every route uses weights you can download and run locally. No closed or API-only models are allowed. The weights are open, but the licenses vary. Set `brief.commercial_use` and check:
- LTX-2: Lightricks Community License (not OSI)
- Stable Audio Open: Stability Community License
- FLUX.2 Klein: check the variant license on its model card (*unverified* per variant)
- insightface buffalo_l (character-swap-h3): non-commercial
- MiniMax H3 weights: license *unverified*
- SeedVR2, FILM, Wan 2.1, Qwen, ACE-Step and Chatterbox: see each skill's `requirements.md`

## Do not copy
- Kara's 50-step, CFG 3.5 settings into distilled Klein.
- leafreel's people-word negative lists, which are a no-op at CFG 1.
- nightshift's 4-step LTX preset, except in draft previs.
- 0.7 stage-1 strength on static shots.
