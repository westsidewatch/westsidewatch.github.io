# Doré local speaker cover — Mac mini M4 / 16GB

This is the first **one-cover** local proof. It does not modify Olive Mountain production and does not require a paid API.

## 1. Prepare a reproducible job

From the repository root:

```sh
python3 scripts/prepare_dore_local_image_job.py --speaker david-pawson
```

Outputs in `local/dore-speaker-jobs/david-pawson/`:
- `design-spec.json`: canonical identity and layout constraints
- `image-prompt.txt`: full background-only image prompt
- `job.json`: input/output contract and local execution checklist
- `typography-proof.svg`: deterministic structural proof, not final art

## 2. Render locally

Use **Draw Things** on the Mac (or another locally installed Metal image model). Start with a model that fits 16GB and generate **one 3:4 image at a time**. Paste the entire `image-prompt.txt` as the positive prompt. Save the generated background to:

`local/dore-speaker-jobs/david-pawson/generated-background.png`

Do not generate speaker likenesses or put Chinese text inside the AI image. Do not claim that the repo automatically drives Draw Things: the first local handoff is manual until a documented supported integration is verified.

## 3. Composite final typography

```sh
python3 -m pip install Pillow
python3 scripts/composite_dore_speaker_cover.py --job local/dore-speaker-jobs/david-pawson
```

Optional: `--font /path/to/licensed/chinese/font.ttf`. This is a temporary proof compositor and does **not** claim to implement all site typography tokens. It writes `final-cover.png`.

## 4. Acceptance

Check actual generated image subject and composition, 720×960 dimensions, readable Chinese name, olive-green and white palette, no fictional portrait, visual quality at mobile thumbnail scale, and compare against Mono Color precedent. Reject weak results instead of shipping generic geometric placeholders.

## Boundaries

The design compiler and compositor are executable locally, but **no local model has been installed or run from GitHub**. A generated image only exists after the user executes the local model and provides its output. No automatic production publishing.
