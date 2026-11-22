# Google Colab runbook (for an agent)

When to use Google Colab: the user has no local GPU (or less than 16 GB), does not want Comfy Cloud credits, and accepts that Google Colab sessions are temporary and billed per connected minute in compute units. Prefer **local** when a 24 GB+ GPU is available. Prefer **Comfy Cloud** when the user already pays for it and needs nothing outside its node set.

## 0. Before anything
- Validate: `python skills/video-director/scripts/direct.py validate m.json`.
- Plan without network: `direct.py run m.json --dry-run`.
- Estimate: `python skills/google-colab-runner/scripts/colab.py estimate m.json --gpu L4` (try T4, L4, A100). Read out the session minutes and compute units, and say that the rates are unverified placeholders.
- Ask for a compute-unit cap and write it to `target.budget.max_credits`. Ask the user to approve the spend: `direct.py approve m.json spend`.

## A. Package mode (the user runs it)
1. `direct.py package --target google-colab m.json --out dist` writes `dist/<id>-google-colab/` and `.zip`:
   - `<id>.ipynb`: settings, unpack (jobs, workflows and runner are embedded as base64), GPU detection, ComfyUI and node install at pinned commits, model downloads, ComfyUI start, watchdog, optional tunnel, runner, collect, teardown
   - `workflows/<tier>/<job>.api.json`: API-format graphs for each shot with every non-file value filled in, for each tier up to the manifest tier
   - `jobs.json`, `manifest.json`, `models.json`, `nodes.lock.json`, `runner.py`, `comfy_client.py`, bundled node packs in `custom_nodes/`, `README.md`
   - `<id>-google-colab-assets.zip` when the manifest references local inputs (reference images, a music track)
2. Tell the user: open the notebook in Google Colab, pick a GPU, add the secret `HF_TOKEN` if a repo is gated, upload the assets zip if there is one, set `MODE = package`, and run all cells.
3. The runner picks the highest packaged tier that fits the GPU (T4 → draft, L4 → standard, A100/H100 → max, never above the manifest tier), renders stills then videos (chained shots use the previous clip's last frame), then audio jobs, and writes `outputs/state.json`. A re-run skips finished jobs.
4. Cell 10 copies `<id>-google-colab-outputs.zip` to Drive or downloads it. The watchdog releases the runtime at the session cap or after `IDLE_MINUTES`.
5. Back home: `colab.py ingest m.json <outputs.zip>` attaches the files as `unjudged` attempts. Judge them with still-qa and shot-qc, then `direct.py run` for continuity, audio mix, assembly and critique (local CPU is enough for those).

## B. Orchestrate mode (the director drives it)
1. Give the user the notebook from step A.1 with `MODE = orchestrate` and `TUNNEL = cloudflared`. Cells 1-8 install, download, start ComfyUI and print a `https://<name>.trycloudflare.com` URL. Warn the user that anyone with that URL can use their ComfyUI while it is up. An ngrok URL, or Google Colab's documented local-runtime connection to a ComfyUI the user runs, works the same way: `--url` only needs the ComfyUI HTTP API.
2. `direct.py run m.json --target google-colab --url <URL>`:
   - reads `/system_stats` for the GPU and VRAM, downgrades the tier if needed, and writes the estimate to `target.colab`
   - exit 6 if there is no cap or the estimate is over it; exit 3 at the `spend` gate until approved
   - then the normal pipeline: preflight against the live `/object_info`, stills with the judge loop, video with shot-qc, continuity, audio, post, assembly and critique. Every render first checks the compute-unit meter against the cap.
3. **Drops.** Exit 5 means the session went away. The manifest has every finished step. Ask the user to re-run the notebook (it reinstalls and re-downloads) and to paste the new URL, then re-run the same command with `--url <new>`. The meter carries the compute units already spent, and `target.colab.drops` counts the drops.
4. **Teardown.** At the end, or when the cap is hit, offer `colab.py teardown --url <URL>`. It clears the queue, interrupts the current job and uploads `gcr_teardown_request.txt`. The watchdog sees it within about 30 s and calls `google.colab.runtime.unassign()`. Ask the user to confirm in Runtime > Manage sessions.

## Compute-unit estimator
`session = bootstrap (6 min) + download_GB × 0.12 min + GPU work × GPU speed factor + 3 min collect-and-stop reserve`; `CU = session / 60 × CU per hour`. The GPU work is the director's own tier estimate (renders × per-render seconds on a 24 GB-class GPU). All factors live in `references/gpu-tiers.json`. They are unverified: override `--cu-per-hour` with the figure from the Google Colab Resources panel.

## Secrets
- The notebook reads `HF_TOKEN` from Google Colab secrets (`google.colab.userdata`) or the environment, uses it only in the request header, deletes the variable after the downloads and never prints it.
- No bundle file contains a token, a tunnel URL or a local path; `tests/test_static.py` checks the bundles for token-shaped strings.

## Limits
- Untested on a real Google Colab GPU: tested only against `tests/mock_comfy.py`.
- The model URL resolution covers 92 of 111 files; `models.json` marks the rest `url: null` and the notebook lists them as not downloaded.
- Custom node `requirements.txt` installs can conflict with Google Colab's preinstalled torch; check `/content/comfyui.log`.
- The T4 has no bf16 and 16 GB; LTX 22B graphs may not fit even at draft.
