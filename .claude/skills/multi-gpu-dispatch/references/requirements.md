# Requirements: multi-gpu-dispatch

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
per worker = the routed workflow; raylight splits one model across GPUs (FSDP/xDiT) - see raylight README

## Node types

### workflows/ui/distributed_wan22_14b_t2v.ui.json
| class_type | node pack |
|---|---|
| CLIPLoaderGGUF | https://github.com/city96/ComfyUI-GGUF |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DistributedCollector | https://github.com/robertvoy/ComfyUI-Distributed |
| DistributedSeed | https://github.com/doubletwisted/ComfyUI-Deadline-Plugin (also in 1 other packs; unverified which) |
| EmptyHunyuanLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageBatchDivider | https://github.com/robertvoy/ComfyUI-Distributed |
| KSamplerAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingSD3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UnetLoaderGGUF | https://github.com/city96/ComfyUI-GGUF |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/distributed_upscale_video.ui.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ConditioningZeroOut | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DisplayAny | https://github.com/ComfyAssets/ComfyUI-KikoTools (also in 1 other packs; unverified which) |
| ImageFromBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageResize+ | https://github.com/BetaDoggo/comfyui-image-resize-plus (also in 2 other packs; unverified which) |
| ImageUpscaleWithModel | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingSD3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UltimateSDUpscaleDistributed | https://github.com/robertvoy/ComfyUI-Distributed |
| UpscaleModelLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VHS_LoadVideo | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| VHS_VideoCombine | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| easy imageInterrogator | https://github.com/yolain/ComfyUI-Easy-Use |

### workflows/ui/raylight_ltx23_i2v.ui.json
| class_type | node pack |
|---|---|
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfyMathExpression | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DualCLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyLTXVLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
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
| ManualSigmas | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveBoolean | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveInt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RayCFGGuider | https://github.com/komikndr/raylight (Apache-2.0) |
| RayInitializer | https://github.com/komikndr/raylight (Apache-2.0) |
| RayLoraLoader | https://github.com/komikndr/raylight (Apache-2.0) |
| RayUNETLoader | https://github.com/komikndr/raylight (Apache-2.0) |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResizeImagesByLongerEdge | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| XFuserSamplerCustomAdvanced | https://github.com/komikndr/raylight (Apache-2.0) |
| easy cleanGpuUsed | https://github.com/yolain/ComfyUI-Easy-Use |

### workflows/ui/raylight_wan22.ui.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageResizeKJv2 | https://github.com/kijai/ComfyUI-KJNodes |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RayInitializer | https://github.com/komikndr/raylight (Apache-2.0) |
| RayLoraLoader | https://github.com/komikndr/raylight (Apache-2.0) |
| RayModelSamplingSD3 | https://github.com/komikndr/raylight (Apache-2.0) |
| RayUNETLoader | https://github.com/komikndr/raylight (Apache-2.0) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| WanImageToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| XFuserKSamplerAdvanced | https://github.com/komikndr/raylight (Apache-2.0) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/ui/distributed_wan22_14b_t2v.ui.json
| file | license |
|---|---|
| WAN\Wan21_T2V_14B_lightx2v_cfg_step_distill_lora_rank32.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| Wan2.2-T2V-A14B-LowNoise-Q8_0.gguf | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| umt5-xxl-encoder-Q8_0.gguf | T5: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |

### workflows/ui/distributed_upscale_video.ui.json
| file | license |
|---|---|
| RealESRGAN_x2.pth | UNVERIFIED |
| Wan2.2-Lightning_T2V-v1.1-A14B-4steps-lora_LOW_fp16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| umt5_xxl_fp16.safetensors | T5: Apache-2.0 (unverified) |
| wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |

### workflows/ui/raylight_ltx23_i2v.ui.json
| file | license |
|---|---|
| LTX23_audio_vae_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| LTX23_video_vae_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| gemma_3_12B_it_fp8_e4m3fn.safetensors | Gemma Terms of Use (unverified) |
| ltx-2.3-22b-distilled_transformer_only_fp8_scaled.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.3-spatial-upscaler-x2-1.1.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.3_text_projection_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| tx_2.3_22b_distilled_1.1_lora_dynamic_fro09_avg_rank_111_bf16.safetensors | UNVERIFIED |

### workflows/ui/raylight_wan22.ui.json
| file | license |
|---|---|
| Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| Wan_2_2_I2V_A14B_HIGH_lightx2v_4step_lora_v1030_rank_64_bf16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| lightx2v_I2V_14B_480p_cfg_step_distill_rank128_bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
