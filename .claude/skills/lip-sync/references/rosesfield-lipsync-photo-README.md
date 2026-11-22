<!-- Copied from rossaai/rosesfield workflows/lipsync-photo-ltx-2-3/README.md (MIT); vendor frontmatter removed. Rows naming closed/hosted models do not apply: use open-weights options only. -->

# Lip sync: a talking video from a photo and audio with LTX 2.3

Makes a video of the person in your photo speaking your audio with LTX 2.3 22B in two stages, half size then twice the size with the spatial upscaler, while your audio stays fixed as the model's audio, and puts your audio on the video. Built from Comfy's template video_ltx2_3_ia2v.

| | |
|---|---|
| Workflow id | `lipsync-photo-ltx-2-3` |
| Run by | [`lipsync`](../../packages/catalog/src/lipsync/), as From a photo's default |
| Core model | LTX 2.3 22B dev, fp8, with the distilled LoRA 1.1 |
| Custom node packs | none, every node is a ComfyUI core node |
| GPU memory | The model files it loads add up to 42.3 GB. |

## Inputs

The catalog binds these names in [`entry.json`](entry.json). The UI file lists the value inputs for App Mode.

| Input | Node | Field | Takes |
|---|---|---|---|
| `photo` | 269 `LoadImage`, Photo | `image` | an uploaded image |
| `audio` | 276 `LoadAudio`, Audio | `audio` | an uploaded audio |
| `scene` | 900 `StringConcatenate`, Talking and scene | `string_b` | a value |
| `seed` | 286 `RandomNoise` | `noise_seed` | a value |
| `width` | 297 `ResizeImageMaskNode`, Photo at the video size | `resize_type.width` | a value |
| `height` | 297 `ResizeImageMaskNode`, Photo at the video size | `resize_type.height` | a value |
| `latentWidth` | 302 `EmptyLTXVLatentVideo` | `width` | a value |
| `latentHeight` | 302 `EmptyLTXVLatentVideo` | `height` | a value |
| `frames` | 302 `EmptyLTXVLatentVideo` | `length` | a value |
| `maskWidth` | 333 `SolidMask` | `width` | a value |
| `maskHeight` | 333 `SolidMask` | `height` | a value |
| `seconds` | 332 `TrimAudioDuration`, Audio at the video length | `duration` | a value |

## Outputs

| Node | Key | Kind |
|---|---|---|
| 341 `SaveVideo` | `images` | video |

## How your audio leads the lips

- Node 297 crops your photo from its center to the video size, and nodes 350 and 334 prepare it the way the template does. The photo is the first frame in both stages, at strength 0.7 in the first, node 325, and 1.0 in the second, node 296.
- Node 332 cuts your audio to the video's length, and node 328 encodes it with the LTX 2.3 audio VAE. Node 327 sets a noise mask of 0 from node 333 on that audio latent, so the first stage denoises the video and keeps your audio as it is. The lips follow the audio the model holds.
- The first stage renders at half the width and the height, nodes 302 to 309. The second stage doubles the size with the spatial upscaler and refines the video, nodes 295 to 311, as in the template.
- Node 312 puts the audio from node 332 on the video, so you hear your own file and not the model's decoded audio.
- The catalog sets 24 frames a second and a frame count of 8 n + 1, the smallest one at least as long as your audio, and cuts the audio to that length, in [`lipsync-frames.ts`](../../packages/catalog/src/lipsync/comfy/lipsync-frames.ts). 5 seconds of audio make 121 frames, 5.04 seconds.

## Models

Rosesfield ships no weights. Each file goes into the model folder its row names.

| File | Model | Licence | Folder | Download |
|---|---|---|---|---|
| `ltx-2.3-22b-dev-fp8.safetensors` | LTX 2.3 22B dev, fp8, with its video and audio VAEs | [LTX-2 Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2) | `models/checkpoints` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.3-fp8/resolve/main/ltx-2.3-22b-dev-fp8.safetensors) |
| `ltx_2.3_22b_distilled_1.1_lora_dynamic_fro09_avg_rank_111_bf16.safetensors` | LTX 2.3 22B distilled LoRA 1.1 | [LTX-2 Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2) | `models/loras` | [Hugging Face](https://huggingface.co/Comfy-Org/ltx-2.3/resolve/main/split_files/loras/ltx_2.3_22b_distilled_1.1_lora_dynamic_fro09_avg_rank_111_bf16.safetensors) |
| `gemma_3_12B_it_fp4_mixed.safetensors` | Gemma 3 12B text encoder, fp4 | [Gemma Terms of Use](https://ai.google.dev/gemma/terms) | `models/text_encoders` | [Hugging Face](https://huggingface.co/Comfy-Org/ltx-2/resolve/main/split_files/text_encoders/gemma_3_12B_it_fp4_mixed.safetensors) |
| `ltx-2.3-spatial-upscaler-x2-1.1.safetensors` | LTX 2.3 spatial upscaler, 2 times | [LTX-2 Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2) | `models/latent_upscale_models` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-spatial-upscaler-x2-1.1.safetensors) |

The LTX-2 Community License asks an entity with annual revenue of 10,000,000 USD or more for a paid licence. The SHA256 of each file in the UI file was read from the Hugging Face API on 2026-10-20.

## Files

- [`lipsync-photo-ltx-2-3.api.json`](lipsync-photo-ltx-2-3.api.json) is the graph every engine runs, in ComfyUI's API format. The catalog imports it.
- [`lipsync-photo-ltx-2-3.json`](lipsync-photo-ltx-2-3.json) is the same graph in ComfyUI's UI format, with positions, groups and one note. Each loader lists its file with a download link and its SHA256. A script writes it from the API file.
- [`entry.json`](entry.json) is the catalog entry: the inputs, the outputs and the models.

## Source

Its nodes follow Comfy's template `video_ltx2_3_ia2v` in [Comfy-Org/workflow_templates](https://github.com/Comfy-Org/workflow_templates/blob/59a3b48bf369c5a15f29a1308bae3e279fa15505/templates/video_ltx2_3_ia2v.json), MIT, with its subgraph opened. Each node keeps its id from the template. The changes:

- The prompt enhancer is left out, nodes 345 to 349, so no Gemma LoRA loads and the model reads a fixed line about talking to the camera, with your scene after it, node 900.
- The primitive and math nodes the template's subgraph holds are left out. The catalog sets the sizes, the frame count and the audio length on the nodes that read them.
- The video carries your audio, node 332, in place of the decoded audio of node 303, which is left out.
- The video size is the catalog's, 512 by 512 for 1:1, half of it in the first stage. The template renders 1280 by 720.

## Checked

Its class names, input names and links follow the template and the LTX 2.5 graphs of this folder. `CreateVideo` takes `fps` and `bit_depth` 8, as in those graphs, where the template sets `bit_depth` to `auto`.
