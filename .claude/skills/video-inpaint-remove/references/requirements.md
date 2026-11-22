# Requirements: video-inpaint-remove

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
Wan VACE / LTX-2.3: 24 GB+ (estimate, unverified)

## Node types

### workflows/wan_vace_inpaint_remove.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageCompositeMasked | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| InvertMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MaskToImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingSD3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| OpenFrameSaveVideo | bundled: assets/openframe-nodes (satianurag/openframe, MIT) |
| OpenFrameVideoInput | bundled: assets/openframe-nodes (satianurag/openframe, MIT) |
| TrimVideoLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| WanVaceToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ltx23_inpaint_remove.api.json
| class_type | node pack |
|---|---|
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyLTXVLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageCompositeMasked | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageCrop | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageToMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXAVTextEncoderLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXAddVideoICLoRAGuideAdvanced | https://github.com/Lightricks/ComfyUI-LTXVideo |
| LTXICLoRALoaderModelOnly | https://github.com/Lightricks/ComfyUI-LTXVideo |
| LTXVAudioVAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConcatAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVCropGuides | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVEmptyLatentAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVLaplacianPyramidBlend | https://github.com/Lightricks/ComfyUI-LTXVideo |
| LTXVSeparateAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSetAudioRefTokens | https://github.com/Lightricks/ComfyUI-LTXVideo |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ManualSigmas | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MaskToImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| OpenFrameGreenFill | bundled: assets/openframe-nodes (satianurag/openframe, MIT) |
| OpenFramePadForRefinement | bundled: assets/openframe-nodes (satianurag/openframe, MIT) |
| OpenFrameSaveVideo | bundled: assets/openframe-nodes (satianurag/openframe, MIT) |
| OpenFrameVideoInput | bundled: assets/openframe-nodes (satianurag/openframe, MIT) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/wan_vace_inpaint_remove.api.json
| file | license |
|---|---|
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan2.1_vace_1.3B_fp16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |

### workflows/ltx23_inpaint_remove.api.json
| file | license |
|---|---|
| gemma_3_12B_it_fp8_scaled.safetensors | Gemma Terms of Use (unverified) |
| ltx-2.3-22b-dev.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.3-22b-distilled-lora-384-1.1.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.3-22b-ic-lora-in-outpainting-0.9.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
