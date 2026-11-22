# Requirements: music-sfx

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
ACE-Step 1.5 ~8 GB; Stable Audio Open ~6-8 GB; MiniMax Music 3 unverified (estimate)

## Node types

### workflows/music_ace_step15.api.json
| class_type | node pack |
|---|---|
| ConditioningZeroOut | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DualCLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyAceStep1.5LatentAudio | https://github.com/comfyanonymous/ComfyUI |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingAuraFlow | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveAudioAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextEncodeAceStepAudio1.5 | https://github.com/comfyanonymous/ComfyUI |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/sfx_stable_audio_open.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyLatentAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/sfx_stable_audio_3.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyLatentAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveAudioMP3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/music_minimax_music3.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ConditioningZeroOut | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyMiniMaxMusic3LatentAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MiniMaxMusic3TextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveAudioMP3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/music_ace_step15.api.json
| file | license |
|---|---|
| ace_1.5_vae.safetensors | ACE-Step: Apache-2.0 (unverified for 1.5) |
| acestep_v1.5_xl_turbo_bf16.safetensors | ACE-Step: Apache-2.0 (unverified for 1.5) |
| qwen_0.6b_ace15.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |
| qwen_4b_ace15.safetensors | Qwen text/VL encoder: Apache-2.0 (unverified) |

### workflows/sfx_stable_audio_open.api.json
| file | license |
|---|---|
| stable-audio-open-1.0.safetensors | Stable Audio Open 1.0: Stability AI Community License (unverified) |
| t5-base.safetensors | T5: Apache-2.0 (unverified) |

### workflows/sfx_stable_audio_3.api.json
| file | license |
|---|---|
| stable_audio_3_medium.safetensors | Stable Audio 3: UNVERIFIED |
| t5gemma_b_b_ul2.safetensors | Gemma Terms of Use (unverified) |

### workflows/music_minimax_music3.api.json
| file | license |
|---|---|
| minimax_music3_dav.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| minimax_music3_dit_fp16.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| minimax_music3_text_encoder_pruned_int8_convrot.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
