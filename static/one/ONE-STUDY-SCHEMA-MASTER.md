# ONE — Study Schema Master

Status: **CANONICAL / MANDATORY**

This is the data-contract layer for every ONE Bible book. A new book may introduce new content, but it may not invent a new book or chapter-study shape.

## Canonical volume contract

Every registered `ONE_DATA.studyBooks[number]` volume must provide the renderer-facing fields below before merge:

- `number`: canonical Bible-book number.
- `key`: stable internal book key.
- `code`, `zhCode`, `enCode`: canonical Scripture codes used by the Chinese and English Scripture links.
- `name`, `nameEn`: Chinese and English book names.
- `summary`: non-empty book summary used by the current-book cards.
- `meta`: array of rows `[label, value]`; it must contain at least one useful row.
- `movements`: array of rows `[folio, chapter range, section title]` used by the frontispiece movement grid.
- `chapters`: ordered array containing every chapter title.
- `chapterStudies`: object containing exactly one study object for every chapter.

`context`, `core`, `period`, `nowCards`, `canonicalDoreMapping`, and audit metadata are strongly recommended when appropriate, but the fields above are the minimum shared-renderer contract.

Do not substitute local aliases such as `en` for `nameEn`, or `structure` for `movements`, in a new book. The runtime gate may normalize old legacy books for backward compatibility, but **a newly produced book must enter with zero normalization warnings**.

## Canonical chapter contract

Every `chapterStudies[n]` uses the shared ONE renderer and must provide these shapes:

- `title`, `passage`, `movement`, `story`, `position`: strings.
- `route`: array of rows `[reference, description]`.
- `background`: array of rows `[heading, explanation, geographic/application note]`.
- `scout`: array of strings.
- `connections`: array of rows `[reference, relationship, explanatory text]`. **Never pass a bare string.** A bare string is indexable character data in JavaScript and will render as broken one-character columns.
- `harmony`: array of table rows. Each row is an array; never a bare string.
- `questions`, `prepare`: arrays of strings.
- `timeline.events`: array of rows `[time/range, event, note]`.
- `map.routes`: array of rows `[route number, reference, note]` when a map is present.

When a map is present it must also provide usable `image` and `source`; `reference`, `title`, `guide`, `imageTitle`, `places`, and optional `preface` must be renderer-safe. The runtime gate fills harmless text fallbacks but suppresses a map entirely if its image/source pair is incomplete.

Optional modules may be empty when the genre does not benefit from them. Empty optional modules must not produce empty visual pages.

## Runtime gate

The script currently loaded as `remaining-nt-epistles-runtime-check.js` is retained at that path to avoid disturbing the proven `index.html` load order, but its role is now **global**: it is the ONE Study Schema Gate.

It runs after book data and before `one-app.js`, audits every registered `ONE_DATA.studyBooks` volume, validates/normalizes renderer-facing volume metadata, normalizes unsafe scalar chapter rows into safe tuples, suppresses incomplete maps, records `window.ONE_STUDY_SCHEMA_AUDIT`, and hides empty optional Cross References / comparison shells.

Backward-compatible normalization is protection for historical data, not permission for new data to drift. New production must be clean before the gate touches it.

The legacy filename must not be interpreted as a scope limitation.

## New-book gate

Before merge, every new book must satisfy all of the following:

1. Copy the volume and chapter data shape from a completed working book, not from memory.
2. Register every chapter in `chapterStudies` and ensure its count exactly matches `chapters`.
3. Provide `nameEn`, Scripture codes, `summary`, `meta`, and `movements` explicitly.
4. Never use string arrays where the renderer expects row arrays.
5. When a map exists, verify the real source image, source URL, title/reference/guide, places, and route-row shape.
6. Confirm `window.ONE_STUDY_SCHEMA_AUDIT.ok === true`.
7. Confirm **no new schema-normalization warnings** are introduced by the new book.
8. Test chapter 1, a middle chapter, and the final chapter.
9. Test at least one populated Cross References module and one intentionally omitted optional module.
10. Verify desktop and mobile rendering.
11. For multi-book batches, verify every book independently and also verify the total batch book/chapter counts before merge.

## Failure policy

A malformed optional module must degrade safely rather than corrupt the page. A structural book/chapter mismatch, missing renderer-required volume field, broken Scripture code, or missing book registration is a release-blocking schema error. Do not patch individual chapters in the renderer; fix the book data or the canonical schema gate.
