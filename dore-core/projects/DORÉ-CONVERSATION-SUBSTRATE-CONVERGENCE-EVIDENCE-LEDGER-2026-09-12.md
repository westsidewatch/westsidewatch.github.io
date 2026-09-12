# DORÉ CONVERSATION SUBSTRATE CONVERGENCE — EVIDENCE LEDGER

Date: 2026-09-12
Status: ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION / EVIDENCE_GATED
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
Related: `NERVOUS-SYSTEM`, `CONV-MEM-V1`, `CONVERSATION`
P01 impact: NONE

## Bounded evidence reviewed

- `dore-core/conversation_substrate.py`
- `dore-core/runtime/conversation_substrate_acceptance.py`
- commit `5dbbdbc3888504d51379e1cb06b62600c13bcded` — `feat(dore-core): converge conversation memory onto shared substrate`
- commit `a8006790a0a6e4ad28789d00095d16f2eb242733` — `test(core): include conversation convergence in substrate acceptance`
- current shared-substrate interpretation under `NERVOUS-SYSTEM`
- current Conversation Memory missing-evidence boundary (`ME-005`)

## Findings

### 1. Conversation memory has a real Core-substrate adapter

`ConversationSubstrate` is executable implementation, not a roadmap memo. It preserves `dore_messages` as conversation-domain truth while projecting durable recall records into `SharedArtifactStore` as protected `conversation-message` artifacts.

The projection preserves stable message identity, conversation/project metadata, role, timestamp, authority (`USER` versus `DORE`) and a provenance edge back to the originating `dore_messages` row. Archive JSON is explicitly treated as export/evidence rather than the truth store.

### 2. Backfill is deliberately idempotent

The adapter scans existing `dore_messages`, derives stable `message:<message_id>` artifact IDs, skips already-projected artifacts and returns created/existing counts. This is the correct migration posture for convergence work: domain rows are retained rather than destructively rewritten, and shared retrieval is a projection rather than a competing source of truth.

### 3. A dedicated acceptance contract exists and is wired into the Core substrate action

`conversation_substrate_acceptance.py` defines a bounded executable fixture that checks:

- conversation-domain rows remain preserved;
- each message is projected once;
- a second backfill is idempotent;
- shared retrieval can find a projected conversation message;
- archive JSON is not required for recall.

Commit `a8006790...` changed `core.substrate.acceptance` so both `common_substrate_acceptance.py` and `conversation_substrate_acceptance.py` must pass before the action reports success.

### 4. The evidence boundary is important

The repository contains the implementation and an executable acceptance contract, but this bounded Sweep pass found no persisted workflow/check-run evidence for commit `a8006790...`; the commit-associated workflow-run lookup returned no runs. Therefore the convergence should **not** be promoted to `VERIFIED_COMPLETE` merely because the test exists or is wired into a production action.

Current classification:

`ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION / UNKNOWN_NEEDS_EVIDENCE for persisted acceptance execution`

### 5. This strengthens but does not yet close the Nervous-System shared-substrate milestone

The adapter is concrete evidence that Conversation is being converged onto the common substrate rather than remaining only a theoretical future consumer. However the canonical Nervous-System next milestone requires a fresh persisted common-substrate acceptance PASS and a proved real cross-product consumer. Repository implementation alone is not that runtime proof.

### 6. This does not replace Conversation Memory Phase 1 evidence

The shared-substrate projection and the existing D1/R2/Vectorize conversation-memory work solve related but different layers. The projection creates a canonical shared-retrieval representation; it does not by itself prove M8 full-history backfill, fresh-conversation consumption of representative real history, tenant/scope hardening, rollback behavior, scale/latency or production-ready memory semantics tracked under `ME-005`.

## Current disposition

- `ConversationSubstrate` implementation: **retain / integrate**.
- Dedicated convergence acceptance: **retain as regression gate**.
- Completion status: **do not promote** until execution evidence is persisted.
- Architecture direction: **supports canonical-substrate convergence** and reduces the risk of separate truth stores.
- Archive JSON: **evidence/export only**, not canonical recall truth.

## Smallest useful next proof

Execute the already-wired `core.substrate.acceptance` capability on a current merged-main checkout and persist its structured output showing both `common.ok=true` and `conversation.ok=true`. Then run the conversation backfill against a bounded representative real-history slice and verify fresh retrieval with provenance while preserving `dore_messages` domain rows.

This proof is subordinate to P01 and must not alter the subtitle critical path.
