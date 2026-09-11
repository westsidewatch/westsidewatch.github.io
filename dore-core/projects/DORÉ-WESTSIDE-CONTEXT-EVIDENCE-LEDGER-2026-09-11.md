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
- current `dore-core/tests/` inventory

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
- uses SQLite FTS5 first and a local CJK substring fallback rather than adding a new vector/database dependency;
- explicitly keeps Context Packet as data, not instruction or write authority.

This is consistent with the governing engineering principle `能力越大、負擔越小`: use the smallest local mechanism that solves the measured retrieval problem before adding heavier infrastructure.

## Evidence boundary

No dedicated Westside Context acceptance test or persisted runtime benchmark was found in the current `dore-core/tests/` inventory reviewed in this bounded pass. Repository implementation therefore proves the foundation exists, but does not by itself prove:

- canonical `MASTER_SITE_ARCHITECTURE.md` retrieval quality on representative Chinese/English queries;
- ancestor/path correctness across all real structural edge cases;
- stable CJK recall/precision under ambiguous terms;
- source-SHA rebuild/invalidation behavior after canonical-source change;
- latency/size behavior on the full canonical architecture;
- actual cross-faculty consumption in Doré Core;
- regression safety against malformed FTS queries or source-structure evolution.

## Current classification

- Westside Context compiler / projection / packet boundary: `ACTIVE / FOUNDATION`.
- Read-only provenance and no-write architecture rule: implemented design property; retain.
- Production-quality retrieval / cross-faculty operational acceptance: `UNKNOWN_NEEDS_EVIDENCE`.
- No completed/revisit/superseded/retired classification is justified from this batch.

## Smallest useful next proof

Create and persist one bounded acceptance suite that compiles the current canonical `docs/MASTER_SITE_ARCHITECTURE.md`, then verifies:

1. exact source SHA/path provenance;
2. representative English + Chinese retrieval;
3. canonical ancestor/path reconstruction;
4. no mutation of the source file;
5. rebuild after a fixture source change;
6. one Doré consumer reading the returned packet through the public adapter boundary;
7. explicit negative cases for empty/malformed/irrelevant queries.

A passing local fixture suite should still not be promoted to broad cognition or memory completion; it would only close the Context foundation acceptance gap.

## Sweep disposition

Retain this layer as small shared infrastructure. Do not replace it with a vector database or third-party memory framework unless benchmark evidence exposes a retrieval gap that the current SQLite/FTS5 + bounded CJK fallback cannot solve.

P01 subtitle/runtime state and ordering were not modified by this review.
