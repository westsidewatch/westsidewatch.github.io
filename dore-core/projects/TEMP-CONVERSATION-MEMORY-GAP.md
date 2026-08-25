# TEMP — Conversation Memory Gap / Sequence Check

Status: TEMPORARY / ACTIVE UNTIL VERIFIED CLOSED
Created: 2026-08-25
Owner: Westside Watch
Executor / steward: Doré
Deletion rule: DELETE this memo only after every completion test below is verified in runtime and the canonical Master Work Register reflects the final durable state.

## Why this temporary memo exists

A live review found that the canonical `DORÉ-MASTER-WORK-REGISTER.md` exists and correctly requires durable work not to remain only in conversation, but the newly agreed full-conversation memory path is not independently represented there. The existing `CONVERSATION` item refers to the future direct human↔Doré Conversation Runtime, not historical/full conversation ingestion and retrieval.

This memo prevents the gap from being lost while the currently running Memory / Researcher / Runtime work finishes and while Doré determines the correct permanent dependency ordering.

## Verified current situation

1. The canonical Master Work Register is live and is the single operational index.
2. CORE includes memory/capability accumulation at a high level.
3. Runtime continuity is ACTIVE and remains an important current critical-path capability.
4. Memory Sweep / Researcher-history reconciliation / Brain→Product bridge work is actively progressing.
5. Recent work is still resolving runtime/evidence boundaries; documentation alone is not accepted as runtime proof.
6. `CONVERSATION` in the register is currently the future direct Conversation Runtime and is PARKED / READINESS-WATCH.
7. Full historical/current conversation ingestion + durable raw preservation + retrieval is not independently listed in the canonical register.
8. Therefore Conversation → Memory → durable-work detection → Work Register → Runtime is not yet proven as a complete autonomous loop.

## Missing / not-yet-proven pieces to reconcile

### A. Full Conversation Ingest
- Capture the complete conversation, not only summaries or manually selected memories.
- Preserve conversation ID and stable message/order metadata.
- Preserve raw source durably (target architecture discussed: R2 or equivalent durable object storage).

### B. Retrieval layer
- Chunk with provenance/metadata.
- Vectorize semantic index.
- Retrieval must combine conversation identity/scope with semantic relevance where appropriate, preventing cross-conversation context leakage while allowing durable cross-conversation knowledge after consolidation.

### C. Consolidation / synthesis
- Distinguish ordinary discussion from durable principle, decision, requirement, project, defect, dependency, learning requirement, or architecture change.
- Deduplicate and reconcile against existing memory/knowledge/projects.
- Preserve provenance back to source conversation evidence.

### D. Durable Work Capture Gate
- A durable new work item must reach the canonical Master Work Register (or a linked authoritative project file indexed by it) without requiring the human to say “remember/record this”.
- Priority/dependency changes discovered in conversation must be reconciled rather than silently creating parallel plans.

### E. Runtime handoff
- Project Runtime must consume reconciled canonical work state and be able to schedule/continue it according to capability/dependency order.

### F. Fresh-context proof
- In a new/fresh context, Doré retrieves the relevant conversation-derived knowledge and can explain what changed, why, and what work follows.
- A deliberate regression test introduces durable work in conversation without an explicit “record this” instruction; Doré must capture it correctly.

## Provisional dependency/order — DO NOT treat as final re-numbering yet

The gap is upstream-critical, but current Runtime/Memory work should not be disrupted blindly. Until Doré reconciles exact existing coverage, use this dependency logic:

`CORE / mission + memory discipline`
→ `current Memory Sweep / evidence reconciliation (continue; do not discard progress)`
↔ `Full Conversation Ingest + raw durable preservation`
→ `ID/metadata + Vectorize retrieval`
→ `Consolidation / Synthesis + Durable Work Capture Gate`
→ `Master Work Register reconciliation`
↔ `Runtime continuity / scheduler consumes canonical state`
→ `P01 and other product executors`

Parallel work that does not violate these dependencies may continue. The final canonical order is Doré's responsibility after it audits existing implementation and evidence.

## Completion tests before deleting this memo

- [ ] Full real conversation is ingested with conversation ID/order/provenance.
- [ ] Raw conversation is durably preserved.
- [ ] Semantic retrieval is live and scoped safely.
- [ ] Fresh-context retrieval succeeds on real conversation material.
- [ ] Consolidation produces durable memory/knowledge without losing source evidence.
- [ ] A durable new project/decision introduced without “record this” is automatically captured.
- [ ] Canonical Master Work Register is updated/reconciled automatically or by the intended verified Doré loop.
- [ ] Runtime demonstrably consumes the reconciled work state.
- [ ] Regression test shows no cross-conversation context leakage caused by vector retrieval.
- [ ] Final permanent architecture/work-register entries replace this temporary memo.

When all boxes are verified with evidence, delete this file. Do not preserve it as permanent documentation.
