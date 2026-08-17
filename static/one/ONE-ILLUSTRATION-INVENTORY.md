# ONE — Illustration Production Inventory

Status: ACTIVE PRODUCTION CONTROL

This inventory implements `ONE-VISUAL-STANDARD.md`. It exists to prevent duplicate generation, uncontrolled variants, and chapter-image drift.

## Production states

- `HISTORICAL` — verified direct historical illustration is fixed; do not generate.
- `GENERATE-ONCE` — no verified direct historical illustration; read the chapter and create exactly one canonical ONE Studio engraving.
- `FIXED-GENERATED` — generated asset has been accepted and stored; never regenerate automatically.
- `REVISION-REQUESTED` — user explicitly requested a change to the fixed image; revise that asset only, then return to `FIXED-GENERATED`.

Runtime code must never generate images. Generation is an editorial production step; accepted images are repository assets.

## Artwork / cover separation

ONE separates the **portrait chapter cover** from the **chapter-body illustrated Scripture spread**.

### Cover

Every chapter cover remains portrait, book-like and full-bleed. This is fixed across all 66 books.

- The cover is rendered by the shared ONE template.
- Artwork fills the portrait cover field; typography is deliberately overlaid on the image.
- The canonical ornate gold frame, book/chapter hierarchy, brand gold and any contextually appropriate Morning Star belong to the renderer, not to the source artwork.
- Historical and generated artwork may require renderer cropping/repositioning for the portrait cover, but the source artwork itself is not destructively rewritten for the cover.
- Do not generate a separate precomposed cover image.

### Chapter-body illustrated Scripture spread

The old pattern of placing a bare illustration into the chapter is retired. Every chapter illustration area is now a designed **horizontal editorial spread** pairing the canonical artwork with **one chapter theme verse**.

The theme verse is selected from the actual chapter and is part of the chapter's fixed editorial metadata. It is not generated decoration and must not be invented or paraphrased as Scripture.

Layout rules:

- **Landscape artwork** — retain the full landscape image; compose the chapter theme verse with it in the horizontal spread, using the established ONE typography, spacing, antique-paper language and brand-gold accents. The image itself is not cropped merely to make room for text.
- **Portrait historical artwork** — retain the full portrait image at one side of the spread; place the chapter theme verse in a deliberately typeset text field beside it. Image + verse together form one horizontal editorial page.
- **Historical artwork always retains its native aspect ratio** in the chapter body: portrait remains portrait, landscape remains landscape.
- **ONE Studio generated artwork is landscape** and is shown uncropped in this spread.
- The theme verse reference must be visible and semantically separate from editorial labels.
- Do not bake the verse into the source image file. Artwork and typography remain separate renderer layers.

The result must feel like an intentionally designed illustrated Bible spread, never "an image dropped into the page".

## Prebuilt 66-book visual system

Cover and illustration-spread behavior is a **shared ONE system that must be completed ahead of individual book production**, not rediscovered when each new book begins.

The target state for all 66 books is:

1. every chapter has a canonical artwork identity (`HISTORICAL` or `FIXED-GENERATED`);
2. every chapter has one selected theme verse from that chapter;
3. every chapter has a fixed portrait-cover composition driven by the shared cover renderer;
4. every chapter has a fixed horizontal illustrated-Scripture spread composition driven by the shared illustration renderer;
5. book production later consumes these completed assets and metadata rather than inventing cover/illustration behavior again.

Once a chapter's artwork, theme verse, focal positioning and layout metadata are approved, they are canonical data. A later book implementation must call them; it must not silently replace, regenerate, reselect, reinterpret or redesign them.

This preproduction rule exists specifically to eliminate recurring cover/illustration regressions as new books are added.

## Current priority inventory

### Psalms — 150 chapters

Historical direct art currently retained only where a defensible chapter-specific relationship survives canonical cleanup. All other Psalms are `GENERATE-ONCE` and must be illustrated from the actual Psalm, not from a generic mood pool.

Production method: work Psalm-by-Psalm; read its text/superscription; choose one principal visual idea and one actual theme verse; create one landscape engraving when needed; store and bind both permanently before advancing.

### Isaiah — 66 chapters

`HISTORICAL`: 1, 13, 27, 36, 37.

`GENERATE-ONCE`: all remaining chapters unless a verified direct historical engraving is found before generation.

Each generated scene must come from that chapter's actual oracle, historical event, sign, vision, judgment, consolation, servant passage, restoration image, or eschatological imagery. Do not substitute a generic prophet image.

### John — 21 chapters

`HISTORICAL`: 2, 4, 6, 8, 11, 18, 19, 21.

`GENERATE-ONCE`: 1, 3, 5, 7, 9, 10, 12, 13, 14, 15, 16, 17, 20.

Direct historical art must remain fixed. Missing chapters receive one chapter-specific landscape engraving only.

### Other currently loaded ONE books

Genesis; 1 Samuel; 2 Samuel; Matthew; Mark; Luke; 1 Thessalonians; 2 Thessalonians are governed by the global canonicalizer/audit before production.

Before generating for any chapter:

1. inspect its post-canonicalization illustration state;
2. retain a direct, unique, testament-correct historical image as `HISTORICAL` in its native aspect ratio;
3. if absent, mark `GENERATE-ONCE`;
4. generate the missing ONE Studio chapter artwork as landscape;
5. select one chapter theme verse from the actual Scripture text;
6. record cover focal positioning and spread layout metadata;
7. never generate merely because another chapter uses the same historical event unless this chapter itself lacks a valid direct image;
8. once generated and committed, mark `FIXED-GENERATED` and remove it from pending production.

## Asset identity

Canonical generated asset naming:

`/images/one/illustrations/<book-code>/<book-code>-<chapter-2digit>.webp`

Example: `/images/one/illustrations/JHN/JHN-01.webp`.

One chapter has one canonical generated asset path. A user-approved revision replaces that chapter's canonical asset rather than creating uncontrolled `v2`, `final2`, `new`, or alternate production paths.

Canonical chapter visual metadata additionally records:

- `type: historical | generated`
- `artist`
- `relation: direct`
- correct `testament`
- chapter-specific `title` and `alt`
- source/native aspect
- `themeVerse.reference`
- `themeVerse.text` from the approved Scripture source
- cover focal position / crop guidance
- spread layout (`landscape` or `portrait-with-verse`)
- `morningStar` only when compositionally appropriate

## Completion rule

A chapter's visual preproduction is complete only when artwork, theme verse, portrait-cover metadata and horizontal-spread metadata are all fixed. A book is visually complete only when every chapter satisfies that condition.

The antique no-image cover is a safe production state, not the final completed illustration state.