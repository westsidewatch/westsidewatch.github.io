# DORÉ FULL MEMORY PHASE 1 EVIDENCE LEDGER — 2026-08-28

Status: SWEEP-01 / BOUNDED EVIDENCE
Related work: `CONV-MEM-V1`, `CONVERSATION`, `MEM-SWEEP-01`

## Why this ledger exists

Sweep 01 found that the older Conversation Memory evidence snapshot had become stale after a rapid Full Memory Phase 1 sequence merged on 2026-08-26/27. This ledger preserves the bounded M1–M7 progression without inflating it into a production-ready/full-memory completion claim.

## Evidence reviewed

- `.github/workflows/dore-full-memory-phase1-m1.yml`
- `.github/workflows/dore-full-memory-phase1-m2-provision.yml`
- `functions/api/dore/memory-phase1-diagnostic.js`
- commit `cce7c414f580acb01c84a58edaf619500a572948` — M5 Memory-Aware Response
- commit `0d3da1160d30d6577cd9db4e332ef3bdf37682a4` — M6 Cross-Conversation Memory
- commit `46197df62272e19d283b53125d8ef3f5f325ab0e` — M7 Memory Lifecycle and Import
- PR #250 — merged M7 lifecycle/import change, whose body states that it adds resumable/idempotent history import, project-level semantic indexing, D1/R2/Vectorize deletion, and a production diagnostic for imported-memory recall plus deletion lifecycle
- `dore-core/projects/DORÉ-CONVERSATION-MEMORY-EVIDENCE-LEDGER-2026-08-27.md` before and after reconciliation

## Milestone interpretation

### M1 — storage / scoped replay foundation

**Classification:** bounded historical milestone, implementation + live-diagnostic contract present.

The production diagnostic writes two conversations in D1, verifies exact replay and cross-conversation isolation for the fixture, cleans up, and emits `M1_STORAGE_SCOPE_PASS` on success.

### M2 — production memory bindings / semantic infrastructure

**Classification:** bounded infrastructure milestone, not full semantic-memory completion.

The provisioning workflow creates/verifies the `dore-conversation-memory` Vectorize index, downloads current Pages configuration, merges production `DORE_MEMORY_VECTOR` and Workers `AI` bindings, deploys the exact resulting configuration, and polls the live diagnostic until the expected bindings are visible.

### M5 — memory-aware response

**Classification:** bounded functional milestone.

Merged code adds a response layer that assembles retrieved conversation memory, treats memory as evidence rather than instruction, invokes Workers AI, and includes a production diagnostic requiring a remembered bilingual Chinese-English map-label decision while excluding a distractor. Named gate: `M5_MEMORY_AWARE_RESPONSE_PASS`.

### M6 — same-project cross-conversation memory

**Classification:** bounded functional milestone.

Merged code creates project-level semantic indexing and cross-conversation retrieval. The diagnostic requires recall from an earlier conversation in the same project, excludes a contradictory foreign-project memory and an unrelated distractor, and checks clean source-conversation scope. Named gate: `M6_CROSS_CONVERSATION_MEMORY_PASS`.

### M7 — memory lifecycle and history import

**Classification:** bounded functional/lifecycle milestone.

Merged code adds resumable batched history import, persistent import progress, idempotent replay/dedup behavior, imported-memory recall, and conversation deletion across D1/R2/Vectorize. The diagnostic requires resumability, dedupe, progress tracking, imported-memory recall, deletion lifecycle and cleanup. Named gate: `M7_MEMORY_LIFECYCLE_AND_IMPORT_PASS`.

M7 itself points next to `M8_FULL_HISTORY_BACKFILL`; therefore M7 cannot be interpreted as full-history completion.

## Current quality judgment

The implementation is materially stronger than the earlier “D1 + unverified semantic hooks” interpretation. By M6/M7, Doré has a coherent same-project cross-conversation retrieval path and an explicit import/lifecycle layer.

The strongest architectural qualities are:

- memory is scoped by project and conversation rather than treated as one flat global store;
- foreign-project and distractor exclusion are explicit acceptance concerns;
- imported history is designed to be resumable and idempotent;
- deletion attempts to propagate across D1/R2/Vectorize instead of deleting only one copy;
- generated answers are instructed to treat retrieved memory as evidence, not executable instruction;
- diagnostics clean up their own fixtures.

Visible debt remains:

- some memory paths still normalize missing project ids to `unscoped` rather than rejecting ambiguous scope;
- project Vectorize namespaces are truncated, and no collision proof was found in this bounded pass;
- synthetic diagnostics are not representative long-history/volume evidence;
- no M8 full-history backfill proof was found;
- no durable failure-injection/rollback benchmark was found for multi-store partial failures;
- no cost/latency/availability benchmark was found under representative free-first volume;
- public tenant isolation remains a separate future concern;
- Sweep 01 did not independently retrieve historical check-run artifacts for every named workflow gate, so merged diagnostics must not be over-described as independently re-executed by this sweep.

## Capability retained

This phase taught/retains reusable capability in:

- scoped persistent conversation storage;
- semantic retrieval over conversation history;
- same-project cross-conversation memory;
- evidence-aware response generation;
- resumable/idempotent history import;
- cross-store deletion lifecycle;
- production diagnostic design for isolation, distractor rejection, recall and cleanup.

These capabilities are reusable by Conversation Runtime and other Doré project-memory surfaces, but broader product use must preserve scope/provenance and must not silently widen authority.

## Current disposition

`CONV-MEM-V1` remains `ACTIVE_PARALLEL / IMPLEMENTING`.

Canonical interpretation after this sweep batch:

> Full Memory Phase 1 M1–M7 are real bounded implementation milestones, including semantic response, same-project cross-conversation recall, resumable/idempotent history import and deletion lifecycle. Production-ready/full-memory completion is not yet justified because M8/full-history backfill, real-history scale/rollback/cost evidence, stronger scope handling and future tenant isolation remain open.

## Revisit / next evidence trigger

Continue from M7 rather than restarting semantic-memory proof. The next high-value evidence is:

`M8 full-history backfill → fresh-conversation recall from representative imported history → negative scope/tenant fixtures → failure/rollback injection → cost/latency evidence → Conversation Runtime integration acceptance`

This work remains subordinate to the active P01 subtitle critical path.
