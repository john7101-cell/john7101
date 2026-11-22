# UI templates converted to API format

The Comfy-Org (and ComfyUI-Distributed / raylight) templates under `skills/*/workflows/ui/*.ui.json` are in ComfyUI's UI format, which `comfy_client.py` cannot submit. Each one was converted with **ComfyUI's own frontend** and saved as `skills/<skill>/workflows/api/<name>.api.json`, so the director and the Google Colab runner can submit them directly.

## How (reproducible)
1. A CPU-only, headless ComfyUI at the pinned commit `b5a432157de6` (`--cpu`, no models), with the node packs from `custom-nodes.lock.json` checked out at their pinned commits, so `/object_info` knows every node class.
2. `scripts/ui_to_api/convert.mjs` (Playwright, headless Chromium) opens the ComfyUI page, calls `app.loadGraphData(workflow)` and then `app.graphToPrompt()`, and keeps `output`. That is the code path ComfyUI's own *Export (API)* uses, so subgraphs are flattened (node ids become `outer:inner`), primitive and reroute nodes are resolved into the inputs they feed, widget values are mapped to input names, notes are dropped, and autogrow inputs become `name.key` entries.
   `COMFY_URL=http://127.0.0.1:8188 node convert.mjs files.json results.json`
3. `scripts/ui_to_api/validate_api.py object_info.json <api files>` checks every output against the live `/object_info`: each class exists, each required input is present (autogrow inputs as `name.x`), every link points at a node in the graph, there is an output node, and no closed hosted API node is used.

Model files are not needed for conversion; they are named in the graphs and listed in `models.json`.

## Result: 26 of 27 converted
| UI template | API file | nodes | status |
|---|---|---|---|
| `control-to-video/workflows/ui/utility_openpose_video.ui.json` | `control-to-video/workflows/api/utility_openpose_video.api.json` | 3 | ok |
| `control-to-video/workflows/ui/wan22_14b_fun_control.ui.json` | `control-to-video/workflows/api/wan22_14b_fun_control.api.json` | 17 | ok |
| `control-to-video/workflows/ui/ltx2_canny_to_video.ui.json` | `control-to-video/workflows/api/ltx2_canny_to_video.api.json` | 50 | ok |
| `control-to-video/workflows/ui/ltx2_depth_to_video.ui.json` | `control-to-video/workflows/api/ltx2_depth_to_video.api.json` | 61 | ok |
| `control-to-video/workflows/ui/ltx2_pose_to_video.ui.json` | `control-to-video/workflows/api/ltx2_pose_to_video.api.json` | 50 | ok |
| `control-to-video/workflows/ui/utility_sdpose_video_to_pose_map.ui.json` | `control-to-video/workflows/api/utility_sdpose_video_to_pose_map.api.json` | 8 | ok |
| `relighting/workflows/ui/character_portrait_relighting.ui.json` | - | 11 | excluded: uses a closed hosted API node (GeminiImage2Node); this collection is open weights only |
| `relighting/workflows/ui/qwen_edit_2509_relight.ui.json` | `relighting/workflows/api/qwen_edit_2509_relight.api.json` | 17 | ok |
| `ltx-iclora-utils/workflows/ui/ltx23_style_transition.ui.json` | `ltx-iclora-utils/workflows/api/ltx23_style_transition.api.json` | 36 | ok |
| `ltx-iclora-utils/workflows/ui/ltx23_remove_subtitles.ui.json` | `ltx-iclora-utils/workflows/api/ltx23_remove_subtitles.api.json` | 49 | ok |
| `ltx-iclora-utils/workflows/ui/ltx23_ic_lora.ui.json` | `ltx-iclora-utils/workflows/api/ltx23_ic_lora.api.json` | 45 | ok |
| `ltx-iclora-utils/workflows/ui/ltx23_id_lora.ui.json` | `ltx-iclora-utils/workflows/api/ltx23_id_lora.api.json` | 49 | ok |
| `ltx-iclora-utils/workflows/ui/ltx23_remove_watermark.ui.json` | `ltx-iclora-utils/workflows/api/ltx23_remove_watermark.api.json` | 49 | ok |
| `ltx-iclora-utils/workflows/ui/ltx23_restore_archival.ui.json` | `ltx-iclora-utils/workflows/api/ltx23_restore_archival.api.json` | 49 | ok |
| `audio-driven-motion/workflows/ui/ltx2_audio_to_video.ui.json` | `audio-driven-motion/workflows/api/ltx2_audio_to_video.api.json` | 101 | ok |
| `audio-driven-motion/workflows/ui/wan22_14b_s2v.ui.json` | `audio-driven-motion/workflows/api/wan22_14b_s2v.api.json` | 29 | ok |
| `audio-driven-motion/workflows/ui/wan21_infinitetalk_music.ui.json` | `audio-driven-motion/workflows/api/wan21_infinitetalk_music.api.json` | 19 | ok |
| `audio-driven-motion/workflows/ui/humo.ui.json` | `audio-driven-motion/workflows/api/humo.api.json` | 16 | ok |
| `audio-driven-motion/workflows/ui/ltx23_image_audio_to_video.ui.json` | `audio-driven-motion/workflows/api/ltx23_image_audio_to_video.api.json` | 55 | ok |
| `audio-driven-motion/workflows/ui/wan21_infinitetalk.ui.json` | `audio-driven-motion/workflows/api/wan21_infinitetalk.api.json` | 47 | ok |
| `multi-gpu-dispatch/workflows/ui/raylight_wan22.ui.json` | `multi-gpu-dispatch/workflows/api/raylight_wan22.api.json` | 19 | ok |
| `multi-gpu-dispatch/workflows/ui/raylight_ltx23_i2v.ui.json` | `multi-gpu-dispatch/workflows/api/raylight_ltx23_i2v.api.json` | 46 | ok |
| `multi-gpu-dispatch/workflows/ui/distributed_wan22_14b_t2v.ui.json` | `multi-gpu-dispatch/workflows/api/distributed_wan22_14b_t2v.api.json` | 21 | ok |
| `multi-gpu-dispatch/workflows/ui/distributed_upscale_video.ui.json` | `multi-gpu-dispatch/workflows/api/distributed_upscale_video.api.json` | 11 | ok |
| `camera-control/workflows/ui/wan21_fun_camera_1_3b.ui.json` | `camera-control/workflows/api/wan21_fun_camera_1_3b.api.json` | 15 | ok |
| `camera-control/workflows/ui/wan22_14b_fun_camera.ui.json` | `camera-control/workflows/api/wan22_14b_fun_camera.api.json` | 16 | ok |
| `camera-control/workflows/ui/wan_ati_trajectory.ui.json` | `camera-control/workflows/api/wan_ati_trajectory.api.json` | 19 | ok |

**Not converted for use:** `relighting/workflows/ui/character_portrait_relighting.ui.json` converts cleanly but needs `GeminiImage2Node`, a closed hosted API node. This collection is open weights only, so no API file is shipped for it. Use `relighting/workflows/ui/qwen_edit_2509_relight.ui.json` (converted) or the `fix.relight*` routes instead.

**Routed now:** `control.ltx`, `control.ltx_canny`, `control.ltx_depth`, `camera.ati`, `video.a2v_ltx`, `post.clean_text`, `post.clean_watermark` (see `video-director/references/routing.md`). The other converted graphs are ready to submit with `comfy_client.py run` and can be routed by adding one row each.

**Caveat:** the conversion and validation are static. No converted graph has been executed on a GPU, and the role-to-node mappings in the new routing rows were read from the graphs by hand.
