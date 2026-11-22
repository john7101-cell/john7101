---
name: frame-interpolation
description: Raise a clip's frame rate (e.g. 24 to 48/60 fps, or smooth slow motion) with open-weights FILM frame interpolation in ComfyUI. Use for slow-mo beats or to match a delivery frame rate.
---

# frame-interpolation

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are listed in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX license, which is **not** an OSI-approved open-source license.

Use `film_frame_interpolation.api.json`: set `1.file` to the clip and `9.multiplier` to 2, 3 or 4 (new fps = source fps × multiplier). The README is in `references/`.

## Rules
- For slow motion, interpolate first, then play the result at the original fps in `film-assembly`.
- FILM smears fast occlusions and whip pans. Run `still-qa` on the middle frames of any shot with fast motion.
- The weights are about 0.1 GB, and their license is unverified.
