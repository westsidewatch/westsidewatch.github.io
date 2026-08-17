# ONE — Cover + Illustration Master Standard

Status: **LOCKED / CANONICAL / PROJECT-WIDE**

This is the binding cover-and-illustration layer of `ONE-VISUAL-STANDARD.md` and `one-cover-policy.js`. It applies to **all 66 books and all 1,189 chapters**, including chapters not yet produced. A local book implementation may not override it.

## 1. Governing principle

ONE uses two separate but joined systems:

1. **Illustration asset** — the narrative/theological image assigned to a chapter.
2. **Cover system** — the fixed ONE editorial frame, typography, brand-gold ornament and Morning Star language that presents that image.

The illustration may change by chapter. The cover identity does not.

An illustration is selected/created once, verified, then treated as a fixed asset. Runtime must reference the fixed asset; it must not guess, fuzzy-search, inherit, or silently substitute another image.

## 2. Illustration priority — immutable order

The allocation order is:

- **P1 ORIGINAL_LOCKED** — Doré's original/canonical scripture placement. Permanent lock.
- **P2 OFFICIAL_PARALLEL** — direct/official parallel scripture use.
- **P3 HISTORICAL_MATCH** — same person, event, or historical setting.
- **P4 TYPOLOGY** — clear theological, typological, prophecy/fulfilment relationship.
- **P5 SEMANTIC_EXPANSION** — strong match to the actual meaning of the illustration.
- **P6 DEUTEROCANON_EXPANSION** — deuterocanonical Doré plate reused by genuine meaning.
- **P7 VISUAL_DIVERSITY** — de-duplication, opening-cover variety and local spacing only.

P1 can never be overwritten. P2–P6 may only be replaced by a strictly higher-priority relationship. P7 never overrides P1–P6.

Existing/earlier-built ONE pages have **no priority** over this hierarchy.

## 3. Doré fixed assets

The 241 Doré IDs and their verified file relationships are fixed infrastructure.

- Never renumber a Doré ID.
- Never rematch an ID to another plate to make an existing page convenient.
- Never use fuzzy filename search as a production fallback.
- If a referenced asset is unavailable, show no wrong image.
- A Doré plate may be reused only when the allocation hierarchy genuinely permits it.

The current expanded chapter mapping is not permission to exhaust Doré beyond semantic credibility. Visual diversity is subordinate to truth of correspondence.

## 4. Future generated illustration policy

Generation is used only where a chapter needs a finished cover/illustration and no approved Doré or other verified historical asset is assigned under P1–P6.

When a chapter receives an original ONE Studio illustration:

- derive the scene from the actual chapter text, narrative, people, geography, prophetic image and theological emphasis;
- keep nineteenth-century biblical engraving character;
- use charcoal / black / deep sepia, etched linework and cross-hatching;
- maintain monumental biblical scale and controlled theological light;
- avoid glossy digital painting, cinema still, anime, comic, modern fantasy and generic biblical filler;
- generate once, review once, then freeze as a fixed chapter asset;
- register a stable local asset path before production use;
- never regenerate merely because a later page needs the same chapter image.

Reader-facing UI must never say AI, generated, fallback, placeholder, missing illustration, or production status.

## 5. Canonical cover architecture — APPROVED

The approved ONE chapter cover is **full-bleed artwork under typography**. It is not a separate image card sitting above a title panel.

### A. Full-image field

- the chapter illustration fills the complete cover field beneath the editorial system;
- artwork extends continuously behind the chapter identification and title;
- do not create a boxed illustration window followed by a separate opaque title block;
- preserve the principal subject and narrative action when positioning/cropping;
- use a controlled darkening/engraving veil only where needed for text legibility;
- the image must remain visibly continuous through the title zone, so the reader experiences one unified engraved cover.

### B. Dark antique binding treatment

- near-black / charcoal / deep olive-black antique printed-book character;
- image and binding treatment merge rather than forming two disconnected rectangles;
- no bright modern gradient background;
- tonal treatment must preserve engraved detail rather than burying the plate in black.

### C. Brand-gold foil frame

- outer fine rule + inner fine rule;
- canonical floral/baroque gilt tooling at all four corners;
- ornament reads as antique hot-stamped book tooling, never clip art;
- corner ornament density and scale remain consistent across all books;
- frame surrounds the entire cover, not merely the artwork;
- frame and ornaments never cover faces or essential narrative action.

### D. Editorial title hierarchy over artwork

The stable hierarchy is:

1. book + chapter identification — restrained;
2. concise Chinese chapter title — principal title;
3. small canonical Morning Star/divider where composition permits;
4. English book + chapter — subordinate;
5. optional concise English chapter title — smallest title tier.

Text is laid directly over the full-image field. Use local tonal control behind typography rather than an opaque title panel.

Text never obscures a face, essential action, or theological focal point. When necessary, reposition the artwork or title group before considering any crop.

### E. Production metadata is never cover content

`ONE ILLUSTRATION PROJECT`, `Fixed Asset`, `Generate Once`, asset paths, status labels and workflow notes belong only to internal documentation/asset sheets. They must never appear on the reader-facing chapter cover.

### F. Attribution

Source/artist credit remains available in chapter metadata/body presentation and is visually subordinate. It is not part of the principal cover title hierarchy.

## 6. Brand gold — locked

Canonical ONE / Westside Watch brand gold is based on **First Light Gold `#CEBD74`**.

Permitted tonal companions are derived only for print-like depth/highlight, not as new brand colors:

- base: `#CEBD74`
- highlight: `#E7D99A`
- shadow/antique: `#8E7430`

Gold application:

- frame rules;
- floral corner tooling;
- chapter/book identification;
- principal title where contrast permits;
- dividers;
- Morning Star;
- tiny editorial marks.

The effect should resemble **restrained antique gold foil / hot stamping**: slight tonal variation, no chrome, no neon, no orange brass, no exaggerated glow.

## 7. Dawn Morning Star — locked brand device

Canonical asset: `/images/westside-watch-morning-star.svg`.

Concept: **Bethlehem star + dawn horizon + gate/light path**. It is the ONE/Westside Watch sign of light before dawn.

Rules:

- the geometry is fixed; do not redesign it per book;
- use brand-gold tonal range only;
- glow is extremely restrained and subordinate to engraved linework;
- on ordinary covers it is a small editorial seal/divider within the title hierarchy;
- it may become a larger celestial element only when the chapter itself naturally supports light, dawn, guidance, promise, glory or heaven;
- never force a large Morning Star into unrelated narrative artwork;
- never place multiple competing Morning Stars on one cover.

## 8. Illustration presentation inside chapter pages — APPROVED

The chapter-body illustration is an **engraving plate**, not a generic responsive image card.

Canonical presentation:

- centered plate;
- 5:8 editorial plate frame is the default reading container;
- the source image retains its native aspect ratio inside the plate;
- never stretch, squash, or crop away narrative content merely to fill 5:8;
- black / charcoal / deep sepia engraving character consistent with the cover;
- double fine First Light Gold keyline: approximately 1px inner + 3px outer visual hierarchy, scaled responsively;
- quiet balanced margin between artwork and frame;
- no rounded-card UI, badges, gradients over the artwork, or oversized captions;
- artist + work title/source is a discreet lower-right caption in the established editorial serif system;
- caption remains outside the narrative image whenever practical;
- on mobile, scale the entire plate proportionally; never show only the left half and never distort the image.

The illustration plate is archival and contemplative. It should feel like opening a nineteenth-century illustrated Bible, not viewing a web-media card.

## 9. Cover/illustration relationship

The cover and the chapter-body illustration normally use the **same fixed chapter asset**, but they are different presentations:

- **cover:** full-bleed artwork beneath the ONE gilt frame and title system;
- **body plate:** quiet 5:8 archival presentation, full composition first, source credit second.

Do not bake title typography, chapter labels, production metadata or the ONE frame permanently into the source illustration file. Keep source art reusable and let the ONE renderer supply the cover system.

## 10. Mandatory first-chapter rule for every book

Every completed/new ONE book must have a finished Chapter 1 cover and body illustration before the book is considered visually complete.

For **Chapter 1**:

1. Check the locked Doré/master allocation first.
2. If Chapter 1 has a valid P1–P6 Doré assignment, that fixed Doré asset is used for both the cover artwork and chapter-body engraving plate. Do not generate a replacement merely for novelty.
3. If Chapter 1 has **no valid approved illustration assignment**, create one ONE Studio illustration from the actual Chapter 1 text under §4.
4. Review the generated illustration for Scripture fidelity and ONE engraving style.
5. Freeze it as a stable local fixed asset (`Generate Once`).
6. Register it to Chapter 1.
7. Render the same fixed asset through the approved full-bleed cover system and 5:8 body-plate system.

A book may not solve a missing Chapter 1 image by inheriting another book/chapter asset, fuzzy searching, or using an unrelated Doré plate.

## 11. Opening-cover diversity

Different books should not casually open with the same image because that creates false identity/repetition. However:

- original Doré placement always wins;
- direct parallel/historical correspondence wins over visual variety;
- only P7-equivalent choices may be changed for opening diversity;
- never move an ORIGINAL_LOCKED plate merely to make book openings look different.

## 12. Fixed-asset lifecycle

For every final illustration asset:

`SELECT / CREATE → VERIFY SCRIPTURE RELATION → ASSIGN PRIORITY → FIX ASSET → REGISTER → RENDER`

Never:

`PAGE LOAD → SEARCH/GUESS → SUBSTITUTE`

A chapter can exist before its final original illustration is produced. Missing future artwork must not cause an unrelated plate to be assigned merely to make the cover look complete.

## 13. Product-wide visual acceptance test

A cover/illustration pair is canonical only when all are true:

- correct chapter asset;
- no stale/fallback image;
- Doré original placement respected;
- cover uses full-bleed artwork under typography;
- no detached opaque title panel;
- First Light Gold double frame and canonical ornate corners are present;
- Morning Star follows the locked rule;
- illustration is undistorted and compositionally legible;
- Chinese title remains the principal editorial title;
- English line remains subordinate;
- body illustration uses the canonical 5:8 engraving-plate presentation;
- no production/debug terminology is reader-visible;
- mobile preserves the complete cover and illustration identity;
- historical and future ONE Studio covers look like one publication family.

Any change to these rules is a **project-wide design-system change**, never a local chapter patch.