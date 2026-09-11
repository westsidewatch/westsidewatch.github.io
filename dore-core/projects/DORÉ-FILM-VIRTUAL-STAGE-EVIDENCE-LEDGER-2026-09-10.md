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

## Current evidence boundary

No workflow run is currently associated with the reviewed corrected/two-anchor, three-anchor Camera Spine, or Experimental Film 01 commits in the available run lookup. Therefore:

- implementation existence: **VERIFIED**;
- corrected workflow definition: **VERIFIED**;
- three-anchor Camera Spine implementation: **VERIFIED**;
- Experimental Film 01 workflow/edition definition: **VERIFIED**;
- rendered visual acceptance: **UNKNOWN_NEEDS_EVIDENCE**;
- one-camera continuity quality: **UNKNOWN_NEEDS_EVIDENCE**;
- preservation of canonical Doré source appearance in the rendered output: **UNKNOWN_NEEDS_EVIDENCE**;
- cinematic pacing/lens-language quality over 24 seconds: **UNKNOWN_NEEDS_EVIDENCE**;
- reusable film-language capability beyond these bounded tests: **UNKNOWN_NEEDS_EVIDENCE**.

A commit or workflow file must not be promoted to `VERIFIED_COMPLETE` without rendered evidence.

## Classification

`DORÉ-FILM / virtual-stage continuity + Experimental Film 01`: **ACTIVE_PARALLEL / EXPERIMENTAL_IMPLEMENTATION**.

This is not a completed product and not a replacement for the active P01 subtitle critical path.

## What was learned so far

1. Source-image recognizability must be an explicit acceptance condition when canonical artwork is placed into spatial/3D treatment.
2. UV mapping/orientation is not an implementation detail; it directly governs whether the film treatment preserves the source rather than visibly corrupting it.
3. A useful Doré film grammar should distinguish continuous world-space movement from slideshow/crossfade behavior.
4. Rendered artifacts, not workflow definitions, are the required evidence unit for visual-film acceptance.
5. A repeatable film-language claim needs multi-anchor evidence; moving from 011→019 to 011→019→021 is the correct architectural stress direction, but only a rendered run can establish that the camera-spine abstraction actually works visually.
6. Experimental Film 01 adds a second evidence axis beyond continuity: cinematic time. Attention dwell, travel speed and lens changes are now part of the intended grammar, but must be judged from the actual rendered film rather than inferred from keyframes.
7. Edition metadata that explicitly distinguishes `generation: false` from generated imagery is useful provenance and should remain in future film experiments.

## Debt / revisit trigger

Revisit when a current workflow run produces inspectable MP4/review-sheet artifacts. The next evaluation must judge:

- opening recognizability of 011;
- spatial departure rather than flat image motion;
- bridge continuity;
- arrival recognizability of 019;
- third-anchor recognizability of 021;
- no cut/camera reset;
- absence of UV/aspect distortion;
- whether 24-second pacing and lens movement feel intentional rather than mechanically interpolated;
- whether the longer edition remains visually coherent without sound;
- whether the result is actually usable as a repeatable visual-production method rather than a one-off road test.

## Smallest next proof

Run the current Experimental Film 01 workflow once and persist the MP4, director-review sheet and explicit pass/fail judgment against the criteria above. If that bounded film passes, then compare it against the shorter Camera Spine experiment before claiming a reusable Doré film grammar.

No new human/environment blocker is established by this ledger; absence of a reviewed run is missing evidence, not a blocker.
