# DORÉ CONVERSATION MEMORY EVIDENCE LEDGER — 2026-08-27

Status: SWEEP-01 / BOUNDED EVIDENCE / RECONCILED 2026-08-31
Related work: `CONV-MEM-V1`, `CONVERSATION`, `MEM-SWEEP-01`

## Evidence reviewed

Initial bounded evidence:

- `dore-core/projects/DORÉ-CONVERSATION-MEMORY-LAYER-V1.md`
- `dore-core/tests/memory-layer-contract.mjs`
- `functions/api/dore/memory.js`
- `cloudflare/d1/002_dore_conversation_memory.sql`
- canonical Master Work Register interpretation for `CONV-MEM-V1`

Sweep-01 reconciliation added on 2026-08-28:

- `.github/workflows/dore-full-memory-phase1-m1.yml`
- `.github/workflows/dore-full-memory-phase1-m2-provision.yml`
- `functions/api/dore/memory-phase1-diagnostic.js`
- merged Full Memory Phase 1 M5 commit `cce7c414f580acb01c84a58edaf619500a572948`
- merged Full Memory Phase 1 M6 commit `0d3da1160d30d6577cd9db4e332ef3bdf37682a4`
- merged Full Memory Phase 1 M7 commit `46197df62272e19d283b53125d8ef3f5f325ab0e`
- PR #250 metadata and body for M7 lifecycle/import
- current `functions/api/dore/cross-memory.js`, `functions/api/dore/memory-lifecycle.js` behavior as represented by the merged diffs

Sweep-01 current-code reconciliation added on 2026-08-31:

- current `functions/api/dore/memory.js` at blob `2ea19bd8359e5a4e4b3a6dc7f64e3e36e350dd6e`;
- `dore-core/tests/memory-layer-contract.mjs` at blob `cd09006b66c89038b5f52cf5b0511f0e0e451ad7`;
- `DORÉ-CONVERSATION-MEMORY-LAYER-V1.md` current documentation snapshot.

## Reconciled findings

1. The implementation has passed through more than one dependency shape. An earlier Sweep snapshot correctly observed a period in which the write path was coupled to D1 + R2 + Workers AI + Vectorize. The **current** `memory.js`, however, no longer has that hard AI/Vectorize dependency: `DORE_SENSORY` and `DORE_MEMORY_ARCHIVE` are mandatory for a new write, while `AI` + `DORE_MEMORY_VECTOR` are handled by `optionalVector(...)`. If semantic indexing is disabled or the semantic adapter is unavailable/fails, the D1+R2 message write can still succeed and returns semantic-adapter status. Therefore the old “current write path hard-requires D1+R2+AI+Vectorize” wording is now superseded by later code and must not be used as the governing runtime description.
2. Full Memory Phase 1 continued through M5–M7. It is no longer accurate to say that semantic recall exists only as an untested upsert hook or that no cross-conversation semantic-memory behavior exists.
3. M1 has a production diagnostic endpoint and workflow asserting `M1_STORAGE_SCOPE_PASS`; its diagnostic writes two conversations, verifies exact replay and cross-conversation isolation inside the bounded fixture, then cleans up.
4. M2 provisioning explicitly creates/verifies the `dore-conversation-memory` Vectorize index, merges production `DORE_MEMORY_VECTOR` and `AI` bindings into the downloaded Pages configuration, deploys it, and polls the live diagnostic until D1 + Vectorize + AI bindings are visible. This remains valid infrastructure evidence even though current base ingestion can degrade to D1+R2 when semantic indexing is unavailable.
5. M5 adds a real memory-aware response path. The merged diagnostic ingests a remembered decision plus a distractor, retrieves semantic context, invokes Workers AI, and requires the answer to preserve the remembered bilingual-label decision while excluding the distractor. Its named gate is `M5_MEMORY_AWARE_RESPONSE_PASS`.
6. M6 adds same-project cross-conversation semantic memory with explicit project namespace isolation. Its diagnostic creates an old and new conversation in project A plus a conflicting foreign conversation in project B, then requires the response to recall the old project-A decision, exclude the French-only foreign-project decision and an unrelated distractor, and report only the old conversation as memory source. Its named gate is `M6_CROSS_CONVERSATION_MEMORY_PASS`.
7. M7 adds resumable/idempotent history import with persisted progress plus conversation-memory deletion across D1/R2/Vectorize. The diagnostic requires resumable batched import, replay deduplication, completed progress tracking, recall of imported history, deletion lifecycle, and cleanup; the named gate is `M7_MEMORY_LIFECYCLE_AND_IMPORT_PASS`. PR #250 was merged and explicitly describes the production diagnostic as proving imported-memory recall plus deletion lifecycle.
8. These are legitimate bounded implementation milestones. They materially reduce the old `ME-005` evidence gap, but they do **not** by themselves prove the whole Conversation Memory Layer production-ready or complete. In particular, no evidence in this sweep batch proves full-history backfill (M7 itself points to `M8_FULL_HISTORY_BACKFILL`), long-horizon load/scale behavior, collision-resistant namespace handling for arbitrary long project ids, public tenant isolation, cost/availability robustness under the free-first rule, or a durable end-to-end Conversation Runtime acceptance using imported production history.
9. The current API still permits `project_id` fallback to `unscoped` on ingestion. The M6 project-isolation fixture is meaningful, but it does not prove that absent/incorrect scope is safely rejected everywhere.
10. The current static `memory-layer-contract.mjs` is partly stale relative to implementation. It still asserts that `DORE_MEMORY_ARCHIVE` and `DORE_MEMORY_VECTOR` are merely “optional hooks”; current code makes R2 archive mandatory but Vectorize genuinely optional. The test remains useful for schema/retrieval-scope/static-policy assertions, but it is not a reliable complete statement of current write dependencies and does not prove production write/replay, rollback integrity, namespace isolation, semantic retrieval, or tenant isolation.
11. The merged code and PR descriptions are strong repository/runtime-contract evidence; this sweep did not independently retrieve the historical GitHub Actions check-run artifacts for every M1–M7 gate. Therefore the correct interpretation is **bounded milestones implemented with production diagnostics and merged acceptance gates**, not an unsupported claim that every named CI gate was independently re-executed by Sweep 01.
12. No P01 subtitle state, deployment, credential, ordering or blocker condition was modified.

## Current evidence boundary

### Strongly evidenced bounded milestones

- D1 conversation/message storage and exact scoped replay foundation.
- current base-ingest dependency boundary: D1 (`DORE_SENSORY`) + R2 archive are mandatory; semantic indexing is an optional adapter on the current write path.
- bounded M1 conversation isolation diagnostic contract.
- production configuration path for D1 + Vectorize + Workers AI bindings.
- semantic memory-aware response implementation and acceptance diagnostic (M5).
- same-project cross-conversation semantic recall with foreign-project exclusion diagnostic (M6).
- resumable/idempotent history import, progress tracking and deletion lifecycle diagnostic (M7).
- merged progression through Full Memory Phase 1 M1–M7, with M7 explicitly naming M8 full-history backfill as the next stage.

### Still missing before production-ready/full-memory completion

- independent persisted check-run/readback evidence for the historical named M1–M7 workflow passes where not already captured in durable runtime ledgers;
- M8 full-history backfill completion and verification;
- representative real-history import beyond synthetic bounded fixtures;
- explicit rejection/safe handling of absent or incorrect project scope across every public/internal entry path;
- namespace collision proof or collision-resistant replacement for truncated project namespaces;
- failure-injection/partial-write rollback proof across D1/R2 and, where semantic indexing is enabled, Vectorize/AI behavior;
- sustained volume/latency/error-rate and deletion consistency evidence;
- R2 recovery proof against real imported history after D1 loss/corruption scenarios;
- free-first cost/availability measurements under representative memory volume, distinguishing core D1+R2 cost from optional semantic-adapter cost;
- durable Conversation Runtime consumption of recalled/imported memory with provenance across fresh sessions;
- authenticated tenant isolation and abuse boundaries for any future public conversation.

## Current disposition

`CONV-MEM-V1`: remain `ACTIVE_PARALLEL / IMPLEMENTING`. The canonical interpretation is now **“Full Memory Phase 1 M1–M7 bounded milestones implemented; current base ingestion requires D1+R2 and can operate without semantic indexing, while semantic response/cross-conversation capabilities depend on the AI+Vectorize path when invoked; M8/full-history and production-readiness evidence remain open.”**

This is not a completion promotion. The correction is an evidence reconciliation: meaningful memory capability exists beyond the older ledger snapshot, and a later implementation change has reduced the base-ingest hard dependency surface without proving the remaining production-readiness gates.

## Smallest useful next proof

Without displacing P01, preserve the M1–M7 fixtures as regression gates and execute the next bounded stage against representative imported history: M8 full-history backfill → readback/semantic recall from a fresh conversation → scope/tenant-negative fixtures → failure/rollback injection → persisted cost/latency evidence. Also update the static memory-layer contract so its R2/Vectorize dependency assertions match current code. Only then reconsider whether `CONV-MEM-V1` can move from `ACTIVE_PARALLEL / IMPLEMENTING` toward a verified production milestone.
