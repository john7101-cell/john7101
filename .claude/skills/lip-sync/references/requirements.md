# Requirements: lip-sync

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
unverified for LTX graphs (24 GB+ est.); lip-service Wan2.1 GGUF + block swap is the lower-VRAM path (figure unverified)

## Node types

### workflows/ltx23_lipsync_photo.api.json
| class_type | node pack |
|---|---|
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyLTXVLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXAVTextEncoderLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConcatAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVCropGuides | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVImgToVideoInplace | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVLatentUpsampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVPreprocess | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSeparateAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LatentUpscaleModelLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ManualSigmas | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SetLatentNoiseMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SolidMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| StringConcatenate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TrimAudioDuration | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ltx23_ic_lora_lipdub_video.api.json
| class_type | node pack |
|---|---|
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyLTXVLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXAVTextEncoderLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXAddVideoICLoRAGuide | https://github.com/Lightricks/ComfyUI-LTXVideo |
| LTXICLoRALoaderModelOnly | https://github.com/Lightricks/ComfyUI-LTXVideo |
| LTXVAudioVAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConcatAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVCropGuides | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVEmptyLatentAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVLatentUpsampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSeparateAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSetAudioRefTokens | https://github.com/Lightricks/ComfyUI-LTXVideo |
| LatentUpscaleModelLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ManualSigmas | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/wan21_infinitetalk_single.api.json
| class_type | node pack |
|---|---|
| CLIPVisionLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MultiTalkModelLoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| MultiTalkWav2VecEmbeds | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| VHS_VideoCombine | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| WanVideoBlockSwap | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoClipVisionEncode | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoImageToVideoMultiTalk | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoLoraSelect | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoModelLoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoPassImagesFromSamples | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoSampler | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoTextEncodeCached | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoVAELoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| Wav2VecModelLoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (also in 1 other packs; unverified which) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/ltx23_lipsync_photo.api.json
| file | license |
|---|---|
| gemma_3_12B_it_fp4_mixed.safetensors | Gemma Terms of Use (unverified) |
| ltx-2.3-22b-dev-fp8.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.3-spatial-upscaler-x2-1.1.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx_2.3_22b_distilled_1.1_lora_dynamic_fro09_avg_rank_111_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |

### workflows/ltx23_ic_lora_lipdub_video.api.json
| file | license |
|---|---|
| gemma_3_12B_it_fp4_mixed.safetensors | Gemma Terms of Use (unverified) |
| ltx-2.3-22b-dev-fp8.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.3-22b-ic-lora-lipdub-0.9.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.3-spatial-upscaler-x2-1.1.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx_2.3_22b_distilled_1.1_lora_dynamic_fro09_avg_rank_111_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |

### workflows/wan21_infinitetalk_single.api.json
| file | license |
|---|---|
| Wan2_1_VAE_bf16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| WanVideo\InfiniteTalk\Wan2_1-InfiniteTalk_Single_Q8.gguf | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| WanVideo\Lightx2v\lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| WanVideo\wan2.1-i2v-14b-480p-Q4_K_M.gguf | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| clip_vision_h.safetensors | UNVERIFIED |
| umt5-xxl-enc-bf16.safetensors | T5: Apache-2.0 (unverified) |
| wav2vec2-chinese-base_fp16.safetensors | wav2vec2 (chinese-base): Apache-2.0 (unverified) |
