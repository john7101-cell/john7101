---
name: camera-control
description: Animate a still with an explicit, repeatable camera move (named trajectories such as orbit, dolly or crane, or drawn ATI point tracks) using open-weights Wan Fun Camera and Wan ATI in ComfyUI. Use when the camera path must be exact rather than prompted.
---

# camera-control

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX-2 license, which is **not** an OSI-approved open-source license.

| graph | format | control |
|---|---|---|
| `wan_fun_camera_i2v.api.json` | API (motionfield) | `OF_Trajectory.trajectory` is a named move (default `locked-off`), plus strength, fps and seed. It goes to `OF_CameraEmbed` and then `WanCameraImageToVideo` |
| `wan_fun_camera_director.api.json` | API (motionfield) | the same chain without CLIP-vision, for a lighter graph |
| `ui/wan22_14b_fun_camera.ui.json` | UI (Comfy-Org) | Wan 2.2 14B Fun Camera with core camera-embedding nodes |
| `ui/wan21_fun_camera_1_3b.ui.json` | UI | 1.3B, so the smallest VRAM (draft tier) |
| `ui/wan_ati_trajectory.ui.json` | UI | ATI: draw point trajectories in the spline editor, so objects follow paths |

The motionfield graphs (MIT) use `{{PLACEHOLDER}}` strings. **Every** placeholder must be replaced with `--set` before you submit (`grep -o '{{[A-Z_]*}}' workflows/<file>` lists them). Pass numbers as JSON (`--set 9.width=832`). Their `OF_*` nodes are bundled in `assets/motionfield_nodes` (MIT; `dwpose_onnx` is Apache-2.0), and they need numpy, torch, opencv and onnxruntime on the **server**. Copy the folder to `ComfyUI/custom_nodes/`.

The valid trajectory names are the keys of the catalog in `assets/motionfield_nodes/core/camera_trajectory.py`. Read them there rather than guessing.

`workflows/ui/*.ui.json` are official Comfy-Org templates (MIT) in **UI format**, and most contain subgraphs. `comfy_client.py` refuses UI format. To use one: open it in ComfyUI, install the missing nodes and models that ComfyUI lists (they are also in `requirements.md`), then use **Workflow → Export (API)** to save it as `workflows/<name>.api.json`. Run `preflight.py` on the export and read off the node ids for `--set`. Node ids change when you export, so do not reuse ids from another graph.

## Picture to 3D to camera move (agentY design)
`references/agentY-camera-move-control.md` (MIT) describes the chain: picture → depth mesh → keyed camera move → rendered clip → control video for Wan Fun Control or an LTX IC-LoRA. In this collection that chain is `image-to-3d` or `previs-control-passes`, then `control-to-video`. The agentY tool names in that file do not exist here.
- Keep a move within about the depth of the picture. Moving further past the content shows holes.
- Check a camera claim with numbers (`shot-qc` motion and freeze), not with a VLM description.
