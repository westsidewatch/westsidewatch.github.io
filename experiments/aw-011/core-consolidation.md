# AW-011 Core Consolidation

AW-011 is the hard first specimen, not a template for making every future shot equally expensive.
Its open scene, long visible depth, foreground/midground occlusions, and weak natural masking make it a useful stress test.

## Lessons from V1–V8

| Stage | Failure / observation | Root cause | Core rule retained |
|---|---|---|---|
| V1 | transparent moving-image feel | flat/backward remap | geometry before synthesis |
| V2 | blurred moving layer | weak surface support | render known world; do not regenerate it |
| V3 | fragmented / stretched splats | depth discontinuities were crossed | preserve occlusion boundaries |
| V4 | parallax appeared; shepherd deformed; camel mosaic/flicker | geometry error + true disocclusion + per-frame fill | separate geometry failure from missing-world failure |
| V5 | MoGe-2 performed best of tested providers | provider matters, but provider is not the Core | keep geometry provider replaceable |
| V6 | two persistent layers were insufficient | fixed global layer budget | no hard-coded global layer count |
| V7 | ~0.235% residual yet rider halo remained | local topology/salience dominates global percentage | local salience beats raw residual percentage |
| V8 | predictive local world demand | Camera Spine is known before render | predict disocclusion before rendering |

## Camera–World Core v1

The Core is deliberately small:

1. **Camera Value** — is the shot narratively worth its cost?
2. **World Demand** — what unseen world will the Camera Spine expose?
3. **Minimum Evidence** — what is the smallest new evidence set needed?
4. **World Memory** — generated evidence is persisted and reused.
5. **World Sufficiency** — stop as soon as the shot is visually and narratively sufficient.

Depth, mesh, point cloud, MPI/LDI, cache representation, view-consistency model, diffusion completion, and residual refinement remain replaceable providers.

## Film-style prior

Doré Film should not optimize for cheap shots. It should optimize for strong cinema with avoidable world cost removed.

The emerging grammar is:

`detail / material / hand / garment / stone / threshold`
→ `foreground occluder / human-scale observation`
→ `slow reveal / lateral discovery / restrained push`
→ `midground social action`
→ `wide scene when the event earns spatial expenditure`
→ `return to material or human detail when appropriate`

This supports an observational, black-and-white documentary / Italian long-take sensibility: the camera behaves like a witness inside material space rather than continuously seeking spectacle.

Wide scenes are not errors. Exodus, the Red Sea, Jerusalem, Crucifixion, Resurrection, Revelation and other large biblical events may intentionally pay high World Demand. The cost metric exists to remove **avoidable** world generation, not to suppress spectacle.

## Camera score

Candidate camera paths can be compared with:

`Shot Score = Narrative Value + Reveal Value + Rhythm Value - Avoidable World Cost`

The cost term is bounded so it cannot overpower a genuinely important wide shot.

This creates a useful production loop:

`Script → camera intention → candidate Camera Spines → World Demand Scan → Camera–World score → selected Spine → minimum evidence → render → sufficiency gate`

## Consolidation rule

**Explore broadly. Consolidate ruthlessly.**

A new technique enters the Core only if it does at least one of the following:

- explains a real AW-011 failure;
- deletes bespoke engineering;
- reduces generated-world area;
- increases reuse of prior evidence;
- reduces retries / human intervention;
- improves camera or script decisions;
- improves visual sufficiency without weakening source authority.

The intended outcome is not an endless `AW-011 V9/V10/...` chain. It is a reusable Camera–World Core that can transfer to AW-019, AW-021, then the larger Doré Film production.