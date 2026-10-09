# OLIVE MOUNTAIN · PORTRAIT ENGRAVING SYSTEM · V1.2

Status: Editorial image-generation authority. This document governs artwork prompts, not CSS typography or site layout. Align implementation with Westside Design OS and existing Olive Mountain profile contract.

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

## Mono-color editorial print integration (V1.2, adapted)

Upstream reference: [yanliudesign/mono-color-skill](https://github.com/yanliudesign/mono-color-skill) (MIT). Incorporate its *process and composition rules*, not its default palettes, poster text, or stock layouts. **Olive Mountain's fixed palette, authentic identity, Doré-style engraving, and Westside Design OS remain authoritative whenever rules differ.** This is an adaptation, not a claim that the upstream skill has been installed or its Python generator invoked.

### Mandatory pre-generation recipe (per speaker)
Record and resolve these fields **before** composing; keep stable across retries unless the brief changes:
- Subject ID and primary authentic photograph; preserve facial identity, anatomy, age, expression, hairstyle, clothing silhouette, and recognizable gesture. Do not silently substitute another preacher. Strip/remove podiums or obstructing props only when requested; reconstruct hands and forearms convincingly.
- Intent: one restrained, biography-grounded editorial portrait; one meaningful symbol or environment **only**, verified against that speaker's actual education, geography, or ministry. Do not illustrate every life event; reject generic olive trees, airplanes, globes, books, churches, mountains, city skylines unless individually justified.
- Image role: dominant human engraving, not photographic collage; 3:4 canvas; no embedded text (site typography remains separate CSS).
- Plates: **Olive Branch #738A5A** carries the entire figure and any representational etched motif, with light/dark achieved only by hatch density and paper knockout. **Dawn Gold #CEBD74** is a minor, strictly separate geometric accent plate; never color skin, suit, hands, hair, or figurative etched motifs gold. **Living Paper #FAF9F5** is an unprinted substrate, not a third ink. No other colors, no black or sepia, no photographic tinted overlays.
- Print mechanics: fine deliberate burin/wood-engraving parallel and crossing strokes, carefully scaled stipple/halftone, clipped paper highlights, realistic continuous fingers and arms, medium contrast, legible likeness at thumbnail size. Use 0–2 restrained mechanical print imperfections, not accumulated generational texture, registration chaos, generic distress, or fake aging. Always regenerate **from the original reference**, never repeatedly transform prior generated images.
- Space: **35–45% quiet, visibly unprinted paper** (within mono-color-skill's 25–55% general range); preserve a coherent right/top release zone for responsive CSS. Outer breathing room about 5–9% where useful, without cutting off essential limbs. Negative space is an active compositional shape, not leftover background.
- Editorial rhythm: one strong event—the subject's expression/gesture—and one supporting asymmetrical gold intervention. Do not add multiple competing decorations. Gold should be a minor, clearly assigned background function rather than arbitrary scatter.
- Final checks: no text, mockup, frame, logos, fake sponsor, decorative blobs, glossy gradient, centered formula, scrapbook treatment, or color-filtered photograph.

### Twelve-speaker originality firewall (hard gate)
Treat other published speaker portraits as a **visual grammar**, not a geometry template. Compare with the full existing gallery before rendering. For every new portrait, change **at least four structural variables** from every relevant reference: (1) geometric family/silhouette, (2) major axis or orientation, (3) scale relationship to the subject, (4) spatial position and anchoring, (5) overlap or cutout behavior, (6) distribution of empty paper. Cosmetic changes, rotations, or replacing the icon within the same left-vertical-bars / oversized-semicircle / diagonal-slash framework **do not count**.

No repeated gold half-discs, halo circles, upright gold plates, radiating arcs, or standard diagonal cuts across multiple speakers. Do not automatically place all figures in the identical lower-left slot or repeat the same scale/crop. Each speaker gets a distinct structural recipe and only one personally meaningful motif. If geometry appears similar at thumbnail scale, reject and **redesign the geometric scaffold**, not merely a landmark or texture.

### Final production gate (all mandatory)
1. Identity corresponds to the requested person and the **original** supplied photo; one person only; no accidental substitutions.
2. Complete convincing anatomy; requested podium/removable obstruction absent; hands, arms and watch/microphone are not mangled or involuntarily cropped.
3. Figure and representational motif strictly olive-green engraved; gold only background geometry, paper exposed; no third ink or clothing colors.
4. Paper silence clearly occupies 35–45%, with a usable contiguous release zone for web type.
5. Unique **geometry skeleton** confirmed against all other speakers; at least four structural differences, not a palette/content swap.
6. One verified, specific biographical symbol rather than a collage of generic travel, theological, or church props.
7. Crisp intentional engraved strokes at full size and identifiable likeness at thumbnail size; do not accept distortion from repeatedly editing renders.

Fail any check → regenerate from the primary photograph with a revised geometry recipe, not from the failed output.

## Related project authorities
- `docs/WESTSIDE-COLOR-AUTHORITY.md`
- `static/dore-design/magazine-profile.olive-speaker.v1.json`
- Westside Design OS (final authority for runtime tokens and CSS)
- https://github.com/yanliudesign/mono-color-skill (printing principles only, not its default poster palette or typography)

This document stores the prompt and review rules. It does not claim that all twelve images are complete, that the visual gate has passed, or that production CSS is changed.
