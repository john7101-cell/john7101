<!-- Copied from rossaai/rosesfield workflows/upscale-video-seedvr2/README.md (MIT); vendor frontmatter removed. Rows naming closed/hosted models do not apply: use open-weights options only. -->

# Upscale a video 2 or 4 times with SeedVR2

Raises the resolution of one clip by 2 or 4 times with SeedVR2 and keeps its frame rate and sound. The model file is an input, so the same graph runs the 3B and the 7B model. Built from Comfy's template upscale_video_seedvr2_3b_int8.

| | |
|---|---|
| Workflow id | `upscale-video-seedvr2` |
| Run by | [`upscale`](../../packages/catalog/src/upscale/) |
| Core model | SeedVR2 3B or 7B |
| Custom node packs | none, every node is a ComfyUI core node |
| GPU memory | The model files it loads add up to 4.0 GB. |

## Inputs

The catalog binds these names in [`entry.json`](entry.json). The UI file lists the value inputs for App Mode.

| Input | Node | Field | Takes |
|---|---|---|---|
| `video` | 1 `LoadVideo` | `file` | an uploaded video |
| `scale` | 111 `ResizeImageMaskNode` | `resize_type.multiplier` | a value |
| `seed` | 109 `KSampler` | `seed` | a value |
| `model` | 108 `UNETLoader` | `unet_name` | a value |

## Outputs

| Node | Key | Kind |
|---|---|---|
| 130 `SaveVideo` | `images` | video |

## Models

Rosesfield ships no weights. Each file goes into the model folder its row names.

| File | Model | Licence | Folder | Download |
|---|---|---|---|---|
| `seedvr2_ema_vae_fp16.safetensors` | SeedVR2 VAE | [Apache-2.0](https://huggingface.co/ByteDance-Seed/SeedVR2-3B) | `models/vae` | [Hugging Face](https://huggingface.co/Comfy-Org/SeedVR2/resolve/main/vae/seedvr2_ema_vae_fp16.safetensors) |
| `seedvr2_3b_int8_convrot.safetensors` | SeedVR2 3B, int8 | [Apache-2.0](https://huggingface.co/ByteDance-Seed/SeedVR2-3B) | `models/diffusion_models` | [Hugging Face](https://huggingface.co/Comfy-Org/SeedVR2/resolve/main/diffusion_models/seedvr2_3b_int8_convrot.safetensors) |

## Files

- [`upscale-video-seedvr2.api.json`](upscale-video-seedvr2.api.json) is the graph every engine runs, in ComfyUI's API format. The catalog imports it.
- [`upscale-video-seedvr2.json`](upscale-video-seedvr2.json) is the same graph in ComfyUI's UI format, with positions, groups and one note. Each loader lists its file with a download link. A script writes it from the API file with the node definitions of ComfyUI v0.41.0.
- [`entry.json`](entry.json) is the catalog entry: the inputs, the outputs and the models.

## Source

Its nodes follow Comfy's blueprint `upscale_video_seedvr2_3b_int8` in [Comfy-Org/workflow_templates](https://github.com/Comfy-Org/workflow_templates), MIT, read on 2026-10-17.

## Checked

Its class names, input names, required inputs, link types and fixed values were checked against the node definitions of ComfyUI v0.41.0, read from source.
