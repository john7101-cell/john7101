<!-- Copied from rossaai/rosesfield workflows/effects-ltx-2-5/README.md (MIT); vendor frontmatter removed. Rows naming closed/hosted models do not apply: use open-weights options only. -->

# Effects: one photo to a short effect video on LTX 2.5

Scales and centre-crops your photo to the chosen shape and makes the effect's last frame from it with Qwen Image Edit 2511, then renders the video between the two on LTX 2.5, with its sound, at the pixel area of the shape. LTX 2.5 is the only video model. This file holds every part a recipe can use, including the subject held through its matte. Each recipe in the catalog removes the parts it does not use.

| | |
|---|---|
| Workflow id | `effects-ltx-2-5` |
| Run by | [`effects`](../../packages/catalog/src/effects/) |
| Core model | LTX 2.5 22B distilled |
| Image model | Qwen Image Edit 2511, for the last frame |
| Custom node packs | two, for the sound only. [ComfyUI-WanVideoWrapper](https://github.com/kijai/ComfyUI-WanVideoWrapper) at commit `088128b224242e110d3906c6750e9a3a348a659b`, Apache-2.0, gives `NormalizeAudioLoudness`. [ComfyUI_AudioTools](https://github.com/lum3on/ComfyUI_AudioTools) at commit `c816d0a1629c05a0f463ddb77ea96ada69875d32`, MIT, gives `AudioAmplify`, `AudioFadeOut`, `AudioFadeIn` and `AudioParametricEQ`. Comfy Cloud lists both in its `object_info`. Every other node is a ComfyUI core node, and a silent look sends no pack node |
| Adapters | none. Comfy Cloud holds no LTX 2.5 adapter, so no recipe loads one |
| GPU memory | LTX's system requirements name at least 32 GB of VRAM for LTX 2.5, on [docs.ltx.io](https://docs.ltx.io/open-source-model/getting-started/system-requirements). The bf16 transformer file alone is 42.0 GB. |

## Inputs

The catalog binds these names in [`entry.json`](entry.json). The UI file lists the value inputs for App Mode.

| Input | Node | Field | Takes |
|---|---|---|---|
| `photo` | 395 `LoadImage`, Photo | `image` | an uploaded image |
| `detail` | 501 `StringConcatenate`, Prompt and detail | `string_b` | a value |
| `seed` | 339 `RandomNoise`, Seed | `noise_seed` | a value |
| `width` | 356 `EmptyLTXVLatentVideo`, Size and length | `width` | a value |
| `height` | 356 `EmptyLTXVLatentVideo`, Size and length | `height` | a value |
| `fitWidth` | 606 `ImageScale`, Fitted photo | `width` | a value |
| `fitHeight` | 606 `ImageScale`, Fitted photo | `height` | a value |
| `endFrameSeed` | 626 `KSampler`, End frame | `seed` | a value, bound when the image edit pass runs |
| `deliveryWidth` | 380 `ImageScale`, Delivery size | `width` | a value |
| `deliveryHeight` | 380 `ImageScale`, Delivery size | `height` | a value |
| `grainSeed` | 381 `ImageAddNoise`, Grain | `seed` | a value, the run's seed |
| `hitSeed1` to `hitSeed6` | 662, 672, 682, 692, 702 and 712 `KSampler`, Hit 1 to Hit 6 | `seed` | a value, the run's seed, each bound when the look has that hit |

The recipe sets the rest: the prompt on node 501, the sound line on node 503, the length on nodes 356 and 366, the edit prompt on node 620, the mid frame's place on nodes 472 and 473, the strengths on nodes 460, 461, 463, 464, 472 and 473, the grain's strength on node 381, and each hit's prompt, length, gain and time on the prompt, length, gain and lead nodes of its slot, per §The hits, the build, the brighten and the fade.

## Outputs

| Node | Key | Kind |
|---|---|---|
| 75 `SaveVideo` | `images` | video, H.264 in MP4 |

## Models

Rosesfield ships no weights. Each file goes into the model folder its row names.

| File | Model | Licence | Folder | Download |
|---|---|---|---|---|
| `ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors` | LTX 2.5 latent upscaler, 2 times | [LTX-2.x Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x) | `models/latent_upscale_models` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.5/resolve/main/latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors) |
| `ltx-2.5-22b-distilled-transformer-bf16.safetensors` | LTX 2.5 22B distilled, bf16, 42.0 GB | [LTX-2.x Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x) | `models/diffusion_models` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.5/resolve/main/diffusion_models/ltx-2.5-22b-distilled-transformer-bf16.safetensors) |
| `ltx-2.5-video-vae-bf16.safetensors` | LTX 2.5 video VAE | [LTX-2.x Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x) | `models/vae` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.5/resolve/main/vae/ltx-2.5-video-vae-bf16.safetensors) |
| `ltx-2.5-audio-vae-bf16.safetensors` | LTX 2.5 audio VAE | [LTX-2.x Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x) | `models/vae` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.5/resolve/main/vae/ltx-2.5-audio-vae-bf16.safetensors) |
| `gemma4-12b-with-proj-ltx-2.5-bf16.safetensors` | Gemma 4 12B text encoder with the LTX 2.5 projections, bf16, 26.3 GB | [the licence of the LTX 2.5 repository it sits in](https://huggingface.co/Lightricks/LTX-2.5) | `models/text_encoders` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.5/resolve/main/text_encoders/gemma4-12b-with-proj-ltx-2.5-bf16.safetensors) |
| `birefnet.safetensors` | BiRefNet, by ZhengPeng7 | [MIT](https://huggingface.co/ZhengPeng7/BiRefNet) | `models/background_removal` | [Hugging Face](https://huggingface.co/Comfy-Org/BiRefNet/resolve/main/background_removal/birefnet.safetensors) |
| `qwen_image_edit_2511_bf16.safetensors` | Qwen Image Edit 2511, bf16, for the last frame | [Apache-2.0](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) | `models/diffusion_models` | [Hugging Face](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_edit_2511_bf16.safetensors) |
| `qwen_2.5_vl_7b_fp8_scaled.safetensors` | Qwen2.5-VL 7B text encoder, fp8 | [Apache-2.0](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct) | `models/text_encoders` | [Hugging Face](https://huggingface.co/Comfy-Org/HunyuanVideo_1.5_repackaged/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors) |
| `qwen_image_vae.safetensors` | Qwen Image VAE | [Apache-2.0](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI) | `models/vae` | [Hugging Face](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors) |
| `stable_audio_3_medium.safetensors` | Stable Audio 3 Medium, by Stability AI, for the hit | [Stability AI Community License](https://stability.ai/community-license-agreement) | `models/checkpoints` | [Hugging Face](https://huggingface.co/Comfy-Org/stable-audio-3/resolve/main/checkpoints/stable_audio_3_medium.safetensors) |
| `t5gemma_b_b_ul2.safetensors` | T5Gemma text encoder of Stable Audio 3 | [Stability AI Community License](https://stability.ai/community-license-agreement) | `models/text_encoders` | [Hugging Face](https://huggingface.co/Comfy-Org/stable-audio-3/resolve/main/text_encoders/t5gemma_b_b_ul2.safetensors) |

Only a look with a hit loads the two Stable Audio 3 files. The Community License grants use below 1,000,000 USD of annual revenue.

Lightricks' LTX 2.5 files are gated on Hugging Face, so their SHA256 digests are not in the UI file. Accept the LTX 2.5 licence on Hugging Face before you download them.

Effects loads the bf16 transformer and the bf16 text encoder, as `motion-guide-ltx-2-5`, `video-ltx-2-5-text` and `video-ltx-2-5-start-frame` do. On Push into eye, the bf16 files give a photo-real iris, natural skin and the person's own eye colour, where the int8 files of the same repository give an iris that reads as drawn and skin like cracked clay. The bf16 files take more GPU time per run. Both files sit in the same Hugging Face repository under the same LTX-2.x Community License as the int8 files.

## The effects

Each effect is a recipe kept as data in [`packages/catalog/src/effects/recipes/`](../../packages/catalog/src/effects/recipes/). A recipe holds its prompt, where the photo sits, its end-frame prompt and strength, its mid frame if it has one, its hold strength, its adapter, which is always none, and its fixed length of 5 to 15 seconds. Its design holds the unit and the family of the reference reading it is designed from, the set piece, the cut windows, the last frame, the sound bed with its loudness band and true peak, and the encode with its grain.

A recipe passes only with the proof of one run: a gate run of the look's criteria list that held its reference outputs and refused one planted output, a judge that wrote none of its inputs and held the run against every criterion that applies, a reading of the file inside the recipe's length, pixel area, cut windows, loudness band and last frame, with a first frame whose mean luma sits above the black floor of 17.5, so a run that starts black does not pass, and the row of that run in the run ledger, [`runs.json`](../../packages/catalog/src/effects/runs.json), with the same effect, graph, seed, resolution and shape and the verdict kept. Each row of that ledger holds its effect, the hash of its graph, the hash of its photo, its seed, resolution and shape, the balance before and after it, and the judge's verdict with the criteria it failed. The catalog refuses a row that starts or ends under 2,000 credits, and a passed recipe that lacks any of these.

A recipe is an example of the Motion app. A recipe also carries a maintainer's approval or none, and an example keeps a result only when it passed or a maintainer approved it. Motion offers the approved recipes. An owner on the local lock can also try the rest, per `packages/catalog/src/motion/examples/offered-examples.ts`.

| End-frame source | What the graph does |
|---|---|
| `none` | no end frame. The video runs on the prompt and the frame 0 lock |
| `edit` | Qwen Image Edit 2511 edits the fitted photo into the effect's last frame |
| `dark` | node 628, an `EmptyImage` at the fitted photo's size in the recipe's grey, `luma` 0 to 40 on the 8-bit scale, guides the last frame at the recipe's strength, so the clip ends on a designed dark frame. No image edit node runs. A look whose photo frame is `last` takes no `dark` end frame |

A recipe can also hold one mid frame: a frame inside the clip, made by the image edit pass from the fitted photo with the recipe's edit prompt, and guided at the recipe's time and strength. The graph has one image edit pass, so a recipe with a mid frame takes a `dark` end frame or none, never an `edit` one.

| Photo frame | What the graph does |
|---|---|
| `first` | the fitted photo is locked at frame 0, and the edited frame guides the last frame |
| `last` | the edited frame is locked at frame 0, and the fitted photo guides the last frame, so the clip lands on the photo. Earth Zoom, the recipe `pull-back-to-space`, opens in orbit and lands on the person, as its reference does. Such a recipe has an edited frame and holds no subject |

## What every run does

1. It scales your photo and crops its centre to the LTX size of the chosen shape at the chosen resolution, node 606, such as 1280 by 720 at 16:9 and 704 by 1280 at 9:16 for 720p, and 1920 by 1088 at 16:9 and 1088 by 1920 at 9:16 for 1080p. No model touches the photo, so frame 0 keeps your pixels. The Effects screen picks the shape nearest your photo's own ratio.
2. It makes the effect's edited frame from the fitted photo with Qwen Image Edit 2511, nodes 600 to 604 and 620 to 627, at the fitted size, when the recipe has one: its last frame or its mid frame.
3. It locks the fitted photo at frame 0 with `LTXVImgToVideoInplace`, or the edited frame when the recipe lands on the photo: at strength 0.7 in the first stage, node 357, and at 1.0 in the second, node 349.
4. It makes a matte of the subject with the core BiRefNet nodes `LoadBackgroundRemovalModel` and `RemoveBackground`, nodes 410 to 412, when the recipe holds the subject.
5. It renders the shot in two stages. A mid frame is an `LTXVAddGuide` guide at its frame, nodes 472 and 473, read from the edited frame resized and preprocessed as frame 0 is, nodes 470 and 471. The last frame is an `LTXVAddGuide` guide at the last frame, nodes 460 and 463, chained after the mid-frame guides. The photo is a second guide at the last frame with the subject matte as its `attention_mask`, nodes 461 and 464, so the subject holds while the scene changes. `LTXVCropGuides` removes the guide frames after each stage, nodes 462 and 465.
6. It decodes the sound with node 358 when the recipe has a sound bed. Node 359 sets its integrated loudness to the middle of the look's band. Nodes 360 and 361 then raise it by the ceiling's distance from 0 dBFS, where `AudioAmplify` clips every sample to full scale, and lower it back, so no sample passes the ceiling, 1 dB under the look's true peak, and quieter samples keep their level. `AudioNormalize` was not used: it moves the sample peak to its target in both directions, so it would undo the loudness of node 359. The ceiling acts only on a sound whose peaks sit higher above its loudness than the band leaves room for. A silent look removes nodes 358 to 361.
7. It levels, lowers, builds and brightens the sound, nodes 648 to 653, and adds the look's hits to it, nodes 630, 631, 633 and 660 to 719, when the look has them, before node 359 sets the loudness, per §The hits, the build, the brighten and the fade. It ends the sound in a fade to silence, node 362, when the look has one.
8. It scales the frames to the pixel area of the chosen resolution in the chosen shape, centre-cropped, node 380, such as 1280 by 720 at 16:9 and 832 by 1110 at 3:4 for 720p, and 1920 by 1080 at 16:9 and 1248 by 1664 at 3:4 for 1080p.
9. It adds faint noise to every frame with the core `ImageAddNoise`, node 381, seeded from the run's seed, at the grain of the recipe's encode. Then it saves H.264 in MP4 at 24 frames a second, nodes 370 and 75.

## How a recipe changes this file

The catalog's [`effect-graph.ts`](../../packages/catalog/src/effects/comfy/effect-graph.ts) derives each recipe's graph from this file:

- It writes the recipe's prompt on node 501, its sound line on node 503 and its length on nodes 356 and 366. Node 356 takes the video's frames, `seconds * 24 + 1`. Node 366 takes one frame more. The core audio VAE makes `round(frames / 24 * 25)` latents and decodes `4 * latents - 3` mel frames at 100 a second, so 169 frames decode to 7.010 s of sound against 7.042 s of video. One frame more makes the sound at least as long as the video for every length from 5 to 15 seconds, and node 75, `SaveVideo`, cuts the sound to the video's length when it writes the file.
- A recipe whose photo frame is `last` reads the edited frame, node 627, in the frame 0 locks 357 and 349, and the fitted photo, node 606, in the last-frame guides 460 and 463.
- A `dark` end frame links node 628 in grey `luma * 0x010101` to the guides 460 and 463. Any other end frame removes node 628.
- The image edit nodes 600 to 604, 620 to 623 and 625 to 627 run when the recipe has an `edit` end frame or a mid frame, and node 620 takes that frame's prompt. Otherwise they are removed, and the size node 624 is removed too unless node 628 reads it.
- A mid frame sets `frame_idx` and the strength of the guides 472 and 473. `frame_idx` is its time at 24 frames a second, rounded to a whole frame, such as frame 132 at 5.5 s. For a guide of one image, `LTXVAddGuide` takes any frame from -9999 to 9999 and places the image at that pixel frame. It rounds a frame only for a guide of more than 8 frames, read in `comfy_extras/nodes_lt.py` of ComfyUI v0.41.0. An effect with no mid frame removes the nodes 470 to 473 and links the end-frame guides to what the mid-frame guides read.
- An effect with no end frame removes the guides 460 and 463, and links the next node to what the guide read.
- An effect with no hold removes the guides 461 and 464 and the matte nodes 410 to 412.
- An effect with no end frame, no mid frame and no hold removes the crop nodes 462 and 465.
- A sounding effect writes the middle of its loudness band on node 359, and its peak ceiling, `truePeakMax` minus 1 dB, as the gain of nodes 360 and 361.
- A silent effect removes the audio decode and the loudness nodes, 358 to 361.
- An effect removes each hit slot it does not use. An effect with no hit also removes the shared nodes 630, 631 and 633, so it loads no Stable Audio 3 file. Node 359 reads the last hit's merge, or the bed when the effect has no hit.
- An effect with a bed gain, a build or a brighten adds node 649, nodes 650 to 652 or node 653 on the bed before the first hit joins.
- An effect with a fade adds node 362, `AudioFadeOut`, after node 361, and node 370 reads it.
- It writes the grain of the recipe's encode as the strength of node 381. The grain is 0 to 0.02 and 0.004 when the recipe names none. `ImageAddNoise` returns `clip(image + strength * randn, 0, 1)` with a separate draw for every pixel of every frame, read in `comfy_extras/nodes_images.py` of ComfyUI v0.41.0. At 0.004 the noise is about one level on the 8-bit scale, which a lit frame does not show. On a black frame, the clip keeps only the positive half, so the mean rises by `strength * 255 / sqrt(2 * pi)`, about 0.4 levels, far under the black floor of 17.5. The grain exists so a clip that ends on black does not repeat one frame: without it, the frames after the clip reaches pure black are byte-identical, and a reference's black tail carries faint noise. The node's schema steps its strength by 0.01 in the canvas, and the catalog sets the exact value in the API graph.
- A recipe with an adapter adds node 420, a `LoraLoaderModelOnly` between the model and both guiders. No recipe has one.

## The hits, the build, the brighten and the fade

A look's sound bed can hold up to six hits: designed sounds, such as a whoosh or a heavy boom, each at a set time. LTX 2.5 makes the sound of the whole clip from one prompt, and it does not place a single sound at an exact moment. So a separate model makes each hit, and the graph places it.

The six hits share the Stable Audio 3 loader, node 630, its text encoder, node 631, and the empty negative prompt, node 633. Each hit has a slot of nine nodes. The slots start at 660, 670, 680, 690, 700 and 710, and each node sits at the same step from its slot's start:

| Step | Node | What it does |
|---|---|---|
| +0 | `CLIPTextEncode` | the hit's prompt |
| +1 | `EmptyLatentAudio` | the hit's length, 0.5 to 5 seconds |
| +2 | `KSampler` | the values of `workflows/audio-sound-stable-audio-3`: 8 steps, CFG 1, `lcm`, `simple`. Its seed is the run's seed |
| +3 | `VAEDecodeAudio` | decodes the hit |
| +9 | `NormalizeAudioLoudness` | levels the hit to -20 LUFS, added at run time |
| +4 | `AudioAdjustVolume` | the hit's gain, a whole number of dB from -24 to 12 |
| +8 | `AudioFadeOut` | fades the last 0.3 s of the hit, so it does not end in a click |
| +5 | `EmptyAudio` | silence as long as the hit's time |
| +6 | `AudioConcat` | puts the hit after the silence, so the hit starts at its time |
| +7 | `AudioMerge` | adds the placed hit to the mix before it |

Before the mix, every layer is levelled to the same loudness, -20 LUFS, by `NormalizeAudioLoudness`. Each hit's level node sits at the slot's step +9, nodes 669, 679, 689, 699, 709 and 719, between its decode and its gain. The LTX sound is levelled by node 648 before the bed gain, the build and the brighten, and only when the look has a hit. A layer's raw level changes from run to run, so the hit's gain and the bed gain are offsets from -20 LUFS, not from that raw level.

A hit at 0 s removes its silence and its `AudioConcat`, and its merge reads the faded hit. The hits merge in the order the recipe lists them: the first onto the bed, each next one onto the mix before it. Node 359 reads the last merge, so the loudness and the peak ceiling act on the whole mix.

A look's sound bed can also hold a bed gain, a build and a brighten, all added to the bed before the first hit joins, in that order:

- The bed gain lowers the LTX sound, so the hits sit above it. Node 649, `AudioAdjustVolume`, reads node 358 at the bed gain, a whole number of dB from -24 to 0. A bed gain of 0 adds no node.
- The build makes the bed rise from a floor. Node 650, `AudioAdjustVolume`, is the bed at the floor's gain, a whole number of dB from -30 to 0. Node 651, `AudioFadeIn` from ComfyUI_AudioTools, fades the bed in over the build's length, 0.5 to 7 seconds in steps of 0.1. Node 652, `AudioMerge`, adds the two, so the bed starts at its floor and reaches full level at the end of the build.
- The brighten, node 653, `AudioParametricEQ` from ComfyUI_AudioTools, cuts under 20 Hz and boosts the presence and air bands, each 0 to 12 dB in steps of 0.5.

A look's sound bed can also end in a fade to silence, 0 to 2 seconds in steps of 0.1. Node 362, `AudioFadeOut`, fades the last seconds of the sound after the peak ceiling, so the clip is silent by its last frame. A fade of 0 adds no node.

Push into eye uses hits, a build, a brighten and a fade.

## Resolutions and the wait

Effects renders at 480p, 720p and 1080p. At 1080p the LTX size is 1920 by 1088 at 16:9, and the delivery size is 1920 by 1080. Motion waits up to 1,800 s for a run, per `limits` in `packages/catalog/src/motion/app.ts`.

The UI file holds a muted `MaskPreview` on the matte and a muted `PreviewImage` on the end frame, so you can turn them on.

## Use restrictions

The LTX-2.x Community License asks Rosesfield to pass its use restrictions to you. They include a statement that the output is machine generated and a ban on deepfakes made without consent. The licence is free for an entity under 10,000,000 USD of annual revenue and needs a paid agreement above that. Read it at [LICENSE-2_x](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x).

## Files

- [`effects-ltx-2-5.api.json`](effects-ltx-2-5.api.json) is the graph every engine runs, in ComfyUI's API format. The catalog imports it.
- [`effects-ltx-2-5.json`](effects-ltx-2-5.json) is the same graph in ComfyUI's UI format, with positions, groups and one note. Each loader lists its file with a download link. A script writes it from the API file.
- [`entry.json`](entry.json) is the catalog entry: the inputs, the outputs and the models.

## Source

Written for Rosesfield from ComfyUI core nodes and the two sound packs. Its two-stage render starts from Comfy's template `video_ltx2_5_i2v` and keeps its node ids, and its end-frame pass starts from the wiring of Comfy's template `image_qwen_image_edit_2511`, both in [Comfy-Org/workflow_templates](https://github.com/Comfy-Org/workflow_templates), MIT. Rosesfield adds the scale to the shape, the end-frame and hold guides, the crop guides, the recipe's length and sound, and the scale to the delivery size. Lightricks' own example workflows carry the LTX-2 Community License and were not used.

## Checked

Every node class this file holds comes from ComfyUI's `nodes` or `comfy_extras` modules, except the sound nodes 359 to 361, whose inputs were read from both packs' source at the pinned commits and from Comfy Cloud's `object_info`, and the fade node 362, `AudioFadeOut`, which Comfy Cloud lists in its `object_info`. The hits' core audio nodes were read from `comfy_extras/nodes_audio.py` of ComfyUI v0.41.0. `AudioFadeIn` and `AudioParametricEQ` were read from the source of ComfyUI_AudioTools at commit `c816d0a`, and its Stable Audio 3 nodes are the ones `workflows/audio-sound-stable-audio-3` runs. The LTX 2.5 and BiRefNet nodes and files were listed by Comfy Cloud's `object_info` and model folders on 2026-10-19, and the Qwen Image Edit 2511 nodes are the ones the workflow `edit-qwen-image-edit-2511` runs. The grain node 381, `ImageAddNoise`, was read from `comfy_extras/nodes_images.py` of ComfyUI v0.41.0, not from Comfy Cloud's `object_info`. Node 75 sets no constant-quality value of its own, so the file is the core `SaveVideo` node's H.264 encode. The run ledger, `packages/catalog/src/effects/runs.json`, holds the runs that prove it. LTX 2.5 can return a run whose first frames decode to black, and the first-frame reading of §The effects refuses such a run for a recipe.
