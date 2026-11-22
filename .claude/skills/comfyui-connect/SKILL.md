---
name: comfyui-connect
description: Submit ComfyUI API-format workflows to any ComfyUI server (local, a Google Colab tunnel, or a hosted instance), poll for completion, download outputs, upload inputs, and cancel jobs. Use whenever another skill needs to run a ComfyUI workflow.
---

# comfyui-connect

`scripts/comfy_client.py` uses only the Python standard library. Every other skill ships a copy of it.

## Targets
- **Local:** `COMFY_URL=http://127.0.0.1:8188`.
- **Google Colab:** start ComfyUI in the notebook, expose it through a tunnel (for example cloudflared), and set `COMFY_URL` to the tunnel URL. Ask before you start a paid Google Colab runtime, and stop it when the job is done.
- **Hosted (Comfy Cloud or any other):** only works if the host exposes the standard `/prompt`, `/history`, `/view` and `/upload/image` routes. Set `COMFY_API_KEY` to send a Bearer token. Whether Comfy Cloud accepts this exact API and auth is **unverified**, so read the host's API docs first.

## Commands
| Do | Command |
|---|---|
| Run a graph end to end | `comfy_client.py run wf.api.json --set 6.text="a red fox" --set 14.noise_seed=7 --out out/` |
| Submit only | `comfy_client.py submit wf.api.json` prints `{"prompt_id": ...}` |
| Wait for several jobs | `comfy_client.py wait ID1 ID2 --timeout 300` |
| Download outputs | `comfy_client.py fetch ID --out out/` |
| Cancel a job | `comfy_client.py cancel ID` |
| Upload an input | `comfy_client.py upload start.png`, then pass the returned `name` to the LoadImage `image` input |

## How wait and cancel behave
- `wait` polls `/history/<id>` and `/queue` until every id is `done` or `error`, or until the timeout. When the timeout runs out, it returns each job's live status (`queued`/`running`) with `timed_out: true`. A timeout is not a failure, so you can call `wait` again. If one id can't be fetched, its error is reported for that id alone and the other ids still return.
- `cancel` checks where the job is. A running job gets `POST /interrupt`. A queued job gets `POST /queue {"delete":[id]}`. A finished job is left alone.
- Keep each timeout short (60-300 s) and loop. That keeps you responsive, so you can report progress or cancel.

## Rules
- Only send API-format graphs. If a JSON file has a top-level `nodes` key, it is UI format: re-export it with "Save (API)".
- `--set` values are parsed as JSON when possible, so `--set 5.width=1024` sends a number.
- If `/prompt` returns `node_errors`, show them and run `comfyui-preflight`. Don't retry blindly.
