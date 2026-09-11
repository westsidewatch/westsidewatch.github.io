# DORÉ CAMERA CORRIDOR / AW-011

AW-011 is the first production specimen for turning one Doré source image into only the world a known camera path actually needs.

It is deliberately **not** a 360° reconstruction, a frame-by-frame regeneration pipeline, or a universal world model.

## Production question

For a fixed Camera Spine, what is the **minimum additional visual evidence** required so that the moving camera never exposes the original source as a flat image?

The corridor is the swept set of views actually visited by the camera. Everything outside that corridor is out of scope.

## Vertical slice

```text
Doré 011 source
  -> fixed Camera Spine
  -> corridor samples
  -> source/scaffold reprojection
  -> known pixels + unseen mask
  -> minimum necessary anchors
  -> scaffold update
  -> reproject known world
  -> synthesize only unseen pixels
  -> camera traverses corridor
  -> return to source pose
  -> exact source relock
```

## Non-negotiable invariants

### 1. Known pixels are immutable

A generative stage may write only where `unseen_mask == true`.

For every rendered corridor sample `t`:

```text
output_t[known_mask_t] == reprojected_known_t[known_mask_t]
```

The initial acceptance target is zero pixel delta. If a later renderer requires a tolerance, that tolerance must be explicit and separately approved; it must never be silently introduced.

### 2. Evidence is purchased only for disocclusion

An anchor exists only to eliminate unseen regions that the Camera Spine will actually reveal. No anchor is justified by completeness outside the corridor.

For each sample `t`, let `U_t` be the currently unseen pixels after reprojection. A candidate anchor `a` has useful coverage `C(a,t)` only where it resolves pixels in `U_t`.

The planner scores the marginal gain:

```text
gain(a) = Σ_t weight(t) * |U_t ∩ C(a,t)|
          - redundancy_penalty(a)
          - weak_overlap_penalty(a)
```

After selecting `a`:

```text
U_t <- U_t \ C(a,t)
```

Selection stops as soon as the corridor satisfies the residual-unseen acceptance threshold. The target is therefore an **evidence budget**, not a fixed anchor count.

### 3. Scaffold provider is replaceable

The corridor contract must not depend on one reconstruction model. The initial provider can be One2Scene-class sparse-view scaffolding; NoPoSplat-class or later providers can replace it without changing corridor planning or acceptance semantics.

Provider output must be reducible to the corridor evidence contract:

- camera pose / intrinsics
- reprojected known RGB
- `known_mask`
- `unseen_mask`
- optional depth
- optional confidence

GenWarp-class warping is useful because it exposes exactly the boundary AW-011 needs: pixels that have a source and pixels that do not.

### 4. Return means exact relock, not resemblance

When the camera returns to the source pose (`P000`), AW-011 hard-locks the Doré 011 source image. A generated approximation does not pass.

```text
frame(P000_return) == Doré_011_source
```

This makes the original engraving the world authority at its canonical view.

## Corridor manifest

`corridor.example.json` defines the provider-independent contract. It intentionally leaves real Doré 011 asset paths and real camera poses unset until the production asset and Camera Spine are bound.

Required runtime products for each sampled pose:

```text
poses/<pose-id>/known.png
poses/<pose-id>/known-mask.png
poses/<pose-id>/unseen-mask.png
```

An anchor candidate contributes one coverage mask per affected corridor pose. The planner operates on coverage counts or masks; it does not need to know which scaffold provider produced them.

## First acceptance gate

AW-011 is considered vertically connected only when one run produces all of the following:

1. A fixed Camera Spine sampled from departure through return.
2. A baseline unseen-area report before new anchors.
3. A deterministic minimum-anchor selection log with marginal gain per selected anchor.
4. Reprojection for every sampled pose.
5. Unseen-only synthesis with a known-pixel conservation check.
6. A rendered traversal of the Camera Corridor.
7. A return frame that is byte/pixel-identical to the Doré 011 source at the canonical source pose.

## Explicitly out of scope

- reconstructing geometry the Camera Spine never sees
- generating rear/side views for completeness
- regenerating every video frame
- letting diffusion repaint already-known engraving pixels
- selecting an arbitrary fixed number of anchors
- coupling AW-011 to a single scaffold implementation
- moving to AW-019 or AW-021 before AW-011 passes the relock gate

## Engineering sequence

1. Bind the real Doré 011 source asset.
2. Bind the approved Camera Spine as ordered poses.
3. Produce baseline reprojection masks from the initial scaffold.
4. Convert all disocclusion into `U_t` evidence debt.
5. Run `tools/aw_corridor/plan_anchors.py` against real candidate coverage.
6. Generate only the selected anchor evidence.
7. Rebuild/update scaffold and rerun masks.
8. Fill only residual unseen pixels.
9. Render the corridor and verify source relock.

The engineering object is not “a generated world.” It is a **camera-certified corridor of evidence** around Doré 011.