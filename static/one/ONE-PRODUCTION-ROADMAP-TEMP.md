# ONE Production Roadmap — TEMPORARY

> Status: TEMPORARY EXECUTION LEDGER — DORÉ STUDIO MEMORY ONLY
>
> Doré AI rule: before every ONE Studio / Doré-continuation production cycle, read this file together with `ONE-DORE-LIVING-STUDIO.md` and `ONE-DORE-VISUAL-GRAMMAR.md`, take the first unchecked task that is ready, and update this ledger after the approved asset is persisted and audited.
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

## Non-negotiable production rules

1. Never fill a Missing Plate by fuzzy thematic similarity to a Doré image.
2. Source-locked Doré originals outrank generated assets.
3. Canonical parallel, historical match, and typology reuse must remain explicit policy data.
4. ONE Studio plates become COVERED only after editorial approval, stable asset registration, explicit chapter assignment, and audit verification.
5. Every completed batch must update this temporary ledger before moving to the next batch.
6. Atlas, Scripture Graph, and Search must all consume the shared Canon Index rather than creating separate book/chapter identities.
7. This ledger is Doré Studio operational memory only and remains outside reader runtime/load behavior.
8. Final cleanup task after all work is complete: delete this file.

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
1. [ ] 25 耶利米哀歌 — 1 missing, 4/5 covered. **Exact gap confirmed: chapter 3.** Existing coverage: ch.1 Doré 127; ch.2/4/5 explicit historical match 127. Next action: ONE Studio plate for ch.3 only.
2. [ ] 41 馬可福音 — 3 missing, 13/16 covered. High reader visibility; finish immediately after Lamentations.
3. [ ] 08 路得記 — 2 missing, 2/4 covered.
4. [ ] 32 約拿書 — 2 missing, 2/4 covered.
5. [ ] 31 俄巴底亞書 — 1 missing.
6. [ ] 57 腓利門書 — 1 missing.
7. [ ] 63 約翰二書 — 1 missing.
8. [ ] 64 約翰三書 — 1 missing.
9. [ ] 65 猶大書 — 1 missing.
10. [ ] 37 哈該書 — 2 missing.
11. [ ] 29 約珥書 — 3 missing.
12. [ ] 34 那鴻書 — 3 missing.
13. [ ] 35 哈巴谷書 — 3 missing.
14. [ ] 36 西番雅書 — 3 missing.
15. [ ] 53 帖撒羅尼迦後書 — 3 missing.
16. [ ] 56 提多書 — 3 missing.
17. [ ] 61 彼得後書 — 3 missing.

Gate after each book:
- [ ] Plate provenance recorded.
- [ ] ONE Studio registry updated if generated.
- [ ] Chapter assignment explicit.
- [ ] Reader cover rendering checked.
- [ ] Mobile cover rendering checked.
- [ ] Global audit remains 66/1189 with 0 structural FAIL.
- [ ] Missing Plate count reduced by exactly the approved number.
- [ ] This ledger updated with completion date / PR / new backlog count.

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
- [ ] No fuzzy Doré mappings introduced.
- [ ] All generated plates have provenance/version metadata.
- [ ] Full reader regression pass.

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
2. [ ] Confirm Atlas shipped and audited.
3. [ ] Confirm Scripture Graph shipped and audited.
4. [ ] Confirm Search shipped and audited.
5. [ ] Confirm global ONE audit is green.
6. [ ] Archive any useful permanent rules into the appropriate canonical specification if necessary.
7. [ ] DELETE `static/one/ONE-PRODUCTION-ROADMAP-TEMP.md` because its list/progress function is finished.
