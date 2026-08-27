# DORÉ Original-Language Reader v0.3 Evidence Ledger — 2026-08-27

Status: SWEEP-01 / BOUNDED RECONCILIATION
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`
Related evidence registers: `DORÉ-MISSING-EVIDENCE-REGISTER.md` (`ME-013`), `DORÉ-SUPERSEDED-RETIRED-INDEX.md` (`SR-012`)

## Bounded evidence reviewed

- `dore_core/readers/original_language.py` — current original-language corpus reader, explicitly identified as v0.3;
- `dore-core/readers/original_language_reader.py` — historical v0.1 reader already indexed as superseded by `SR-012`;
- `dore-core/tests/test_original_language_reader.py` — reader-specific acceptance specification;
- `dore-core/knowledge/foundation/scripture-canon/CORPUS-SNAPSHOT-2026-08-26.yaml`;
- `dore-core/knowledge/foundation/scripture-canon/CORPUS-READER-ACCEPTANCE-v0.1.yaml`;
- existing `ME-013` / `SR-012` interpretations.

## Reconciliation findings

1. The current reader implementation has materially advanced beyond the historical v0.1 file. `dore_core/readers/original_language.py` v0.3 pins the same OSHB and MorphGNT/SBLGNT snapshots, maps MorphGNT book prefixes across all 27 New Testament books, preserves source-native and Doré canonical references, separates textual and analytical provenance, and validates surface/reference/provenance/language invariants.
2. Mixed-language handling is also more mature than the historical v0.1 interpretation. v0.3 provides verse-level Hebrew/Aramaic boundaries for Daniel and Ezra, while deliberately returning `und` / warning at Daniel 2:4 where verse-level classification is unsafe. This is a stronger implementation of the existing uncertainty-preservation doctrine rather than a claim of corpus completion.
3. Reader-specific acceptance evidence has **not** advanced in parallel. `dore-core/tests/test_original_language_reader.py` still imports a placeholder module, explicitly says it is non-runnable pending package/import wiring, and records `TEST_SPEC_PENDING_PACKAGE_WIRING`.
4. Therefore two claims must remain separate: **current reader implementation = real active foundation progress**; **reader-specific acceptance suite = still `UNKNOWN_NEEDS_EVIDENCE`**. The v0.3 implementation must not be downgraded to the old v0.1 description, but it also must not be promoted to `VERIFIED_COMPLETE` without executing the acceptance contract.
5. `CORPUS-READER-ACCEPTANCE-v0.1.yaml` still requires zero critical failures across pinned-snapshot use, complete reference mapping, zero silent token loss, textual/analytical provenance, mixed-language integrity, reversible normalization, witness/analysis separation, uncertainty preservation, and Lesson-03 provenance tests. No new pass artifact for these gates was found in this bounded batch.
6. Existing canonical classifications remain correct: `SR-012` governs the v0.1→v0.3 implementation supersession; `ME-013` remains valid for the missing runnable acceptance evidence. No separate new active workstream is justified in the Master Register.
7. No P01 state, code, runtime, credential, deployment or subtitle action was modified by this sweep batch.

## Current disposition

- historical `dore-core/readers/original_language_reader.py` v0.1: `SUPERSEDED` as current executable behavior, retained as provenance;
- current `dore_core/readers/original_language.py` v0.3: `CORE/CONTINUOUS` Language/Text foundation progress;
- reader-specific runnable acceptance: `ACTIVE / UNKNOWN_NEEDS_EVIDENCE`;
- Scripture Canon / global corpus graduation: unchanged and separately evidence-gated.

## Smallest future proof

Wire the current v0.3 reader into an importable executable test target, convert the existing acceptance specification into runnable tests, execute bounded pinned OSHB/MorphGNT fixtures, and persist explicit pass/fail results for token reconciliation, reference identity, provenance, Daniel/Ezra mixed-language boundaries, and uncertainty behavior. Only then reconsider `ME-013`.

## Sweep interpretation

This batch accounts for the current-vs-historical original-language reader implementation boundary. It does **not** justify `VERIFIED_COMPLETE` for Sweep 01 or for the reader/corpus curriculum, and it creates no new human or environment blocker.
