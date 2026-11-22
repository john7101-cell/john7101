<!-- Copied from rossaai/rosesfield workflows/motion-guide-ltx-2-3-ic-lora/README.md (MIT); vendor frontmatter removed. Rows naming closed/hosted models do not apply: use open-weights options only. -->

# Motion: move a photo along a depth guide on LTX 2.3

Renders the person in your photo moving along your guide video, on LTX 2.3 22B distilled with its union control IC-LoRA in 8 steps. The guide is a depth video you made, such as one rendered in Blender, and its frames go straight to the IC-LoRA, so the guide sets the camera path, the blocking and the timing. Your photo sets the first frame. The video starts on the first frame the model makes, after your photo, and keeps the guide's frame count and frame rate, with no sound. Built from Comfy's template video_ltx2_3_ic_lora.

| | |
|---|---|
| Workflow id | `motion-guide-ltx-2-3-ic-lora` |
| Run by | [`motion`](../../packages/catalog/src/motion/), in Follow a guide |
| Core model | LTX 2.3 22B distilled, with the LTX 2.3 union control IC-LoRA |
| Custom node packs | none, every node is a ComfyUI core node |

## Inputs

The catalog binds these names in [`entry.json`](entry.json). The UI file lists the value inputs for App Mode.

| Input | Node | Field | Takes |
|---|---|---|---|
| `photo` | 200 `LoadImage`, Photo | `image` | an uploaded image |
| `clip` | 199 `LoadVideo`, Guide video | `file` | an uploaded video: the depth guide |
| `scene` | 900 `StringConcatenate`, Motion and scene | `string_b` | a value |
| `shortSide` | 702 `PrimitiveInt`, Short side | `value` | a value: 448 for 480p, or 704 for 720p |
| `seed` | 704 `KSampler` | `seed` | a value |

## Outputs

| Node | Key | Kind |
|---|---|---|
| 68 `SaveVideo` | `images` | video, MP4 with H.264 |

## How it runs

It is the graph of [`motion-ltx-2-3-ic-lora`](../motion-ltx-2-3-ic-lora/README.md) with three changes.

- **The guide goes straight in.** The person detector and SDPose, nodes 707 to 712, are gone. Nodes 717 and 719 take the guide's own frames from node 706, so the IC-LoRA reads your depth video frame by frame. The union control IC-LoRA takes pose, depth and edges, per its [model card](https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Union-Control). A depth guide carries the camera, the room and the bodies, so it sets the camera path as well as the movement.
- **The prompt.** Node 900 puts a fixed sentence before your words about the scene, which keeps the person from your photo the same in every shot. It names no control and no motion, because the guide carries the motion.
- **No sound.** Node 122 takes no audio, because a depth guide carries none, and the video has no audio track.

Everything else is the Motion graph's own. Node 692 keeps the first 10 seconds of the guide. LTX renders 8 n + 1 frames, and the last guide frame is repeated up to that count, nodes 714 to 719. Node 724 keeps the guide's n frames from render frame 1 on, so output frame k follows guide frame k + 1, and frame 0, your photo, is not shown. Nodes 721 to 723 set the short side to the bound value and keep the photo's ratio, each side a multiple of 64. Node 115 fits the guide to that size with a centre crop, so a guide in another shape than your photo loses its edges, and the Motion screen refuses such a guide.

## Models

Rosesfield ships no weights. Each file goes into the model folder its row names. Each digest is the SHA256 Hugging Face lists for the file, read on 2026-10-20.

| File | Model | Licence | Folder | Download |
|---|---|---|---|---|
| `ltx-2.3-22b-distilled-fp8.safetensors` | LTX 2.3 22B distilled, fp8, with its video and audio VAEs | [LTX-2 Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2), card tag `ltx-2-community-license-agreement` on Lightricks/LTX-2.3-fp8 at `1d756cd27fa11c0896c4dfee093cd1bf36c7f7a1` | `models/checkpoints` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.3-fp8/resolve/main/ltx-2.3-22b-distilled-fp8.safetensors) |
| `ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors` | LTX 2.3 union control IC-LoRA, reference at half size | [LTX-2 Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2), card tag `ltx-2-community-license` on Lightricks/LTX-2.3-22b-IC-LoRA-Union-Control at `b4d1c4d8c9e544e9bbbd6811bb4363708b6093ff` | `models/loras` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Union-Control/resolve/main/ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors) |
| `gemma_3_12B_it_fp4_mixed.safetensors` | Gemma 3 12B text encoder, fp4 | [Gemma Terms of Use](https://ai.google.dev/gemma/terms) of its base model google/gemma-3-12b-it | `models/text_encoders` | [Hugging Face](https://huggingface.co/Comfy-Org/ltx-2/resolve/main/split_files/text_encoders/gemma_3_12B_it_fp4_mixed.safetensors) |

## Files

- [`motion-guide-ltx-2-3-ic-lora.api.json`](motion-guide-ltx-2-3-ic-lora.api.json) is the graph every engine runs, in ComfyUI's API format. The catalog imports it.
- [`motion-guide-ltx-2-3-ic-lora.json`](motion-guide-ltx-2-3-ic-lora.json) is the same graph in ComfyUI's UI format, with positions, groups and one note. Each loader lists its file with a download link and its digest. A script writes it from the Motion graph's UI file.
- [`entry.json`](entry.json) is the catalog entry: the inputs, the outputs and the models.

## Source

The graph of [`motion-ltx-2-3-ic-lora`](../motion-ltx-2-3-ic-lora/README.md), which follows Comfy's template `video_ltx2_3_ic_lora` at commit `59a3b48bf369c5a15f29a1308bae3e279fa15505` of [Comfy-Org/workflow_templates](https://github.com/Comfy-Org/workflow_templates), MIT. The template guides the IC-LoRA with a depth video, as this graph does.

## Checked

Every node class it runs is listed by Comfy Cloud's `GET /api/object_info`, read on 2026-10-28, and `packages/catalog/src/comfy/cloud-weights.json` records each of its three files from that read: the checkpoint under `CheckpointLoaderSimple`, the IC-LoRA under `LoraLoaderModelOnly` and the text encoder under `CLIPLoader`. Its class names, input names and links are the Motion graph's, checked against the node definitions of ComfyUI v0.41.0.
