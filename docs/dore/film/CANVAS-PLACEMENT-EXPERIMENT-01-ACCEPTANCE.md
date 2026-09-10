# DORÉ FILM — Canonical Canvas Placement Experiment 01

Status: **OBJECTIVE ENGINEERING PASS / VISUAL DIRECTOR REVIEW REQUIRED**  
Experiment: `DF-CANVAS-EXP-01`  
Camera Spine: `DF-CAM-EXP-01`  
Passage: Abraham → Isaac → Jacob

## Purpose

Prove the camera-first production order with real canonical Doré originals:

> 先計算鏡頭位置，再去鋪畫布。

The camera is not created to match a selected picture. The existing Camera Spine remains primary; each canonical original is placed into the world so the camera encounters it at an authored point.

## First canonical anchors

| Anchor | Doré ID | Canonical title | Camera node | Function |
|---|---:|---|---|---|
| A001 | 011 | Abraham Journeying into the Land of Canaan | P001 | departure-world |
| A002 | 019 | The Meeting of Isaac and Rebekah | P008 | generation-arrival |
| A003 | 021 | Jacob's Dream | P020 | vertical-attention |

All IDs, canonical titles and filenames are resolved from the locked ONE Doré Original Library. No generated substitute is permitted.

## Engineering pass conditions now satisfied

1. Placement data is separate from and subordinate to the Camera Spine.
2. All three Doré IDs and filenames are exact registry matches.
3. Frame nodes P001, P008 and P020 exist in the same 20-node Camera Spine.
4. One camera / zero conventional cuts remains intact.
5. `goldenLightEnabled`, `lifeAnimationEnabled`, `scriptureEnabled`, `nvsEnabled`, and `full3DEnabled` remain false.
6. Full original composition is fitted without changing image aspect ratio.
7. Placement is solved from camera position + look target + lens + viewport + source-image aspect + desired distance/fill.
8. Three.js vertical FOV is derived correctly from the authored focal length and viewport aspect.
9. The Canvas Lab uses control-point parameterization (`curve.getPoint`) so an authored frame node resolves to that exact Camera Spine node rather than a merely equal arc-length fraction.
10. GitHub Actions workflow `DORÉ FILM Canonical Canvas Placement` completed successfully for the validation gate.
11. A direct `gh-pages` copy exists at `/dore/film/canvas-motion-lab-01.html`; it is not a loader wrapper.
12. `ONE-ASSET-LIBRARIES-MASTER.md` remained untouched and locked.

## What has deliberately NOT been added

- no golden Light Engine
- no grace/life animation
- no Scripture emergence
- no character animation
- no NVS
- no Full 3D reconstruction
- no AI-generated Doré replacement
- no sound

The experiment must answer the canvas/camera question before any later layer can hide a weak result.

## Visual director review question

Does the viewer feel that one camera **discovers** Abraham, Isaac/Rebekah and Jacob's Dream in an already-existing world, or does it still feel like three pictures being presented in sequence?

A successful Canonical Frame Moment has this rhythm:

`approach world → composition gathers → exact Doré original resolves → hold full canonical composition → camera departs without a cut`

If that rhythm is visually convincing, Experiment 01 can be frozen and the next whole production stage can begin: first Light-on-Canvas experiment. If not, modify placement distance/fill/orientation and Camera Spine approach/departure geometry before adding any new visual capability.

## Public lab

`https://westsidewatch.github.io/dore/film/canvas-motion-lab-01.html`

Repository-side publication is confirmed. Browser-side texture/WebGL behavior still requires visual inspection; do not infer visual PASS from CI alone.
