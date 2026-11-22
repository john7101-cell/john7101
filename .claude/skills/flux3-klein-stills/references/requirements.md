# Requirements: flux3-klein-stills

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
~12 GB for int8/fp8 Klein; 9B bf16 ~24 GB (estimate, unverified)

## Node types

### workflows/flux3_klein_distilled_t2i.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyFlux2LatentImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/flux3_klein_t2i.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfySwitchNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateBoundingBoxes | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyFlux2LatentImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Flux3LayoutPrompt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewAny | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveStringMultiline | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResolutionSelector | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextGenerate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/flux3_klein_t2i_template.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfySwitchNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyFlux2LatentImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewAny | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveStringMultiline | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResolutionSelector | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextGenerate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/flux2_klein_9b_t2i.api.json
| class_type | node pack |
|---|---|
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ConditioningZeroOut | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyFlux2LatentImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Flux2Scheduler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/flux2_klein_t2i_lean.api.json
| class_type | node pack |
|---|---|
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ConditioningZeroOut | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyFlux2LatentImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Flux2Scheduler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/flux3_klein_distilled_t2i.api.json
| file | license |
|---|---|
| flux2-vae.safetensors | FLUX.2 VAE: Apache-2.0 (unverified) |
| flux3-image-klein-int8-convrot.safetensors | FLUX 3 Klein: UNVERIFIED (check the BFL model card) |
| qwen3vl_4b_int8_convrot.safetensors | Qwen3-VL text encoder: Apache-2.0 (unverified) |

### workflows/flux3_klein_t2i.api.json
| file | license |
|---|---|
| flux2-vae.safetensors | FLUX.2 VAE: Apache-2.0 (unverified) |
| flux3-image-klein-base-int8-convrot.safetensors | FLUX 3 Klein: UNVERIFIED (check the BFL model card) |
| qwen3.5_9b_flux3_prompt_upsampler_w4a8.safetensors | SAM 2/3.x (Meta): license UNVERIFIED (SAM 2 is Apache-2.0; SAM 3.x has its own license) |
| qwen3vl_4b_int8_convrot.safetensors | Qwen3-VL text encoder: Apache-2.0 (unverified) |

### workflows/flux3_klein_t2i_template.api.json
| file | license |
|---|---|
| flux2-vae.safetensors | FLUX.2 VAE: Apache-2.0 (unverified) |
| flux3_image_klein_base_int8_convrot.safetensors | FLUX 3 Klein: UNVERIFIED (check the BFL model card) |
| qwen3.5_9b_flux3_prompt_upsampler_w4a8.safetensors | SAM 2/3.x (Meta): license UNVERIFIED (SAM 2 is Apache-2.0; SAM 3.x has its own license) |
| qwen3vl_4b_int8_convrot.safetensors | Qwen3-VL text encoder: Apache-2.0 (unverified) |

### workflows/flux2_klein_9b_t2i.api.json
| file | license |
|---|---|
| flux-2-klein-9b-nvfp4.safetensors | FLUX.2 [klein] 9B: FLUX Non-Commercial License (unverified for this file) |
| flux2-vae.safetensors | FLUX.2 VAE: Apache-2.0 (unverified) |
| qwen_3_8b_fp8mixed.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |

### workflows/flux2_klein_t2i_lean.api.json
| file | license |
|---|---|
| flux-2-klein-4b-fp8.safetensors | FLUX.2 [klein] 4B: Apache-2.0 (unverified for this file) |
| flux2-vae.safetensors | FLUX.2 VAE: Apache-2.0 (unverified) |
| qwen_3_4b_fp8_mixed.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
