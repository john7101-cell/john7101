---
name: shot-qc
description: Model-free quality control for rendered shots and final cuts using ffprobe/ffmpeg measurements: duration, aspect, audio present, frozen frames, black frames, hard-cut count, flicker, soft (blurry) frames and clipped highlights/shadows, with a 0-100 score. Use after every video render and before delivery; numbers override VLM descriptions.
---

# shot-qc

These are measurements, not opinions. When a vision-model judge (`still-qa`) and the numbers disagree about motion, freezes or black frames, **trust the numbers and say so**. agentY's director applies the same rule.

## scripts/shot_qc.py (original, stdlib + ffmpeg/ffprobe)
`python scripts/shot_qc.py <video> [--duration 5] [--ratio 16:9] [--audio] [--fps 24] [--json]`

| check | ffmpeg source | flag when |
|---|---|---|
| duration | ffprobe | off by more than max(0.6 s, 5%) |
| aspect | ffprobe | off by more than 3% |
| audio | ffprobe | `--audio` is set and there is no audio stream |
| frozen frames | `freezedetect` (n=0.003, d=0.5) | any freeze of 0.5 s or more. Exempt when the shot is meant to be static: use `--static` |
| black frames | `blackdetect` (d=0.1) | any |
| hard cuts | `select=gt(scene,0.35)` | more than 0 inside one shot |
| flicker | `signalstats` YAVG frame-to-frame | the 95th-percentile luma jump is above 12 (0–255) |
| soft frames | `blurdetect` (ffmpeg 6+; skipped if missing) | the median blur is above 8 |
| clipping | `signalstats` YMAX/YMIN | 5% or more of frames at YMAX ≥ 250 or YMIN ≤ 5 |

**Score:** start at 100 and subtract the weight of each flag (duration 15, aspect 15, audio 10, freeze 20, black 20, cuts 15, flicker 15, soft 10, clipping 5), with a floor of 0. Pass when the score is 70 or more and there are no freeze or black flags.

The thresholds are starting values and are **unverified** on a large set. Tune them per project in the manifest log.

## scripts/hyperkut_export_qc.py
This is HyperKut-Studio's export gate (MIT, copied, with its import adapted to `media_info.py`). It reports duration, ratio, missing audio and remix cut-count drift as warning codes. Run `python scripts/hyperkut_export_qc.py <video> --duration 15 --ratio 9:16 --audio`.

## Provenance
NovaField's `shot_qc.py` (AGPL-3.0) covers a similar check list. It was used **only** as a design reference, its code was not copied, and `shot_qc.py` here is an independent implementation built on standard ffmpeg filters.

## In video-director
After each video attempt, run `shot_qc.py`. Treat a freeze or black flag as a failed attempt that counts against `video_retries`. Run it again on the final cut with `--duration length_s --ratio aspect --audio`.
