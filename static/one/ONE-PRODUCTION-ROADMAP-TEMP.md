# ONE Production Roadmap — TEMPORARY

> Status: TEMPORARY EXECUTION LEDGER — DORÉ STUDIO MEMORY ONLY
>
> Doré AI rule: before every ONE Studio / Doré-continuation production cycle, read this file together with `ONE-DORE-LEARNING-CURVE.md`, `ONE-DORE-LIVING-STUDIO.md` and `ONE-DORE-VISUAL-GRAMMAR.md`, take the first unchecked task that is ready, and update this ledger after the approved asset is persisted and audited.
>
> Runtime isolation: this is Markdown research/production memory only. It must never be referenced by `static/one/index.html`, any `<script>`, `<link>`, preload, loader, service worker, `ONE_DATA`, `ONE_COVER_POLICY`, Canon Index, or reader code. Its presence beside the Doré Studio documents does not make it a runtime dependency.
>
> Deletion rule: delete this file after the Missing Plate backlog reaches 0 and Atlas / Scripture Graph / Search are fully shipped and verified.

## Current verified baseline

- Canon: 66/66 books, 1189/1189 chapters.
- Structural FAIL: 0.
- Actionable WARNING excluding Missing Plate: 0.
- Timeline coverage: 1189/1189.
- Covered chapter plates: 206.
- Missing Plate BACKLOG: 983.
- Existing cover provenance: 186 A1 source-locked Doré, 11 A2 canonical parallel, 6 A3 historical match, 2 A4 explicit typology, 1 B1 ONE Studio editorial fixed.
- Fuzzy semantic Doré expansion: DISABLED.
- Canon Index: 1189/1189 searchable chapters, 441 explicit places, 71 map IDs, 715 chapters with explicit places, 2290 normalized chapter-to-chapter Scripture edges, 0 broken graph edges.

## Progress protocol — this ledger is the fast path

The purpose of this ledger is to eliminate repeated full-canon recounting during normal production. Doré AI should normally trust the last **LIVE_VERIFIED** ledger state and inspect only the active/changed chapter. A full-canon progress recount is required only when a reconciliation check fails, at a major phase gate, or before final deletion of this ledger.

Synchronization is also part of the Doré learning curriculum. At book, wave and final-canon checkpoints, follow `ONE-DORE-LEARNING-CURVE.md`: revisit canonical Doré originals, compare the completed sequence, identify stable visual rules and Studio drift, and promote reusable findings into Living Studio / Visual Grammar. The goal is to avoid a full 1,189-chapter recount after every plate **without** losing repeated exposure to the original Doré Bible corpus.

### Stable chapter identity

Every generated Missing Plate task must use a stable chapter key:

`BOOK-CHAPTER`, zero padded, for example `025-003` = Lamentations 3.

Before generating a multi-chapter/book row, Doré AI must expand that row into chapter-key child tasks. A book row is complete only when every child chapter key is `DONE`.

### Recognized states

Doré AI must distinguish these states and never collapse them prematurely:

- `TODO` — no accepted plate yet.
- `GENERATED` — candidate image exists; still editable.
- `APPROVED` — editor explicitly says the image itself needs no more modification.
- `PERSISTED` — approved binary has a stable file/asset ID and revision.
- `ASSIGNED` — chapter key explicitly resolves to that stable asset through the Studio registry/resolver.
- `DEPLOYED` — the commit containing the final asset + assignment is on the production branch/site deployment.
- `LIVE_VERIFIED` — the public ONE chapter actually renders the expected asset/revision with no fallback, cache substitution, broken cover, or wrong chapter mapping.
- `DONE` — synonym for `LIVE_VERIFIED`; only now may `[x]` be written in this ledger.

**Hard rule:** editorial approval alone is not completion. A plate cannot be marked `[x]` until public/live verification succeeds.

### Required proof for every DONE chapter

When a chapter becomes `DONE`, its ledger record must contain enough compact evidence for Doré AI to recognize it without rescanning the whole canon:

`KEY | DONE | asset_id | revision | assignment_source | deploy_commit_or_PR | live_url_or_route | verified_date`

Example format only:

`025-003 | DONE | studio-lam-003 | r1 | Studio registry | PR/commit | /one/?book=25&chapter=3 | YYYY-MM-DD`

If any proof field is missing or contradicts the current registry/live route, Doré AI must downgrade the entry from `DONE` and reconcile it.

### Simple synchronization with the full-canon state

Use a two-level check instead of rereading all 1189 chapters after every plate:

1. **Delta check after each completed plate** — verify only the changed chapter key against the final Studio asset registry/resolver and the live route. If it matches, mark `DONE` and decrement `Missing Plate BACKLOG` by exactly 1. Also perform the chapter-level learning comparison required by the Learning Curve against neighboring/canonical Doré precedents.
2. **Book checkpoint** — when the last missing child task in a book becomes `DONE`, compare that book's ledger DONE keys/count with the canonical cover audit for that book only. Then review that book's complete visual sequence and record a learning harvest; do not rescan unrelated books merely for progress counting.
3. **Global checksum checkpoint** — at the end of each production wave, compare only global totals: `Covered + Missing = 1189`, structural FAIL = 0, and the audit Missing count must equal this ledger's Missing count. Separately perform the Learning Curve's cross-genre canonical sample so Doré AI continues learning from original Bible plates across the canon.
4. **Escalation rule** — perform a full 66-book/1189-chapter recount only if a delta/book/global checkpoint disagrees, if registry identity is ambiguous, or at the final completion gate. A full-canon learning review is also required at final completion even if counts already match.

This makes the normal relationship:

`Ledger DONE keys ↔ explicit registry assignment ↔ deployed live chapter`

The three must stay one-to-one. A mismatch is an error, not a reason to guess.

### Current progress counters

- Generated backlog completed after this ledger baseline: **0 / 983**.
- Missing Plate remaining: **983 / 983**.
- Missing Plate completion: **0.00%**.
- Covered total: **206 / 1189**.

Doré AI must update these four counters whenever a chapter first reaches `DONE`. Do not change them for `GENERATED`, `APPROVED`, `PERSISTED`, `ASSIGNED`, or `DEPLOYED` states.

## Non-negotiable production rules

1. Never fill a Missing Plate by fuzzy thematic similarity to a Doré image.
2. Source-locked Doré originals outrank generated assets.
3. Canonical parallel, historical match, and typology reuse must remain explicit policy data.
4. ONE Studio plates become COVERED only after editorial approval, stable asset registration, explicit chapter assignment, deployment, and live verification.
5. Every newly `DONE` chapter must update this ledger before moving to the next task.
6. Atlas, Scripture Graph, and Search must all consume the shared Canon Index rather than creating separate book/chapter identities.
7. This ledger is Doré Studio operational memory only and remains outside reader runtime/load behavior.
8. Book/wave/final synchronization must include the Learning Curve's required Doré-original study harvest, not only progress counting.
9. Final cleanup task after all work is complete: delete this file.

# Phase A — Missing Plate production

## A0 — Classification complete

- [x] Classify all 1189 chapters.
- [x] Separate 206 covered from 983 Missing Plate.
- [x] Grade existing provenance.
- [x] Route backlog by production grammar.
- [x] Establish production waves.

Backlog routes:
- 377 — STUDIO_SCRIPTURE_SCENE
- 167 — STUDIO_PROPHETIC_VISION
- 150 — STUDIO_PSALM_GRAMMAR
- 121 — STUDIO_EPISTLE_GRAMMAR
- 91 — STUDIO_POETIC_SYMBOLIC
- 62 — STUDIO_PROPHETIC_ORACLE
- 15 — STUDIO_APOCALYPTIC_VISION

## A1 — W1 FINISH BOOKS first

Goal: close nearly complete books before large-volume generation. Total current W1 target: 36 plates.

Execution order:
1. [ ] 25 耶利米哀歌 — 1 missing, 4/5 covered. **Exact gap confirmed: `025-003`.** Existing coverage: ch.1 Doré 127; ch.2/4/5 explicit historical match 127. Next action: ONE Studio plate for ch.3 only.
   - `025-003 | TODO | asset_id:- | revision:- | assignment:- | deploy:- | live:- | verified:-`
2. [ ] 41 馬可福音 — 3 missing, 13/16 covered. High reader visibility; before generation expand this row into the three exact missing chapter keys from the current book audit.
3. [ ] 08 路得記 — 2 missing, 2/4 covered. Expand into exact missing child keys before generation.
4. [ ] 32 約拿書 — 2 missing, 2/4 covered. Expand into exact missing child keys before generation.
5. [ ] 31 俄巴底亞書 — 1 missing. Expand into exact child key before generation.
6. [ ] 57 腓利門書 — 1 missing. Expand into exact child key before generation.
7. [ ] 63 約翰二書 — 1 missing. Expand into exact child key before generation.
8. [ ] 64 約翰三書 — 1 missing. Expand into exact child key before generation.
9. [ ] 65 猶大書 — 1 missing. Expand into exact child key before generation.
10. [ ] 37 哈該書 — 2 missing. Expand into exact missing child keys before generation.
11. [ ] 29 約珥書 — 3 missing. Expand into exact missing child keys before generation.
12. [ ] 34 那鴻書 — 3 missing. Expand into exact missing child keys before generation.
13. [ ] 35 哈巴谷書 — 3 missing. Expand into exact missing child keys before generation.
14. [ ] 36 西番雅書 — 3 missing. Expand into exact missing child keys before generation.
15. [ ] 53 帖撒羅尼迦後書 — 3 missing. Expand into exact missing child keys before generation.
16. [ ] 56 提多書 — 3 missing. Expand into exact missing child keys before generation.
17. [ ] 61 彼得後書 — 3 missing. Expand into exact missing child keys before generation.

Gate after each book:
- [ ] Every missing chapter has a stable child key.
- [ ] Every checked child is `LIVE_VERIFIED` with full proof fields.
- [ ] Plate provenance recorded.
- [ ] ONE Studio registry updated if generated.
- [ ] Chapter assignment explicit.
- [ ] Reader cover rendering checked on the deployed site.
- [ ] Mobile cover rendering checked on the deployed site.
- [ ] Book-level canonical cover audit agrees with ledger child keys/count.
- [ ] Required book-level Doré learning harvest completed and reusable findings persisted where appropriate.
- [ ] Global structural audit remains 66/1189 with 0 structural FAIL.
- [ ] Missing Plate count reduced by exactly the number of newly LIVE_VERIFIED chapters.
- [ ] This ledger updated with completion date / PR or commit / new backlog count.

## A2 — W2 HIGH VISIBILITY

Current target: 47 plates.
1. [ ] Four Gospels remaining gaps: Matthew, Luke, John after Mark completion.
2. [ ] Revelation remaining 15 plates.
3. [ ] Acts high-value narrative/map chapters where an explicit scene grammar is available.

Rule: do not let high visibility override source integrity.

## A3 — W3 BUILD REUSABLE GRAMMARS

Current target: 349 plates.
1. [ ] Psalm visual grammar — 150 chapters.
2. [ ] Epistle visual grammar — 121 chapters.
3. [ ] Poetic / wisdom symbolic grammar — 91 chapters, accounting for overlap in wave allocation as classified by audit.

Deliverable before large batch production: create one approved grammar exemplar for each family, document composition constraints, then batch only within that approved grammar.

## A4 — W4 NARRATIVE COVERAGE

Current target: 340 plates.
- [ ] Pentateuch narrative/law gaps.
- [ ] Historical books.
- [ ] Remaining Gospel/Acts narrative gaps not already closed.

## A5 — W4 PROPHETIC COVERAGE

Current target: 211 plates.
- [ ] Major prophetic visions.
- [ ] Minor prophetic oracles.
- [ ] Apocalyptic vision gaps not already completed under W2.

## A6 — Missing Plate completion gate

- [ ] Covered = 1189.
- [ ] Missing Plate BACKLOG = 0.
- [ ] Ledger generated-backlog DONE = 983/983.
- [ ] Ledger DONE keys reconcile one-to-one with explicit final registry/live assignments.
- [ ] No fuzzy Doré mappings introduced.
- [ ] All generated plates have provenance/version metadata.
- [ ] One final full 66-book / 1189-chapter reader regression pass.
- [ ] One final full-canon Doré learning synthesis completed before deleting this temporary ledger.

# Phase B — Atlas

Shared data baseline: 441 explicit places, 71 map IDs, 715 chapters with explicit place data.
1. [ ] Build Atlas reader shell using Canon Index only.
2. [ ] Place index: location → related chapters.
3. [ ] Chapter reverse link: chapter → explicit places / maps.
4. [ ] Route grouping for Abraham, Exodus, Conquest, David, Elijah/Elisha, Exile/Return, Jesus' ministry, Paul's journeys where explicit data exists.
5. [ ] Do not infer missing geography.
6. [ ] Mobile interaction and chapter deep-link verification.
7. [ ] Atlas regression against all 715 place-bearing chapters.

Completion gate:
- [ ] Every Atlas result resolves to canonical `/one/?book=X&chapter=Y` identity.
- [ ] No invented locations.
- [ ] Map and illustration remain separate layers.

# Phase C — Scripture Graph

Shared data baseline: 2290 normalized explicit chapter edges from 885 chapters; broken edges = 0.
1. [ ] Build chapter-neighborhood graph view from explicit edges only.
2. [ ] Support forward and reverse relationships.
3. [ ] Distinguish connection source types where available: explicit cross-reference, harmony/parallel, canonical policy.
4. [ ] Add direct navigation from a graph node to the target chapter.
5. [ ] Add graceful sparse-state UI for chapters with few/no explicit edges.
6. [ ] Do not introduce AI-inferred theological edges into the canonical graph.

Completion gate:
- [ ] Broken graph edges = 0.
- [ ] Every graph node uses Canon Index identity.
- [ ] Reverse traversal verified.

# Phase D — Search

Shared data baseline: 1189/1189 chapters in corpus.
1. [ ] Add reader search entry without disrupting current chapter navigation.
2. [ ] Search book names, chapter titles, story/background/observation text, chronology, explicit places, and connection text.
3. [ ] Rank exact book/chapter matches ahead of broad body-text matches.
4. [ ] Add result grouping/filtering for book, chapter, place, chronology, connection when useful.
5. [ ] Search result opens canonical chapter URL.
6. [ ] Mobile keyboard/focus/accessibility regression.

Completion gate:
- [ ] Search corpus remains 1189/1189.
- [ ] Known-book and known-place smoke tests pass.
- [ ] No separate search-only chapter registry.

# Phase E — Cross-system integration

1. [ ] Atlas location → chapter → Graph neighbors works.
2. [ ] Graph node → chapter → Atlas location works where geography exists.
3. [ ] Search result → chapter → Atlas/Graph context works.
4. [ ] All three systems share Canon Index IDs and URLs.
5. [ ] Desktop and mobile regression across representative OT, Gospel, Epistle, Revelation chapters.

# Phase F — Final cleanup

Only after all prior gates pass:
1. [ ] Confirm Missing Plate BACKLOG = 0.
2. [ ] Confirm ledger DONE generated backlog = 983/983 and final full-canon reconciliation passes.
3. [ ] Confirm final full-canon Doré learning synthesis has been harvested into permanent Studio learning documents.
4. [ ] Confirm Atlas shipped and audited.
5. [ ] Confirm Scripture Graph shipped and audited.
6. [ ] Confirm Search shipped and audited.
7. [ ] Confirm global ONE audit is green.
8. [ ] Archive any useful permanent rules into the appropriate canonical specification if necessary.
9. [ ] DELETE `static/one/ONE-PRODUCTION-ROADMAP-TEMP.md` because its list/progress function is finished.
