# DORÉ WESTSIDE CONTEXT EVIDENCE LEDGER — 2026-09-11

Status: ACTIVE / BOUNDED FOUNDATION EVIDENCE
Sweep: DORÉ Memory Consolidation Sweep 01
Related: CORE, NERVOUS-SYSTEM, MEM-SWEEP-01

## Scope reviewed

- `dore-core/context/README.md`
- `dore_core/context/compiler.py`
- `dore_core/context/interface.py`
- `dore_core/context/packet.py`
- `dore_core/context/retrieve.py`
- top-level `tests/test_westside_context.py`
- top-level `tests/test_context_retrieve.py`
- top-level `tests/test_westside_context_capability.py`
- top-level `tests/test_context_packet.py`
- top-level `tests/benchmark_westside_context.py`
- commits `51e158a`, `b474bbb`, `1483562`, `0eaab14`, `75d5120`, `14603e6`, `905209a`, merge `9ed724f`

## What is implemented

A real dependency-light Westside Context foundation exists. It is not only a design memo.

The current implementation:

- treats canonical Markdown as source of truth;
- builds a disposable SQLite / FTS5 projection rather than writing back to canonical architecture;
- records source path and source SHA-256 on every derived node;
- preserves heading hierarchy, parent relationships and source ordinal;
- promotes bounded canonical structural bullets without rewriting the source document;
- returns context packets containing the match plus canonical ancestor chain and provenance;
- provides a read-only consumer protocol and Doré-facing retrieval adapter;
- uses SQLite FTS5 first and a local CJK substring/n-gram fallback rather than adding a new vector/database dependency;
- explicitly keeps Context Packet as data, not instruction or write authority;
- is registered as the local, network-free, read-only `westside.context` capability with `docs/MASTER_SITE_ARCHITECTURE.md` as source of truth.

This is consistent with the governing engineering principle `能力越大、負擔越小`: use the smallest local mechanism that solves the measured retrieval problem before adding heavier infrastructure.

## Correction to the first bounded sweep interpretation

The first version of this ledger incorrectly said that no dedicated Westside Context acceptance test or real baseline benchmark had been found. That conclusion came from inspecting only the `dore-core/tests/` inventory. The actual Westside Context tests and benchmark live under the repository-level `tests/` directory.

The corrected evidence inventory includes:

- `tests/test_westside_context.py`: hierarchy/provenance, FTS retrieval, empty-query behavior, CJK substring fallback, question-form CJK retrieval and canonical ancestor recovery;
- `tests/test_context_retrieve.py`: real `MASTER_SITE_ARCHITECTURE.md` adapter retrieval, bounded packet size, provenance/path and read-only boundary checks;
- `tests/test_context_packet.py`: packet ancestry/provenance and no-write-path behavior;
- `tests/test_westside_context_capability.py`: capability-registry contract proving local adapter execution, no network, no write access, canonical source-of-truth binding and no accidental new memory/vector/graph store;
- `tests/benchmark_westside_context.py`: a 12-query bilingual real-architecture baseline benchmark covering Main Site, Journal, Emmaus, ONE, 多寫, 黎明書局, editorial model, knowledge context, Church Prayer Meeting, Doré Search, Storybook and 多雷探索.

Commit history also shows the CJK retrieval defect was not merely documented: merge `9ed724f` changed the compiler to use deterministic CJK n-grams, corrected section-boundary handling and added a Chinese natural-question regression (`多雷探索是什么意思？`).

No workflow run was found for the merge commit in the available pull-request workflow query, so the existence of these executable tests/benchmark must not be upgraded into a claim that a fresh current-head suite has been persisted as passing.

## Evidence boundary after correction

Repository evidence now strongly supports that the Context foundation has dedicated executable test/benchmark assets and a deliberate capability boundary. What remains unproven strongly enough in this sweep is narrower:

- a fresh persisted current-head execution of the full Context test set and 12-query real baseline after all later source/compiler changes;
- quantitative precision/recall beyond the fixed baseline queries, especially ambiguous CJK terms;
- source-SHA rebuild/invalidation behavior after canonical-source change as an explicit regression;
- latency/size behavior as `MASTER_SITE_ARCHITECTURE.md` grows;
- materially different Doré faculties consuming the public adapter in real work, rather than only contract-level capability discovery;
- regression behavior under malformed/hostile FTS syntax and future source-structure evolution.

## Current classification

- Westside Context compiler / projection / packet / capability boundary: `ACTIVE / IMPLEMENTED_FOUNDATION`.
- Dedicated fixture tests and real bilingual baseline benchmark: `IMPLEMENTED_EVIDENCE_ASSETS`.
- Read-only provenance and no-write architecture rule: implemented and directly tested as a bounded contract.
- Production-quality retrieval / broad cross-faculty operational acceptance: `UNKNOWN_NEEDS_EVIDENCE`.
- No `VERIFIED_COMPLETE`, revisit, superseded or retired classification is justified yet.

## Smallest useful next proof

Run the current top-level Context test family plus `tests/benchmark_westside_context.py` against current `docs/MASTER_SITE_ARCHITECTURE.md`, persist the exact output and source SHA, then add one materially different Doré consumer exercising `westside.context` through capability discovery. Only after that should this bounded foundation be considered for a stronger completed milestone.

A passing fixture/current-head suite still must not be promoted to broad cognition or memory completion; it would close only the Context foundation acceptance gap.

## Sweep disposition

Retain this layer as small shared infrastructure. Do not replace it with a vector database or third-party memory framework unless benchmark evidence exposes a retrieval gap that the current SQLite/FTS5 + bounded CJK fallback cannot solve.

This correction supersedes the earlier ledger sentence claiming there were no dedicated Westside Context tests/benchmark. P01 subtitle/runtime state and ordering were not modified by this review.
