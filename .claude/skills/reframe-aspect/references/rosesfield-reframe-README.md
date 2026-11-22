<!-- Copied from rossaai/rosesfield workflows/video-edit-reframe-ltx-2-3/README.md (MIT); vendor frontmatter removed. Rows naming closed/hosted models do not apply: use open-weights options only. -->

# Video edit: reframe a clip to another format with LTX 2.3

Places your clip in the middle of a black frame of another format, then fills the frame with LTX 2.3 and the outpainting IC-LoRA, at your clip's frame rate, with its sound kept or left out. Built from Comfy's template template_ltx2_3_lora_video_outpainting.

| | |
|---|---|
| Workflow id | `video-edit-reframe-ltx-2-3` |
| Run by | [`video-edit`](../../packages/catalog/src/video-edit/) |
| Core model | LTX 2.3 22B dev, fp8, with the distilled LoRA and an outpainting IC-LoRA |
| Custom node packs | [ComfyUI-LTXVideo](https://github.com/Lightricks/ComfyUI-LTXVideo) at commit `82bd963cdeb66d023bed8c99324a307020907ef8`, the commit Comfy's template names, LTX-2 Community License. It gives `LTXAddVideoICLoRAGuide`. Comfy Cloud installs it, so the graph runs on Comfy Cloud. |

## Inputs

The catalog binds these names in [`entry.json`](entry.json). The UI file lists the value inputs for App Mode.

| Input | Node | Field | Takes |
|---|---|---|---|
| `source` | 1 `LoadVideo` | `file` | an uploaded video |
| `keepSound` | 41 `PrimitiveBoolean` | `value` | a value |
| `width` | 12 `PrimitiveInt` | `value` | a value, a multiple of 32 |
| `height` | 13 `PrimitiveInt` | `value` | a value, a multiple of 32 |
| `prompt` | 5138 `CLIPTextEncode` | `text` | a value |
| `seed` | 5117 `RandomNoise` | `noise_seed` | a value |

## Outputs

| Node | Key | Kind |
|---|---|---|
| 44 `SaveVideo` | `images` | video |

## How it fills the frame

- Nodes 14 and 15 fit your clip inside the frame of `width` by `height` without cropping it. Node 16 resizes every frame to that size.
- Node 20 makes a black frame for each of your frames, and node 21 places your picture in its middle, at the offsets nodes 17 and 19 compute. The template pads with black the same way, with a node from comfyui-kjnodes.
- Node 5142 gives the padded clip to LTX 2.3 as the IC-LoRA guide at full strength, and nodes 5112 and 5121 make the video and audio latents at your clip's size, length and frame rate. LTX keeps 8 times n plus 1 frames, so the output can be up to 7 frames shorter than your clip.
- One sampling pass of 8 steps runs on the distilled LoRA at 0.5 and the outpainting IC-LoRA at 1.0, with the sigmas of the template. `LTXVCropGuides` removes the guide frames, and node 5154 decodes the frames.
- Node 43 writes the frames at your clip's frame rate, with your clip's sound when `keepSound` is on. The sound LTX makes is not used.

## Models

Rosesfield ships no weights. Each file goes into the model folder its row names.

| File | Model | Licence | Folder | Download |
|---|---|---|---|---|
| `ltx-2.3-22b-dev-fp8.safetensors` | LTX 2.3 22B dev, fp8, with its video VAE and audio VAE | [LTX-2.x Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x) | `models/checkpoints` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.3-fp8/resolve/main/ltx-2.3-22b-dev-fp8.safetensors) |
| `ltx-2.3-22b-distilled-lora-384.safetensors` | LTX 2.3 distilled LoRA | [LTX-2.x Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x) | `models/loras` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-22b-distilled-lora-384.safetensors) |
| `ltx-2.3-22b-ic-lora-outpaint.safetensors` | Outpainting IC-LoRA for LTX 2.3, by oumoumad | [its licence on Hugging Face](https://huggingface.co/oumoumad/LTX-2.3-22b-IC-LoRA-Outpaint) | `models/loras` | [Hugging Face](https://huggingface.co/oumoumad/LTX-2.3-22b-IC-LoRA-Outpaint/resolve/main/ltx-2.3-22b-ic-lora-outpaint.safetensors) |
| `gemma_3_12B_it.safetensors` | Gemma 3 12B text encoder | [Gemma Terms of Use](https://ai.google.dev/gemma/terms) | `models/text_encoders` | [Hugging Face](https://huggingface.co/Comfy-Org/ltx-2/resolve/main/split_files/text_encoders/gemma_3_12B_it.safetensors) |

The LTX-2 Community License dated January 5, 2026 asks for a paid licence from an entity with annual revenue of at least 10,000,000 USD. The UI file carries no SHA256 digest for these files. None was read on the machine that wrote this folder.

## Files

- [`video-edit-reframe-ltx-2-3.api.json`](video-edit-reframe-ltx-2-3.api.json) is the graph every engine runs, in ComfyUI's API format. The catalog imports it.
- [`video-edit-reframe-ltx-2-3.json`](video-edit-reframe-ltx-2-3.json) is the same graph in ComfyUI's UI format, with positions, groups and one note. Each loader lists its file with a download link. A script writes it from the API file with the node definitions of ComfyUI v0.41.0 and of ComfyUI-LTXVideo.
- [`entry.json`](entry.json) is the catalog entry: the inputs, the outputs and the models.

## Source

Its nodes follow Comfy's template `template_ltx2_3_lora_video_outpainting` in [Comfy-Org/workflow_templates](https://github.com/Comfy-Org/workflow_templates), MIT, read at commit `59a3b48bf369c5a15f29a1308bae3e279fa15505`, with its subgraph opened. Nodes from 5110 up keep the template's ids. Four changes keep the graph on core nodes and the one pack:

- `LoadVideo`, `GetVideoComponents` and `GetImageSize` read the clip, its frame rate and its size in place of the comfyui-videohelpersuite nodes, and `CreateVideo` and `SaveVideo` write it.
- `EmptyImage` and `ImageCompositeMasked` pad with black in place of comfyui-kjnodes' `ImagePadKJ`, and `PrimitiveInt` sets the frame size in place of the aspect ratio and the half-size scale.
- `ComfyMathExpression` and the float frame rate of `LTXVEmptyLatentAudio` replace ComfyMath's `CM_FloatToInt`.
- The template's two `Float32ColorCorrect` nodes are left out. Their pack is not named in the template, so their inputs could not be read. The image to video node it bypasses and the comparison clip are left out too.

## Checked

Its core class names, input names, link types and fixed values were checked against the node definitions of ComfyUI v0.41.0, read from source. `LTXAddVideoICLoRAGuide` was checked against ComfyUI-LTXVideo at commit `44c8a36b7c31ee00b4271daed11dc2a4aa481140`, a later commit than the pinned one, whose seven value inputs match the template's values.
