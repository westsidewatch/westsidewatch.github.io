# DORÉ ANCHORED WORLD — Route 01

Status: **ROUTE SELECTED FOR FIRST REAL FILM ATTEMPT**  
Date: 2026-09-10  
Target: Doré 011, AW-5 / AW-6

## Objective

The only objective is to make the first film fragment in which the camera actually enters the Doré world. Algorithm distillation remains deferred until a successful film loop exists.

Acceptance remains:

`canonical Doré 011 → camera enters world → no literal plane/canvas boundary → coherent off-axis world → camera can return → canonical Doré 011 re-locks`

## Exploration result: the missing middle is now an adapter problem

Repository-level inspection confirms that the useful One2Scene scaffold boundary is ordinary multi-view data, not a semantic dependency on panorama itself.

Its data contracts use:
- context images;
- 3×3 intrinsics;
- 4×4 extrinsics;
- arbitrary target camera extrinsics/intrinsics.

Its Gaussian representation is a small explicit structure:
- means;
- covariances;
- spherical-harmonic appearance coefficients;
- opacities.

Its CUDA splat decoder renders those Gaussians directly at supplied target cameras.

Therefore Camera Spine can be translated into target camera matrices without making Blender the source of truth.

## Important correction to the earlier route

Do **not** vendor or adopt the complete One2Scene demo as Doré production code.

Reasons found in repository inspection:
1. the published demo path is panorama-specific and hardcodes six cube directions;
2. Fast3R code contains six-view assumptions in image-position setup;
3. demo/config files contain machine-local checkpoint/data paths;
4. the public demo script references local helper layout rather than presenting a clean library API;
5. embedded CroCo/Fast3R code carries CC BY-NC-SA 4.0 non-commercial licensing even where surrounding repositories may have different top-level licenses;
6. the 19GB denoiser is unnecessary for the first Doré world proof.

One2Scene remains a **validated topology and interface reference**, not a dependency we must swallow whole.

## Key route discovery

One2Scene itself contains a `re10k_3view` path using `noposplat_multi + croco_multi` with `num_context_views: 3`. This proves that the scaffold idea is not intrinsically tied to six cubemap faces.

The general multi-view backbone computes context relationships from the actual view count `v`; the Gaussian encoder then builds an explicit scaffold from those observations.

Therefore the first Doré corridor does not need a 360° panorama.

## Route 01

### Stage A — Camera Spine → minimal anchor poses

For Doré 011 choose the canonical pose plus the minimum off-axis poses required by the AW-5 camera corridor.

First production budget:
- `A0` = canonical Doré 011, immutable Authority Anchor;
- `A1` = first off-axis observation;
- `A2` = second off-axis observation if required by disocclusion.

Start with three observations because a mature three-view scaffold path already exists. Do not generate six views merely because a panorama demo uses six.

### Stage B — Anchor generation

Use a GenWarp-class adapter for A1/A2 because the inspected API already exposes exactly the evidence Doré needs:
- `synthesized` novel view;
- `warped` source evidence;
- `mask` for regions with no source splat;
- `correspondence` map.

This is materially better than treating the generated image as an undifferentiated frame. The mask/correspondence become provenance inputs.

For each anchor store:
- target pose;
- source Authority Anchor hash;
- warped image;
- unseen mask;
- synthesized completion;
- correspondence;
- model/version;
- A/B/D coverage.

### Stage C — Sparse observations → Gaussian scaffold

Adapter contract:

```text
context.image       [1,V,3,H,W]
context.intrinsics  [1,V,3,3]
context.extrinsics  [1,V,4,4]
            ↓
ScaffoldProvider
            ↓
Gaussians {
  means,
  covariances,
  harmonics,
  opacities
}
```

Provider is replaceable. The first implementation may reproduce the proven NoPoSplat/One2Scene-style multi-view scaffold path, but Doré code must own the adapter contract rather than import the research repo as architecture.

### Stage D — Camera Spine → scaffold renderer

Camera Spine poses become target `extrinsics + intrinsics`.

The Gaussian renderer already accepts arbitrary target views, so this stage is deterministic after scaffold creation.

Outputs per frame:
- scaffold RGB;
- depth;
- target camera pose;
- canonical reprojection evidence where available.

### Stage E — Canonical Authority composite

At/near the canonical camera, the Doré original is not regenerated.

Policy:
1. canonical source wins;
2. source/accepted-anchor warp wins over generation;
3. scaffold supplies spatial continuity;
4. generated pixels own only genuinely unseen regions;
5. returning to the canonical pose restores the Authority Anchor rather than a model approximation.

This is the first Doré Appearance Lock. It is a compositor policy before it is an AI model.

## What is deliberately NOT in Route 01

- full 360° panorama generation;
- One2Scene 19GB SEVA denoiser;
- whole-frame image-to-video;
- Light;
- Scripture;
- character animation;
- 011→019 bridge;
- algorithm distillation;
- web runtime optimization.

None may block AW-5/AW-6.

## Licensing / dependency boundary

GenWarp source is MIT, but its README explicitly warns that downloaded third-party checkpoints may have their own licenses. Checkpoint licenses must be recorded separately.

NoPoSplat's top-level repository is MIT, but embedded CroCo source explicitly states CC BY-NC-SA 4.0 / non-commercial use. One2Scene also embeds that CroCo/Fast3R lineage. Therefore research code may be used to prove the film route where permitted, but Doré must not assume the surrounding repository license automatically covers every embedded component.

This reinforces the adapter boundary and future replaceability.

## Engineering completion after this route selection

Architecture translation: **100%**.

Route uncertainty has materially fallen. The remaining blocker is no longer “how does one image become a world?” It is now the execution of one narrow chain:

`011 + Camera corridor → A1/A2 → sparse scaffold → Camera render → canonical composite → AW-5/AW-6 film`

Estimated solution coverage from mature existing work: **~75–80%**.

Actual Doré Anchored World implementation remains approximately **20–25%** until these adapters produce accepted visual evidence. Do not inflate implementation progress from research confidence.

## Next engineering node

Build the **AW-1/AW-2 Anchor Corridor package for Doré 011**:

1. resolve Authority Anchor 011;
2. derive a short enter-and-return Camera Spine corridor;
3. emit A0/A1/A2 camera matrices;
4. emit a provider-neutral anchor manifest;
5. wire GenWarp input/output contract including warp/mask/correspondence provenance;
6. stop only if a real execution blocker requires a different provider.

After A1/A2 exist, proceed directly into scaffold construction. The acceptance node remains the film, not the manifest or the adapter commit.
