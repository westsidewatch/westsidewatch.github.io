# ONE — Canonical Cover Runtime Audit

Status: **CANONICAL CLEANUP / 2026-08-17**

This audit records the removal of the historical cover/illustration patch stack. It does not alter Doré IDs or the locked 418 chapter mapping.

## Canonical runtime chain

The only supported runtime chain is:

1. Book/content data and registries load.
2. `one-dore-cover-registry.js` loads **metadata only**.
3. `one-dore-assets-241.js` supplies the fixed 241 exact asset filenames.
4. `one-dore-round3-maps.js` supplies the current 418 chapter mapping **as data only**.
5. `one-cover-policy.js` clears legacy illustration fields and becomes the **sole chapter illustration writer**.
6. `one-app.js` renders the fixed chapter asset.
7. `one-cover-visual-v2.css`, loaded last, is the **sole canonical cover/body-illustration presentation layer**.

No `document.write` loader, fuzzy search, inherited previous image, book-specific illustration writer, or visual fix stylesheet is permitted in this chain.

## Retired from active loading

The following historical layers may remain in repository history but must not participate in current runtime:

- `one-dore-fixed-assets.js` — retired partial exact-file patch; superseded by the 241 master.
- `one-illustration-fix.css` — retired visual regression/override layer; canonical rules moved into `one-cover-visual-v2.css`.
- `one-background-fix.css` — retired cover/engraving presentation patch; no longer in the active cover CSS chain.
- `john-illustrations.js` — retired book-local illustration writer.
- `psalms-illustrations-*.js` — retired book-local illustration writers.
- `isaiah-illustrations.js` — retired book-local illustration writer.
- Genesis illustration assignment formerly inside `genesis-postfix.js` — removed; useful registry/Scripture compatibility behavior retained.

A future book must not revive any of these patterns.

## Black-cover diagnosis

### 1 Samuel 1

The locked mapping remains **Book 9 / Chapter 1 → Doré ID 114**.

A historical partial asset patch used an incorrect filename form for ID 114. The canonical 241 registry uses:

`107.Ezra Kneels in Prayer.jpg`

The chapter mapping itself is not changed.

### 2 Thessalonians 1

The locked mapping remains **Book 53 / Chapter 1 → Doré ID 240**.

The historical partial asset registry did not contain ID 240 at all, so a central policy depending on that partial table could legitimately produce no artwork/black background. The canonical 241 registry contains:

`LastJudgementDoré.jpg`

The chapter mapping itself is not changed.

## Visual corrections

The canonical `one-cover-visual-v2.css` now owns:

- full-bleed chapter artwork beneath typography;
- First Light Gold (`#CEBD74`) double cover rules;
- brighter but restrained antique-gilt corner tooling using only the locked brand-gold tonal range;
- canonical Dawn Morning Star treatment;
- 5:8 archival chapter engraving plate;
- `object-fit: contain` for the body plate;
- discreet lower-right artwork credit;
- responsive/mobile preservation of the full composition.

No `!important` regression guard is required to make this system win: it is loaded last by design.

## Invariants

This cleanup MUST NOT:

- renumber any of the 241 Doré IDs;
- rematch an existing fixed Doré ID to a different work;
- change the locked Round 3 418 chapter mapping merely to repair presentation;
- allow an existing/earlier-built page to outrank Doré source correspondence;
- reintroduce a second illustration writer;
- reintroduce a book-local cover CSS system.

## Acceptance checks before merge

Representative books to inspect in the browser:

- Genesis 1 — canonical original Doré opening.
- 1 Samuel 1 — ID 114 must render, no black cover.
- 2 Samuel 1 — verifies historical-book inheritance.
- Psalm 1 — verifies wisdom/poetry and body 5:8 plate.
- Isaiah 1 — verifies prophet cover and no old Isaiah illustration writer.
- Matthew 1, Mark 1, Luke 1, John 1 — verifies Gospel inheritance without local illustration scripts.
- 1 Thessalonians 1 and 2 Thessalonians 1 — ID 240 must render on 2 Thess 1, no black cover.

For every sample verify: full-image cover, brighter canonical gilt tooling, correct artwork, 5:8 body plate, no stale previous-book artwork, and no mobile clipping.