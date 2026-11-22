# Requirements: restyle

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
24 GB+ (estimate, unverified)

## Node types

### workflows/ltx_ic_lora_depth_restyle.api.json
| class_type | node pack |
|---|---|
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CFGNorm | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DepthAnythingV2Preprocessor | https://github.com/Fannovel16/comfyui_controlnet_aux |
| EmptyLTXVLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetICLoRAParameters | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageFromBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAddGuide | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConcatAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVCropGuides | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVEmptyLatentAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVImgToVideoInplace | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSeparateAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ManualSigmas | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeQwenImageEditPlus | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VHS_LoadVideo | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |

### workflows/ltx25_motion_guide.api.json
| class_type | node pack |
|---|---|
| AudioAmplify | UNVERIFIED (not in ComfyUI core or ComfyUI-Manager extension-node-map; probably custom nodes from rossaai/rosesfield) |
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfyMathExpression | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyLTXVLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetICLoRAParameters | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetImageSize | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GrowMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageBlur | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageFromBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageToMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| InvertMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAddGuide | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConcatAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVCropGuides | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVEmptyLatentAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVImgToVideoInplace | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVLatentUpsampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVPreprocess | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSeparateAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LatentUpscaleModelLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ManualSigmas | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MaskComposite | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MaskToImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| NormalizeAudioLoudness | https://github.com/kijai/ComfyUI-WanVideoWrapper (also in 1 other packs; unverified which) |
| PrimitiveInt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RepeatImageBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SolidMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| StringConcatenate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Video Slice | https://github.com/comfyanonymous/ComfyUI |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/ltx_ic_lora_depth_restyle.api.json
| file | license |
|---|---|
| Qwen-Image-Edit-2509-Lightning-8steps-V1.0-bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| depth_anything_v2_vits.pth | Depth Anything: license varies by size (V2-Small Apache-2.0; larger V2/V3 checkpoints CC-BY-NC-4.0) - UNVERIFIED for this file |
| gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.5-audio-vae-bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.5-video-vae-bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_edit_2509_fp8_e4m3fn.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |

### workflows/ltx25_motion_guide.api.json
| file | license |
|---|---|
| gemma4-12b-with-proj-ltx-2.5-bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.5-22b-distilled-transformer-bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.5-audio-vae-bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.5-video-vae-bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
