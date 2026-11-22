# Example: story-short-30s

Manifest: `story-short-30s.manifest.json`. It validates with `python3 scripts/direct.py validate references/examples/story-short-30s.manifest.json`. Dry-run it with `run … --dry-run` (no network).

## Brief
> make me a video about a lighthouse keeper who finds a message in a bottle

- kind story, 30 s, 16:9 @ 24 fps, deliverables 16:9, 9:16, captions sidecar, commercial use False
- style: painterly 35mm film still, muted teal and amber, soft dusk light, shallow depth of field
- defaults filled: aspect 16:9, fps 24, captions sidecar, narration + music + sfx
- target: google_colab L4 (24 GB), budget 60 GPU-min

## Tier: **standard**
24 GB rules out max (needs 40); standard est fits 60 GPU-min

Why standard: a 24 GB L4 on Google Colab rules out max. The human plan gate lets the user approve the beats before any render. s04 chains from s03 (the bottle reveal). s06 uses first and last frame to land on the boat light.

## Caps
| still_retries | still_variants | video_retries | continuity_regens | max_renders | pass_mean | pass_min |
|---|---|---|---|---|---|---|
| 2 | 1 | 1 | 1 | 40 | 3.5 | 3 |

Gates: bible=auto, plan=human, spend=auto, final=auto

## Shot plan and routing
| shot | t | dur | type | camera | still route → skill | video route → skill | fallback | notes |
|---|---|---|---|---|---|---|---|---|
| s01 | 0.0 | 5 | establishing | static locked-off | still.klein → flux3-klein-stills | video.i2v → ltx25-image-to-video | video.i2v_se | VO “Every night for eleven years, Mara kept the light.”; strength1 1.0 |
| s02 | 5.0 | 5 | character | slow push-in | still.klein → flux3-klein-stills | video.i2v → ltx25-image-to-video | video.i2v_se |  |
| s03 | 10.0 | 5 | action | handheld drift | still.klein → flux3-klein-stills | video.i2v → ltx25-image-to-video | video.i2v_se |  |
| s04 | 15.0 | 5 | insert | static locked-off | still.klein → flux3-klein-stills | video.i2v → ltx25-image-to-video | video.i2v_se | chain from s03; VO “Inside was a letter. It had her name on it.”; strength1 1.0 |
| s05 | 20.0 | 5 | character | slow push-in | still.klein → flux3-klein-stills | video.i2v → ltx25-image-to-video | video.i2v_se |  |
| s06 | 25.0 | 5 | establishing | slow crane up | still.klein → flux3-klein-stills | video.i2v_se → ltx25-image-to-video | - | VO “Someone out there had been watching the light, too.” |

## Audio and post
- voiceover: `audio.voice` {}
- music: `audio.music` {"tags": "sparse solo piano and cello, 70 bpm, melancholic then hopeful, no vocals", "lyrics": "[instrumental]"}
- sfx: `audio.sfx` {"prompt": "pebbles shifting under boots, small wave wash on a stony beach", "seconds": 5}
- sfx: `audio.sfx` {"prompt": "distant foghorn over open sea, long reverb", "seconds": 5}
- post: `post.grade`
- assembly: xfade 0.3, captions sidecar, exports ['16:9/crop', '9:16/crop']
