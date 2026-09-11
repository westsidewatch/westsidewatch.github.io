# DORÉ WESTSIDE CONTEXT EVIDENCE LEDGER — 2026-09-11

Status: SUPERSEDED_DUPLICATE / CORRECTION_RECORD
Sweep: DORÉ Memory Consolidation Sweep 01
Canonical evidence ledger: `DORÉ-WESTSIDE-CONTEXT-ADAPTER-EVIDENCE-LEDGER-2026-09-08.md`
Related checkpoint: `DORE-MEMORY-SWEEP-01-CHECKPOINT-44-2026-09-08.md`
Related: CORE, NERVOUS-SYSTEM, MEM-SWEEP-01

## Why this file is superseded

This file was created after Westside Context had already been fully reconciled in Sweep Checkpoint 44 and the canonical evidence ledger dated 2026-09-08. Its first version also made an incorrect bounded-search conclusion: it inspected `dore-core/tests/` but missed the actual Westside Context test and benchmark family under the repository-level `tests/` directory.

The governing classification therefore remains the earlier evidence-based judgment:

`COMPLETED_REVISIT_CANDIDATE / MAINTENANCE`

for the bounded minimal Westside Context adapter milestone, with stronger/current retrieval acceptance still evidence-gated.

This file is retained only as provenance for the duplicate-ledger error and its correction. It must not override the 2026-09-08 canonical ledger.

## Corrected evidence inventory

The bounded implementation is real and includes:

- `dore-core/context/README.md`;
- `dore_core/context/compiler.py`;
- `dore_core/context/interface.py`;
- `dore_core/context/packet.py`;
- `dore_core/context/retrieve.py`;
- `tests/test_westside_context.py`;
- `tests/test_context_retrieve.py`;
- `tests/test_context_packet.py`;
- `tests/test_westside_context_capability.py`;
- `tests/benchmark_westside_context.py`;
- capability registration as local, network-free, read-only `westside.context` with `docs/MASTER_SITE_ARCHITECTURE.md` as source of truth;
- merged PR #409 for the minimal adapter;
- merged PR #412 for CJK natural-question retrieval and hierarchy-boundary repair.

The test/benchmark assets cover hierarchy/provenance, bounded read-only packet retrieval, capability authority boundaries, bilingual real-architecture queries, CJK fallback and natural-question recall. PR #412 specifically added deterministic CJK n-grams and a regression for `多雷探索是什么意思？`.

## Evidence boundary that remains open

The earlier canonical ledger's boundary still stands:

- no dedicated persisted current post-PR-412 acceptance artifact was found proving the full Context benchmark against the current canonical architecture;
- no broad unseen-query precision/recall claim is justified;
- no measured scale/latency history justifies heavier retrieval infrastructure;
- multi-source Context assembly and broad cross-faculty real-work consumption remain unproven.

The smallest useful next proof remains a persisted current-head Context benchmark/acceptance run against current `MASTER_SITE_ARCHITECTURE.md`, including unseen Chinese natural-language questions and precision-negative cases.

## Consolidation lesson

Sweep evidence discovery must search the repository evidence family, not only a similarly named subdirectory. A missing artifact in `dore-core/tests/` is not evidence that no test exists when top-level `tests/`, commit history, PRs or workflow artifacts may contain the governing proof.

This duplicate is now explicitly superseded so it cannot later downgrade or contradict the canonical 2026-09-08 Context judgment.

P01 subtitle/runtime state and ordering were not modified.
