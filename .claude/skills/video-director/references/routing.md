# Routing table

`video-director` routes every task through this table. `scripts/direct.py` reads it directly: it parses every line that starts with `| ` and has 9 cells, after the header row.

## Row format (adding a skill = adding one row)
`| id | stage | need | skill | workflow | inputs | requires | fallback | tiers |`

| Column | Meaning |
|---|---|
| `id` | A unique route id, `<stage>.<name>`. Manifest shots refer to routes by this id. |
| `stage` | One of `plan`, `still`, `still-fix`, `video`, `video-fix`, `transition`, `vfx`, `audio`, `qa`, `post`, `assembly`. |
| `need` | Plain words the agent matches a shot's need against. |
| `skill` | A folder name under `skills/`. It must exist. |
| `workflow` | A file in that skill's `workflows/`, or `script:<file>` for a file in its `scripts/`, or `-` when the skill is instructions only. |
| `inputs` | `role=node.input` pairs separated by `; `. One role may set several nodes, separated by `,`. Roles: `prompt image last_image video audio voice seed width height frames fps text lyrics tags seconds strength1 strength2 mask preset negative tracks`. Graphs with `{{PLACEHOLDER}}` strings (motionfield, forkfield) take UPPERCASE job params (for example `"MOVES": "arc-left-45"`) plus `workflows/<file>.defaults.json`. That sidecar can also set `fps` and `frame_rule: 4n+1` for Wan graphs. `direct.py` refuses to submit if any placeholder is left unfilled. `api/<name>.api.json` files are the Comfy-Org UI templates converted to API format with ComfyUI's own frontend (`graphToPrompt`); see `references/ui-to-api.md` in google-colab-runner. A `-` workflow on a video row means no API graph exists yet. |
| `requires` | The main open-weights models (for people; preflight decides whether they are actually available). |
| `fallback` | The route id to try when preflight says this workflow isn't ready, or `-`. Chains are followed until a ready route is found, or the step is marked `blocked`. |
| `tiers` | The tiers where this route is preferred: `draft`, `standard`, `max` (comma list) or `*`. |

To plug in a new skill: create `skills/<new>/`, then add **one row** here. If it should replace an existing route as the preferred option for a tier, set that row's `tiers` and point the old route's `fallback` at it. Nothing else changes.

## Routes
| id | stage | need | skill | workflow | inputs | requires | fallback | tiers |
|---|---|---|---|---|---|---|---|---|
| plan.bible | plan | story bible, cast, look | story-bible | - | - | LLM only | - | * |
| plan.shots | plan | beats, shot list, estimate | shot-planning | - | - | LLM only | - | * |
| plan.preflight | plan | check server nodes and weights | comfyui-preflight | script:preflight.py | - | none | - | * |
| still.klein | still | keyframe, character, establishing | flux3-klein-stills | flux3_klein_distilled_t2i.api.json | prompt=4.text; seed=7.seed; width=6.width; height=6.height | FLUX 3 Klein distilled int8 + qwen3vl_4b | still.flux2_4b | draft,standard |
| still.klein_base | still | hero keyframe, text in frame, layout-heavy | flux3-klein-stills | flux3_klein_t2i.api.json | prompt=18:17.value; seed=18:7.seed | FLUX 3 Klein base int8 + Qwen upsampler | still.klein | max |
| still.flux2_4b | still | keyframe fallback, fast draft | flux3-klein-stills | flux2_klein_t2i_lean.api.json | prompt=74.text; seed=73.noise_seed; width=62.width,66.width; height=62.height,66.height | FLUX.2 Klein 4B fp8 | - | draft |
| still.flux2_9b | still | keyframe alternative | flux3-klein-stills | flux2_klein_9b_t2i.api.json | prompt=6.text; seed=14.noise_seed; width=5.width,13.width; height=5.height,13.height | FLUX.2 Klein 9B (non-commercial, unverified) | still.klein | - |
| fix.edit | still-fix | instruction edit, fix detail, change wardrobe | image-edit | qwen_edit_2511_instruct.api.json | image=41.image; prompt=100.prompt; seed=106.seed | Qwen-Image-Edit 2511 | fix.edit_fast | standard,max |
| fix.edit_fast | still-fix | fast angle or edit | image-edit | qwen_edit_2509_angle_lightning.api.json | image=img1.image; prompt=pos.prompt; seed=k.seed | Qwen-Image-Edit 2509 + Lightning | - | draft |
| fix.angle | still-fix | new camera angle, coverage from master | image-edit | qwen_edit_2511_angles.api.json | image=41.image; seed=106.seed | Qwen-Image-Edit 2511 + multi-angle LoRA | fix.edit_fast | * |
| fix.closeup | still-fix | push-in, close-up coverage | image-edit | qwen_edit_2509_coverage_lightning.api.json | image=img1.image; prompt=pos.prompt; seed=k.seed | Qwen-Image-Edit 2509 | - | * |
| fix.relight | still-fix | relight, time of day | image-edit | qwen_edit_2509_relight.api.json | image=1.image; prompt=11.prompt; seed=14.seed | Qwen-Image-Edit 2509 | - | * |
| fix.outpaint | still-fix | still to other aspect | image-edit | qwen_image_outpaint_format.api.json | image=1.image; prompt=37.text; seed=41.seed | Qwen-Image | - | * |
| fix.tryon | still-fix | product or garment on person | image-edit | qwen_edit_2511_try_on.api.json | image=41.image; prompt=149.prompt; seed=169.seed | Qwen-Image-Edit 2511 | fix.edit | * |
| fix.matte | still-fix | cut out product, transparent background | background-matte | birefnet_image_transparent.api.json | image=1.image | BiRefNet | - | * |
| video.i2v | video | animate keyframe (default) | ltx25-image-to-video | ltx25_i2v_two_pass.api.json | image=395.image; prompt=364.text; width=356.width; height=356.height; frames=356.length; seed=338.noise_seed; strength1=357.strength; strength2=349.strength | LTX-2.5 (Lightricks license, not OSI) | video.i2v_se | * |
| video.i2v_se | video | start and end frame, chained shot | ltx25-image-to-video | ltx25_start_frame_i2v.api.json | image=401.image; last_image=402.image; prompt=900.string_a; width=356.width; height=356.height; frames=356.length; seed=338.noise_seed; strength1=357.strength; strength2=349.strength | LTX-2.5 | - | * |
| video.t2v | video | abstract or b-roll with no keyframe | ltx25-image-to-video | ltx25_t2v.api.json | prompt=900.string_a; width=356.width; height=356.height; frames=356.length; seed=338.noise_seed | LTX-2.5 | video.i2v | draft |
| video.lipsync | video | talking head, presenter, dialogue | lip-sync | ltx23_lipsync_photo.api.json | image=269.image; audio=276.audio; prompt=900.string_a; frames=302.length | LTX-2.3 + Gemma 3 | video.lipsync_wan | * |
| video.lipsync_wan | video | singing, low-VRAM lip sync | lip-sync | wan21_infinitetalk_single.api.json | image=1.image; audio=6.audio; prompt=13.positive_prompt; seed=15.seed | Wan 2.1 + InfiniteTalk GGUF | - | * |
| video.redub | video-fix | re-dub existing clip | lip-sync | ltx23_ic_lora_lipdub_video.api.json | video=7.file; prompt=11.text | LTX-2.3 lipdub IC-LoRA | - | * |
| vfx.restyle | vfx | restyle clip keep motion | restyle | ltx_ic_lora_depth_restyle.api.json | video=src.video; prompt=pos.text; seed=noise.noise_seed | LTX IC-LoRA union + Qwen edit | vfx.motion | max |
| vfx.motion | vfx | drive photo with reference motion | restyle | ltx25_motion_guide.api.json | video=199.file; image=200.image | LTX-2.5 | - | * |
| vfx.onetake | vfx | fire, freeze, hologram, portal effect | one-take-vfx | one_take_vfx_preset_node.api.json | video=load_video.video; preset=preset.preset; seed=noise.noise_seed | LTX-2.5 + IC-LoRA union | - | standard,max |
| vfx.remove | video-fix | remove object, clean rig or logo | video-inpaint-remove | ltx23_inpaint_remove.api.json | video=source.filename; mask=source.mask_filename; prompt=positive.text; seed=noise.noise_seed | LTX-2.3 in/outpaint IC-LoRA + SAM 2 | vfx.remove_wan | standard,max |
| vfx.remove_wan | video-fix | remove object (light) | video-inpaint-remove | wan_vace_inpaint_remove.api.json | video=source.filename; mask=source.mask_filename; prompt=positive.text; seed=sample.seed | Wan 2.1 VACE 1.3B | - | draft |
| vfx.swap | video-fix | recast person, swap face or product | character-swap-h3 | h3_swap_simple.api.json | video=5.video; image=2.image; seed=11.seed | MiniMax H3 local weights (license unverified) | vfx.swap_ltx | max |
| vfx.swap_ltx | video-fix | open swap fallback | character-swap-h3 | ltx23_motion_swap_open_fallback.api.json | video=1.file; image=2.image; prompt=3.text; seed=5.noise_seed | LTX-2.3 masked r2v + SAM 3.1 | - | * |
| vfx.matte_video | post | remove video background | background-matte | birefnet_video_background.api.json | video=1.file | BiRefNet | - | * |
| vfx.comp | post | composite generated element on plate | background-matte | platelock_comp.api.json | video=1.file | PlateLock nodes | - | * |
| transition.flf | transition | bridge two shots, morph, match cut | shot-transitions | seam_ltx25_flf2v_transition.api.json | image=31.image; last_image=39.image; prompt=251:252.value | LTX-2.5 22B int8 (~31 GB peak VRAM) | transition.cut | max |
| transition.cut | transition | plain cut or crossfade | film-assembly | - | - | none | - | draft,standard |
| audio.voice | audio | narration, voice-over | voiceover | voice_chatterbox_multilingual.api.json | text=1.text; voice=2.audio; seed=1.seed | Chatterbox Multilingual (MIT) | - | * |
| audio.music | audio | music bed, song | music-sfx | music_ace_step15.api.json | tags=4.tags; lyrics=4.lyrics; seconds=6.seconds; seed=4.seed | ACE-Step 1.5 | audio.music_mm | * |
| audio.music_mm | audio | music fallback | music-sfx | music_minimax_music3.api.json | tags=13.caption; lyrics=13.lyrics | MiniMax Music 3 (license unverified) | - | - |
| audio.sfx | audio | sound effect, ambience | music-sfx | sfx_stable_audio_open.api.json | prompt=3.text; seconds=5.seconds; seed=6.seed | Stable Audio Open 1.0 | audio.sfx3 | * |
| audio.sfx3 | audio | sfx fallback | music-sfx | sfx_stable_audio_3.api.json | prompt=6.text; seconds=11.seconds; seed=3.seed | Stable Audio 3 | - | - |
| qa.still | qa | judge keyframe or frame | still-qa | script:judge.py | - | open VLM (Qwen2.5-VL) | - | * |
| qa.continuity | qa | check joins between shots | continuity-check | - | - | open VLM | - | * |
| post.upscale | post | final upscale of approved shot | video-upscale | seedvr2_video_upscale.api.json | video=1.file; seed=109.seed | SeedVR2 3B | - | max |
| post.interp | post | slow motion, higher fps | frame-interpolation | film_frame_interpolation.api.json | video=1.file | FILM | - | * |
| post.reframe | post | vertical or square deliverable without crop | reframe-aspect | ltx23_video_reframe.api.json | video=1.file; prompt=5138.text; width=12.value; height=13.value; seed=5117.noise_seed | LTX-2.3 outpaint IC-LoRA | assembly.cut | max |
| post.grade | post | LUT, lens, camera shake, letterbox | camera-lens-lut | backlot_direct.api.json | video=1.file | none (post nodes) | - | standard,max |
| post.captions | post | captions, subtitles | subtitles-captions | script:make_srt.py | - | none (ASR optional) | - | * |
| assembly.cut | assembly | final edit, audio mix, export | film-assembly | script:assemble.py | - | ffmpeg | - | * |
| plan.lora | plan | recurring identity, product or style needs a LoRA (human dataset gate) | lora-training | script:dataset_check.py | - | ai-toolkit (external) + open base model | - | - |
| plan.previs_passes | plan | 3D blocking to OpenPose, depth and camera passes | previs-control-passes | script:binding_apply.py | - | Motion Previs Studio app (external, WebGL) | plan.previs | - |
| plan.dispatch | plan | spread shots over several GPUs or servers | multi-gpu-dispatch | script:dispatch.py | - | none (ComfyUI-Distributed or raylight optional) | - | - |
| fix.relight_lights | still-fix | placed lights, match plate lighting | relighting | klein_relight_normals.api.json | prompt=4.text; image=10.image; seed=23.noise_seed | FLUX.2 Klein + Depth Anything 3 (license per file) | fix.relight | max |
| control.pose | video | follow pose or blocking from a clip (previs or reference performance) | control-to-video | wan_vace_pose_control.api.json | prompt=4.text; video=6.video,40.video; width=6.custom_width,9.width; height=6.custom_height,9.height; frames=6.frame_load_cap,9.length; fps=6.force_rate,13.frame_rate; seed=10.seed | Wan 2.1 VACE 14B + DWPose ONNX | video.i2v | - |
| control.canny | video | follow layout or edges from a clip | control-to-video | wan_vace_canny_control.api.json | prompt=4.text; video=6.video,40.video; width=6.custom_width,9.width; height=6.custom_height,9.height; frames=6.frame_load_cap,9.length; fps=6.force_rate,13.frame_rate; seed=10.seed | Wan 2.1 VACE 14B | control.pose | - |
| control.ltx | video | pose control on LTX-2 (official Comfy-Org template, converted to API) | control-to-video | api/ltx2_pose_to_video.api.json | prompt=143:124.text; negative=143:119.text; image=160.image; video=185.file; seed=143:126.noise_seed; width=166.value; height=167.value; frames=168.value; fps=143:145.value | LTX-2 19B (Lightricks license, not OSI) | control.pose | - |
| control.ltx_canny | video | canny edge control on LTX-2 (official template, converted to API) | control-to-video | api/ltx2_canny_to_video.api.json | prompt=143:124.text; negative=143:119.text; image=160.image; video=127.file; seed=143:126.noise_seed; width=166.value; height=167.value; frames=168.value; fps=143:145.value | LTX-2 19B (Lightricks license, not OSI) | control.canny | - |
| control.ltx_depth | video | depth control on LTX-2 (official template, converted to API) | control-to-video | api/ltx2_depth_to_video.api.json | prompt=143:124.text; negative=143:119.text; image=160.image; video=183.file; seed=143:126.noise_seed; width=166.value; height=167.value; frames=168.value; fps=143:145.value | LTX-2 19B (Lightricks license, not OSI) | control.ltx | - |
| camera.fun | video | exact named camera move from a still (dolly, orbit, crane, whip) | camera-control | wan_fun_camera_i2v.api.json | prompt=4.text; image=6.image; seed=7.seed,21.seed | Wan Fun Camera + CLIP vision | video.i2v | - |
| camera.ati | video | drawn object or camera trajectories (official template, converted to API; `params.tracks` = FL_PathAnimator paths_data JSON) | camera-control | api/wan_ati_trajectory.api.json | prompt=99:16.positive_prompt; image=58.image; seed=99:27.seed; width=110.value; height=111.value; tracks=89.paths_data | Wan 2.1 ATI (WanVideoWrapper) | camera.fun | - |
| video.s2v | video | full-body talking or singing performance driven by audio | audio-driven-motion | wan22_s2v.api.json | prompt=4.text; audio=8.audio; image=10.image; width=11.width; height=11.height; frames=11.length; seed=12.seed; fps=14.frame_rate | Wan 2.2 S2V 14B | video.lipsync_wan | - |
| video.talk_music | video | singer on a full music mix (vocal separation then InfiniteTalk) | audio-driven-motion | wan21_infinitetalk_vocal_sep.api.json | prompt=312.text; image=284.image; audio=125.audio; seed=128.seed | InfiniteTalk (Wan 2.1) + MelBand RoFormer | video.s2v | - |
| video.a2v_ltx | video | LTX-2 audio-to-video from a still and a track (official template, converted to API) | audio-driven-motion | api/ltx2_audio_to_video.api.json | prompt=994:921.text; negative=994:922.text; image=444.image; audio=565.audio; seed=994:978:863.noise_seed; frames=994:855.length | LTX-2 19B (Lightricks license, not OSI) | video.s2v | - |
| vfx.motion_ref | vfx | transfer motion from a reference clip onto a still (IC-LoRA) | ltx-iclora-utils | ltx23_ic_lora_motion.api.json | image=200.image; video=199.file; seed=704.seed | LTX-2.3 22B + motion IC-LoRA (Lightricks license) | vfx.motion | - |
| vfx.effect_ltx | vfx | LTX-2.5 effect from a photo | ltx-iclora-utils | ltx25_effects.api.json | image=395.image; seed=338.noise_seed | LTX-2.5 (Lightricks license) | vfx.onetake | - |
| post.clean_text | post | remove burned-in subtitles (rights-cleared footage only; official template, converted to API) | ltx-iclora-utils | api/ltx23_remove_subtitles.api.json | video=5160.file; seed=5161:5078.noise_seed | LTX-2.3 22B + IC-LoRA (Lightricks license) | - | - |
| post.clean_watermark | post | remove a platform watermark (rights-cleared footage only; converted template) | ltx-iclora-utils | api/ltx23_remove_watermark.api.json | video=5160.file; seed=5161:5078.noise_seed | LTX-2.3 22B + IC-LoRA (Lightricks license) | - | - |
| vfx.recipe_read | vfx | read an effect off a reference clip into a JSON recipe | effect-recipe-read | forkfield_read_effect.api.json | image=1.image | Qwen3-VL 8B int8 | - | - |
| vfx.recipe_apply | vfx | apply a read recipe to the user's photo | effect-recipe-read | forkfield_apply_open_ltx.api.json | image=1.image; seed=22.seed,54.noise_seed | Qwen-Image-Edit + LTX-2 (Lightricks license) | vfx.onetake | - |
| qa.shot | qa | measured QC: freeze, black, cuts, flicker, soft, clipping (overrides VLM) | shot-qc | script:shot_qc.py | - | ffmpeg | - | * |
| plan.previs | plan | prop or set previs mesh, blocking | image-to-3d | trellis2_image_to_3d.api.json | image=1.image | TRELLIS.2 + BiRefNet | - | max |
| plan.connect | plan | submit, poll, fetch, cancel | comfyui-connect | script:comfy_client.py | - | none | - | * |
| plan.google_colab | plan | run on Google Colab: package a notebook bundle, or drive a running Google Colab ComfyUI (CU estimate, spend gate, resume) | google-colab-runner | script:colab.py | - | Google Colab runtime (user account; compute units) | - | * |

## MORE_SKILLS.md
`analysis/MORE_SKILLS.md` proposes 22 candidates, and 10 are now skills in this collection with rows above: video-upscale, frame-interpolation, reframe-aspect, video-inpaint-remove, lip-sync, character-swap-h3, shot-transitions, one-take-vfx, subtitles-captions and background-matte. The other 12 are not built yet. Each one plugs in as a single row at the stage below:

| Candidate | Stage it would add a row to |
|---|---|
| face-restore | still-fix / post |
| product-ad | video, H3-based |
| music-video-beat-cut | assembly |
| kinetic-type | vfx |
| motion-swap-ltx | video-fix (partly covered by `vfx.swap_ltx`) |
| camera-move-verify | qa |
| previs-blocking-3d | plan |
| audio-stems | audio |
| mcp-bridge | plan.connect alternative |
| gpu-queue | plan |
| lora-dataset | plan |
| color-match | post |

## MORE_SKILLS_PASS2.md (pass 2)
`analysis/MORE_SKILLS_PASS2.md` added 10 skills, each with the rows above:

| Skill | Rows |
|---|---|
| lora-training | plan.lora |
| control-to-video | control.pose, control.canny, control.ltx, control.ltx_canny, control.ltx_depth |
| camera-control | camera.fun, camera.ati |
| audio-driven-motion | video.s2v, video.talk_music, video.a2v_ltx |
| previs-control-passes | plan.previs_passes |
| multi-gpu-dispatch | plan.dispatch |
| relighting | fix.relight_lights |
| shot-qc | qa.shot |
| ltx-iclora-utils | vfx.motion_ref, vfx.effect_ltx, post.clean_text, post.clean_watermark |
| effect-recipe-read | vfx.recipe_read, vfx.recipe_apply |
| google-colab-runner | plan.google_colab |

Pass-1 candidates now covered: previs-blocking-3d (`plan.previs_passes`), gpu-queue (`plan.dispatch`), lora-dataset (`plan.lora`) and camera-move-verify (`qa.shot`, measured motion and freezes).
