---
name: still-qa
description: Judge loop for generated stills and video frames using an open-weights vision-language model (e.g. Qwen2.5-VL/Qwen3-VL via an OpenAI-compatible local server) - score prompt match, identity, artifacts, composition and style, then retry once with a concrete fix. Use after every keyframe and before image-to-video.
---

# still-qa

`python scripts/judge.py --endpoint $VLM_ENDPOINT --model $VLM_MODEL --image out/s03.png --prompt "<shot prompt>" --bible bible.md [--ref cast/mara_front.png]`

This prints JSON with `scores`, `mean`, `verdict` (`pass`/`retry`), `issues` and `fix`.

## The loop
1. Generate the still, then judge it.
2. If the verdict is `pass` (every score 3 or higher and a mean of 3.5 or higher), accept it.
3. If the verdict is `retry`, apply the single `fix`: a prompt edit, a new seed, or an `image-edit` pass. Regenerate and judge again. Allow at most 2 retries, then show the best take to the user with its issues.
4. Log every take's scores in the plan so `continuity-check` can use them.

## Judge setup
- Serve an open-weights VLM (Qwen2.5-VL-7B-Instruct, Apache-2.0, unverified for your build) with vLLM, llama.cpp server, Ollama or LM Studio. Any OpenAI-compatible `/v1/chat/completions` endpoint works. A 7B VLM needs about 16 GB in bf16, or about 6-8 GB quantized (estimate, unverified).
- In Comfyrizz-style setups, the orchestrator's own judge (for example Pi) can replace `judge.py` as long as it keeps the same rubric and JSON shape.
- The judge must see the prompt and the bible descriptors, not only the image.
- For video, judge 3 frames: the first, the middle and the last.

## Anti-slop checklist
Check for these as well as the rubric: a waxy, over-smoothed skin look; extra or merged fingers; garbled text or signage; duplicated faces in crowds; the same centered composition in every shot; HDR-like over-sharpening; a wardrobe that drifts between takes; and generic "cinematic" teal-orange whatever the bible says.
