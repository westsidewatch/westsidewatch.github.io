# DORÉ ANCHORED WORLD — Engineering Translation

Status: **ENGINEERING TRANSLATION / PRE-IMPLEMENTATION BASELINE**  
Project: DORÉ FILM — Biblical Long Scroll  
Date: 2026-09-10

## 0. Why this translation exists

Experimental Film 01 proved the render pipeline but failed the visual world test. The camera was moving around textured image planes; the Doré originals did not become an explorable world.

The missing layer is therefore not another camera rig. It is the production translation between a canonical Doré image and a camera-traversable world.

This document translates the current Doré Exploration into executable system boundaries. It deliberately does **not** select a final model before the missing interfaces are understood.

## 1. Binding production invariant

> **Canonical Doré pixels are authoritative. Geometry extends them. Generation only fills what the camera genuinely reveals beyond them.**

The runtime provenance classes are:

- `A_CANONICAL` — pixels directly from the locked Doré original;
- `B_REPROJECTED` — canonical/approved-anchor pixels moved by deterministic geometry/camera reprojection;
- `C_RECONSTRUCTED` — geometry/radiance reconstructed from approved observations;
- `D_INFERRED_UNSEEN` — content inferred only because the approved camera reveals space absent from all authoritative observations.

A generated result must never silently become `A_CANONICAL`.

## 2. Camera-first production order

The film algorithm is:

`SCRIPTURE / NARRATIVE`
→ `CAMERA INTENTION`
→ `CAMERA SPINE`
→ `VISIBILITY FORECAST`
→ `ANCHOR PLAN`
→ `WORLD SCAFFOLD`
→ `KNOWN-PIXEL REPROJECTION`
→ `UNSEEN-REGION COMPLETION`
→ `PROVENANCE COMPOSITE`
→ `DORÉ FIDELITY GATE`
→ `FRAME / FILM`

The Camera Spine is upstream of world generation. We do not build an unrestricted 360° world when the approved camera corridor does not require it.

## 3. The missing production modules

### M1 — Authority Anchor Resolver

Input:
- canonical Doré ID;
- locked 241 registry relationship;
- highest approved faithful high-resolution reset of the same original, if required;
- canonical camera/framing target.

Output:
- `AuthorityAnchor`;
- immutable source hash/provenance;
- canonical image dimensions/aspect;
- canonical camera lock target.

Rule: no generative model is allowed to replace this source.

### M2 — Visibility Forecaster

Input:
- Camera Spine segment;
- Authority Anchor;
- initial depth/geometry prior.

Output:
- visibility corridor;
- expected disocclusion masks along the camera path;
- required off-axis coverage;
- estimate of how much of the shot can remain A/B/C versus requiring D.

Purpose: generation demand is calculated from the camera, not guessed globally.

### M3 — Anchor Planner

Input:
- visibility corridor;
- camera trajectory;
- canonical authority view.

Output:
- the **minimum** set of additional camera-conditioned anchor poses needed to support the approved shot;
- priority/order for producing those anchors;
- explicit relationship of every generated anchor to the Authority Anchor.

This is the Doré-specific replacement for blindly generating a full panorama. The planner may choose 0, 1, 3, 6, etc. anchors according to actual camera need.

### M4 — Anchor Expansion Adapter

Input:
- Authority Anchor;
- planned target camera pose;
- depth/geometry cues where useful.

Output:
- candidate off-axis anchor observation;
- confidence/consistency metadata;
- generated-region mask;
- model/tool provenance.

Mature solution families to adapt rather than re-invent include camera-conditioned novel-view generation and warp-guided completion (e.g. GenWarp/WAVE/SEVA-class capabilities). This module is an adapter boundary: the Doré pipeline must remain replaceable if a better model appears.

### M5 — Lightweight World Scaffold Builder

Input:
- Authority Anchor;
- accepted expanded anchors;
- depth/geometry priors.

Output:
- explicit lightweight scene scaffold usable by the camera renderer;
- observation-to-world correspondence;
- confidence/visibility fields.

Candidate representations include point/Gaussian/radiance/depth-layer scaffolds. A full handcrafted CG environment is **not** required by default.

The engineering topology follows the mature single-image-to-explorable-world family: broaden reliable observations, then lift them into an explicit scaffold, rather than pretending the original plane itself is the world.

### M6 — Known-Pixel Reprojector

Input:
- current camera pose;
- Authority Anchor + accepted anchors;
- scaffold.

Output:
- deterministic rendered pixels wherever the world is already observed;
- visibility/depth/confidence;
- `unseen_mask`.

Rule: if a pixel can be reliably rendered from A/B/C evidence, do not ask a generator to redraw it.

### M7 — Unseen-Region Completion Adapter

Input:
- `unseen_mask` only;
- neighboring known pixels;
- geometry/scaffold guidance;
- current and neighboring camera poses;
- accepted anchor observations.

Output:
- D-class inferred content only;
- temporal/multiview consistency metadata.

This is not a full-frame image-to-video call. It fills genuinely unseen/disoccluded regions that the approved camera makes unavoidable.

### M8 — Provenance Compositor

For every rendered frame, maintain a source map:

`A_CANONICAL | B_REPROJECTED | C_RECONSTRUCTED | D_INFERRED_UNSEEN`

Output:
- composite frame;
- provenance matte;
- percentages by provenance class;
- D-region persistence/reuse information.

The compositor makes the production principle measurable rather than rhetorical.

### M9 — Canonical Re-lock / Doré Fidelity Gate

At a Canonical Frame Moment:
- framing must be solvable back to the Authority Anchor;
- canonical source must dominate the visible canonical composition;
- generated unseen content may not overwrite canonical source pixels;
- identity/provenance must remain inspectable.

The gate reports PASS/FAIL and must be usable in CI on deterministic checks, with visual director review retained for perceptual fidelity.

## 4. Mature research → Doré engineering translation

The explored projects are not treated as competing end-to-end products. They occupy different layers:

- **Depth Anything / DA3 class** → geometry prior / spatial cue, not final world;
- **GenWarp class** → camera-conditioned off-axis anchor / selective novel view;
- **WAVE class** → warp-guided view-consistency mechanism;
- **SEVA class** → camera-trajectory-conditioned view/video generation candidate;
- **One2Scene class** → reference topology: expanded anchor observations → explicit scaffold → scaffold-conditioned exploration;
- **VistaDream class** → reference for global scaffold plus multiview-consistent completion;
- **MetaView class** → reference for minimal explicit geometry cues plus implicit/generative large-viewpoint handling;
- **Blender** → camera/previs/composite/render host, not the world representation itself;
- **Camera Spine** → authoritative camera source of truth, not merely Blender keyframes.

## 5. What Film 01 skipped

Film 01 effectively executed:

`Doré Original → textured plane / shallow wall → Blender Camera → MP4`

It skipped:

- Visibility Forecaster;
- Anchor Planner;
- Anchor Expansion;
- actual World Scaffold;
- Known/Unknown pixel separation;
- provenance compositor;
- canonical re-lock gate.

Therefore its failure does not falsify Camera Spine or single-image world reconstruction. It falsifies **textured-plane-as-world** as the production representation.

## 6. Minimal executable data contracts

### `AuthorityAnchor`

```json
{
  "dore_id": "011",
  "source": "canonical-241",
  "source_hash": "...",
  "image": {"width": 0, "height": 0},
  "canonical_camera": {"position": [], "look": [], "lens_mm": 0}
}
```

### `AnchorPlan`

```json
{
  "camera_segment": "...",
  "authority_anchor": "011",
  "poses": [
    {"id": "A01", "pose": {}, "reason": "predicted-disocclusion", "required": true}
  ]
}
```

### `FrameProvenance`

```json
{
  "frame": 0,
  "camera_pose": {},
  "coverage": {
    "A_CANONICAL": 0.0,
    "B_REPROJECTED": 0.0,
    "C_RECONSTRUCTED": 0.0,
    "D_INFERRED_UNSEEN": 0.0
  },
  "unseen_mask": "...",
  "fidelity_gate": "PASS|FAIL|REVIEW"
}
```

These contracts are intentionally model-agnostic.

## 7. Production burden policy

Optimization target:

> **Use the least generation required by the approved camera path.**

Therefore:
- do not create a 360° world if the camera needs a 35° corridor;
- do not generate every video frame independently;
- reuse accepted inferred regions after they become persistent world evidence;
- prefer reprojection/reconstruction for already-observed surfaces;
- keep heavy model inference behind replaceable adapters;
- cache anchors/scaffold/results by source hash + camera-plan hash + model/version hash.

This is the engineering form of: **能力越大，負擔越小；越發展，越輕量。**

## 8. Acceptance ladder — do not jump directly to Film 02

### Gate AW-0 — Architecture translated
PASS when M1–M9 have explicit responsibilities, data boundaries, provenance rules and failure semantics.

### Gate AW-1 — Authority + Camera corridor
For Doré 011, resolve canonical source and use a short approved Camera Spine segment to calculate a visibility corridor and anchor plan. No generated image required yet.

### Gate AW-2 — One accepted off-axis anchor
Produce one planned noncanonical view while preserving the canonical source untouched. Record its D regions and provenance.

### Gate AW-3 — Minimal scaffold
Build a scene representation from canonical + accepted anchor(s). Demonstrate that the camera can move without exposing a literal image plane.

### Gate AW-4 — Known/unknown compositor
Render a short camera move with provenance mattes proving known pixels are reprojected and only unseen regions are inferred.

### Gate AW-5 — Enter Doré 011
Start at a recognizable canonical Doré 011 composition, move materially into/off-axis through the depicted space, reveal no literal canvas boundary, and retain coherent engraving/world identity.

### Gate AW-6 — Canonical re-lock
Return/re-align to the canonical camera and recover the original Doré composition without a regenerated replacement.

Only after AW-5/AW-6 should the production connect 011 to another Doré anchor and shoot the next experimental film.

## 9. Failure semantics

The pipeline must stop or downgrade instead of silently substituting a plane when:
- required anchor expansion is unavailable;
- scaffold confidence is insufficient for the requested camera move;
- D-class area exceeds an approved threshold;
- canonical pixels would be overwritten;
- multiview consistency breaks;
- model/runtime cost violates the current production budget.

A failed world build must remain a visible FAIL in the Production Ledger.

## 10. Current engineering-completion assessment

This translation separates **architecture completion** from **implementation completion**.

At the moment this document lands:

- Camera Spine / one-camera source-of-truth groundwork: **substantially present**;
- canonical Doré registry/provenance groundwork: **present**;
- DA3/depth/geometry capability evidence: **present as probes**;
- Blender render/MP4 pipeline: **present**;
- M1 Authority Anchor Resolver: **partially available through existing registry, not yet packaged for film**;
- M2 Visibility Forecaster: **missing**;
- M3 Anchor Planner: **missing**;
- M4 Anchor Expansion Adapter: **researched, not integrated**;
- M5 World Scaffold Builder: **capability fragments exist, correct anchored-world implementation missing**;
- M6 Known-Pixel Reprojector: **missing as a provenance-aware film module**;
- M7 Unseen Completion Adapter: **researched, not integrated**;
- M8 Provenance Compositor: **missing**;
- M9 Canonical Re-lock/Fidelity Gate: **specified, not implemented**.

Estimated completion of the **new Anchored World bridge itself**: approximately **20–25%**. The percentage reflects reusable groundwork plus the now-complete architecture translation; it does **not** claim that Image→World is 20–25% visually solved.

Estimated completion of **AW-0 Architecture Translation**: **100%**.

The next Doré Exploration should therefore be driven by the translated gaps, especially M2–M7, and should search for mature implementations that can eliminate or collapse modules before we write custom code.

## 11. Next exploration question

Do not ask broadly “which NVS model is best?”

Ask:

> **Which mature open-source single-image-to-explorable-world implementation already supplies the largest contiguous subset of M2 Visibility Forecast → M3 Anchor Planning → M4 Anchor Expansion → M5 Scaffold → M6 Reprojection → M7 Selective Completion, while allowing Doré's Authority Anchor and provenance compositor to remain outside and authoritative?**

If a mature system covers several modules correctly, adapt it. Do not rebuild those modules merely to preserve a Doré-specific implementation.
