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

### Commit `5de0d4ee4569fdf8907a79343e6b4c61946b9b8a`

Introduced `.github/workflows/dore-film-experimental-film-01.yml`, advancing the same three-anchor idea into an explicitly editioned 24-second silent film fragment rather than a short camera-spine probe. The workflow:

- keeps the canonical `011 → 019 → 021` anchor sequence;
- uses one Blender world and one camera with `camera_resets: 0`;
- extends the path to 576 frames / 24 seconds at 24 fps, with deliberately slower attention near anchors and faster travel through bridge space;
- varies lens length during the shot rather than resetting the camera;
- keeps bridge geometry deliberately minimal so the experiment judges cinematic continuity rather than set polish;
- renders PNG frames, a 3×3 director review sheet, a `.blend` scene, metadata and an H.264 MP4 artifact;
- explicitly records `generation: false`, `sound: false`, and `acceptance: judge as cinema, not capability demo`.

This is a meaningful product-history transition: Doré Film is no longer only testing whether one camera can technically traverse multiple anchors; it is beginning to test duration, attention rhythm, lens language and edition-level cinematic judgment. However the reviewed commit-workflow lookup returned no associated workflow run for this commit. Therefore the film itself, its review sheet and its visual quality remain unverified.

### 2026-09-11 — Anchored World / AW011 corridor implementation

A later bounded Film branch advances the experiment from hand-authored anchor placement toward an explicit provider-facing Anchored World package around canonical Doré plate 011:

- commit `782adb48ec503ab5ae31d222e4b0199195c4e6fb` defines the AW011 camera-conditioned anchor corridor;
- commit `42b4758d30c1d8ea63f2cdb59452fe1bcdb84d31` adds the AW011 anchor-package compiler;
- commit `5b3621aa12e22f9c76010c14e30e2aa767f9959e` adds `.github/workflows/dore-film-aw011-anchor-corridor.yml` and validation assertions.

The persisted workflow compiles a provider package whose authority anchor is Doré ID 11, uses three corridor anchors `A0/A1/A2`, emits generation jobs only for `A1/A2`, preserves `A0` as identity camera-to-world authority, and requires the enter/return path `A0 → A1 → A2 → A1 → A0`. Its hard rule explicitly states that generation owns absence only. This is important architectural evidence: generated world extension is subordinate to the canonical anchor rather than silently replacing the original image authority.

Connected evidence remains bounded. The reviewed commit has no commit statuses and no associated pull-request workflow runs in the available lookup. Therefore the compiler/workflow contract is **IMPLEMENTED**, but an executed anchor package, provider generation result, camera-conditioned world coherence and returned-to-authority visual acceptance remain **UNKNOWN_NEEDS_EVIDENCE**.

## Current evidence boundary

No reviewed workflow run establishes rendered acceptance for the corrected/two-anchor, three-anchor Camera Spine, Experimental Film 01, or AW011 Anchored World corridor. Therefore:

- implementation existence: **VERIFIED**;
- corrected workflow definition: **VERIFIED**;
- three-anchor Camera Spine implementation: **VERIFIED**;
- Experimental Film 01 workflow/edition definition: **VERIFIED**;
- AW011 authority/corridor/compiler/workflow contract: **VERIFIED_IMPLEMENTED**;
- AW011 executed provider package + generated anchor evidence: **UNKNOWN_NEEDS_EVIDENCE**;
- rendered visual acceptance: **UNKNOWN_NEEDS_EVIDENCE**;
- one-camera continuity quality: **UNKNOWN_NEEDS_EVIDENCE**;
- preservation of canonical Doré source appearance in the rendered output: **UNKNOWN_NEEDS_EVIDENCE**;
- cinematic pacing/lens-language quality over 24 seconds: **UNKNOWN_NEEDS_EVIDENCE**;
- reusable film-language capability beyond these bounded tests: **UNKNOWN_NEEDS_EVIDENCE**.

A commit or workflow file must not be promoted to `VERIFIED_COMPLETE` without executed/rendered evidence.

## Classification

`DORÉ-FILM / virtual-stage continuity + Experimental Film 01 + AW011 Anchored World`: **ACTIVE_PARALLEL / EXPERIMENTAL_IMPLEMENTATION**.

This is not a completed product and not a replacement for the active P01 subtitle critical path.

## What was learned so far

1. Source-image recognizability must be an explicit acceptance condition when canonical artwork is placed into spatial/3D treatment.
2. UV mapping/orientation is not an implementation detail; it directly governs whether the film treatment preserves the source rather than visibly corrupting it.
3. A useful Doré film grammar should distinguish continuous world-space movement from slideshow/crossfade behavior.
4. Rendered artifacts, not workflow definitions, are the required evidence unit for visual-film acceptance.
5. A repeatable film-language claim needs multi-anchor evidence; moving from 011→019 to 011→019→021 is the correct architectural stress direction, but only a rendered run can establish that the camera-spine abstraction actually works visually.
6. Experimental Film 01 adds a second evidence axis beyond continuity: cinematic time. Attention dwell, travel speed and lens changes are now part of the intended grammar, but must be judged from the actual rendered film rather than inferred from keyframes.
7. Edition metadata that explicitly distinguishes `generation: false` from generated imagery is useful provenance and should remain in future film experiments.
8. AW011 sharpens the authority boundary: the canonical anchor remains authoritative while generated material is permitted only to fill absence around it; an enter-and-return camera path is part of the contract rather than an incidental animation choice.

## Debt / revisit trigger

Revisit when a current workflow run produces inspectable MP4/review-sheet or AW011 provider-package/render artifacts. The next evaluation must judge:

- opening recognizability of 011;
- spatial departure rather than flat image motion;
- bridge continuity;
- arrival recognizability of 019;
- third-anchor recognizability of 021;
- no cut/camera reset;
- absence of UV/aspect distortion;
- whether 24-second pacing and lens movement feel intentional rather than mechanically interpolated;
- whether the longer edition remains visually coherent without sound;
- whether AW011 generated anchors preserve the canonical authority boundary and return cleanly to `A0`;
- whether the result is actually usable as a repeatable visual-production method rather than a one-off road test.

## Smallest next proof

Run one current Film proof with persisted artifacts. For the existing edition path, persist the Experimental Film 01 MP4, director-review sheet and explicit pass/fail judgment. For the newer AW011 path, persist the compiled anchor package plus provider/render output and an explicit authority/enter-return visual judgment. Neither implementation branch should be called reusable Film capability before at least one such executed proof passes.

No new human/environment blocker is established by this ledger; absence of a reviewed run is missing evidence, not a blocker.
