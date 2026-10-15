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

## Recovery pass 3 — canonical image-space / anchored-world chain (2026-10-15)

### Verified existing files on main
- `docs/dore/film/DORÉ-ANCHORED-WORLD-ROUTE-01.md` — explicit film acceptance: Doré 011 → camera enters → no plane boundary → coherent off-axis world → return → canonical Doré 011 re-lock. Route specifies A0 authority pixels, A1/A2 off-axis views, GenWarp-class warp/mask/correspondence, sparse Gaussian scaffold, frame depth and canonical composite. **This is a selected production route, not evidence that final tear metric has passed.**
- `docs/dore/film/aw011-anchor-corridor-v1.json` — PRODUCTION_INPUT for Doré 011, original 2617×2074, A0/A1/A2 poses, enter-and-return path A0→A1→A2→A1→A0, provenance labels A_CANONICAL / B_REPROJECTED / C_RECONSTRUCTED / D_INFERRED_UNSEEN.
- `docs/dore/film/tools/aw011-anchor-package.py` — actual provider-neutral camera matrix / adapter job compiler; explicitly no inference in this script.
- `static/dore/film/canvas-motion-lab-01.html` — canonical canvas lab.
- `dore-core/projects/DORÉ-FILM-CAMERA-CANVAS-EVIDENCE-LEDGER-2026-09-10.md` — historical evidence classification; Camera Spine and Canvas Placement objective milestones marked VERIFIED_COMPLETE but director-level visual acceptance withheld.
- `.github/workflows/dore-film-projection-stage-011.yml`, `.github/workflows/dore-film-micro-011-depth.yml`, `.github/workflows/dore-film-micro-011-geometry.yml`, `.github/workflows/dore-film-micro-011-camera.yml`, `.github/workflows/dore-film-two-anchor-handoff-011-019.yml`, `.github/workflows/dore-film-experimental-film-01.yml` — historical workflow files found by commit file lists; runtime/output evidence still needs inspection.

### Historical commit anchors
- `174e17085ee3c9f4ca14b3ddebecf47b153fe7c4` selected anchored-world route.
- `782adb48ec503ab5ae31d222e4b0199195c4e6fb` camera-conditioned anchor corridor.
- `42b4758d30c1d8ea63f2cdb59452fe1bcdb84d31` anchor package compiler.
- `f2c7085c56a3131d704ae77b8cf7bc2ec6933adc` real parallax experiment.
- `06535be49d961d221ef60bd902884937b4fc9ee8` depth geometry experiment.
- `e8b5ae12a82707d5f019541ac91bf753569ea5b4` depth/anchor handoff.
- `5de0d4ee4569fdf8907a79343e6b4c61946b9b8a` experimental film workflow.

### Crucial distinction
The exact original known-pixel/canonical re-lock **policy and adapter contracts are recovered**. We have not yet located proof of a successful near-zero tear metric, accepted rendered frames, or actual synthesized anchor outputs. Do not confuse planned acceptance, compiler success or workflow presence with measured film quality. Continue investigating workflow scripts, artifacts and acceptance records without altering originals.

### Preservation
Documentation-only update. No runtime, motion, camera or source imagery changed.

## Recovery pass 4 — ONE Matthew engraved-water motion (2026-10-15)

**Chapter correction:** Historical implementation is **Matthew chapter 3 (Baptism)**, not verified as chapter 2. Do not relabel it as Matthew 2 without locating another original.

- `static/one/one-baptism-motion.js` — existing live ONE motion runtime; conditionally enables only `?book=40&chapter=3`; injects SVG ripple paths (slow, quick, glints) and light/dove layers. Its animated water is genuine stroke-dashoffset motion, not a CSS-translated still plate.
- `static/one/one-baptism-motion.css` — actual `ripple-slow` (5.6 s), `ripple-quick` (3.7 s), `ripple-glints` (2.8 s) keyframes; grayscale source image and layered light/dove motion; reduced-motion safeguard.
- `dore-core/cloudflare/ASSET-MIGRATION-BATCH-001.json` — governed final asset registry lists `ONE-MAT-03-BAPTISM-COVER-MOTION`, r5-mobile GIF `static/one/share/matthew-03-baptism-motion-r5-mobile.gif`, GitHub blob SHA `8716328e69e194ff314803d0af4ea61aad238555`, expected 7,819,362 bytes. **Registry evidence is not proof that the binary is currently accessible via the file API**; direct fetch returned 404, so storage availability remains to be checked.
- Original implementation commit `29f882e22` (feat(one): animate Matthew 3 cover and share GIF); consolidation commit `afae59f0e` records final r5 and obsolete r2–r4 removal.

### Reuse policy
Recover and test existing ONE ripple code as a reference for the Living Water web animation. Do not transplant the Matthew baptism artwork, bird, chapter-specific imagery, or overwrite the approved v10. Do not duplicate a motion engine until original runtime behavior is verified. ONE chapter 3 remains the canonical owner of this motion asset.
