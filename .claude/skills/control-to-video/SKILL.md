---
name: control-to-video
description: Generate video that follows a control signal (depth, OpenPose skeleton or canny edges extracted from a reference or previs clip) with open-weights LTX-2 and Wan 2.2 Fun Control / Wan VACE in ComfyUI. Use when motion, blocking or layout must match a source clip exactly.
---

# control-to-video

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX-2 license, which is **not** an OSI-approved open-source license.

## Pick a graph
| control | graph | format | notes |
|---|---|---|---|
| pose (DWPose) to Wan VACE | `wan_vace_pose_control.api.json` | API (motionfield) | `{{INPUT_VIDEO}}` is the driving clip, `{{PROMPT}}` the look |
| canny edges to Wan VACE | `wan_vace_canny_control.api.json` | API (motionfield) | best for layout and architecture |
| depth to LTX-2 | `ui/ltx2_depth_to_video.ui.json` | UI (Comfy-Org) | LTX 8n+1 frames, sizes in multiples of 32 |
| pose to LTX-2 | `ui/ltx2_pose_to_video.ui.json` | UI | |
| canny to LTX-2 | `ui/ltx2_canny_to_video.ui.json` | UI | |
| depth, pose or canny to Wan 2.2 14B Fun Control | `ui/wan22_14b_fun_control.ui.json` | UI | high and low-noise experts with a 4-step lightx2v LoRA |
| make the pose video only | `ui/utility_openpose_video.ui.json`, `ui/utility_sdpose_video_to_pose_map.ui.json` | UI | preprocessors: Fannovel16/comfyui_controlnet_aux (Apache-2.0) |

The motionfield graphs (MIT) use `{{PLACEHOLDER}}` strings. **Every** placeholder must be replaced with `--set` before you submit (`grep -o '{{[A-Z_]*}}' workflows/<file>` lists them). Pass numbers as JSON (`--set 9.width=832`). Their `OF_*` nodes are bundled in `assets/motionfield_nodes` (MIT; `dwpose_onnx` is Apache-2.0), and they need numpy, torch, opencv and onnxruntime on the **server**. Copy the folder to `ComfyUI/custom_nodes/`.

`workflows/ui/*.ui.json` are official Comfy-Org templates (MIT) in **UI format**, and most contain subgraphs. `comfy_client.py` refuses UI format. To use one: open it in ComfyUI, install the missing nodes and models that ComfyUI lists (they are also in `requirements.md`), then use **Workflow → Export (API)** to save it as `workflows/<name>.api.json`. Run `preflight.py` on the export and read off the node ids for `--set`. Node ids change when you export, so do not reuse ids from another graph.

## Rules
- Match the control clip's fps and length to the target. For LTX the frame count is 8n+1. For Wan the length is 4n+1 (Wan convention, unverified per graph).
- Pose control carries no identity. Feed the approved still as the reference or first frame so the cast matches the bible.
- Previs passes from `previs-control-passes` (depth, OpenPose MP4) go straight in as the control video.
- Extract depth with Depth Anything. The larger V2 and V3 checkpoints are CC-BY-NC, so use V2-Small (Apache-2.0) for commercial work. Their licenses are listed per file in `requirements.md`.
