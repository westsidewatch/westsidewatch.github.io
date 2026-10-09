# OLIVE MOUNTAIN · PORTRAIT ENGRAVING SYSTEM · V1.1

Status: Editorial image-generation authority proposal. This document governs artwork prompts, not CSS typography or site layout. Align implementation with Westside Design OS and existing Olive Mountain profile contract.

## Purpose
Create a coherent twelve-speaker portrait series: recognizable real people, Gustave Doré-inspired olive-green engravings, living-paper negative space, and individual asymmetrical gold geometry informed by Italian cultural and fashion editorial art direction. David Pawson's existing published image is a series-quality reference, never a composition template.

## Palette and separation
- Living Paper substrate: `#FAF9F5`.
- Olive Branch printing ink: `#738A5A` — **all figurative engraving** (skin, hair, clothing, hands, microphone, botanical and architectural linework).
- Dawn Gold: `#CEBD74` — **only** irregular abstract background planes and accents.
- CSS text: `#252525` — **never** baked into the image.
No black-and-gold treatment, natural skin colors, photographic color gradients, gold portrait ink, or additional palette. Preserve true unprinted paper. Olive tones must arise from engraved line density, not digital color overlays.

## Master image-generation prompt (English)

Create a museum-quality editorial portrait engraving for OLIVE MOUNTAIN, the Christian teaching and sermon archive of Westside Watch.

**Subject:** [PERSON NAME]
**Primary reference photograph:** [REFERENCE PHOTO]
**Pose and expression:** [POSE / EXPRESSION]
**Distinctive biographical motif:** [ENVIRONMENTAL MOTIF]
**Unique irregular gold composition:** [GOLD GEOMETRY IDENTITY]

Preserve the subject's recognizable age, facial proportions, hair, expression, pose, clothing details, and personal likeness from the supplied authentic photograph. Do not invent a new identity. Use the already-published David Pawson Olive Mountain image only as a reference for publication quality, line precision, paper atmosphere, and editorial restraint; never copy his pose, crop, or geometry.

Render the portrait as sophisticated nineteenth-century wood engraving informed by Gustave Doré: fine tapered burin-like parallel hatching, controlled cross-hatching, stippling, variable line spacing, and subtle mechanical halftone. Construct dimensional form by ink density and untouched paper highlights, not photography, painted gradients, airbrushing, or filtered photographs. Delicate natural features; no artificial aging, excessive wrinkles, harsh shadows, or reconstructed anatomy. Detailed subject, quieter secondary environmental marks, nearly invisible paper texture.

Print every figurative element, including the face, hands, hair, clothing, accessories, microphone, and biographical environment, exclusively in Olive Branch Green #738A5A on Living Paper #FAF9F5. Do not retain the original photograph's garment or skin colors.

Art-direct the composition like a premium Italian cultural/fashion magazine: sophisticated asymmetry, strong negative space, unusual but controlled editorial cropping, layered depth, and disciplined visual rhythm. Introduce a **distinctive, irregular, non-repeating abstract geometric background** in Dawn Gold #CEBD74: offset planes, fractured or incomplete polygons, angled architectural cuts, interrupted arcs, asymmetric fields, or cropped geometric fragments chosen to suit this particular person. Gold is confined to this secondary geometry, never the portrait's engraved marks. Do not automatically use circles or a halo. Each of the twelve speakers must have a materially different geometric vocabulary, scale, placement, angle, overlap, and spatial rhythm, not the same template rearranged.

Use one restrained environmental motif grounded in the speaker's biography, ministry geography, or character. Render representational motif details in olive-green engraving, secondary to the face and hands. Avoid generic religious symbols, stereotypical sermon posters, decorative frames, and irrelevant landmarks.

Target a vertical 3:4 artwork. Keep the speaker prominent and recognizable, generally in the left/lower-left, with approximately 35–45% quiet, mostly unprinted paper reserved for CSS typography, principally on the right when composition permits. Allow engraving to fade naturally into blank paper without artificial split panels. Protect face, hands, and microphone from responsive crops. The image must remain complete without text.

The result must feel like an exceptionally printed, limited-edition archival-paper editorial engraving, with subtle print irregularities and precise sculptural linework, not a photographic collage or generic luxury poster.

**Absolute exclusions:** no generated text, letters, Chinese characters, numbers, captions, logos, watermark, signature, typography, mockup, frame, black-and-gold palette, photographic skyline, painted skin tones, colored garments, identical background geometry across speakers, or centered halo.

Final artwork only, high resolution, flat and borderless, prepared for responsive web use and separate CSS typography.

## Subject-specific variable contract
Change only these inputs per portrait:
1. PERSON NAME — verified speaker identity.
2. REFERENCE PHOTO — authentic source photograph, with provenance and rights reviewed.
3. POSE / EXPRESSION — preserve the source image's real posture and expression.
4. ENVIRONMENTAL MOTIF — one historically/personally grounded motif.
5. GOLD GEOMETRY IDENTITY — a **unique** irregular shape system, different across all twelve portraits.

The fifth variable is mandatory in V1.1; no generic or duplicated gold layout.

## Established art-direction examples (not templates)
- **David Pawson:** retain the published reference artwork's distinct geometric composition; do not duplicate for others.
- **Watchman Nee:** background tied to biography/ministry, using a distinct architectural/geometric rhythm.
- **Jiang Xiuqin:** delicate botanical engraving and soft, asymmetric gold curves; preserve her authentic speaking likeness.
- **Derek Prince:** geographic/biographical engraving with angular, directional geometry.
- **Huang Shuhua:** preserve the original olive-green engraving of her speaking with microphone, raised open hand, hairstyle, and embroidered jacket. Add **engraved Canadian maple leaves only** as the geographic motif; **no Toronto skyline or CN Tower**. Preserve or carefully adapt her individual irregular gold planes; do not obscure her face or hand. Maintain living-paper negative space.

The remaining speakers receive individual biographically grounded motifs and distinct geometry after confirming their references. Do not invent biographies or prescribe duplicate layouts.

## Quality gate
All five must pass:
1. Facial likeness and source-photo fidelity.
2. Correct color separation: olive figurative engraving / gold geometry / living paper.
3. Sculptural Doré-like line quality, no digital gradient substitution.
4. Responsive CSS typography-safe negative space.
5. Unique biographical motif and genuinely non-repeated geometric identity.

Reject and regenerate nonconforming artwork; do not hide image failures using CSS overlays. Review against the published David Pawson image and the existing speaker gallery.

## Related project authorities
- `docs/WESTSIDE-COLOR-AUTHORITY.md`
- `static/dore-design/magazine-profile.olive-speaker.v1.json`
- Westside Design OS (final authority for runtime tokens and CSS)
- https://github.com/yanliudesign/mono-color-skill (printing principles only, not its default poster palette or typography)

This document stores the prompt and review rules. It does not claim that all twelve images are complete, that the visual gate has passed, or that production CSS is changed.
