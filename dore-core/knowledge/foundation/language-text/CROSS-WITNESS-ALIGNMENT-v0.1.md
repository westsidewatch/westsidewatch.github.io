# DORÉ Cross-Witness Alignment — v0.1

Status: **FOUNDATION IMPLEMENTATION CONTRACT**

## Purpose

Doré must relate textual witnesses through stable canonical passage identity without collapsing one witness into another. Alignment is a relationship layer, not a harmonized replacement Bible.

## Invariants

1. Every aligned item retains `witness_id`, language, edition and provenance.
2. Canonical IDs are routing identities, not claims that every textual tradition has identical versification or contents.
3. Missing text is never synthesized.
4. LXX, Vulgate, Hebrew/Aramaic, Greek NT, Chinese and English witnesses remain independent evidence.
5. Psalm numbering, deuterocanonical scope, additions, omitted verses and versification differences enter an exception queue until explicitly classified.
6. Copyright-restricted witnesses may be represented by lawful reader/access metadata without bulk-storing protected text.
7. Alignment errors must degrade to `REVIEW`, not false `PASS`.

## Initial exception classes

- `UNALIGNED_UNIT` — source unit has no canonical identity.
- `DUPLICATE_CANONICAL_REF` — one witness maps multiple units to one canonical identity without an explicit split/merge rule.
- `MISSING_WITNESS_AT_REF` — expected witness lacks an aligned unit at a reference.
- `UNKNOWN_WITNESS` — metadata is unavailable.
- `WITNESS_NOT_INGESTED` — expected witness did not enter the audit.
- `VERSIFICATION_DIFFERENCE` — known reference-system difference requiring mapping rather than correction.
- `CANON_SCOPE_DIFFERENCE` — witness contains material outside the Protestant-66 routing baseline.
- `TEXTUAL_ABSENCE_OR_ADDITION` — genuine textual-tradition difference, not an ingestion failure.
- `ACCESS_ONLY_WITNESS` — licensed/copyright witness available through external reader/API but not locally retained.

## Milestone definition

`CROSS_WITNESS_ALIGNMENT_ENGINE_READY` requires:

- executable grouping by `canonical_ref_id`;
- witness identity preservation;
- machine-readable audit report;
- exception queue rather than silent filling;
- CI coverage for identity preservation and missing-witness behavior.

`CORPUS_WIDE_ALIGNMENT_AUDITED` is a later execution milestone. It requires real full-corpus witness inventories, explicit versification exception classification and a persisted report. Engine readiness must not be mislabeled as corpus completion.
