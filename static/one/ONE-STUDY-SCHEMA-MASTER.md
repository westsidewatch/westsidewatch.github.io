# ONE — Study Schema Master

Status: **CANONICAL / MANDATORY**

This is the data-contract layer for every ONE Bible book. A new book may introduce new content, but it may not invent a new chapter-study shape.

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

Optional modules may be empty when the genre does not benefit from them. Empty optional modules must not produce empty visual pages.

## Runtime gate

The script currently loaded as `remaining-nt-epistles-runtime-check.js` is retained at that path to avoid disturbing the proven `index.html` load order, but its role is now **global**: it is the ONE Study Schema Gate.

It runs after book data and before `one-app.js`, audits every registered `ONE_DATA.studyBooks` volume, normalizes unsafe scalar rows into safe tuples, suppresses incomplete maps, records `window.ONE_STUDY_SCHEMA_AUDIT`, and hides empty optional Cross References / comparison shells.

The legacy filename must not be interpreted as a scope limitation.

## New-book gate

Before merge, every new book must satisfy all of the following:

1. Copy the data shape from a completed working book, not from memory.
2. Register every chapter in `chapterStudies`.
3. Never use string arrays where the renderer expects row arrays.
4. Confirm `window.ONE_STUDY_SCHEMA_AUDIT.ok === true`.
5. Confirm no new schema-normalization warnings are introduced by the new book.
6. Test chapter 1, a middle chapter, and the final chapter.
7. Test at least one populated Cross References module and one intentionally omitted optional module.
8. Verify desktop and mobile rendering.

## Failure policy

A malformed optional module must degrade safely rather than corrupt the page. A structural book/chapter mismatch is a release-blocking schema error. Do not patch individual chapters in the renderer; fix the book data or the canonical schema gate.
