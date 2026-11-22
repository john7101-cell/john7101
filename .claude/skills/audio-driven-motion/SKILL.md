---
name: audio-driven-motion
description: Make video whose motion is driven by an audio track (a talking or singing avatar with body motion, or music-reactive motion) using open-weights LTX-2 audio-to-video, LTX-2.3 image+audio-to-video, Wan 2.2 S2V, InfiniteTalk or HuMo in ComfyUI. Use for presenters, singers and audio-synced performance beyond mouth-only lip-sync.
---

# audio-driven-motion

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX-2 license, which is **not** an OSI-approved open-source license.

Use `lip-sync` when only the mouth has to move on an existing shot. Use this skill when the audio drives the **whole performance**: body, head and gesture.

| graph | format | model | use |
|---|---|---|---|
| `wan22_s2v.api.json` | API (motionfield) | Wan 2.2 S2V 14B | image + speech or song to a full-body performance. Placeholders: PROMPT, NEGATIVE, INPUT_AUDIO, INPUT_IMAGE, WIDTH, HEIGHT, FRAMES, SEED, FPS |
| `wan21_infinitetalk_vocal_sep.api.json` | API (kitty-open-studio, MIT) | InfiniteTalk (Wan 2.1) + MelBand RoFormer vocal separation | a singer on a full music mix: it separates the vocals first. Set `125.audio`, `284.image`, `312.text` and `128.seed` |
| `ui/ltx2_audio_to_video.ui.json` | UI (Comfy-Org) | LTX-2 a2v | audio-conditioned LTX |
| `ui/ltx23_image_audio_to_video.ui.json` | UI | LTX-2.3 ia2v | image + audio |
| `ui/wan22_14b_s2v.ui.json` | UI | Wan 2.2 S2V | the official version of the first row |
| `ui/wan21_infinitetalk.ui.json`, `ui/wan21_infinitetalk_music.ui.json` | UI | InfiniteTalk | long talking clips; music variant |
| `ui/humo.ui.json` | UI | HuMo | text + image + audio to a human video |

The motionfield graphs (MIT) use `{{PLACEHOLDER}}` strings. **Every** placeholder must be replaced with `--set` before you submit (`grep -o '{{[A-Z_]*}}' workflows/<file>` lists them). Pass numbers as JSON (`--set 9.width=832`). Their `OF_*` nodes are bundled in `assets/motionfield_nodes` (MIT; `dwpose_onnx` is Apache-2.0), and they need numpy, torch, opencv and onnxruntime on the **server**. Copy the folder to `ComfyUI/custom_nodes/`.

`workflows/ui/*.ui.json` are official Comfy-Org templates (MIT) in **UI format**, and most contain subgraphs. `comfy_client.py` refuses UI format. To use one: open it in ComfyUI, install the missing nodes and models that ComfyUI lists (they are also in `requirements.md`), then use **Workflow → Export (API)** to save it as `workflows/<name>.api.json`. Run `preflight.py` on the export and read off the node ids for `--set`. Node ids change when you export, so do not reuse ids from another graph.

## Rules
- Trim the audio to the shot window (`ffmpeg -ss S -t D`). Frames = duration × fps, rounded to the model's lattice: 8n+1 for LTX, 4n+1 for Wan (unverified per graph).
- Use clean vocals (stems) for the best sync. A full mix only works with the vocal-separation graph.
- The face should be at least 25% of the frame height and frontal or three-quarter. Judge three frames and the mouth region with `still-qa`.
- Weight licenses: Wan, InfiniteTalk and HuMo are listed as Apache-2.0 (unverified). LTX uses the Lightricks license (not OSI). The MelBand RoFormer license is unverified.
