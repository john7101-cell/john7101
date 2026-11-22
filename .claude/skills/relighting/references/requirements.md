# Requirements: relighting

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
FLUX.2 Klein + DA3: 16-24 GB (estimate, unverified)

## Node types

### workflows/klein_relight_normals.api.json
| class_type | node pack |
|---|---|
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ConditioningZeroOut | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DA3Inference | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DA3Render | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyFlux2LatentImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Flux2Scheduler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetImageSize | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleToTotalPixels | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadDA3Model | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| OF_Relight | bundled: assets/motionfield_nodes (jalajbhandula/motionfield, MIT; dwpose_onnx Apache-2.0) |
| OF_RelightNormals | bundled: assets/motionfield_nodes (jalajbhandula/motionfield, MIT; dwpose_onnx Apache-2.0) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ReferenceMultiLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/normals_from_da3.api.json
| class_type | node pack |
|---|---|
| DA3Inference | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DA3Render | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleToTotalPixels | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadDA3Model | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| OF_RelightNormals | bundled: assets/motionfield_nodes (jalajbhandula/motionfield, MIT; dwpose_onnx Apache-2.0) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/qwen_edit_2509_relight.ui.json
| class_type | node pack |
|---|---|
| CFGNorm | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FluxKontextImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveStringMultiline | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| StringConcatenate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeQwenImageEditPlus | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/character_portrait_relighting.ui.json
| class_type | node pack |
|---|---|
| GeminiImage2Node | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/klein_relight_normals.api.json
| file | license |
|---|---|
| depth_anything_3_mono_large.safetensors | Depth Anything: license varies by size (V2-Small Apache-2.0; larger V2/V3 checkpoints CC-BY-NC-4.0) - UNVERIFIED for this file |
| flux-2-klein-4b.safetensors | FLUX.2 [klein] 4B: Apache-2.0 (unverified for this file) |
| flux2-vae.safetensors | FLUX.2 VAE: Apache-2.0 (unverified) |
| qwen_3_4b_fp8_mixed.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |

### workflows/normals_from_da3.api.json
| file | license |
|---|---|
| depth_anything_3_mono_large.safetensors | Depth Anything: license varies by size (V2-Small Apache-2.0; larger V2/V3 checkpoints CC-BY-NC-4.0) - UNVERIFIED for this file |

### workflows/ui/qwen_edit_2509_relight.ui.json
| file | license |
|---|---|
| Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| Qwen-Image-Edit-2509-Relight.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_edit_2509_fp8_e4m3fn.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |

### workflows/ui/character_portrait_relighting.ui.json
| file | license |
|---|---|
| (none named) | |
