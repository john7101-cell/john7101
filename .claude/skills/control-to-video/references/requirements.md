# Requirements: control-to-video

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
Wan VACE 14B / LTX-2: 24 GB+ (estimate, unverified); Wan 2.2 14B Fun Control fp8 ~24 GB+ (unverified)

## Node types

### workflows/wan_vace_pose_control.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageFromBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| OF_DWPose | bundled: assets/motionfield_nodes (jalajbhandula/motionfield, MIT; dwpose_onnx Apache-2.0) |
| OF_PlateAudio | bundled: assets/motionfield_nodes (jalajbhandula/motionfield, MIT; dwpose_onnx Apache-2.0) |
| TrimVideoLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VHS_LoadVideo | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| VHS_VideoCombine | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| WanVaceToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/wan_vace_canny_control.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Canny | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageFromBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| OF_PlateAudio | bundled: assets/motionfield_nodes (jalajbhandula/motionfield, MIT; dwpose_onnx Apache-2.0) |
| TrimVideoLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VHS_LoadVideo | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| VHS_VideoCombine | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| WanVaceToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/ltx2_depth_to_video.ui.json
| class_type | node pack |
|---|---|
| BasicGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| BasicScheduler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ConditioningZeroOut | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DisableNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyLTXVLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetImageSize | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageFromBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageInvert | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleBy | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXAVTextEncoderLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAddGuide | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConcatAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVCropGuides | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVEmptyLatentAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVImgToVideoInplace | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVLatentUpsampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVScheduler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSeparateAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LatentUpscaleModelLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LotusConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ManualSigmas | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveBoolean | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveFloat | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveInt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SetFirstSigma | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/ltx2_pose_to_video.ui.json
| class_type | node pack |
|---|---|
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ConditioningZeroOut | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DWPreprocessor | https://github.com/Fannovel16/comfyui_controlnet_aux (also in 2 other packs; unverified which) |
| EmptyLTXVLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetImageSize | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageFromBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleBy | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXAVTextEncoderLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAddGuide | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConcatAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVCropGuides | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVEmptyLatentAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVImgToVideoInplace | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVLatentUpsampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVScheduler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSeparateAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LatentUpscaleModelLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ManualSigmas | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveBoolean | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveFloat | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveInt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/ltx2_canny_to_video.ui.json
| class_type | node pack |
|---|---|
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Canny | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ConditioningZeroOut | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyLTXVLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetImageSize | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageFromBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleBy | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXAVTextEncoderLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAddGuide | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConcatAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVCropGuides | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVEmptyLatentAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVImgToVideoInplace | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVLatentUpsampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVScheduler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSeparateAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LatentUpscaleModelLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ManualSigmas | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveBoolean | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveFloat | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveInt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/wan22_14b_fun_control.ui.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Canny | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingSD3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Wan22FunControlToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/utility_openpose_video.ui.json
| class_type | node pack |
|---|---|
| DWPreprocessor | https://github.com/Fannovel16/comfyui_controlnet_aux (also in 2 other packs; unverified which) |
| VHS_LoadVideo | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| VHS_VideoCombine | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |

### workflows/ui/utility_sdpose_video_to_pose_map.ui.json
| class_type | node pack |
|---|---|
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SDPoseDrawKeypoints | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SDPoseKeypointExtractor | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/wan_vace_pose_control.api.json
| file | license |
|---|---|
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan2.1_vace_1.3B_fp16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |

### workflows/wan_vace_canny_control.api.json
| file | license |
|---|---|
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan2.1_vace_1.3B_fp16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |

### workflows/ui/ltx2_depth_to_video.ui.json
| file | license |
|---|---|
| gemma_3_12B_it_fp4_mixed.safetensors | Gemma Terms of Use (unverified) |
| lotus-depth-d-v1-1.safetensors | UNVERIFIED |
| ltx-2-19b-dev-fp8.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-19b-distilled-lora-384.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-19b-distilled.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-19b-ic-lora-depth-control.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-spatial-upscaler-x2-1.0.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| vae-ft-mse-840000-ema-pruned.safetensors | UNVERIFIED |

### workflows/ui/ltx2_pose_to_video.ui.json
| file | license |
|---|---|
| dw-ll_ucoco_384_bs5.torchscript.pt | DWPose ONNX (IDEA-Research): Apache-2.0 (per motionfield NOTICE) |
| gemma_3_12B_it_fp4_mixed.safetensors | Gemma Terms of Use (unverified) |
| ltx-2-19b-dev-fp8.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-19b-distilled-lora-384.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-19b-distilled.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-19b-ic-lora-pose-control.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-spatial-upscaler-x2-1.0.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| yolox_l.onnx | DWPose ONNX (IDEA-Research): Apache-2.0 (per motionfield NOTICE) |

### workflows/ui/ltx2_canny_to_video.ui.json
| file | license |
|---|---|
| gemma_3_12B_it_fp4_mixed.safetensors | Gemma Terms of Use (unverified) |
| ltx-2-19b-dev-fp8.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-19b-distilled-lora-384.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-19b-distilled.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-19b-ic-lora-canny-control.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-spatial-upscaler-x2-1.0.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |

### workflows/ui/wan22_14b_fun_control.ui.json
| file | license |
|---|---|
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan2.2_fun_control_high_noise_14B_fp8_scaled.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan2.2_fun_control_low_noise_14B_fp8_scaled.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |

### workflows/ui/utility_openpose_video.ui.json
| file | license |
|---|---|
| dw-ll_ucoco_384_bs5.torchscript.pt | DWPose ONNX (IDEA-Research): Apache-2.0 (per motionfield NOTICE) |
| yolox_l.onnx | DWPose ONNX (IDEA-Research): Apache-2.0 (per motionfield NOTICE) |

### workflows/ui/utility_sdpose_video_to_pose_map.ui.json
| file | license |
|---|---|
| sdpose_wholebody_fp16.safetensors | SDPose: license UNVERIFIED |
