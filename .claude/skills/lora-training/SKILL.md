---
name: lora-training
description: Train a LoRA (character, product, style or motion) for an open-weights image or video model with ostris/ai-toolkit, behind a hard human approval gate on the dataset. Use for "train a LoRA of my product", "make a style LoRA", "teach the model this character". Nothing trains until the user approves the dataset.
---

# lora-training

Train with **ostris/ai-toolkit** (MIT, https://github.com/ostris/ai-toolkit). It is an external install that the user does on the training machine. This skill never installs or runs it for them. The design follows agentY's lora-training skill (MIT, copied to `references/agentY-lora-training.md`; its tool names are agentY-specific). Use open-weights base models only.

## 0. Should this be a LoRA?
Only when an identity, style, product or motion has to come back reliably across many prompts. For a single look, use a reference image with `image-edit` (Qwen edit) or `fix.edit` instead. It is cheaper and needs no training.

## 1. Build the dataset (`scripts/dataset_check.py`)
`python scripts/dataset_check.py <folder> --kind character|product|style|motion [--trigger tok]`. It is stdlib only and reads nothing over the network. It checks:
- the item count against the targets (character 15–40, product 15–30, style 25–60, motion 10–30 clips of 2–5 s)
- for each item, a matching `<name>.txt` caption
- exact duplicates (by sha256) and empty captions
- tiny images (PNG/JPEG headers are read for the size)
- whether a caption contains the trigger word, which it should not, because the trainer prepends it

It writes `dataset.json` (items, warnings and a `sha256` of the whole set) and prints the warnings.

**Captions** describe what should stay *changeable*: setting, pose, clothes, light, camera, motion. They do **not** describe what the LoRA must learn (the face, the product's shape, the style's look). Write natural sentences for FLUX.2, Qwen and Z-Image. For video, write subject, action and camera move in one paragraph.

## 2. Gate: the user approves the dataset (hard)
Show the user a contact sheet (`ffmpeg -pattern_type glob -i '<folder>/*.png' -vf tile=6x6,scale=1600:-1 sheet.png`) plus the trigger word and the warnings. **End your turn and wait.** Never approve on the user's behalf.
- When the user says yes: `python scripts/dataset_check.py <folder> --approve "<their words>"` writes `APPROVED.json` with the dataset hash.
- If any file changes after that, the hash no longer matches and the approval is void.

## 3. Config and command (`scripts/aitoolkit_config.py`)
`python scripts/aitoolkit_config.py <folder> --model flux2_klein_4b|qwen_image|wan22_14b|ltx2 --trigger tok --out train.yaml`
- It **refuses** to run without a valid `APPROVED.json` whose hash matches the current files.
- It writes an ai-toolkit-style YAML with the preset steps, rank and learning rate, and prints the command (`python run.py train.yaml` inside the user's ai-toolkit checkout). It does not run the command.
- The presets are starting points and are **unverified**. Check the field names against the ai-toolkit `config/examples/` for the version the user has installed.

| preset | steps | rank | lr | VRAM (unverified) | base weights license |
|---|---|---|---|---|---|
| flux2_klein_4b | 2000 | 16 | 1e-4 | ~16–24 GB | check the model card (unverified) |
| qwen_image | 2500 | 16 | 1e-4 | ~24 GB+ | Apache-2.0 (unverified) |
| wan22_14b | 2000 | 32 | 1e-4 | 24–48 GB | Apache-2.0 (unverified) |
| ltx2 | 2000 | 32 | 1e-4 | ~32 GB INT8 (agentY notes this is uncertain) | Lightricks LTX-2 license (not OSI) |

Training occupies the GPU for minutes to hours. On Google Colab it spends compute units, so **ask before starting** and show the estimate.

## 4. Test
Copy the LoRA to `ComfyUI/models/loras/`. Render the same prompts and seed at strength 0, 0.8 and 1.0 using the base model's usual graph (for example `flux3-klein-stills`), then judge them with `still-qa`.
- **Under-trained:** the trigger word does nothing.
- **Overfit:** the subject appears without the trigger word, or the training backgrounds repeat. Use an earlier checkpoint or fewer steps.

Register the result in the video-director manifest's `bible.cast[].lora`. Note that this field is free text in `log`, not part of the schema.
