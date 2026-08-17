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

ONE separates the **portrait chapter cover** from the **chapter-body artwork presentation**.

### Cover

Every chapter cover remains portrait, book-like and full-bleed. This is fixed across all 66 books.

- The cover is rendered by the shared ONE template.
- Artwork fills the portrait cover field; typography is deliberately overlaid on the image.
- The canonical ornate gold frame, book/chapter hierarchy, brand gold and any contextually appropriate Morning Star belong to the renderer, not to the source artwork.
- Historical and generated artwork may require renderer cropping/repositioning for the portrait cover, but the source artwork itself is not destructively rewritten for the cover.
- Do not generate a separate precomposed cover image.

### Chapter-body illustration

The illustration shown inside the chapter follows the artwork's canonical source rules:

- verified Doré / approved historical artwork keeps **its original aspect ratio** — portrait remains portrait; landscape remains landscape;
- ONE Studio generated artwork is **landscape by default and by canonical production rule**;
- chapter-body presentation shows the artwork itself, without cover typography or the cover frame baked into the image.

Therefore a generated chapter normally has one landscape canonical artwork asset which is reused by the portrait cover renderer through controlled crop/repositioning and displayed uncropped in the chapter body.

Historical Doré/approved engravings retain their native geometry and are likewise reused by the portrait cover renderer without creating a second generated asset.

Never generate title typography, chapter numbers, production metadata, asset paths, status labels, dates, ornate UI frames or other cover-template elements inside a generated artwork asset. Those belong to the shared renderer.

Do not create separate generated `cover` and `illustration` files for one chapter. **One canonical artwork asset feeds both uses.**

## Current priority inventory

### Psalms — 150 chapters

Historical direct art currently retained only where a defensible chapter-specific relationship survives canonical cleanup. All other Psalms are `GENERATE-ONCE` and must be illustrated from the actual Psalm, not from a generic mood pool.

Production method: work Psalm-by-Psalm; read its text/superscription; choose one principal visual idea; create one landscape engraving; store and bind permanently before advancing.

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
5. never generate merely because another chapter uses the same historical event unless this chapter itself lacks a valid direct image;
6. once generated and committed, mark `FIXED-GENERATED` and remove it from pending production.

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
- `aspect: landscape` for ONE Studio generated artwork
- `morningStar` only when compositionally appropriate

## Completion rule

A book's illustration production is complete only when every chapter is either `HISTORICAL` or `FIXED-GENERATED`. The antique no-image cover is a safe production state, not the final completed illustration state.