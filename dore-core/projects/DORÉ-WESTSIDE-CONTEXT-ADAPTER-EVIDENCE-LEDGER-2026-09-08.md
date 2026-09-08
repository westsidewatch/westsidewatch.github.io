# DORÉ WESTSIDE CONTEXT ADAPTER — EVIDENCE LEDGER

Date: 2026-09-08
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Classification: `COMPLETED_REVISIT_CANDIDATE / MAINTENANCE`
P01 impact: NONE

## Original objective

Build the smallest useful, local, read-only Context Adapter between Doré Core and the canonical Westside architecture without changing the public main-site structure, replacing Doré Knowledge/Memory, adding external APIs, or introducing vector/graph machinery before measured evidence requires it.

Canonical source remains `docs/MASTER_SITE_ARCHITECTURE.md`; the derived projection is disposable.

## Evidence reviewed

- `dore-core/context/README.md`;
- merged PR #409, `DORÉ: minimal Westside Context adapter` (`d616b67e6af328739c0efbb6b9444a35ab8b9db8`);
- `dore_core/context/compiler.py`, `interface.py`, `packet.py`, `retrieve.py` as introduced by PR #409;
- Context capability registration in `dore-core/runtime/capability-registry.v1.json`;
- `tests/benchmark_westside_context.py` and the focused Context test family introduced by PR #409;
- merged PR #412, `fix: make CJK Westside Context questions retrievable` (`9ed724fc40c4b108913e18297c78c148da6fd3e3`), including the question-form CJK regression and hierarchy-boundary correction;
- PR #412 Cloudflare preview deployment success for head `706c5e7`;
- Foundation workflow run `34091566593` associated with the earlier PR #409 head, where unit-test/foundation steps succeeded but the overall job failed later at `Enforce Doré Foundation result` for broader Foundation criteria.

## What is actually implemented

The bounded Context slice is real implementation, not a memo:

- dependency-free Markdown hierarchy compiler;
- SQLite + FTS5 local projection;
- source SHA-256 provenance;
- heading level, parent relationship and source-order retention;
- matched-node + canonical-ancestor `ContextPacket`;
- explicit read-only Doré-facing adapter boundary;
- capability-registry entry `westside.context` with `write_access: false`;
- deterministic local fallback for mixed/CJK queries;
- later CJK n-gram fallback for natural question-form recall;
- benchmark cases against real Westside architecture concepts including Main Site, Journal, ONE, Liming Library, Three Morning Stars, Search, Storybook and Doré Exploration.

## Completion judgment

### Historical milestone

The **minimal adapter implementation milestone is complete**. PR #409 was merged, the capability was registered, the intended source-of-truth/write boundary is explicit, and the first real CJK retrieval defect was repaired through merged PR #412 rather than by expanding to a heavier architecture.

### Evidence boundary

Do **not** reinterpret this as proof of universal Context quality or autonomous structural understanding.

The repository contains focused tests and a real benchmark harness, but this sweep batch did not find a dedicated persisted CI artifact stating the complete current Westside Context benchmark suite passed against the current canonical architecture after PR #412. The available Foundation run is not a clean Context acceptance record: its relevant earlier unit-test steps succeeded, while the overall Foundation job failed later for broader Foundation enforcement.

Therefore:

- minimal implementation milestone: **verified as implemented and merged**;
- universal/current retrieval acceptance: **UNKNOWN_NEEDS_EVIDENCE**;
- no vector database, graph database or third-party memory framework is justified by current evidence.

## Current quality judgment

Strong qualities:

- unusually small dependency surface;
- clear source-of-truth/provenance boundary;
- no write capability from retrieved Context Packets;
- hierarchy is preserved rather than flattening architecture into anonymous snippets;
- the first observed CJK question-form failure was fixed with a bounded local method;
- the design follows the Doré principle `能力越大、負擔越小`.

Current limitations:

- retrieval is still lexical/substring/n-gram rather than semantic;
- benchmark coverage is intentionally small;
- no persisted current benchmark run proves recall/precision across a wider unseen query set;
- no demonstrated cross-source context assembly beyond the single canonical architecture projection;
- no measured latency/index-size/false-positive history has yet justified or rejected future retrieval layers quantitatively.

## Revisit trigger

Reopen the implementation only when measured real-product evidence shows one of the following:

1. repeated Context misses that cannot be repaired safely within the existing local retriever;
2. false-positive/precision debt that harms real Doré tasks;
3. a need to assemble multiple canonical source families that the current single-source projection cannot represent cleanly;
4. scale/latency evidence showing SQLite/FTS5 is no longer adequate;
5. a blind-transfer benchmark demonstrates that semantic/vector/graph capability would materially improve outcomes without unacceptable complexity.

Do not add heavier memory/retrieval infrastructure merely because it is fashionable.

## Current disposition

`COMPLETED_REVISIT_CANDIDATE / MAINTENANCE`

Retain the minimal adapter as the current Westside Context foundation. Treat PR #412 as a healthy example of measured-gap-driven evolution. The next evidence task is a persisted post-PR-412 benchmark/acceptance run against the current canonical architecture, preferably including unseen Chinese natural-language questions and precision-negative cases.

## Capability retained

This milestone contributes a reusable Doré engineering skill:

`canonical structured Markdown → provenance-preserving disposable projection → lightweight local retrieval → ancestor-aware Context Packet → measured-gap repair without architecture inflation`

That skill is reusable for other canonical internal documents if and only if their source-of-truth and authority boundaries remain explicit.
