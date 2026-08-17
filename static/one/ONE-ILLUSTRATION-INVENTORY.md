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

ONE produces **chapter artwork, not precomposed cover images**.

Each chapter has at most one canonical artwork asset. That same artwork is reused in two contexts:

1. the shared ONE cover renderer places it beneath the canonical ornate frame, book/chapter typography, brand gold and any contextually appropriate Morning Star;
2. the chapter body may display the same artwork as an illustration without duplicating or regenerating the image.

Historical Doré/approved engravings and ONE Studio generated engravings are therefore equivalent at the renderer boundary: both are canonical chapter artwork. Their provenance differs, but the cover system does not.

Never generate title typography, chapter numbers, production metadata, asset paths, status labels, dates, ornate UI frames or other cover-template elements inside a generated artwork asset. Those belong to the shared renderer.

Do not create separate `cover` and `illustration` generated files for one chapter. **One chapter artwork asset feeds both uses.**

## Current priority inventory

### Psalms — 150 chapters

Historical direct art currently retained only where a defensible chapter-specific relationship survives canonical cleanup. All other Psalms are `GENERATE-ONCE` and must be illustrated from the actual Psalm, not from a generic mood pool.

Production method: work Psalm-by-Psalm; read its text/superscription; choose one principal visual idea; create one engraving; store and bind permanently before advancing.

### Isaiah — 66 chapters

`HISTORICAL`: 1, 13, 27, 36, 37.

`GENERATE-ONCE`: all remaining chapters unless a verified direct historical engraving is found before generation.

Each generated scene must come from that chapter's actual oracle, historical event, sign, vision, judgment, consolation, servant passage, restoration image, or eschatological imagery. Do not substitute a generic prophet image.

### John — 21 chapters

`HISTORICAL`: 2, 4, 6, 8, 11, 18, 19, 21.

`GENERATE-ONCE`: 1, 3, 5, 7, 9, 10, 12, 13, 14, 15, 16, 17, 20.

Direct historical art must remain fixed. Missing chapters receive one chapter-specific engraving only.

### Other currently loaded ONE books

Genesis; 1 Samuel; 2 Samuel; Matthew; Mark; Luke; 1 Thessalonians; 2 Thessalonians are governed by the global canonicalizer/audit before production.

Before generating for any chapter:

1. inspect its post-canonicalization illustration state;
2. retain a direct, unique, testament-correct historical image as `HISTORICAL`;
3. if absent, mark `GENERATE-ONCE`;
4. never generate merely because another chapter uses the same historical event unless this chapter itself lacks a valid direct image;
5. once generated and committed, mark `FIXED-GENERATED` and remove it from pending production.

## Asset identity

Canonical generated asset naming:

`/images/one/illustrations/<book-code>/<book-code>-<chapter-2digit>.webp`

Example: `/images/one/illustrations/JHN/JHN-01.webp`.

One chapter has one canonical generated asset path. A user-approved revision replaces that chapter's canonical asset rather than creating uncontrolled `v2`, `final2`, `new`, or alternate production paths.

Metadata binds the asset explicitly to book + chapter and includes:

- `type: generated`
- `artist: ONE Studio`
- `relation: direct`
- correct `testament`
- chapter-specific `title` and `alt`
- `morningStar` only when compositionally appropriate

## Completion rule

A book's illustration production is complete only when every chapter is either `HISTORICAL` or `FIXED-GENERATED`. The antique no-image cover is a safe production state, not the final completed illustration state.