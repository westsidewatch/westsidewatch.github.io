# Doré × Mono Color — upstream import staging

Upstream: https://github.com/yanliudesign/mono-color-skill
Source license: MIT; upstream example images and third-party reference images are NOT covered by the MIT source license. Do not vendor those images without rights review.

## Current import status
- Original SKILL.md: imported verbatim.
- design-system/rhythm.json: imported verbatim.
- design-system/typography.json: imported verbatim.
- Remaining upstream machine-readable catalogs, scripts, evaluations and LICENSE: **not yet imported**. This is a staging PR, not a completed integration.
- No runtime image generator has been wired up. No generated covers should be deployed from this import.

## Doré integration contract
1. Doré remains the single design-generation authority; upstream skill is a reusable grammar source, not a second production gateway.
2. Resolve each site's section palette first; disallow upstream defaults that violate that palette. Olive Mountain uses olive green and white, never gold or arbitrary blue.
3. Preserve Doré's current approved typography tokens and exact text. Upstream typography describes *roles*, not permission to swap font families.
4. Replace upstream mechanical halftone/engraving texture with an independent Doré historical-engraving layer based on rights-cleared Gustave Doré work. The hatching must model directional strokes, line-density shadows and light, not random decorative stripes.
5. No synthesized identifiable portraits of speakers; use rights-verified portraits or clearly non-identity-bearing abstract artwork.
6. Render to an isolated preview first, inspect real desktop/mobile screenshots, require human approval before publication.
7. Do not call this a self-contained image model: the skill compiles visual recipes and prompts, and requires a compatible generation backend for raster image output.

## Next import work
Inventory all upstream source files and vendor the remaining licensed design-system catalogs, validators and evaluations. Pin upstream commit and preserve its license. Add an adapter that maps upstream recipe IDs into Doré brief → generation → render → review, and run one isolated sample before touching Olive production.
