# Doré Learning Heartbeat

Status: ACTIVE
Established: 2026-08-23
Updated: 2026-08-24

## Rule
Doré learning does not wait for a human to say `continue`, `execute`, `next`, or approve each course. On wake, read current state, execute `AUTONOMOUS_ALLOWED` work, self-check, persist evidence/failures/state/next action, and continue while evidence and authority remain clear. Course completion requires exam gates. Retention/transfer failures reopen learning.

Human approval is reserved for irreversible/destructive external actions, paid obligations, official outward doctrinal/editorial publication, brand/governance changes, new private credentials/access, material legal/security/privacy consequences, or genuine unresolved value conflicts.

## Major completed milestones
- Biblical Languages I: `PASS / GRADUATED`.
- Researcher 04 — Autonomous Learning I: `COMPLETE → RETENTION_WATCH`, final 12/12 PASS.
- Researcher 05 — Biblical Concept Development I: `PASS / GRADUATED → RETENTION_WATCH`, independent resurrection transfer 6/6 PASS.
- First durable sensory → research → brain consolidation: `馬利亞有幾位?` consolidated to `research.nt.mary-count` after independent research and 7/7 examination.
- Generic Brain → Product repository regression established without per-question answer logic.
- Researcher 06 — Noise-Aware Scripture Retrieval I: `PASS / GRADUATED → RETENTION_WATCH` after Unit 09 fresh integration-transfer final 7/7 PASS.

## Sensory state checked this heartbeat
`dore-core/memory/sensory-active.json` contains no `RESEARCHING` signal without a `brain_node`. Existing Mary signal remains `CONSOLIDATED → research.nt.mary-count`; therefore no live sensory research preempted the course loop.

## Researcher 06 retention transfer — Phase B
The product-neutral evidence contract separates:
- `quotation_recovery`;
- `paraphrase_retrieval`;
- `correction_proposal`;
- `review`;
- `abstain`.

Development execution previously passed 6/6 under frozen thresholds while preserving provenance, abstention, and `silent_overwrite=false`.

### Sealed held-out first run — PASS
The held-out partition was frozen before opening at commit:
`136a3eec9e4a35df2fe46bb7a2e9a8a8873d1248`.

Frozen fixture:
`fixtures/researcher06-retention-phase-b-heldout.json`.

First-run evidence:
`evidence/researcher06-retention-phase-b-heldout-first-run.json`.

Result: **6/6 PASS** with no post-open threshold tuning.

Coverage included adjacent-verse quotation, genuine paraphrase, ASR-like corruption, ambiguity/review, ordinary negative, one-verse control, and Search-like/subtitle-like/neutral surfaces under one evidence class.

### Critical limitation
Both dev and held-out cases still supplied candidate evidence channels as fixture inputs. Therefore this is a transfer PASS for classification and evidence discipline, not proof of independent candidate retrieval, calibrated probabilities, production Search accuracy, or production subtitle accuracy.

No Researcher 07 is justified by this result.

## Retention Practicum 02 — Probe A advanced
The authoritative Scripture corpus has now been located and its provenance contract identified.

- Generated corpus: `static/dore/search-index.json` (`dore.browser-search-core.v1`).
- Generator: `scripts/build_dore_browser_search_index.py`.
- Current Bible Search workflow asserts >=31,000 verses and canonical control refs.
- Generator pins CUV Traditional 1919, WEBU, OSHB/WLC and MorphGNT/SBLGNT snapshots.
- Current `static/dore/dore-search.js` confirms free-text retrieval is verse-by-verse; it does not independently generate contiguous 2/3-verse free-text candidates.

Evidence:
`evidence/researcher06-retention-practicum02-corpus-location-2026-08-24.md`.

Result: **PASS for corpus location and implementation-gap classification.**

### Execution boundary encountered
The available repository connector cannot execute repository code and does not expose the multi-megabyte one-line generated search-index body through its file-content action. A full-corpus top-K window-retrieval measurement therefore cannot be honestly produced in this run.

This is recorded as an unresolved tool/execution dependency, not a learning failure and not evidence for opening Researcher 07.

## Current next action
`BUILD_AND_EXECUTE_NON_PRODUCTION_CONTIGUOUS_WINDOW_RETRIEVAL_HARNESS_WHEN_REPOSITORY_EXECUTION_OR_FULL_CORPUS_BYTES_ARE_AVAILABLE`.

Harness contract is already fixed: same-chapter contiguous windows of lengths 1/2/3, component-ref provenance, expected refs used only for evaluation, frozen candidate budget, verse-only baseline comparison, and first failures preserved.

After Probe A execution, inspect an existing generic semantic mechanism for paraphrase candidate generation. Semantic similarity may retrieve but must never become textual-correction evidence by itself.

## Brain/Product status
This heartbeat changed no product-readable knowledge node in `static/dore/brain/knowledge-index.json`; therefore no Brain → Product regression was required. Researcher 06 remains a graduated capability under retention testing, not automatically production-promoted.

## Closed-loop remaining acceptance
Repository-level durable sensory → research → brain and generic Brain → Product regression are evidenced. Browser-level acceptance remains: a current Search deployment must itself POST a fresh unknown query into sensory memory and later surface the consolidated live brain result without per-question UI logic.
