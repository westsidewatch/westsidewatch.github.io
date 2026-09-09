# DORÉ SHARED MEMORY / CONTEXT SUBSTRATE — EVIDENCE LEDGER

Date: 2026-09-09
Status: ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION / ACCEPTANCE_EVIDENCE_BOUNDED
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
P01 impact: NONE

## Bounded evidence reviewed

- `dore-core/substrate.py`
- `dore-core/conversation_substrate.py`
- `dore-core/context/README.md`
- `dore-core/tests/memory-layer-contract.mjs`
- `dore-core/tests/test_conversation_context.py`

## Classification

The shared-artifact / conversation-context substrate is **real implementation evidence**, not only architecture prose. It is classified as `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION` within the already-canonical Conversation Memory / Full Memory history.

This batch does **not** justify `VERIFIED_COMPLETE` for production Conversation Memory, multi-user long-horizon recall, public Conversation, or the broader Full Memory program. Repository test definitions exist, but this Sweep run did not execute them and therefore does not create a fresh runtime PASS.

## Evidence judgment

### 1. Original objective

Provide a durable substrate in which project/conversation state can be stored and shared without relying on transient chat context, while preserving versioned artifacts, grants/scope and explicit context-service boundaries.

### 2. Implementation evidence

`dore-core/substrate.py` defines a SQLite-backed `SharedArtifactStore` for durable shared artifacts/state with versioning and grant-oriented access semantics.

`dore-core/conversation_substrate.py` builds conversation/context behavior over that shared store rather than treating conversational continuity as process-local memory.

`dore-core/context/README.md` records the context-service boundary and tenant/residency-safe handling expectations.

`dore-core/tests/memory-layer-contract.mjs` and `dore-core/tests/test_conversation_context.py` provide explicit contract/behavior test definitions around the memory/context layer.

### 3. Current quality judgment

The implementation is materially stronger than an architecture-only milestone because code, context-service documentation and dedicated tests coexist. The design direction is compatible with Doré's governing rule that durable project knowledge must survive individual conversations.

The evidence remains bounded. A file-defined test suite is not equivalent to a persisted current CI/runtime PASS, and SQLite/local substrate existence is not evidence of production D1/R2/Vectorize isolation, public tenant isolation, long-horizon retrieval quality or broad product adoption.

### 4. Durable capability retained

- separate transient conversation state from durable artifacts;
- make shared project state addressable/versioned rather than implicit;
- place conversation context on a reusable substrate instead of a single product-specific chat store;
- keep scope/access/residency concerns at the context-service boundary;
- define memory behavior through explicit contract tests rather than prose alone.

### 5. Weaknesses / debt

- no fresh execution result for the reviewed tests was persisted by this Sweep batch;
- broad adoption across Doré products is not proven by these files alone;
- production-grade multi-tenant isolation, D1/R2 recovery and semantic/vector recall require separate evidence;
- `SharedArtifactStore` and later production memory layers may overlap in responsibility; no supersession/retirement claim is justified without explicit migration/deprecation evidence.

### 6. Revisit trigger

Revisit when a later production memory substrate becomes canonical, when duplicated persistence responsibilities create maintenance cost, when the reviewed tests fail, or when a cross-product memory exam exposes context leakage / missing continuity.

### 7. Current disposition

Retain as an implemented foundational layer and historical capability source. Do not retire or supersede it from naming/age alone. Require explicit migration evidence before changing its lifecycle classification.

## Canonical reconciliation

The Master Work Register already records both **Conversation Memory implementation-contract drift** and **Full Memory Phase 1 M1–M7 bounded implementation history** under `MEM-SWEEP-01`; this batch strengthens the evidence behind that existing canonical interpretation rather than creating a new independent workstream.

No Master Register status change is warranted from this bounded batch. The new evidence ledger supplies the exact implementation-level provenance missing from the broad canonical phrase.

## P01 isolation

No subtitle URL, caption acquisition, audio/transcription executor, Cloudflare binding, production deployment or P01 runtime state was changed.
