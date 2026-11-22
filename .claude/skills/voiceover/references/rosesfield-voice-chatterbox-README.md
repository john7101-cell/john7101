<!-- Copied from rossaai/rosesfield workflows/voice-chatterbox/README.md (MIT); vendor frontmatter removed. Rows naming closed/hosted models do not apply: use open-weights options only. -->

# Speech: 23 languages with Chatterbox

Reads your script aloud in one of 23 languages. With a recording, it speaks in the voice of that recording. Without one, the voice node runs with no audio_prompt and uses the model's own voice. Built from Comfy's template audio-chatterbox_tts_multilingual.

| | |
|---|---|
| Workflow id | `voice-chatterbox` |
| Run by | [`audio`](../../packages/catalog/src/audio/), Speech and Voice clone |
| Core model | Chatterbox Multilingual |
| Custom node packs | [ComfyUI_Fill-ChatterBox](https://github.com/filliptm/ComfyUI_Fill-ChatterBox) at commit `f7d7a16187430abcaf91a3039b9c83aa9960816a`, MIT, per its README |
| GPU memory | The node pack's README recommends an NVIDIA GPU with 8 GB of VRAM or more, and runs on a CPU or a Mac too. The model files it loads add up to 3.2 GB. |

## Inputs

The catalog binds these names in [`entry.json`](entry.json). The UI file lists the value inputs for App Mode.

| Input | Node | Field | Takes |
|---|---|---|---|
| `script` | 1 `FL_ChatterboxMultilingualTTS`, Speech | `text` | a value |
| `language` | 1 `FL_ChatterboxMultilingualTTS`, Speech | `language` | a value |
| `expression` | 1 `FL_ChatterboxMultilingualTTS`, Speech | `exaggeration` | a value |
| `seed` | 1 `FL_ChatterboxMultilingualTTS`, Speech | `seed` | a value |
| `voice` | 2 `LoadAudio`, Voice to clone | `audio` | an uploaded audio |
| `length` | 5 `TrimAudioDuration`, Speech at the script's length | `duration` | a value |

## Outputs

| Node | Key | Kind |
|---|---|---|
| 3 `SaveAudioMP3` | `audio` | audio |

## Models

Rosesfield ships no weights. Each file goes into the model folder its row names.

| File | Model | Licence | Folder | Download |
|---|---|---|---|---|
| `t3_mtl23ls_v2.safetensors` | Chatterbox Multilingual, by Resemble AI | [MIT](https://huggingface.co/ResembleAI/chatterbox) | `models/chatterbox/chatterbox_multilingual` | [Hugging Face](https://huggingface.co/ResembleAI/chatterbox/resolve/5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18/t3_mtl23ls_v2.safetensors) |
| `s3gen.pt` | Chatterbox Multilingual, by Resemble AI | [MIT](https://huggingface.co/ResembleAI/chatterbox) | `models/chatterbox/chatterbox_multilingual` | [Hugging Face](https://huggingface.co/ResembleAI/chatterbox/resolve/5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18/s3gen.pt) |
| `ve.pt` | Chatterbox Multilingual, by Resemble AI | [MIT](https://huggingface.co/ResembleAI/chatterbox) | `models/chatterbox/chatterbox_multilingual` | [Hugging Face](https://huggingface.co/ResembleAI/chatterbox/resolve/5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18/ve.pt) |
| `conds.pt` | Chatterbox Multilingual, by Resemble AI | [MIT](https://huggingface.co/ResembleAI/chatterbox) | `models/chatterbox/chatterbox_multilingual` | [Hugging Face](https://huggingface.co/ResembleAI/chatterbox/resolve/5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18/conds.pt) |

## Two forms

- With a recording, node 2 loads it and node 1 clones its voice through `audio_prompt`. The pack's README asks for a recording of at least 5 to 6 seconds.
- Without one, the catalog removes node 2 and the `audio_prompt` link, and the model reads your script in its own voice.

The pack also holds `FL_ChatterboxTTS` for English and `FL_ChatterboxTurboTTS` for English with tags such as `[laugh]`. This workflow does not use them. The Turbo weights come from `ResembleAI/chatterbox-turbo` at revision `749d1c1a46eb10492095d68fbcf55691ccf137cd`.

The pack downloads any missing weight file into `models/chatterbox/chatterbox_multilingual/` on its first run. It also reads `grapheme_mtl_merged_expanded_v1.json` and `Cangjie5_TC.json` from the same revision, which Hugging Face stores without a digest. Each run makes about 40 seconds of speech at most, per the pack's README. The speech node takes no length input, so a short script can come back with up to 40 seconds of speech. The core node `TrimAudioDuration` keeps the first part of the speech, up to 2 seconds plus a length per character of the script: 0.3 seconds for Chinese and Japanese, 0.2 for Korean and 0.12 for every other language, never more than 40 seconds. The catalog writes that length into node 5 for each run. With `resemble-perth` installed, every output carries Resemble's hidden watermark.

Never use the other speech pack on Comfy Cloud, `ComfyUI-Qwen-TTS` by mailzwj. It calls Alibaba's DashScope API with a key, a closed API.

## Files

- [`voice-chatterbox.api.json`](voice-chatterbox.api.json) is the graph every engine runs, in ComfyUI's API format. The catalog imports it.
- [`voice-chatterbox.json`](voice-chatterbox.json) is the same graph in ComfyUI's UI format, with positions, groups and one note. The voice node has no model loader, so ComfyUI shows no download button. The note lists the weight files. A script writes it from the API file with the node definitions of ComfyUI v0.41.0.
- [`entry.json`](entry.json) is the catalog entry: the inputs, the outputs and the models.

## Source

Its nodes follow Comfy's template `audio-chatterbox_tts_multilingual` in [Comfy-Org/workflow_templates](https://github.com/Comfy-Org/workflow_templates), MIT, read on 2026-10-17.

## Checked

Its class names, input names, required inputs, link types and fixed values were checked against the node definitions of ComfyUI v0.41.0 and the pinned node pack, read from source.
