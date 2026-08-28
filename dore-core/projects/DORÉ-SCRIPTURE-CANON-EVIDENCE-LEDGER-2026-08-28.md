# DORÉ Scripture Canon Foundation Evidence Ledger — 2026-08-28

Status: SWEEP-01 / BOUNDED RECONCILIATION
Related canonical work: `SCRIPTURE-CANON`, `CORE`
Related missing evidence: `ME-009`, `ME-013`

## Evidence reviewed

- `dore-core/knowledge/foundation/scripture-canon/COURSE-01-SCRIPTURE-CANON.md`
- `dore-core/knowledge/foundation/scripture-canon/CORPUS-READER-SPEC-v0.1.md`
- `dore-core/knowledge/foundation/scripture-canon/CORPUS-READER-ACCEPTANCE-v0.1.yaml`
- `dore-core/knowledge/foundation/scripture-canon/CORPUS-INGESTION-MANIFEST-v0.1.yaml`
- `dore-core/knowledge/foundation/scripture-canon/CORPUS-SNAPSHOT-2026-08-26.yaml`
- existing Sweep reconciliation for `dore-core/readers/original_language_reader.py` and `ME-013`
- existing `ME-009 — Foundation Scripture Canon course completion`

## Classification

**Current classification:** `ACTIVE / FOUNDATION / UNKNOWN_NEEDS_EVIDENCE` for Course 01 completion.

The course itself remains explicitly `IN PROGRESS`. This is not a downgrade: substantial machine-readable foundation work exists, but specification, pinned-source preparation and partial reader implementation are not equivalent to satisfying the course graduation contract.

## What is already real

1. The course has a coherent machine-readable architecture: stable canonical identity, provenance separation, witness/analysis distinction, licensing discipline, original-language substrate and explicit epistemic classes.
2. A corpus reader contract exists with fail-closed rules and ten critical acceptance gates (`CR001–CR010`), including zero silent token loss, reference preservation, textual/analytical provenance, mixed-language integrity and uncertainty preservation.
3. A reproducible pinned corpus snapshot now exists for OSHB and MorphGNT/SBLGNT, with concrete commit SHAs and an explicit no-silent-upgrade rule.
4. Existing Sweep evidence separately confirms a real original-language reader foundation, while its dedicated acceptance suite remains non-runnable pending package/import wiring (`ME-013`).

## Contradiction / chronology reconciliation

`CORPUS-INGESTION-MANIFEST-v0.1.yaml` still lists `pin_upstream_commit_SHAs_before_reproducible_ingestion` under `still_required`. That statement is now stale as an operational requirement: `CORPUS-SNAPSHOT-2026-08-26.yaml` subsequently pins both upstream commits and establishes the reproducibility rule.

Current governing interpretation:

- **snapshot pinning:** satisfied as a bounded foundation milestone on 2026-08-26;
- **full corpus-reader acceptance / Lesson 03 completion:** not satisfied;
- **Course 01 completion:** not satisfied.

The older manifest should remain as historical provenance; its stale `still_required` line is superseded by the later snapshot rather than treated as current truth.

## Completion evaluation

### Original objective
Create a provenance-aware canonical Scripture substrate that can normalize stable references, preserve textual/source identity, distinguish analysis from text, support Hebrew/Aramaic/Greek research and refuse unsupported certainty.

### Completion evidence
Only bounded sub-milestones are currently evidenced: architecture/specification, source-manifest work, pinned corpus snapshot and partial reader implementation. No persisted artifact was found that passes the full Course 01 exercises plus all ten corpus-reader critical gates.

### Current quality
The architecture is strong in provenance and epistemic discipline. The main weakness is evidence-layer fragmentation: several files describe required behavior, later files satisfy individual prerequisites, and the runnable acceptance boundary is still incomplete. Without a single executable graduation report, narrative progress could be mistaken for course completion.

### Durable learning
- Pinned source identity is a separate milestone from reader correctness.
- Textual surface and analytical metadata require separate provenance.
- Mixed-language Scripture must fail closed rather than inherit a book-level language label.
- A later evidence artifact may supersede an older `still_required` item without making the larger course complete.

### Debt / missing evidence
- executable Course 01 canonical-reference exercises;
- runnable reader-specific acceptance wiring;
- zero-silent-token-loss reconciliation across bounded pinned fixtures and eventually full supported corpora;
- persisted `CR001–CR010` results with zero critical failures;
- explicit Lesson 03 completion artifact before issuing `LESSON_03_CORPUS_FOUNDATION_COMPLETE`;
- course-status update only after the exact graduation contract passes.

## Current disposition

- Keep the architecture and pinned snapshot.
- Treat commit pinning as a bounded completed prerequisite, not an unfinished requirement.
- Keep Course 01 `ACTIVE / FOUNDATION`.
- Do not issue `LESSON_03_CORPUS_FOUNDATION_COMPLETE` or Course 01 completion.
- Do not create a revisit item: this is unfinished foundation work, not a historically completed milestone needing redesign.
- Do not interrupt P01; all next evidence work is subordinate to the active subtitle critical path.

## Smallest next proof

Wire the existing reader acceptance specification into an executable bounded fixture suite, run the Course 01 canonical-reference exercises and `CR001–CR010` against the pinned snapshot, persist token/provenance/mixed-language results, and only then reconsider Course 01 completion.
