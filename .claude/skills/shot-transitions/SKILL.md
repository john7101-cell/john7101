---
name: shot-transitions
description: Generate a bridging transition clip between two shots (first-frame/last-frame video) with open-weights LTX-2.5 or LTX-2.3 transition LoRA via Seam's graphs, with an optional VLM that describes both frames to write the transition prompt. Use for match cuts, morphs and seamless scene changes.
---

# shot-transitions

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are listed in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX license, which is **not** an OSI-approved open-source license.

**Heavy:** Seam measured a peak of about **31 GB VRAM** on a 32 GB card (24 GB is untested), and its full weight download is about **44 GB**. Use an A100 or larger on Google Colab, and run preflight first.

| Need | Workflow | Set |
|---|---|---|
| Describe two frames to get a transition prompt | `seam_describe_frames.api.json` | `2.image`, `3.prompt`; read the text output (`texts` in the client result) |
| LTX-2.5 first/last-frame transition | `seam_ltx25_flf2v_transition.api.json` | `31.image` start (last frame of shot A), `39.image` end (first frame of shot B), prompt in `251:252.value`, `251:198.value` seconds, `251:205.value` fps, `251:215`/`251:216` W/H |
| LTX-2.3 transition LoRA | `seam_ltx23_transition.api.json` | `138.image` first, `137.image` last, `139:128.text`, `139:98`/`139:113` W/H |

## Rules
- Extract the frames with ffmpeg: `-sseof -0.05 -frames:v 1` for the last frame and `-frames:v 1` for the first.
- Keep transitions short (1-2 s). Each one is an extra shot in `film-assembly`.
- Seam's slot and preset reference is in `references/seam-slots.json` and `references/seam-presets.py.txt`.
