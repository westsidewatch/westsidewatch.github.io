# DORÉ MEMORY SWEEP 01 — CHECKPOINT 108

Date: 2026-09-13
Status: ACTIVE_PARALLEL / BOUNDED_RECONCILIATION
Primary register: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`
Related work: `MEM-SWEEP-01`, `CONV-MEM-V1`, `CONVERSATION`
P01 impact: NONE — subtitle critical path and blocker state untouched.

## Bounded evidence reviewed

- `dore-core/tests/memory-layer-contract.mjs`
- `dore-core/projects/DORÉ-CONVERSATION-MEMORY-LAYER-V1.md`
- `functions/api/dore/memory.js`
- `dore-core/projects/DORÉ-CONVERSATION-MEMORY-EVIDENCE-LEDGER-2026-08-27.md`
- canonical `CONV-MEM-V1` entry in `DORÉ-MASTER-WORK-REGISTER.md`

## Classification result

`CONV-MEM-V1` remains `ACTIVE_PARALLEL / IMPLEMENTING`.

No completion promotion is warranted. Existing M1–M7 bounded capability evidence remains valid, but current source exposes a stronger project-isolation defect that must be added to the production-readiness evidence boundary.

## New reconciliation finding

The current base memory API treats `conversation_id` too independently from `project_id` in several identity-critical places:

1. Deduplication selects by `conversation_id + content_sha256 + role` only; `project_id` is not part of the predicate.
2. On a dedupe hit, the API returns the incoming request's `project_id`, not the stored message's project identity.
3. `dore_conversations.id` is keyed only by conversation id, and the upsert can update its `project_id` on conflict.
4. GET supports conversation-only replay without a project predicate.
5. The static memory contract has no negative same-conversation-id / different-project fixture.

Therefore a reused conversation id can create cross-project dedupe/identity ambiguity and potential conversation-only retrieval contamination. This is stronger and more concrete than the earlier general warning that missing project scope can fall back to `unscoped`.

## Current evidence judgment

### Retain as real bounded progress

- D1/R2 core ingestion architecture;
- scoped conversation+project query path;
- M1–M7 bounded diagnostics/implementation history;
- semantic-adapter degradation behavior;
- same-project cross-conversation semantic-memory fixture with foreign-project exclusion.

### Still not earned

- production-ready project isolation;
- immutable conversation→project identity;
- safe dedupe across reused conversation ids;
- public tenant isolation;
- full-memory completion.

## Smallest future correction/proof

Without interrupting P01:

- include project identity in message dedupe, or prove/enforce globally unique conversation ids with immutable project binding;
- return stored identity on dedupe;
- reject conversation project reassignment;
- require strong project scope where the entry path demands isolation;
- add a negative acceptance fixture using the same conversation id under two different projects and prove no cross-project dedupe, replay or metadata misattribution.

## Durable updates

- Updated `DORÉ-CONVERSATION-MEMORY-EVIDENCE-LEDGER-2026-08-27.md` with the exact source-level defect and required acceptance proof.
- Canonical Master Register classification remains correct (`ACTIVE_PARALLEL / IMPLEMENTING`), so no status change is justified in this checkpoint.

## Sweep status

Sweep 01 remains `ACTIVE_PARALLEL`.

This checkpoint is ordinary consolidation progress. It does not establish `VERIFIED_COMPLETE` and does not introduce a `HUMAN_DECISION_BLOCKED` or new `ENVIRONMENT_BLOCKED` condition.
