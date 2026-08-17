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

Generation is a future production stage, not a reason to weaken the historical mapping now.

When a chapter eventually receives an original ONE Studio illustration:

- derive the scene from the actual chapter;
- keep nineteenth-century biblical engraving character;
- use charcoal / black / deep sepia, etched linework and cross-hatching;
- maintain monumental biblical scale and controlled theological light;
- avoid glossy digital painting, cinema still, anime, comic, modern fantasy and generic biblical filler;
- generate once, review once, then freeze as a fixed chapter asset.

Reader-facing UI must never say AI, generated, fallback, placeholder, missing illustration, or production status.

## 5. Canonical cover architecture

Every finished chapter cover uses one ONE architecture:

**A. Dark antique binding field**
- near-black / charcoal / deep olive-black antique book surface;
- subtle printed-cloth or aged-book texture;
- no bright modern gradient background.

**B. Brand-gold foil frame**
- outer fine rule + inner fine rule;
- restrained floral/baroque corner ornaments at all four corners;
- ornament must read as antique gilt tooling / foil stamping, not clip-art decoration;
- corners mirror consistently and never compete with the narrative image;
- frame inset and line weight remain stable across books.

**C. Illustration window**
- the illustration is the dominant visual field;
- preserve original aspect ratio and principal subject;
- never stretch or squash;
- use `object-fit: contain` where full composition matters;
- crop only when the canonical cover composition requires it and never crop away the narrative subject;
- historical and future generated illustrations use the same tonal treatment so they belong to one family.

**D. Editorial title field**
- book/chapter identification is secondary;
- concise Chinese chapter title is primary;
- English book/chapter line is tertiary;
- hierarchy must remain stable across all books;
- text never obscures a face, essential action, or the theological focal point of the image.

**E. Attribution**
- source/artist credit remains available but visually subordinate;
- metadata belongs outside the principal title hierarchy.

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
- it may appear as a small seal/divider in the title field or as a larger celestial element only when the chapter imagery naturally supports light, dawn, guidance, promise, glory or heaven;
- it is not mandatory inside every narrative illustration;
- when omitted from the image, the cover may still use the small canonical Morning Star as an editorial divider;
- never place multiple competing Morning Stars on one cover.

## 8. Illustration presentation inside chapter pages

The chapter-body illustration is an **engraving plate**, not a generic responsive image card.

Canonical presentation:

- centered plate;
- 5:8 editorial plate frame as the default reading container;
- image itself retains its native aspect ratio inside that container;
- dark/sepia engraving treatment consistent with the cover;
- double fine brand-gold keyline;
- generous quiet margin between image and frame;
- artist/title caption aligned discreetly at lower right;
- no rounded corners, drop-card UI, badges, gradients over the artwork, or oversized captions;
- on mobile, scale the whole plate proportionally; never show only the left half and never distort the image.

## 9. Cover/illustration relationship

The cover and the chapter-body illustration may use the same fixed chapter asset, but they are different presentations:

- **cover:** immersive dark binding, gilt tooling, title hierarchy, controlled image treatment;
- **body plate:** quieter archival presentation, full composition first, source credit second.

Do not bake title typography, chapter labels, production metadata or the ONE frame permanently into the source illustration file. Keep source art reusable and let the ONE renderer supply the cover system.

## 10. Opening-cover diversity

Different books should not casually open with the same image because that creates false identity/repetition. However:

- original Doré placement always wins;
- direct parallel/historical correspondence wins over visual variety;
- only P7-equivalent choices may be changed for opening diversity;
- never move an ORIGINAL_LOCKED plate merely to make book openings look different.

## 11. Fixed-asset lifecycle

For every final illustration asset:

`SELECT / CREATE → VERIFY SCRIPTURE RELATION → ASSIGN PRIORITY → FIX ASSET → REGISTER → RENDER`

Never:

`PAGE LOAD → SEARCH/GUESS → SUBSTITUTE`

A chapter can exist before its final original illustration is produced. Missing future artwork must not cause an unrelated plate to be assigned merely to make the cover look complete.

## 12. Product-wide visual acceptance test

A cover is canonical only when all are true:

- correct chapter asset;
- no stale/fallback image;
- Doré original placement respected;
- dark antique binding field;
- First Light Gold foil frame;
- four consistent ornate corners;
- Morning Star follows the locked rule;
- illustration is undistorted and compositionally legible;
- Chinese title remains the principal editorial title;
- English line remains subordinate;
- no production/debug terminology is visible;
- mobile preserves the complete cover identity;
- historical and future ONE Studio covers look like one publication family.

Any change to these rules is a **project-wide design-system change**, never a local chapter patch.