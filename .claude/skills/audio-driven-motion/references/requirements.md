# Requirements: audio-driven-motion

Generated statically from the bundled workflows. Node packs are resolved against ComfyUI core (commit b5a4321, read 2026-10-30) and ComfyUI-Manager `extension-node-map.json` (read 2026-10-30). Run `scripts/preflight.py` against your server before you submit.

## VRAM
Wan S2V 14B / LTX-2 a2v: 24 GB+; InfiniteTalk GGUF + block swap lower (all unverified)

## Node types

### workflows/wan22_s2v.api.json
| class_type | node pack |
|---|---|
| AudioEncoderEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| AudioEncoderLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingSD3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VHS_VideoCombine | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| WanSoundImageToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/wan21_infinitetalk_vocal_sep.api.json
| class_type | node pack |
|---|---|
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPVisionLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DownloadAndLoadWav2VecModel | https://github.com/kael558/ComfyUI-GGUF-FantasyTalking (also in 2 other packs; unverified which) |
| GetImageSizeAndCount | https://github.com/kijai/ComfyUI-KJNodes |
| INTConstant | https://github.com/kijai/ComfyUI-KJNodes |
| ImageResizeKJv2 | https://github.com/kijai/ComfyUI-KJNodes |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MelBandRoFormerModelLoader | https://github.com/kijai/ComfyUI-MelBandRoFormer |
| MelBandRoFormerSampler | https://github.com/kijai/ComfyUI-MelBandRoFormer |
| MultiTalkModelLoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| MultiTalkWav2VecEmbeds | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| PreviewAny | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VHS_VideoCombine | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| WanVideoBlockSwap | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoClipVisionEncode | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoImageToVideoMultiTalk | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoLoraSelect | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoLoraSelectMulti | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoModelLoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoPassImagesFromSamples | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoSampler | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoTextEmbedBridge | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoTorchCompileSettings | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoVAELoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| Wav2VecModelLoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (also in 1 other packs; unverified which) |

### workflows/ui/ltx2_audio_to_video.ui.json
| class_type | node pack |
|---|---|
| AudioCrop | https://github.com/christian-byrne/audio-separation-nodes-comfyui |
| AudioSeparation | https://github.com/christian-byrne/audio-separation-nodes-comfyui |
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ConditioningZeroOut | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DualCLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyLTXVLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| FloatConstant | https://github.com/kijai/ComfyUI-KJNodes |
| GetImageRangeFromBatch | https://github.com/kijai/ComfyUI-KJNodes |
| ImageBatchExtendWithOverlap | https://github.com/kijai/ComfyUI-KJNodes |
| ImageResizeKJv2 | https://github.com/kijai/ComfyUI-KJNodes |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTX2SamplingPreviewOverride | https://github.com/kijai/ComfyUI-KJNodes |
| LTX2_NAG | https://github.com/kijai/ComfyUI-KJNodes |
| LTXVAddGuideMulti | https://github.com/kijai/ComfyUI-KJNodes |
| LTXVAudioVAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVideoMask | https://github.com/kijai/ComfyUI-KJNodes |
| LTXVChunkFeedForward | https://github.com/kijai/ComfyUI-KJNodes |
| LTXVConcatAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVCropGuides | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVImgToVideoInplaceKJ | https://github.com/kijai/ComfyUI-KJNodes |
| LTXVPreprocess | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVScheduler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSeparateAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveFloat | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SetLatentNoiseMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SolidMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TrimAudioDuration | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoaderKJ | https://github.com/kijai/ComfyUI-KJNodes |
| VHS_VideoCombine | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |

### workflows/ui/ltx23_image_audio_to_video.ui.json
| class_type | node pack |
|---|---|
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CheckpointLoaderSimple | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfyMathExpression | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ComfySwitchNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| EmptyLTXVLatentVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXAVTextEncoderLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAEEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVAudioVAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConcatAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVConditioning | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVCropGuides | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVImgToVideoInplace | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVLatentUpsampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVPreprocess | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LTXVSeparateAVLatent | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LatentUpscaleModelLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ManualSigmas | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PreviewAny | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveBoolean | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveFloat | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveInt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveStringMultiline | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RecordAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ResizeImageMaskNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SetLatentNoiseMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SolidMask | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TextGenerateLTX2Prompt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| TrimAudioDuration | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecodeTiled | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/wan22_14b_s2v.ui.json
| class_type | node pack |
|---|---|
| AudioEncoderEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| AudioEncoderLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ImageFromBatch | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LatentConcat | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LatentCut | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingSD3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveFloat | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveInt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| WanSoundImageToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| WanSoundImageToVideoExtend | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/wan21_infinitetalk.ui.json
| class_type | node pack |
|---|---|
| AudioConcat | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| AudioEncoderEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| AudioEncoderLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| BasicScheduler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| BatchImagesNode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CFGGuider | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ConditioningZeroOut | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSamplerSelect | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelPatchLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| Painter | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| PrimitiveInt | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RandomNoise | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SamplerCustomAdvanced | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| WanInfiniteTalkToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

### workflows/ui/wan21_infinitetalk_music.ui.json
| class_type | node pack |
|---|---|
| AudioSeparation | https://github.com/christian-byrne/audio-separation-nodes-comfyui |
| CLIPVisionLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| DownloadAndLoadWav2VecModel | https://github.com/kael558/ComfyUI-GGUF-FantasyTalking (also in 2 other packs; unverified which) |
| GetImageSizeAndCount | https://github.com/kijai/ComfyUI-KJNodes |
| ImageResizeKJv2 | https://github.com/kijai/ComfyUI-KJNodes |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| MultiTalkModelLoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| MultiTalkWav2VecEmbeds | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| WanVideoClipVisionEncode | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoDecode | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoImageToVideoMultiTalk | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoLoraSelect | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoModelLoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoSampler | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoTextEncodeCached | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |
| WanVideoVAELoader | https://github.com/kijai/ComfyUI-WanVideoWrapper (other packs reuse these names; this is the canonical one) |

### workflows/ui/humo.ui.json
| class_type | node pack |
|---|---|
| AudioEncoderEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| AudioEncoderLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CLIPTextEncode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| CreateVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| KSampler | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoadImage | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| LoraLoaderModelOnly | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| ModelSamplingSD3 | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| RecordAudio | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| SaveVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| UNETLoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAEDecode | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| VAELoader | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |
| WanHuMoImageToVideo | ComfyUI core (comfyanonymous/ComfyUI @b5a4321) |

## Model files and weight licenses
Licenses are from public knowledge of the model family. Confirm each one on its model card before commercial use.

### workflows/wan22_s2v.api.json
| file | license |
|---|---|
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan2.2_s2v_14B_fp8_scaled.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wav2vec2_large_english_fp16.safetensors | wav2vec2 (chinese-base): Apache-2.0 (unverified) |

### workflows/wan21_infinitetalk_vocal_sep.api.json
| file | license |
|---|---|
| MelBandRoformer_fp32.safetensors | MelBand RoFormer vocal separation: license UNVERIFIED |
| Wan2_1-I2V-14B-480p_fp8_e4m3fn_scaled_KJ.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| clip_vision_h.safetensors | UNVERIFIED |
| lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wav2vec2-chinese-base_fp16.safetensors | wav2vec2 (chinese-base): Apache-2.0 (unverified) |

### workflows/ui/ltx2_audio_to_video.ui.json
| file | license |
|---|---|
| LTX2_audio_vae_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| LTX2_video_vae_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| gemma_3_12B_it_fp8_scaled.safetensors | Gemma Terms of Use (unverified) |
| ltx-2-19b-distilled_transformer_only_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2-19b-embeddings_connector_distill_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |

### workflows/ui/ltx23_image_audio_to_video.ui.json
| file | license |
|---|---|
| gemma-3-12b-it-abliterated_lora_rank64_bf16.safetensors | Gemma Terms of Use (unverified) |
| gemma_3_12B_it_fp4_mixed.safetensors | Gemma Terms of Use (unverified) |
| ltx-2.3-22b-dev-fp8.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx-2.3-spatial-upscaler-x2-1.1.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |
| ltx_2.3_22b_distilled_1.1_lora_dynamic_fro09_avg_rank_111_bf16.safetensors | Lightricks LTX-2 license (NOT an OSI-approved open-source license; open weights with use restrictions - read it; copy at RahmelJackson/frameforge-studio workflows/native/LTX-LICENSE.txt) |

### workflows/ui/wan22_14b_s2v.ui.json
| file | license |
|---|---|
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan2.2_s2v_14B_fp8_scaled.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wav2vec2_large_english_fp16.safetensors | wav2vec2 (chinese-base): Apache-2.0 (unverified) |

### workflows/ui/wan21_infinitetalk.ui.json
| file | license |
|---|---|
| Wan2_1-I2V-14B-480p_fp8_e4m3fn_scaled_KJ.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| Wan2_1_VAE_bf16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan2.1_infiniteTalk_multi_fp16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| wav2vec2-chinese-base_fp16.safetensors | wav2vec2 (chinese-base): Apache-2.0 (unverified) |

### workflows/ui/wan21_infinitetalk_music.ui.json
| file | license |
|---|---|
| Wan2_1-InfiniTetalk-Single_fp16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| Wan2_1_VAE_bf16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| clip_vision_h.safetensors | UNVERIFIED |
| lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| umt5-xxl-enc-bf16.safetensors | T5: Apache-2.0 (unverified) |
| wan2.1_i2v_480p_14B_fp16.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |

### workflows/ui/humo.ui.json
| file | license |
|---|---|
| humo_17B_fp8_e4m3fn.safetensors | HuMo (ByteDance): Apache-2.0 per upstream (UNVERIFIED) |
| lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors | lightx2v Lightning LoRA: Apache-2.0 (unverified) |
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | T5: Apache-2.0 (unverified) |
| wan_2.1_vae.safetensors | Wan 2.1 / VACE: Apache-2.0 (unverified) |
| whisper_large_v3_fp16.safetensors | Whisper: MIT (unverified for this build) |
