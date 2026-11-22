# Requirements: effect-recipe-read

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
Qwen3-VL 8B reader ~16-20 GB (estimate, unverified); apply graph LTX-2 24 GB+

## Node types

### workflows/forkfield_read_effect.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewAny | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextGenerate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/forkfield_apply_open_ltx.api.json
| class_type | node pack |
|---|---|
| CFGNorm | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfyMathExpression | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyLTXVLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FluxKontextImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FluxKontextMultiReferenceLatentMethod | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetImageSize | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAddGuide | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConcatAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVCropGuides | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVDualCFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVEmptyLatentAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVPreprocess | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSeparateAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ManualSigmas | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveInt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerEulerAncestral | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeQwenImageEditPlus | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/forkfield_read_effect.api.json
| file | license |
|---|---|
| qwen3vl_8b_int8_convrot.safetensors | Qwen3-VL text encoder: Apache-2.0 (unverified) |

### workflows/forkfield_apply_open_ltx.api.json
| file | license |
|---|---|
| Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.5-audio-vae-bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.5-video-vae-bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_edit_2511_int8_convrot.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
