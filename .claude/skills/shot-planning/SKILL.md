---
name: shot-planning
description: Staged preproduction from a sentence or script to a locked shot list - beats, shots with camera/duration/narration, per-shot prompts, cost and time estimate - with human approval gates and no auto-spend. Use before generating any film, ad or episode.
---

# shot-planning

Based on ZeroField's crew-preproduction and shot-beats skills (MIT). The full copies are in `references/`; read them for the details of each stage.

## Stages and gates
Every gate stops for approval. Nothing is spent until gate 4.
1. **Intake:** goal, audience, length, aspect, style, must-haves. Ask only what you can't infer. Then write or update the `story-bible`. **Gate 1:** bible approved.
2. **Beats:** a timed beat sheet. Each beat has a start, a duration, what happens, and an emotional turn, and the durations add up to the target length. **Gate 2:** beats approved.
3. **Shots:** each beat becomes 1-3 shots. Each shot has an id, a duration (from the model's limits, for example about 5 s for LTX-2.5 at 121 frames), framing, camera move, cast and location ids, a narration line, SFX or music cues, and a "chain from" (a previous shot id or none).
4. **Prompts and estimate:** compile a keyframe prompt and a motion prompt for each shot, using the bible's descriptors. Estimate the cost: the number of renders (keyframes × expected retries + video + audio), multiplied by the measured or assumed seconds per render on the target GPU, gives GPU time. On Google Colab, show it in compute units. **Gate 4:** the user approves the spend.
5. **Previs (optional):** block the key shots in 3D (`image-to-3d`; see `references/zerofield-previs-blocking.md`).
6. **Hand-off:** shots go through `flux3-klein-stills`, `still-qa`, `ltx25-image-to-video`, `continuity-check` and `film-assembly`.

## Rules
- **No auto-spend:** without an approved estimate, render only one test shot.
- If a stage fails (a model limit, or a beat that doesn't fit), change the plan and show what changed. Don't silently stretch durations.
- Keep `plan.json` as the single source of truth. Chat edits change the plan first, and then only the affected shots are re-run.
