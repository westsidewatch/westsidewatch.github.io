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

## Recovery pass 2 — verified executable chain (2026-10-15)

All paths below exist on GitHub `main`, not reconstructed substitutes:

- `docs/dore/film/camera-spine-experiment-01.json` — authored `dore-film-camera-spine/v0.1` camera track, **20 nodes P001–P020**, Abraham → Isaac → Jacob, one camera, zero conventional cuts; noncanonical previs experiment. Each node has position `p`, look target, lens, speed, dwell and camera grammar provenance. Two authored time bridges: ABRAHAM_TO_ISAAC and ISAAC_TO_JACOB. References TARR-01 / ANGELOPOULOS-01 / ANTONIONI-01 as camera grammar sources, explicitly **not style presets**.
- `docs/dore/film/tools/camera-spine-timeline.js` — deterministic 52-second target timing solver and sampler, distributing travel time by path distance and authored speed, preserving dwell.
- `docs/dore/film/tools/camera-spine-parity-check.py` — 20-node, one-camera, zero-cut, duration and vector/speed validation. This validates timeline parity; **it is not a seam/tear quality metric**.
- `docs/dore/film/tools/import-camera-spine.py` — Blender importer reading same JSON as source of truth.
- `.github/workflows/dore-film-camera-spine-parity.yml` — existing parity CI workflow.
- `static/dore/film/camera-motion-lab-01.html` — web motion lab, existing live-path source.
- `docs/dore/film/camera-spine-experiment-01.html` — earlier experiment page, also present.
- Historical commits: `bf476a11efa81a6fe3f2bffd3dbece327168efeb` JSON track; `cc177f5a7a808b7ee7f369bfcf1c5d7397d19e83` first executable page; `be9a017e7e7fb9d3a53be902689e5cf4af370696` Blender importer; `3cac5379b15699f8c170d0771c2bcb78f9801e2e` parity script; `1223476ee908317d6eb407bc144156cdd13345bc` parity workflow; `4d51f49fc630ab8a7a7efdefe3c125e7d4130407` authored web timing lab.

### Historical aesthetic provenance (verified in track metadata)
- TARR-01, ANGELOPOULOS-01 and ANTONIONI-01 appear in the camera track. These establish provenance for shot grammar, **not proof of a recovered Italian monochrome grading specification**. That original aesthetic document remains to be located.

### Still unverified
- Exact location of precomputed reprojection / tiny tear evaluation / known-pixel restoration / canonical original re-lock implementation.
- Italian black-and-white film grading/lookbook and its precise decisions.
- Prior referenced `SHADOW-MAP-EDITORIAL-CANON.md` and `SCRIPT-NODE-000-BERESHIT.md` are not found at those paths on main or three `dore-shadow64-*` branches checked. This does **not** establish deletion.

### Preservation action
- This pass only expands the asset register. **No existing camera, film, parity, engraving, or church preview runtime file was modified.**
