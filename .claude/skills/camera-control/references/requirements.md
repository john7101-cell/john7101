# Requirements: camera-control

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
Wan 2.1 Fun Camera 1.3B ~8-12 GB (estimate); Wan 2.2 14B fp8 24 GB+ (unverified)

## Node types

### workflows/wan_fun_camera_i2v.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPVisionEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPVisionLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| OF_CameraEmbed | bundled: assets/motionfield_nodes (jalajbhandula/motionfield, MIT; dwpose_onnx Apache-2.0) |
| OF_Trajectory | bundled: assets/motionfield_nodes (jalajbhandula/motionfield, MIT; dwpose_onnx Apache-2.0) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VHS_VideoCombine | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| WanCameraImageToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/wan_fun_camera_director.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| OF_CameraEmbed | bundled: assets/motionfield_nodes (jalajbhandula/motionfield, MIT; dwpose_onnx Apache-2.0) |
| OF_Trajectory | bundled: assets/motionfield_nodes (jalajbhandula/motionfield, MIT; dwpose_onnx Apache-2.0) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VHS_VideoCombine | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| WanCameraImageToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/wan22_14b_fun_camera.ui.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingSD3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| WanCameraEmbedding | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| WanCameraImageToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/wan21_fun_camera_1_3b.ui.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPVisionEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPVisionLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingSD3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveAnimatedWEBP | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| WanCameraEmbedding | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| WanCameraImageToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/wan_ati_trajectory.ui.json
| class_type | node pack |
|---|---|
| CLIPVisionLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FL_PathAnimator | https://github.com/filliptm/ComfyUI_FL-Path-Animator (also in 1 other packs; unverified which) |
| ImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadWanVideoT5TextEncoder | https://github.com/LeonQ8/ComfyUI-Dynamic-Lora-Scheduler (also in 2 other packs; unverified which) |
| PrimitiveInt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| WanVideoATITracks | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoATITracksVisualize | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoClipVisionEncode | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoDecode | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoImageToVideoEncode | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoLoraSelect | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoModelLoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoSampler | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoTextEncode | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoVAELoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/wan_fun_camera_i2v.api.json
| file | license |
|---|---|
| clip_vision_h.safetensors | UNVERIFIED |
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan2.1_fun_camera_v1.1_1.3B_bf16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |

### workflows/wan_fun_camera_director.api.json
| file | license |
|---|---|
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan2.1_fun_camera_v1.1_1.3B_bf16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |

### workflows/ui/wan22_14b_fun_camera.ui.json
| file | license |
|---|---|
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan2.2_fun_camera_high_noise_14B_fp8_scaled.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan2.2_fun_camera_low_noise_14B_fp8_scaled.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |

### workflows/ui/wan21_fun_camera_1_3b.ui.json
| file | license |
|---|---|
| clip_vision_h.safetensors | UNVERIFIED |
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan2.1_fun_camera_v1.1_1.3B_bf16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |

### workflows/ui/wan_ati_trajectory.ui.json
| file | license |
|---|---|
| CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors | UNVERIFIED |
| Wan21_T2V_14B_lightx2v_cfg_step_distill_lora_rank32.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| Wan2_1-I2V-ATI-14B_fp8_e4m3fn.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| Wan2_1_VAE_bf16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| umt5-xxl-enc-bf16.safetensors | T5: Apache-2.0 (unverified) |
