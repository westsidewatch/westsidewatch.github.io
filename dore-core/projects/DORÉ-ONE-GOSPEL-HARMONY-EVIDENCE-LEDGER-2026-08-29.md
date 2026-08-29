# DORÉ ONE GOSPEL HARMONY EVIDENCE LEDGER — 2026-08-29

Status: ACTIVE / SWEEP-01 EVIDENCE
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`
Product: ONE

## Bounded evidence reviewed

- `docs/one/GOSPEL-HARMONY-FINAL-AUDIT-20260829.md`;
- `docs/dore/lessons/ONE-LESSON-001-GOSPEL-HARMONY-AUDIT.md`;
- commit `e90f829d02b1c7fb6d1d44a679da4f4c9c15b464` (`audit(one): complete four-Gospel harmony review`);
- commit `d085f5d28d900eeabfb770b578745f754e58b66d` (`fix(one): distinguish resurrection harmony scenes`);
- commit `828d3f567062495f1e0a1ef381d75a125d875ffd` (`fix(one): show Luke Plain Sermon as explicit harmony event`).

## Current classification

### Four-Gospel structural audit
`VERIFIED_COMPLETE` as a bounded maintenance/audit milestone.

Evidence:

- 23 Gospel source files traversed;
- 288 discoverable harmony rows inspected;
- 0 wrong Gospel-column / chapter-bound findings after the audit pass;
- 0 sermon-label placement findings in the machine-readable audit result;
- syntax validation was part of the final audit workflow;
- the audit artifact is persisted in `docs/one/` rather than existing only in an ephemeral workflow log.

This proves a bounded structural/reference audit. It does **not** prove that every harmony row is finally correct in historical-event identity, editorial extent, chronology, or reader-facing semantics.

### Editorial harmony reconciliation
`MAINTENANCE / ACTIVE`.

The final audit deliberately surfaced 12 duplicate event labels with differing verse extents/notes for editorial judgment rather than mechanically normalizing them. Subsequent product corrections demonstrate that this distinction matters:

- Matthew 28's broad `向門徒顯現` row conflated different resurrection appearances across time/place; it was corrected to preserve the Galilee appearance separately and to label the Great Commission parallels as different post-resurrection scenes.
- Matthew 5 initially placed `平原寶訓` in the correct Luke column but under a generic shared `寶訓` event label. User-facing inspection showed that data-column correctness did not make the reader-facing semantics sufficiently clear; the data was then split into explicit `山上寶訓` and `平原寶訓` rows.

Therefore the remaining editorial review set must stay open as maintenance evidence debt rather than being silently declared complete.

## Retrospective evaluation

**Original objective**
Correct the Matthew 5 harmony presentation and inspect ONE's existing Gospel-harmony data for wider errors.

**Completion evidence**
A repository-persisted whole-family audit traversed 23 source files / 288 rows and subsequent commits corrected two concrete semantic problems exposed by code/data review plus actual product inspection.

**Current quality**
Stronger than before: column placement and chapter bounds have bounded machine checks, and the maintenance process now explicitly distinguishes textual similarity from identity of historical event. However the audit itself still records 12 editorial-difference groups and 6 non-literal parser-review findings, so a universal `all Gospel harmony editorial content verified` claim is not supported.

**What was learned**

1. Data correctness and interface communication are separate acceptance layers.
2. Gospel parallels must distinguish `similar teaching / theological parallel` from `same historical event`.
3. Differences in Gospel order, scene, extent or editorial note should be represented, not erased merely to make tables uniform.
4. Automated structural checks should surface ambiguous/non-literal blocks rather than silently skip them.
5. Product acceptance must include reader-visible inspection after data/schema validation.

**Weaknesses / debt**

- 12 duplicate-label groups remain an explicit editorial review set rather than a completed reconciliation ledger.
- 6 harmony blocks were non-literal/JS-expression parser-review findings in the audit; they were surfaced rather than falsely counted as parsed.
- Harmony knowledge is duplicated across multiple Gospel source files, which permits extent/note drift even when individual rows remain syntactically valid.
- Current audit checks reference placement and chapter bounds, not historical-scene identity or full exegetical correctness.

**Revisit trigger**
Reopen when ONE harmony data is centralized, when a canonical Scripture-relationship graph becomes available, when any reader flags a misleading parallel, or before treating ONE harmony as a reusable authoritative relationship source for Search/Library/other products.

**Current disposition**
Keep the structural audit closed as a bounded `VERIFIED_COMPLETE` maintenance milestone. Keep Gospel-harmony editorial reconciliation open under ONE `MAINTENANCE`; do not promote ONE itself to complete.

## Capability retention

This milestone contributes reusable evidence for:

- repository-scale structured-content audit;
- Gospel parallel / event-identity editorial judgment;
- evidence-preserving automation that self-removes one-shot workflows after persisting results;
- distinction between schema/data correctness and reader-visible product semantics;
- maintenance learning loop: user report → bounded whole-family audit → semantic correction → product-facing correction → durable lesson/evidence.

These capabilities should transfer to Liming Library Scripture relationships and future ONE/Search relationship validation only after held-out evidence confirms transfer; this ledger is not itself proof of cross-product autonomy.

## Master Register interpretation

No top-level status change is warranted. `ONE` remains `MAINTENANCE`.

The canonical ONE row should treat the 2026-08-29 four-Gospel structural audit as a second bounded verified maintenance milestone alongside the earlier Priority-A private-R2 delivery cutover, while retaining editorial harmony reconciliation as open maintenance rather than claiming full harmony completion.

## P01 isolation

No P01 subtitle code, runtime state, deployment, binding, credential, priority, ordering, or blocker state was modified by this reconciliation.
