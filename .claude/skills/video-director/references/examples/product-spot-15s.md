# Example: product-spot-15s

Manifest: `product-spot-15s.manifest.json`. It validates with `python3 scripts/direct.py validate references/examples/product-spot-15s.manifest.json`. Dry-run it with `run … --dry-run` (no network).

## Brief
> a 15-second spot for our Aurora insulated steel bottle

- kind product, 15 s, 9:16 @ 24 fps, deliverables 9:16, 1:1, 16:9, captions burned, commercial use True
- style: clean premium product commercial, glacier blue and white, crisp studio light, macro detail
- defaults filled: fps 24
- target: local A100 80GB (80 GB), budget 120 GPU-min

## Tier: **max**
80 GB and 120 GPU-min budget fit max

Why max: an 80 GB A100 with a 120 GPU-min budget. Every gate is human because this is a commercial deliverable. **Commercial caveat:** LTX-2 weights are under the Lightricks license (not OSI), so the user must confirm their eligibility. The product reference image drives `fix.edit` on identity fails. s03 adds a OneTake time-freeze VFX pass. The 16:9 export uses `post.reframe`.

## Caps
| still_retries | still_variants | video_retries | continuity_regens | max_renders | pass_mean | pass_min |
|---|---|---|---|---|---|---|
| 3 | 2 | 2 | 2 | 48 | 4.0 | 3 |

Gates: bible=human, plan=human, spend=human, final=human

## Shot plan and routing
| shot | t | dur | type | camera | still route → skill | video route → skill | fallback | notes |
|---|---|---|---|---|---|---|---|---|
| s01 | 0.0 | 4 | product | static locked-off | still.klein_base → flux3-klein-stills | video.i2v → ltx25-image-to-video | video.i2v_se | VO “Cold that lasts.”; strength1 1.0 |
| s02 | 4.0 | 4 | product | slow orbit | still.klein_base → flux3-klein-stills | video.i2v → ltx25-image-to-video | video.i2v_se | chain from s01; VO “Twenty-four hours on the ice.” |
| s03 | 8.0 | 4 | vfx | static locked-off | still.klein_base → flux3-klein-stills | video.i2v → ltx25-image-to-video | video.i2v_se | in: flf; +vfx.onetake; strength1 1.0 |
| s04 | 12.0 | 3 | title | slow push-in | still.klein_base → flux3-klein-stills | video.i2v → ltx25-image-to-video | video.i2v_se | VO “Aurora. Built for cold.” |

## Audio and post
- voiceover: `audio.voice` {}
- music: `audio.music` {"tags": "minimal electronic pulse, 110 bpm, cold shimmering pads, confident, no vocals", "lyrics": "[instrumental]"}
- sfx: `audio.sfx` {"prompt": "ice cracking and freezing, crisp close-up crackle", "seconds": 4}
- assembly: xfade 0.0, captions burned, exports ['1:1/crop', '16:9/reframe']
