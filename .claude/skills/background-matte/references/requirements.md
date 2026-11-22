# Requirements: background-matte

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
BiRefNet ~2-4 GB (estimate, unverified)

## Node types

### workflows/birefnet_image_transparent.api.json
| class_type | node pack |
|---|---|
| InvertMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| JoinImageWithAlpha | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadBackgroundRemovalModel | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RemoveBackground | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/birefnet_image_solid.api.json
| class_type | node pack |
|---|---|
| EmptyImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetImageSize | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageCompositeMasked | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadBackgroundRemovalModel | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RemoveBackground | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/birefnet_video_background.api.json
| class_type | node pack |
|---|---|
| ComfyMathExpression | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfySwitchNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetImageSize | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageCompositeMasked | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadBackgroundRemovalModel | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveBoolean | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RemoveBackground | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/platelock_comp.api.json
| class_type | node pack |
|---|---|
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PlateLockBeforeAfter | bundled: assets/comfyui-platelock (TusharTechs/platelock, MIT) |
| PlateLockComposite | bundled: assets/comfyui-platelock (TusharTechs/platelock, MIT) |
| PlateLockDifferenceMatte | bundled: assets/comfyui-platelock (TusharTechs/platelock, MIT) |
| PlateLockExtractElement | bundled: assets/comfyui-platelock (TusharTechs/platelock, MIT) |
| PlateLockFidelityReport | bundled: assets/comfyui-platelock (TusharTechs/platelock, MIT) |
| PlateLockMatteOverlay | bundled: assets/comfyui-platelock (TusharTechs/platelock, MIT) |
| PlateLockRefineMatte | bundled: assets/comfyui-platelock (TusharTechs/platelock, MIT) |
| PlateLockTemporalStabilize | bundled: assets/comfyui-platelock (TusharTechs/platelock, MIT) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/birefnet_image_transparent.api.json
| file | license |
|---|---|
| birefnet.safetensors | BiRefNet: MIT (unverified) |

### workflows/birefnet_image_solid.api.json
| file | license |
|---|---|
| birefnet.safetensors | BiRefNet: MIT (unverified) |

### workflows/birefnet_video_background.api.json
| file | license |
|---|---|
| birefnet.safetensors | BiRefNet: MIT (unverified) |

### workflows/platelock_comp.api.json
| file | license |
|---|---|
| (none named) | |
