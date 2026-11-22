---
name: continuity-check
description: Sweep adjacent shots and takes for continuity breaks (cast, wardrobe, props, grade, lighting, screen direction, timing) at plan level and take level, and report findings with proposed fixes - never edits. Use before locking a cut, after a take is replaced, or when asked "do these cut together?".
---

# continuity-check

This follows ZeroField's continuity-check (MIT). The full method is in `references/zerofield-continuity-check.md`.

## Procedure
1. List every join (shot N to shot N+1) and mark the ones touched by recent changes.
2. **Plan level:** for each join, compare the plan entries. Cast and wardrobe ids, props, location and time of day, screen direction (the 180° rule), the camera axis, and the grade or LUT should agree unless the plan marks a deliberate change.
3. **Take level:** for each join, compare the last frame of N with the first frame of N+1. Extract them with ffmpeg (`-sseof -0.05 -frames:v 1` / `-frames:v 1`). Use a VLM: `still-qa/scripts/judge.py` with `--ref` set to the other frame, the prompt "same character, wardrobe, props, lighting, direction?", and the judge scores from `still-qa`.
4. **Classify** each finding as *break* (must fix), *drift* (should fix) or *note*, with evidence: the frame paths and the plan fields involved. If you have no evidence, report nothing.
5. **Propose the cheapest fix:** edit the prompt, re-seed, `image-edit` the keyframe, chain from the last frame, or re-grade. A proposal names its target skill and parameters.
6. Report breaks first, then drift. The user or the orchestrator decides what to apply.

## Hard rule
This skill never writes to the plan, the files or the renders. It returns findings and proposals only.
