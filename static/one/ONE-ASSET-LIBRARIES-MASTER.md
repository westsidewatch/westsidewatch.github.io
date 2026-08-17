# ONE — Illustration Asset Libraries Master

Status: **LOCKED / CANONICAL / PROJECT-WIDE**

This document is the binding asset-library companion to `ONE-COVER-ILLUSTRATION-MASTER.md` and `one-cover-policy.js`.

## 1. Two libraries, one resolver

ONE permanently separates illustration provenance into two asset libraries:

### A. Doré Original Library

Runtime objects/files:

- `one-dore-cover-registry.js`
- `one-dore-assets-241.js`
- chapter mappings such as `one-dore-round3-maps.js`

Rules:

- contains the canonical 241 Gustave Doré Bible illustration assets only;
- Doré IDs 001–241 are immutable;
- generated images, ONE Studio images, derivative images, substitute images and unrelated historical illustrations must never be inserted into this library;
- an asset may not claim a Doré ID unless it is the verified Doré original represented by that ID;
- P1 ORIGINAL_LOCKED assignments remain permanently superior to all non-Doré assets.

### B. ONE Studio Fixed Asset Library

Runtime file:

- `one-studio-assets.js`

Rules:

- contains reviewed and permanently frozen ONE Studio generated illustrations;
- may also contain approved non-Doré historical/public-domain fixed illustrations when explicitly registered with truthful provenance;
- must never copy, alias, renumber or impersonate a Doré original;
- every asset must have a stable asset ID and stable source path before production use;
- generated assets use `Generate Once`: create, review, freeze, register, then reuse permanently;
- a registered asset and registered chapter assignment are immutable in normal production; replacement requires an explicit project-wide editorial decision, never runtime fallback.

## 2. One writer / resolver

`ONE_COVER_POLICY` is the sole layer allowed to write `study.illustration`.

Resolution order:

1. canonical Doré/master chapter assignment;
2. if and only if no approved Doré/master assignment exists, ONE Studio Fixed Asset assignment;
3. otherwise no illustration.

Never:

`page -> fuzzy search -> substitute image`

Always:

`chapter -> canonical mapping -> fixed asset library -> ONE_COVER_POLICY -> cover/body renderer`

## 3. Provenance must remain visible internally

Doré assets carry:

- `origin: DORE_ORIGINAL_LIBRARY`
- `doreId`
- `master: ONE-DORE-241-MASTER-MAPPING`

ONE Studio assets carry:

- `origin: ONE_STUDIO` or another truthful non-Doré provenance value;
- `studioAssetId`;
- `fixedStatus: FIXED_GENERATED` when generated;
- `master: ONE-STUDIO-FIXED-ASSET-LIBRARY`.

Reader-facing UI does not show production/debug terminology, but internal metadata must never blur the distinction between an original Doré work and a generated/non-Doré work.

## 4. Chapter assignment rule

A chapter with any approved Doré/master allocation under the canonical hierarchy keeps that allocation. A ONE Studio asset fills only a genuinely unassigned chapter.

This means visual novelty, de-duplication or a newly generated image can never displace an ORIGINAL_LOCKED Doré image.

## 5. File organization

Recommended fixed paths:

- Doré: managed by the canonical 241 registry; do not reorganize by book.
- ONE Studio: `/images/one/illustrations/<BOOK_CODE>/<BOOK_CODE>-<CHAPTER>.webp`

Examples:

- `/images/one/illustrations/REV/REV-02.webp`
- `/images/one/illustrations/REV/REV-22.webp`

The source artwork file contains artwork only. ONE cover typography, gold frame, Morning Star and chapter labels are rendered by the canonical ONE visual system and are never baked into the source asset.

## 6. Revelation precedent

Revelation establishes the first full use of this architecture:

- Doré P1 originals remain locked for chapters 1, 6, 12, 18, 20 and 21;
- other chapters may receive reviewed ONE Studio fixed assets;
- chapter 22 may use the approved full-colour ONE Studio treatment, while chapters 1–21 remain in the black/white engraving family unless an original asset dictates otherwise;
- all assets, regardless of library, are presented by the same canonical full-bleed cover and 5:8 body-plate system.

Any local book rule that writes a generated/non-Doré image into the Doré 241 library is invalid.