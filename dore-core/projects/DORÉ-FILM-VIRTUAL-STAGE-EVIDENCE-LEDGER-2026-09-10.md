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

## Current evidence boundary

No workflow run is currently associated with the corrected commit in the reviewed GitHub run lookup. Therefore:

- implementation existence: **VERIFIED**;
- corrected workflow definition: **VERIFIED**;
- rendered visual acceptance: **UNKNOWN_NEEDS_EVIDENCE**;
- one-camera continuity quality: **UNKNOWN_NEEDS_EVIDENCE**;
- preservation of canonical Doré source appearance in the rendered output: **UNKNOWN_NEEDS_EVIDENCE**;
- reusable film-language capability beyond this 011→019 test: **UNKNOWN_NEEDS_EVIDENCE**.

A commit or workflow file must not be promoted to `VERIFIED_COMPLETE` without rendered evidence.

## Classification

`DORÉ-FILM / virtual-stage continuity experiment`: **ACTIVE_PARALLEL / EXPERIMENTAL_IMPLEMENTATION**.

This is not a completed product and not a replacement for the active P01 subtitle critical path.

## What was learned so far

1. Source-image recognizability must be an explicit acceptance condition when canonical artwork is placed into spatial/3D treatment.
2. UV mapping/orientation is not an implementation detail; it directly governs whether the film treatment preserves the source rather than visibly corrupting it.
3. A useful Doré film grammar should distinguish continuous world-space movement from slideshow/crossfade behavior.
4. Rendered artifacts, not workflow definitions, are the required evidence unit for visual-film acceptance.

## Debt / revisit trigger

Revisit when a corrected workflow run produces inspectable MP4/contact-sheet artifacts. The next evaluation must judge:

- opening recognizability of 011;
- spatial departure rather than flat image motion;
- bridge continuity;
- arrival recognizability of 019;
- no cut/camera reset;
- absence of UV/aspect distortion;
- whether the result is actually usable as a repeatable visual-production method rather than a one-off road test.

## Smallest next proof

Run the corrected workflow once and persist the resulting MP4/contact sheet plus pass/fail judgment against its own acceptance contract.

No human/environment blocker is established by this ledger; absence of a reviewed run is missing evidence, not a blocker.
