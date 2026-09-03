# DORÉ BIBLICAL WORLD BW-1 RECONCILIATION — 2026-09-02

Status: SWEEP_01 / BOUNDED_RECONCILIATION
Related canonical work: Biblical World foundation; `MEM-SWEEP-01`
Source milestone: `dore-core/knowledge/foundation/biblical-world/BW-1-GRADUATION.md`
Machine evidence: `reports/DORÉ-BW1-ENTITY-GRADUATION.json`

## Classification

- BW-1 Entity identity and aliases: `VERIFIED_COMPLETE` as a bounded section milestone.
- Whole Biblical World curriculum: **not complete**; the source explicitly reserves `BIBLICAL_WORLD_COMPLETE` for BW-1 through BW-6 plus a canon-spanning blind exam.
- Current disposition: retain BW-1 as completed foundation capability; continue later Biblical World sections under their own evidence gates.

## Evidence reviewed

The narrative graduation record states that BW-1 completed on 2026-08-22 and names a bounded capability set: evidence-bearing entity ingestion, person/place separation, stable individual identities, canonical attestations, conservative cross-language aliases, scoped ranking, same-name aggregation, natural-language count intent, Search runtime connection and explicit protection against substring identity pollution.

The persisted machine report records `status: PASS` and every named boolean check as true, including schema, entity coverage, Chinese alias coverage, Mary/Samaria separation, translated-name cluster expansion, person-only counts, natural-language count intent, unseen count-intent transfer, public runtime connection, preserved Scripture Search and public loader connection.

Machine counts in that report are:

- entities: 4,293;
- Chinese aliases: 2,876;
- Mary direct-alias candidates: 2;
- Mary source-name cluster: 6;
- Samaria candidates: 1.

## Contradiction found and resolved

Before this sweep pass, `BW-1-GRADUATION.md` claimed **3,592** conservative Chinese aligned aliases, while the persisted machine graduation report records **2,876**.

This is a real evidence conflict, but it does not overturn the bounded PASS: the measured count is descriptive, while the persisted machine report still records all graduation checks as true.

Resolution applied:

1. machine report governs the measured count because it is the direct persisted graduation output;
2. `BW-1-GRADUATION.md` was corrected from 3,592 to 2,876;
3. a Sweep 01 reconciliation note was added to the source milestone so the correction is provenance-preserving rather than silent;
4. no stronger `BIBLICAL_WORLD_COMPLETE` claim was issued.

Correction commit: `c410f0094f0e61db721bd9cbd1ad900e19208bf4`.

## Completed-work evaluation

### Original objective
Build a source-grounded biblical entity layer that can resolve names and aliases without collapsing different people/places, while supporting natural-language Search and ONE scope.

### Completion evidence
Strong for the bounded BW-1 milestone: the source graduation record plus a persisted machine `PASS` report with explicit real-corpus checks and public-runtime connection.

### Current quality
Good bounded foundation. The strongest quality is evidence discipline: source identity is preserved, translated aliases are routing aids rather than identity proof, same-looking names remain separable, and uncertain identity questions are not silently collapsed.

### Durable learning
A product-facing entity layer should separate routing convenience from identity evidence. Scope can rank candidates without erasing global alternatives. Machine graduation reports should govern measured facts when narrative summaries conflict.

### Weaknesses / debt
The corrected count discrepancy shows that narrative completion documents can drift from generated reports. Future graduation writers should preferably source measured totals directly from the report or include report hashes/commit references.

### Revisit trigger
Revisit BW-1 if later source updates, alias-generation changes, entity-merge policy changes, Search regressions or BW-2+ integration alter the entity corpus or its measured coverage.

### Current disposition
`KEEP / MAINTAIN AS REGRESSION GATE`. Do not reopen merely because of the corrected count; reopen only on a substantive corpus/behavior change.

## Capability retention

BW-1 retains reusable capability in:

- provenance-bearing entity ingestion;
- conservative alias alignment;
- identity/type separation;
- scope-aware candidate ranking;
- ambiguity-preserving aggregation;
- natural-language entity-count routing;
- Search/ONE shared biblical-world substrate design;
- evidence reconciliation between narrative milestones and machine reports.

## Sweep implication

This bounded family is now reconciled at the milestone-evidence level. The finding does not alter P01 or its environment blocker and does not justify Sweep 01 completion. Remaining Biblical World sections and other unreconciled source families must continue to be reviewed independently.
