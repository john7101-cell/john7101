# Example: music-video-20s

Manifest: `music-video-20s.manifest.json`. It validates with `python3 scripts/direct.py validate references/examples/music-video-20s.manifest.json`. Dry-run it with `run … --dry-run` (no network).

## Brief
> music video snippet for my track 'Neon Chorus' - singer in a rainy neon alley

- kind music-video, 20 s, 9:16 @ 24 fps, deliverables 9:16, captions burned, commercial use False
- style: neon noir, magenta and cyan, wet reflections, anamorphic flares
- defaults filled: fps 24, captions burned (lyrics)
- target: google_colab T4/L4 (unknown) (16 GB), budget 25 GPU-min

## Tier: **draft**
16 GB and 25 GPU-min only fit draft

Why draft: 16 GB, 25 GPU-min and 10 Google Colab compute units. Video retries and continuity regens are 0, so failures are reported, not re-rendered. The user's track drives the music, so ACE-Step is skipped. Lip-sync uses Wan InfiniteTalk (`video.lipsync_wan`) per vocal line. Lyrics are burned in from `make_srt.py`.

## Caps
| still_retries | still_variants | video_retries | continuity_regens | max_renders | pass_mean | pass_min |
|---|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 20 | 3.0 | 2 |

Gates: bible=auto, plan=auto, spend=human, final=auto

## Shot plan and routing
| shot | t | dur | type | camera | still route → skill | video route → skill | fallback | notes |
|---|---|---|---|---|---|---|---|---|
| s01 | 0.0 | 4 | establishing | slow push-in | still.flux2_4b → flux3-klein-stills | video.i2v → ltx25-image-to-video | video.i2v_se |  |
| s02 | 4.0 | 4 | performance | static locked-off | still.flux2_4b → flux3-klein-stills | video.lipsync_wan → lip-sync | - | +video.lipsync_wan; lyric “Neon chorus, sing it back to me”; strength1 1.0 |
| s03 | 8.0 | 4 | broll | whip pan | still.flux2_4b → flux3-klein-stills | video.i2v → ltx25-image-to-video | video.i2v_se |  |
| s04 | 12.0 | 4 | performance | handheld drift | still.flux2_4b → flux3-klein-stills | video.lipsync_wan → lip-sync | - | chain from s02; +video.lipsync_wan; lyric “Every light in the city knows my name” |
| s05 | 16.0 | 4 | broll | slow crane up | still.flux2_4b → flux3-klein-stills | video.t2v → ltx25-image-to-video | video.i2v |  |

## Audio and post
- music: `audio.music` {"file": "neon-chorus-mv/inputs/neon_chorus_chorus.wav"}
- assembly: xfade 0.0, captions burned, exports master only
