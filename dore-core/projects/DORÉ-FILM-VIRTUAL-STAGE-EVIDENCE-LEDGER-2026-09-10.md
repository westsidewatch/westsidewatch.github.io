# DORÉ FILM VIRTUAL STAGE — EVIDENCE LEDGER

Date: 2026-09-10
Status: ACTIVE_PARALLEL / EXPERIMENTAL_IMPLEMENTATION
Sweep parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
P01 impact: NONE

## Objective

Evaluate whether Doré can move from flat/slideshow treatment of original works toward a continuous spatial film language in which one camera can leave one canonical Doré image, traverse world-space, and arrive at another without a cut or camera reset.

## Bounded implementation evidence

### Commit `91c4060e423b78c68fc836257e7e47589541c442`

Introduced `.github/workflows/dore-film-virtual-stage-011-019.yml` with:

- canonical Doré 011 and 019 source retrieval;
- Blender-based shallow virtual-production walls;
- one continuous camera path across 128 frames at 24 fps;
- bridge geometry between two projected image surfaces;
- MP4 encoding plus contact-sheet evidence artifacts;
- explicit acceptance criterion: leave Doré 011 spatially and arrive at Doré 019 without cut/slideshow reset.

This is real executable workflow code, not a concept memo.

### Commit `da8e8136f9d592a0d7bcfd8109541ccc3b4dfb6a`

Corrected the first implementation's source-preservation weaknesses by replacing ambiguous generated-grid UV behavior with:

- explicit XY wall geometry;
- explicit UV map;
- front-facing wall orientation;
- canonical image-aspect preservation;
- `CLIP` texture extension;
- updated acceptance language requiring Doré 011 to be recognizable at opening and Doré 019 recognizable at arrival.

This correction is meaningful evidence of visual-production iteration rather than proof of final quality.

### Commit `316cda12142279a14a8c7a734929382a80f3eb47`

Extended the same experiment from a two-anchor road test to a three-anchor Camera Spine (`011 → 019 → 021`) in one uninterrupted 210-frame camera path. The workflow:

- fetches three canonical Doré anchors;
- builds three explicitly UV-mapped shallow walls in one Blender world;
- uses one camera with `camera_resets: 0`;
- states that bridge polish is secondary to recognizable encounter with all three anchors;
- emits MP4, contact-sheet, `.blend` and metadata evidence when the workflow actually runs.

This strengthens the architectural hypothesis that the virtual-stage method is intended to generalize beyond a single pair, but it is still implementation evidence only. The reviewed commit-workflow lookup returned no associated run for this commit, so three-anchor rendered acceptance remains unverified.

## Current evidence boundary

No workflow run is currently associated with the reviewed corrected/two-anchor or three-anchor commits in the available run lookup. Therefore:

- implementation existence: **VERIFIED**;
- corrected workflow definition: **VERIFIED**;
- three-anchor Camera Spine implementation: **VERIFIED**;
- rendered visual acceptance: **UNKNOWN_NEEDS_EVIDENCE**;
- one-camera continuity quality: **UNKNOWN_NEEDS_EVIDENCE**;
- preservation of canonical Doré source appearance in the rendered output: **UNKNOWN_NEEDS_EVIDENCE**;
- reusable film-language capability beyond these bounded tests: **UNKNOWN_NEEDS_EVIDENCE**.

A commit or workflow file must not be promoted to `VERIFIED_COMPLETE` without rendered evidence.

## Classification

`DORÉ-FILM / virtual-stage continuity experiment`: **ACTIVE_PARALLEL / EXPERIMENTAL_IMPLEMENTATION**.

This is not a completed product and not a replacement for the active P01 subtitle critical path.

## What was learned so far

1. Source-image recognizability must be an explicit acceptance condition when canonical artwork is placed into spatial/3D treatment.
2. UV mapping/orientation is not an implementation detail; it directly governs whether the film treatment preserves the source rather than visibly corrupting it.
3. A useful Doré film grammar should distinguish continuous world-space movement from slideshow/crossfade behavior.
4. Rendered artifacts, not workflow definitions, are the required evidence unit for visual-film acceptance.
5. A repeatable film-language claim needs multi-anchor evidence; moving from 011→019 to 011→019→021 is the correct architectural stress direction, but only a rendered run can establish that the camera-spine abstraction actually works visually.

## Debt / revisit trigger

Revisit when a corrected workflow run produces inspectable MP4/contact-sheet artifacts. The next evaluation must judge:

- opening recognizability of 011;
- spatial departure rather than flat image motion;
- bridge continuity;
- arrival recognizability of 019;
- third-anchor recognizability of 021 for the three-anchor spine;
- no cut/camera reset;
- absence of UV/aspect distortion;
- whether the result is actually usable as a repeatable visual-production method rather than a one-off road test.

## Smallest next proof

Run one current three-anchor Camera Spine workflow and persist the resulting MP4/contact sheet plus pass/fail judgment against its own acceptance contract. If it passes, then compare the bounded result to the earlier two-anchor acceptance criteria before claiming reusable film grammar.

No human/environment blocker is established by this ledger; absence of a reviewed run is missing evidence, not a blocker.
