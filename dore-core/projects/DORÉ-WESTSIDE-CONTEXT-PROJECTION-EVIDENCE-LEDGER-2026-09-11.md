# DORÉ WESTSIDE CONTEXT PROJECTION — EVIDENCE LEDGER

Date: 2026-09-11
Status: ACTIVE / BOUNDED FOUNDATION EVIDENCE
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01`

## Scope

This ledger reconciles the repository's minimal Westside Context projection: the read-only compiler/retriever that derives a local SQLite/FTS5 context index from canonical Westside architecture Markdown without changing the public site or replacing Doré Knowledge/Memory.

## Evidence reviewed

- `dore-core/context/README.md`
- `dore_core/context/compiler.py`
- `dore_core/context/packet.py`
- `tests/benchmark_westside_context.py`

## What is implemented

1. Canonical Markdown remains source of truth. The projection records source path and SHA-256 and never writes back to the architecture source.
2. The implementation is dependency-light: Python stdlib + SQLite/FTS5, with a CJK substring fallback for the known `unicode61` segmentation limitation.
3. Compiled nodes preserve heading level, parent relation, source order, complete section content, source path and source hash.
4. The canonical site architecture receives one bounded structural adaptation: top-level descriptive bullets may be promoted to derived child nodes while indented evidence remains inside the parent block.
5. Retrieval can return both direct nodes and provenance-bearing `ContextPacket` values containing canonical ancestor chains.
6. The serialized packet boundary is explicit and read-only data, not an instruction or mutation capability.
7. A real benchmark script exists with 12 retrieval cases plus 3 ancestor-chain context cases against `docs/MASTER_SITE_ARCHITECTURE.md`.

## Evidence boundary

The repository proves a real implemented local context-projection capability and a concrete benchmark contract. This bounded sweep did not find a persisted benchmark-run artifact proving the current repository head passes all 12 retrieval and 3 context-chain cases. The existence of the benchmark script must therefore not be promoted into a current `VERIFIED_COMPLETE` quality claim.

The architecture also intentionally rejects premature vector/database expansion: a vector database or third-party memory framework is not justified until measured retrieval gaps require one. This is a durable lightweight-system principle consistent with `能力越大、負擔越小`.

## Current classification

- Westside Context projection implementation: `CORE/CONTINUOUS / IMPLEMENTED_FOUNDATION`
- current benchmark acceptance: `UNKNOWN_NEEDS_EVIDENCE`
- public-site architecture impact: none; `docs/MASTER_SITE_ARCHITECTURE.md` remains canonical
- replacement of Doré Knowledge/Memory: explicitly out of scope

## Smallest useful next evidence

Execute `tests/benchmark_westside_context.py` against the current canonical `docs/MASTER_SITE_ARCHITECTURE.md`, persist the source SHA, 12/12 retrieval result and 3/3 ancestor-chain result, and keep that result as a regression artifact. If any case fails, repair the smallest retrieval/compiler issue first rather than adding a heavier retrieval stack by default.

## Revisit trigger

Revisit the architecture only if representative real queries expose a retrieval/context gap that cannot be solved by the present SQLite/FTS5 + bounded CJK fallback model, or if canonical architecture structure changes make the derived-node rules brittle.

## P01 isolation

No P01 subtitle state, ordering, blocker, deployment or audio/transcription dependency was modified by this reconciliation.
