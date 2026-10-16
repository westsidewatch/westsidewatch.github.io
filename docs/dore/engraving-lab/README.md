# Doré Engraving Lab v0 — Classical Print Linework

Status: **experimental / isolated**. This lab does not modify Olive Mountain, the homepage, or the Mono Color production texture. The imported Mono Color print technique remains the reliable baseline until the lab demonstrably exceeds it.

## Research taxonomy: style, process, and purpose
| Historical method | Mark grammar | Tonal/structural use | Doré adaptation |
|---|---|---|---|
| Burin engraving / copperplate | tapered deliberate cuts, swelling and thinning strokes | precise contour, metal, architecture, controlled shadows | directional path thickness, contour-following line fields |
| Etching | freer, drawing-like bitten lines | atmospheric landscape, irregular expressive detail | irregular but repeatable stroke trajectories |
| Drypoint | soft burr and velvety edge | intimate dark tone, rough edges | edge softness as a separate raster post-process |
| Mezzotint | dense granular field, highlights scraped out | darkness-to-light chiaroscuro | luminance-based grain, preserve highlights |
| Wood engraving (end grain) | white cuts in dark mass, sharp hatch clusters | illustrated books, architectural detail, light beams | **priority Doré reference**: white-line carving, clusters, directional shadows |
| Woodcut (plank) | broad carved masses and bold contours | emphatic silhouette, poster-scale expression | mass-first carving and exposed paper |
| Lithography | crayon/grain tonal marks | soft atmosphere and gradients | grain module, not falsely labeled incised engraving |
| Stipple / dotted engraving | variable dot size and density | skin, soft tone, transition | stipple layer |
| Parallel hatching | spacing and weight | midtone, material and directional volume | starter method |
| Cross-hatching | multiple angle families | deeper shadows and volumetric form | layer angle/density controlled by luminance |
| Contour hatching | strokes follow object geometry | fabric, faces, rocks, carved form | gradient/tangent flow fields |
| White-line / negative cutting | remove strokes from dark area | rays, reflected light, architectural edge | highlight knockout and inverted masks |

These are **not** interchangeable artistic schools. A historical process, a mark-making method and an aesthetic period are distinct classifications.

## Schools / visual reference lenses
- Renaissance Northern European (Dürer): analytical contours, disciplined burin engraving, intricate textures.
- Italian Renaissance (Marcantonio Raimondi): contour, modeling, figure-focused engraved tonal systems.
- Baroque (Rembrandt): etching/drypoint, selective darkness, atmospheric irregularity.
- Romantic and 19th-century illustrated wood engraving (Gustave Doré and workshop engravers): dramatic chiaroscuro, rays of light, layered landscapes, biblical narrative, dense line clusters and white-line cutting.
- 19th-century reproductive engraving: highly controlled tonal translation from drawings into print.
- Arts and Crafts / revival woodcut: visible carving, mass and expressive simplification.

Important historical caveat: many illustrations *after Gustave Doré* were engraved by professional engravers interpreting his drawings. Do not assume every engraved stroke was physically cut by Doré.

## Functional use cases
1. Illustrated Bible scenes and long-form journal openings: dramatic subject-focused wood engraving.
2. Architecture and city diagrams: precise directional engraving with geometry preservation.
3. Background textures: quiet low-density linework, not busy decorative noise.
4. Cover images: subject-first chiaroscuro; preserve readable typography.
5. Small mobile cards: simplified silhouette and coarse marks; no microscopic moiré.
6. Mono Color integration: mechanical print screening remains default; engraving is optional and independently scored.

## Reusable open-source candidates — evaluate, do not vendor blindly
- https://github.com/plottertools/hatched — OpenCV-based image-to-hatching, SVG via vpype; **first candidate** for deterministic raster→lines.
- https://github.com/kylberg/ScribbleTrace — image-to-vector; cross-hatching and GUI presets; test algorithm quality, license and dependencies.
- https://github.com/abey79/vpype — MIT vector post-processing, SVG, path cleanup and layering.
- https://github.com/Veedubin/hatchsvg — MIT, image-to-layered hatch SVG, replayable JSON sessions; newer/smaller project, benchmark rather than blindly adopt.
- https://github.com/SonarSonic/DrawingBotV3 — GPL-3.0 free version with limited algorithms; **premium-only** features excluded. Not selected for embedding.
- https://github.com/msurguy/SquiggleCam — MIT image→oscillating lines; useful alternate line field, not authentic wood engraving.

## Lab learning pipeline
A. Input: rights-cleared raster image or a synthetic test target; never download historic art into repository by default.
B. Semantic masks: subject, background, architecture, fabric, sky, face, light-source direction; start with manually supplied masks, no claimed automatic scene understanding.
C. Tone extraction: luminance map, edge/gradient map, local orientation field, silhouette.
D. Print baseline: Mono Color halftone, plate separation and controlled imperfections.
E. Vector engraving: parallel/cross-hatch → gradient-aligned contours → selective white-line carving; deterministic seed and explicit density, width, angles.
F. SVG rendering: vector geometry with clip masks; export PNG preview; 1x/2x and mobile downsample.
G. Critique: subject legibility, value range, directional coherence, light continuity, line collisions, moiré, output size, runtime and image diversity.
H. Human comparison: print baseline vs hatching vs cross-hatching vs contour/wood-engraving. Only promote an effect that is better for its declared use case.

## v0 acceptance gates
- 4 synthetic fixtures: sphere with side lighting, draped fabric, stepped architecture, cloud/ray landscape.
- At least 3 techniques rendered from the same input; stable seed yields identical SVG.
- Output remains readable at 320px width and 1200px width.
- Black/white or section-specific approved ink only; no black-gold.
- No borrowed artwork, fonts or portraits bundled without separate permission.
- A side-by-side preview is reviewed by a human; passing code tests alone cannot promote to production.
- Each candidate records algorithm, source version, license, settings, runtime and failures.
- If no algorithm reaches minimum quality, continue using Mono Color print baseline.

## Implementation order
1. Inventory and benchmark **hatched** + **ScribbleTrace** with synthetic fixtures, and validate license/dependencies.
2. Integrate one engine behind a narrow CLI contract `image → engraving SVG + manifest` in the lab only.
3. Add contour-following and white-line modules only where benchmarks show a gap.
4. Compare with rights-cleared Doré print examples as **references**, not automatic model training.
5. Connect optional effect to Doré generation manifest, never overwrite mature Mono Color defaults.

## Engineering boundaries
No paid API. No production site mutation. No new parallel Doré design gateway. No requirement to download third-party corpus. License review before code vendoring. This is a research plan and acceptance contract, not a claim of a finished engraving renderer.
