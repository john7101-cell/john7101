---
name: multi-gpu-dispatch
description: Spread a production across several GPUs or ComfyUI servers: round-robin shots across server URLs with a stdlib dispatcher, or install ComfyUI-Distributed (parallel workers and tiles) or raylight (split one large model across GPUs with FSDP/xDiT). Use when one GPU is too slow or too small for the plan.
---

# multi-gpu-dispatch

There are three levels. Pick the lowest one that solves the problem.

| need | use | license |
|---|---|---|
| many independent shots, several servers (local, LAN, Google Colab tunnels, cloud) | `scripts/dispatch.py` (original, stdlib) | this collection |
| one graph, run in parallel on several GPUs (seeds and batches, tiled upscale, Wan t2v) | **robertvoy/ComfyUI-Distributed** node pack | Apache-2.0 |
| one model too big for one GPU (Wan 2.2 14B, LTX-2.3 22B, Flux) | **komikndr/raylight** node pack (FSDP / xDiT USP) | Apache-2.0 |

## dispatch.py
`python scripts/dispatch.py plan manifest.json --url http://gpu0:8188 --url http://gpu1:8188 [--weights 2,1]`
- It assigns each pending shot to a server. Weighted round-robin is used, chained shots (`chain_from`) stay on the server of the shot they chain from, and the assignment is written to `<manifest>.dispatch.json`.
- `run --dry-run` prints the per-server queue without network access.
- `run` writes one manifest copy per server and starts `video-director/scripts/direct.py run <copy> --only s01,s03…` for each one in parallel. Each worker does stills and video for its own shots only, and each server has to pass its own preflight. Approve the `bible`, `plan` and `spend` gates on the main manifest **before** you dispatch, because the copies inherit them.
- `merge` copies the worker shots back. Then run `direct.py run manifest.json` once for continuity, audio, post and assembly.
- Budget: the GPU-minute caps are per manifest, summed across servers.

## ComfyUI-Distributed and raylight
Their READMEs are copied in `references/` (Apache-2.0) and cover install steps, worker setup and limits. Example graphs, all UI format:
- `ui/distributed_wan22_14b_t2v.ui.json`
- `ui/distributed_upscale_video.ui.json`
- `ui/raylight_ltx23_i2v.ui.json`
- `ui/raylight_wan22.ui.json`

`workflows/ui/*.ui.json` are official Comfy-Org templates (MIT) in **UI format**, and most contain subgraphs. `comfy_client.py` refuses UI format. To use one: open it in ComfyUI, install the missing nodes and models that ComfyUI lists (they are also in `requirements.md`), then use **Workflow → Export (API)** to save it as `workflows/<name>.api.json`. Run `preflight.py` on the export and read off the node ids for `--set`. Node ids change when you export, so do not reuse ids from another graph.

## Rules
- The user installs node packs on their own servers. Never install packs or start workers from this skill.
- Every remote worker on Google Colab or Comfy Cloud spends credit. Show the per-worker estimate, then pass the video-director spend gate.
- raylight needs matched GPUs and NCCL. Distributed needs the same models on every worker. Check with `preflight.py` against **each** URL.
