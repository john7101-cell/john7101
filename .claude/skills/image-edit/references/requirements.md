# Requirements: image-edit

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
16-20 GB fp8/int8 + Lightning LoRA; bf16 2511 ~40 GB (estimate, unverified)

## Node types

### workflows/qwen_edit_2511_instruct.api.json
| class_type | node pack |
|---|---|
| CFGNorm | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FluxKontextMultiReferenceLatentMethod | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleToTotalPixels | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeQwenImageEditPlus | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/qwen_edit_2511_angles.api.json
| class_type | node pack |
|---|---|
| CFGNorm | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FluxKontextImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FluxKontextMultiReferenceLatentMethod | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| StringConcatenate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeQwenImageEditPlus | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/qwen_edit_2509_relight.api.json
| class_type | node pack |
|---|---|
| CFGNorm | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleToTotalPixels | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RegexReplace | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RepeatLatentBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| StringConcatenate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeQwenImageEditPlus | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/qwen_image_outpaint_format.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfyMathExpression | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ControlNetInpaintingAliMamaApply | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ControlNetLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetImageSize | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GrowMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageBlur | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageCompositeMasked | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImagePadForOutpaint | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageToMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MaskToImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveInt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RepeatImageBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/qwen_edit_2509_angle_lightning.api.json
| class_type | node pack |
|---|---|
| CFGNorm | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeQwenImageEditPlus | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/qwen_edit_2509_pushin_lightning.api.json
| class_type | node pack |
|---|---|
| CFGNorm | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeQwenImageEditPlus | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/qwen_edit_2509_coverage_lightning.api.json
| class_type | node pack |
|---|---|
| CFGNorm | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeQwenImageEditPlus | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/qwen_edit_2511_try_on.api.json
| class_type | node pack |
|---|---|
| CFGNorm | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FluxKontextMultiReferenceLatentMethod | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleToTotalPixels | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeQwenImageEditPlus | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/qwen_edit_2511_angles_set.api.json
| class_type | node pack |
|---|---|
| CFGNorm | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FluxKontextImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FluxKontextMultiReferenceLatentMethod | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| StringConcatenate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeQwenImageEditPlus | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/qwen_edit_2511_layers_edit.api.json
| class_type | node pack |
|---|---|
| CFGNorm | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FluxKontextMultiReferenceLatentMethod | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetImageSize | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageCompositeMasked | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScale | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleToTotalPixels | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| InvertMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| JoinImageWithAlpha | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeQwenImageEditPlus | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/qwen_edit_2511_instruct.api.json
| file | license |
|---|---|
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_edit_2511_fp8mixed.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |

### workflows/qwen_edit_2511_angles.api.json
| file | license |
|---|---|
| Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| qwen-image-edit-2511-multiple-angles-lora.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_edit_2511_bf16.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |

### workflows/qwen_edit_2509_relight.api.json
| file | license |
|---|---|
| Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| Qwen-Image-Edit-2509-Relight.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_edit_2509_fp8_e4m3fn.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |

### workflows/qwen_image_outpaint_format.api.json
| file | license |
|---|---|
| Qwen-Image-InstantX-ControlNet-Inpainting.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| Qwen-Image-Lightning-4steps-V1.0.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_fp8_e4m3fn.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |

### workflows/qwen_edit_2509_angle_lightning.api.json
| file | license |
|---|---|
| Qwen-Edit-2509-Multiple-angles.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| Qwen-Image-Edit-2509-Lightning-8steps-V1.0-bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_edit_2509_fp8_e4m3fn.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |

### workflows/qwen_edit_2509_pushin_lightning.api.json
| file | license |
|---|---|
| Qwen-Edit-2509-Multiple-angles.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| Qwen-Image-Edit-2509-Lightning-8steps-V1.0-bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_edit_2509_fp8_e4m3fn.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |

### workflows/qwen_edit_2509_coverage_lightning.api.json
| file | license |
|---|---|
| Qwen-Image-Edit-2509-Lightning-8steps-V1.0-bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_edit_2509_fp8_e4m3fn.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |

### workflows/qwen_edit_2511_try_on.api.json
| file | license |
|---|---|
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_edit_2511_fp8mixed.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |

### workflows/qwen_edit_2511_angles_set.api.json
| file | license |
|---|---|
| Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| qwen-image-edit-2511-multiple-angles-lora.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_edit_2511_bf16.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |

### workflows/qwen_edit_2511_layers_edit.api.json
| file | license |
|---|---|
| Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| qwen_2.5_vl_7b_fp8_scaled.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_image_edit_2511_bf16.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
| qwen_image_vae.safetensors | Qwen-Image family: Apache-2.0 (unverified for 2.1/2511 builds) |
