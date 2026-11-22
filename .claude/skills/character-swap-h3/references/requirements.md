# Requirements: character-swap-h3

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
unverified (H3 int8 + qwen3vl 32B int4: likely 32 GB+)

## Node types

### workflows/h3_swap_simple.api.json
| class_type | node pack |
|---|---|
| AudioAdjustVolume | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| BasicGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| BasicScheduler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfyMathExpression | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GrowMaskWithBlur | https://github.com/kijai/ComfyUI-KJNodes |
| H3ClipShots | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| H3FillShots | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| H3GreyMannequins | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| H3OneClickSwapPlan | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| H3PeopleMask | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| H3SourceSlice | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| ImageFromBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleToMaxDimension | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MaskComposite | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MiniMaxH3ChainAssemble | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainContext | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainCurrent | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainLoopEnd | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainLoopStart | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainPlanModern | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainReview | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainSegmentSave | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ContexMaskGridPreview | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ContexMaskedTarget | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3FantasticVideoEditLatent | "Fantastic PromptBuilder" node pack (named in openjutsu CUSTOM_NODES_REPORT.md; repo URL UNVERIFIED) |
| MiniMaxH3GenerationProfile | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3LoopTrim | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ReferenceToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MiniMaxH3SigmaShift | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MiniMaxH3SourceTimeline | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| ModelAttentionBackend | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewAny | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveBoolean | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SAM3_TrackToMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SAM3_VideoTrack | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextGenerate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TrimAudioDuration | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VHS_LoadVideo | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| VHS_SelectEveryNthImage | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite (also in 1 other packs; unverified which) |

### workflows/h3_swap_face.api.json
| class_type | node pack |
|---|---|
| BasicGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| BasicScheduler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| H3FaceChunks | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| H3FaceJoin | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| H3FaceMaskSAM | https://github.com/Carasibana/ComfyUI-H3-FaceRefine (per openjutsu CUSTOM_NODES_REPORT.md; needs insightface) |
| H3FaceStitch | https://github.com/Carasibana/ComfyUI-H3-FaceRefine (per openjutsu CUSTOM_NODES_REPORT.md; needs insightface) |
| H3FaceTrackCrop | https://github.com/Carasibana/ComfyUI-H3-FaceRefine (per openjutsu CUSTOM_NODES_REPORT.md; needs insightface) |
| ImageBlur | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleToMaxDimension | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MiniMaxH3ContexMaskedTarget | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3FantasticVideoEditLatent | "Fantastic PromptBuilder" node pack (named in openjutsu CUSTOM_NODES_REPORT.md; repo URL UNVERIFIED) |
| MiniMaxH3ReferenceToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelAttentionBackend | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SAMLoader | https://github.com/ltdrdata/ComfyUI-Impact-Pack |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextGenerate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VHS_LoadVideo | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| VHS_VideoCombine | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |

### workflows/h3_swap_object.api.json
| class_type | node pack |
|---|---|
| BasicGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| BasicScheduler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfyMathExpression | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GrowMaskWithBlur | https://github.com/kijai/ComfyUI-KJNodes |
| H3ClipShots | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| H3FillShots | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| H3GreyMannequins | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| H3ObjectSwapPlan | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| H3PeopleMask | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| H3SourceSlice | bundled: assets/comfyui-h3-oneclick-swap (D3voz, MIT) |
| ImageFromBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleToMaxDimension | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MiniMaxH3ChainAssemble | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainContext | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainCurrent | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainLoopEnd | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainLoopStart | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainPlanModern | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainReview | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ChainSegmentSave | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ContexMaskGridPreview | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ContexMaskedTarget | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3FantasticVideoEditLatent | "Fantastic PromptBuilder" node pack (named in openjutsu CUSTOM_NODES_REPORT.md; repo URL UNVERIFIED) |
| MiniMaxH3GenerationProfile | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3LoopTrim | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| MiniMaxH3ReferenceToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MiniMaxH3SigmaShift | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MiniMaxH3SourceTimeline | https://github.com/ethanfel/ComfyUI-MiniMaxH3-Context-Loop |
| ModelAttentionBackend | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewAny | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SAM3_VideoTrack | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextGenerate | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TrimAudioDuration | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VHS_LoadVideo | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |

### workflows/ltx23_motion_swap_open_fallback.api.json
| class_type | node pack |
|---|---|
| BlockifyMask | https://github.com/kijai/ComfyUI-KJNodes |
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfyMathExpression | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DualCLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetImageSize | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GetVideoComponents | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| GrowMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageCompositeMasked | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageFromBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageScaleBy | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAddGuideMulti | https://github.com/kijai/ComfyUI-KJNodes |
| LTXVConcatAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVCropGuides | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVEmptyLatentAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVLatentUpsampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVPreprocess | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSeparateAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LatentUpscaleModelLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadBackgroundRemovalModel | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ManualSigmas | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RemoveBackground | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RepeatImageBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ReservedRegionFrameComposer | https://github.com/alisson-anjos/ComfyUI-BFSNodes |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SAM3_TrackToMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SAM3_VideoTrack | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoaderKJ | https://github.com/kijai/ComfyUI-KJNodes |
| Video Slice | https://github.com/comfyanonymous/ComfyUI |
| VideoFrameSample | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/h3_swap_simple.api.json
| file | license |
|---|---|
| minimax_h3_DMAD_4step_full_lora_avg_rank_39_bf16.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| minimax_h3_audio_vae_fp32.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| minimax_h3_ref2va_pruned_int8_convrot.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| minimax_h3_video_vae_int8_convrot.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| qwen3vl_32b_minimax_h3_int4_convrot.safetensors | Qwen3-VL text encoder: Apache-2.0 (unverified) |
| qwen3vl_8b_int8_convrot.safetensors | Qwen3-VL text encoder: Apache-2.0 (unverified) |
| sam3.1_multiplex_fp16.safetensors | SAM 2/3.x (Meta): license UNVERIFIED (SAM 2 is Apache-2.0; SAM 3.x has its own license) |

### workflows/h3_swap_face.api.json
| file | license |
|---|---|
| bbox\face_yolov8m.pt | ACE-Step: Apache-2.0 (unverified for 1.5) |
| minimax_h3_DMAD_4step_full_lora_avg_rank_39_bf16.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| minimax_h3_audio_vae_fp32.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| minimax_h3_ref2va_pruned_int8_convrot.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| minimax_h3_video_vae_int8_convrot.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| qwen3vl_32b_minimax_h3_int4_convrot.safetensors | Qwen3-VL text encoder: Apache-2.0 (unverified) |
| qwen3vl_8b_int8_convrot.safetensors | Qwen3-VL text encoder: Apache-2.0 (unverified) |
| sam_vit_b_01ec64.pth | SAM 2/3.x (Meta): license UNVERIFIED (SAM 2 is Apache-2.0; SAM 3.x has its own license) |
| segm\person_yolov8m-seg.pt | UNVERIFIED |

### workflows/h3_swap_object.api.json
| file | license |
|---|---|
| minimax_h3_DMAD_4step_full_lora_avg_rank_39_bf16.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| minimax_h3_audio_vae_fp32.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| minimax_h3_ref2va_pruned_int8_convrot.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| minimax_h3_video_vae_int8_convrot.safetensors | MiniMax H3 / MiniMax open weights (local weights, not an API): license UNVERIFIED |
| qwen3vl_32b_minimax_h3_int4_convrot.safetensors | Qwen3-VL text encoder: Apache-2.0 (unverified) |
| qwen3vl_8b_int8_convrot.safetensors | Qwen3-VL text encoder: Apache-2.0 (unverified) |
| sam3.1_multiplex_fp16.safetensors | SAM 2/3.x (Meta): license UNVERIFIED (SAM 2 is Apache-2.0; SAM 3.x has its own license) |

### workflows/ltx23_motion_swap_open_fallback.api.json
| file | license |
|---|---|
| LTX23_audio_vae_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| LTX23_video_vae_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| birefnet.safetensors | BiRefNet: MIT (unverified) |
| gemma_3_12B_it_fp8_scaled.safetensors | Gemma Terms of Use (unverified) |
| ltx-2.3-22b-distilled_transformer_only_fp8_input_scaled_v3.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.3-spatial-upscaler-x2-1.0.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.3_text_projection_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx23_inpaint_masked_r2v_rank32_v1_3000steps.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| sam3.1_multiplex_fp16.safetensors | SAM 2/3.x (Meta): license UNVERIFIED (SAM 2 is Apache-2.0; SAM 3.x has its own license) |
