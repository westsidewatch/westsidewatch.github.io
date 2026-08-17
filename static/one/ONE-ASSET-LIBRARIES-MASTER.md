# ONE — Illustration Asset Libraries Master

Status: **LOCKED / CANONICAL / PROJECT-WIDE**

This document is the binding asset-library companion to `ONE-COVER-ILLUSTRATION-MASTER.md` and `one-cover-policy.js`.

## 1. Two libraries, one resolver

ONE permanently separates illustration provenance into two asset libraries.

### A. Doré Original Library — immutable originals

Runtime objects/files:

- `one-dore-cover-registry.js`
- `one-dore-assets-241.js`
- chapter mappings such as `one-dore-round3-maps.js`

Rules:

- contains the canonical 241 Gustave Doré Bible illustration assets only;
- Doré IDs 001–241 and verified file relationships are immutable;
- generated images, ONE Studio images, derivative images, substitute images and unrelated historical illustrations must never be inserted into this library;
- an asset may not claim a Doré ID unless it is the verified Doré original represented by that ID;
- P1 ORIGINAL_LOCKED assignments remain permanently superior to all non-Doré assets;
- an original Doré placement is not replaced for visual novelty, quality preference, colour treatment or later generated alternatives.

### B. ONE Studio Versioned Asset Library — fixed at runtime, replaceable editorially

Runtime file:

- `one-studio-assets.js`

ONE Studio assets are **not equivalent to original-source assets**. They are stable production assets, but they may be improved or replaced later.

Rules:

- contains reviewed ONE Studio generated illustrations and approved non-Doré fixed illustrations;
- must never copy, alias, renumber or impersonate a Doré original;
- every active asset must have a stable asset ID and stable source path before production use;
- runtime always uses the currently approved active revision;
- runtime is never allowed to regenerate, search for or silently swap an image;
- editors may explicitly replace an active ONE Studio asset after review using a new revision;
- replacement keeps revision history so the previous approved image is traceable;
- a chapter may also be explicitly reassigned to another approved ONE Studio asset when editorial judgment changes;
- replacement/reassignment requires a stated editorial action; it is never a fallback mechanism.

Therefore:

**Doré = source-locked.**

**ONE Studio = versioned editorial asset.**

`Generate Once` means "do not regenerate at page load". It does **not** mean a generated image can never be improved in a later editorial revision.

## 2. One writer / resolver

`ONE_COVER_POLICY` is the sole layer allowed to write `study.illustration`.

Resolution order:

1. canonical Doré/master chapter assignment;
2. if and only if no approved Doré/master assignment exists, current active ONE Studio assignment;
3. otherwise no illustration.

Never:

`page -> fuzzy search / generation -> substitute image`

Always:

`chapter -> canonical mapping -> approved asset revision -> ONE_COVER_POLICY -> cover/body renderer`

## 3. Provenance and revision metadata

Doré assets carry:

- `origin: DORE_ORIGINAL_LIBRARY`
- `doreId`
- `master: ONE-DORE-241-MASTER-MAPPING`

ONE Studio assets carry:

- `origin: ONE_STUDIO` or another truthful non-Doré provenance value;
- stable asset ID;
- revision number;
- active approved source path;
- palette;
- scripture reference;
- approval/replacement note where relevant;
- `master: ONE-STUDIO-VERSIONED-ASSET-LIBRARY`.

Reader-facing UI does not show production/debug terminology, but internal metadata must never blur an original Doré work with a generated/non-Doré work.

## 4. Chapter assignment rule

A chapter with any approved Doré/master allocation under the canonical hierarchy keeps that allocation. A ONE Studio asset fills only a genuinely unassigned chapter.

A later ONE Studio replacement may improve composition, Scripture fidelity, engraving quality or visual continuity **only within that non-Doré chapter assignment**. It cannot displace a locked Doré original.

## 5. File organization and revisions

Canonical paths:

- Doré: managed by the canonical 241 registry; do not reorganize by book.
- ONE Studio current approved asset: `/images/one/illustrations/<BOOK_CODE>/<BOOK_CODE>-<CHAPTER>.webp`

Examples:

- `/images/one/illustrations/REV/REV-02.webp`
- `/images/one/illustrations/REV/REV-22.webp`

When an image is replaced, the public/current path may remain stable while Git history retains the prior file; alternatively archival revision files may be retained outside the reader-facing path. In either case the registry revision number must increase.

The source artwork file contains artwork only. ONE cover typography, gold frame, Morning Star and chapter labels are rendered by the canonical ONE visual system and are never baked into the source asset.

## 6. Revelation precedent

Revelation establishes the first full use of this architecture:

- Doré P1 originals remain locked for chapters 1, 6, 12, 18, 20 and 21;
- chapters 2–5, 7–11, 13–17, 19 and 22 may receive ONE Studio versioned assets;
- chapters 1–21 stay in the black/white engraving family;
- chapter 22 is the approved exception and may use the full-colour life-river / New Jerusalem / Bright Morning Star treatment;
- if a generated Revelation illustration is later judged weak, it may be explicitly replaced with revision 2, 3, etc. without touching the Doré library;
- all assets, regardless of library, are presented by the same canonical full-bleed cover and 5:8 body-plate system.

Any local book rule that writes a generated/non-Doré image into the Doré 241 library is invalid.