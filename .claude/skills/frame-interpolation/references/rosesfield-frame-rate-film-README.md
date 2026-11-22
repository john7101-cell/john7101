<!-- Copied from rossaai/rosesfield workflows/video-edit-frame-rate-film/README.md (MIT); vendor frontmatter removed. Rows naming closed/hosted models do not apply: use open-weights options only. -->

# Video edit: raise the frame rate of a clip 2 or 4 times with FILM

Makes new frames between the frames of your clip with FILM and raises its frame rate 2 or 4 times, with the sound kept or left out. Built from Comfy's template utility-frame_interpolation-film.

| | |
|---|---|
| Workflow id | `video-edit-frame-rate-film` |
| Run by | [`video-edit`](../../packages/catalog/src/video-edit/) |
| Core model | FILM |
| Custom node packs | none, every node is a ComfyUI core node |
| GPU memory | The model files it loads add up to 0.1 GB. |

## Inputs

The catalog binds these names in [`entry.json`](entry.json). The UI file lists the value inputs for App Mode.

| Input | Node | Field | Takes |
|---|---|---|---|
| `source` | 1 `LoadVideo` | `file` | an uploaded video |
| `keepSound` | 11 `PrimitiveBoolean` | `value` | a value |
| `multiplier` | 9 `FrameInterpolate` | `multiplier` | a value |
| `frameRateExpression` | 10 `ComfyMathExpression` | `expression` | a value |

## Outputs

| Node | Key | Kind |
|---|---|---|
| 14 `SaveVideo` | `images` | video |

## Models

Rosesfield ships no weights. Each file goes into the model folder its row names.

| File | Model | Licence | Folder | Download |
|---|---|---|---|---|
| `film_net_fp16.safetensors` | FILM frame interpolation | [Apache-2.0](https://github.com/google-research/frame-interpolation) | `models/frame_interpolation` | [Hugging Face](https://huggingface.co/Comfy-Org/frame_interpolation/resolve/main/frame_interpolation/film_net_fp16.safetensors) |

## Files

- [`video-edit-frame-rate-film.api.json`](video-edit-frame-rate-film.api.json) is the graph every engine runs, in ComfyUI's API format. The catalog imports it.
- [`video-edit-frame-rate-film.json`](video-edit-frame-rate-film.json) is the same graph in ComfyUI's UI format, with positions, groups and one note. Each loader lists its file with a download link. A script writes it from the API file with the node definitions of ComfyUI v0.41.0.
- [`entry.json`](entry.json) is the catalog entry: the inputs, the outputs and the models.

## Source

Its nodes follow Comfy's template `utility_video_frame_interpolation` in [Comfy-Org/workflow_templates](https://github.com/Comfy-Org/workflow_templates), MIT, read on 2026-10-17, with the subgraphs opened.

## Checked

Its class names, input names, required inputs, link types and fixed values were checked against the node definitions of ComfyUI v0.41.0, read from source.
