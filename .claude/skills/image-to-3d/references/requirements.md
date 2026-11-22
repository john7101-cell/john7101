# Requirements: image-to-3d

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
16-24 GB (estimate, unverified)

## Node types

### workflows/trellis2_image_to_3d.api.json
| class_type | node pack |
|---|---|
| CFGOverride | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPVisionLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DecimateMesh | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyTrellis2LatentStructure | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageCropToMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadBackgroundRemovalModel | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MeshSmoothNormals | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingSD3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PaintMesh | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RemeshMesh | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RemoveBackground | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RescaleCFG | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveGLB | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Trellis2Conditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Trellis2ShapeStage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Trellis2TextureStage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Trellis2UpsampleStage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VaeDecodeShapeTrellis | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VaeDecodeStructureTrellis2 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VaeDecodeTextureTrellis | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/pixal3d_image_to_3d.api.json
| class_type | node pack |
|---|---|
| CFGOverride | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPVisionLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DecimateMesh | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyTrellis2LatentStructure | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageCropToMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadBackgroundRemovalModel | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadMoGeModel | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MeshSmoothNormals | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MoGeGeometryToFOV | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MoGeInference | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingSD3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PaintMesh | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Pixal3DConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RemeshMesh | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RemoveBackground | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RescaleCFG | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveGLB | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Trellis2ShapeStage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Trellis2TextureStage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Trellis2UpsampleStage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VaeDecodeShapeTrellis | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VaeDecodeStructureTrellis2 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VaeDecodeTextureTrellis | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/pixal3d_multiview_to_3d.api.json
| class_type | node pack |
|---|---|
| CFGOverride | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPVisionLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DecimateMesh | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyTrellis2LatentStructure | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageCropToMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadBackgroundRemovalModel | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MeshSmoothNormals | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingSD3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PaintMesh | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Pixal3DMultiViewConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RemeshMesh | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RemoveBackground | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RescaleCFG | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveGLB | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Trellis2ShapeStage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Trellis2TextureStage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Trellis2UpsampleStage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VaeDecodeShapeTrellis | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VaeDecodeStructureTrellis2 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VaeDecodeTextureTrellis | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/trellis2_image_to_3d.api.json
| file | license |
|---|---|
| birefnet.safetensors | BiRefNet: MIT (unverified) |
| dino_v3_L_naf_fp32.safetensors | DINOv3: DINOv3 License (unverified) |
| trellis_2_int8_convrot.safetensors | TRELLIS.2: MIT (unverified) |
| trellis_2_shape_vae_bf16.safetensors | TRELLIS.2: MIT (unverified) |
| trellis_2_texture_vae_bf16.safetensors | TRELLIS.2: MIT (unverified) |

### workflows/pixal3d_image_to_3d.api.json
| file | license |
|---|---|
| birefnet.safetensors | BiRefNet: MIT (unverified) |
| dino_v3_L_naf_fp32.safetensors | DINOv3: DINOv3 License (unverified) |
| moge_2_vitl_normal_fp16.safetensors | MoGe-2: UNVERIFIED |
| pixal3d_int8_convrot.safetensors | Pixal3D: UNVERIFIED |
| trellis_2_shape_vae_bf16.safetensors | TRELLIS.2: MIT (unverified) |
| trellis_2_texture_vae_bf16.safetensors | TRELLIS.2: MIT (unverified) |

### workflows/pixal3d_multiview_to_3d.api.json
| file | license |
|---|---|
| birefnet.safetensors | BiRefNet: MIT (unverified) |
| dino_v3_L_naf_fp32.safetensors | DINOv3: DINOv3 License (unverified) |
| pixal3d_multiview_int8_convrot.safetensors | Pixal3D: UNVERIFIED |
| trellis_2_shape_vae_bf16.safetensors | TRELLIS.2: MIT (unverified) |
| trellis_2_texture_vae_bf16.safetensors | TRELLIS.2: MIT (unverified) |
