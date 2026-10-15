# 十字架的影子 — Existing Asset Recovery / 既有資產恢復登記

Status: DISCOVERY IN PROGRESS — do not replace original assets or infer missing code is deleted.
Date: 2026-10-15

## Confirmed on GitHub main

1. `docs/dore/film/DORÉ-FILM-PRODUCTION-HANDBOOK.md` — original full-record creative brief, including Christ-centered golden engraving line, typology, Genesis-to-Revelation scope. Preserve original wording.
2. `docs/dore/film/camera-spine-experiment-01.html` — existing executable camera motion lab. Current file is present and nonempty. Earlier creation commit: `cc177f5a7a808b7ee7f369bfcf1c5d7397d19e83`.
3. `docs/dore/film/tools/import-camera-spine.py` — Blender camera spine importer, source-of-truth JSON `camera-spine-experiment-01.json`. Earlier creation commit: `be9a017e7e7fb9d3a53be902689e5cf4af370696`.
4. `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md` — canonical project register.

## Historical implementation pointers
- `1223476ee908317d6eb407bc144156cdd13345bc` — “DORÉ FILM: automate Camera Spine parity gate”.
- Further historical investigation required for track preprocessing, pixel reprojection, seam/tear metrics, off-axis anchors, unseen-region completion, canonical re-lock and Italian black-and-white cinema art direction. **Not yet verified in code.**

## Current Living Water counterpart
- Approved static SVG: `static/experiments/assets/living-water-contour-engraving-v10.svg`.
- v1 visually confirmed moving: `static/experiments/living-water-motion-study.html`.
- v2 visible but movement too subtle: `static/experiments/living-water-motion-flow-v2.html`.
- v1 checkpoint: `docs/design/LIVING-WATER-MOTION-V1-CHECKPOINT.md` on church editorial preview branch.

## Integration principles
- Recover first, evaluate second, integrate third. No parallel new film engine.
- Precomputed camera trajectory and image-space processing stay in film pipeline; local living engravings can supply web runtime and/or pre-rendered moving materials.
- Preserve original composition, original text, approved v10, and all working film experiments.
- Do not assert historical tear metrics or confirmed Italian cinema reference list without locating the evidence.

## Next discovery actions
1. Locate Camera Spine JSON and parity gate implementation; verify execution and data contracts.
2. Search commit history and branches for seam/tear and reprojection work.
3. Recover black-and-white Italian cinema visual reference and grading specification.
4. Build an evidence-based asset map with exact paths, commits and tests before changing runtime.
