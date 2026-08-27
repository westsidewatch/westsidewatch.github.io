# DORÉ CONVERSATION MEMORY EVIDENCE LEDGER — 2026-08-27

Status: SWEEP-01 / BOUNDED EVIDENCE
Related work: `CONV-MEM-V1`, `CONVERSATION`, `MEM-SWEEP-01`

## Evidence reviewed

- `dore-core/projects/DORÉ-CONVERSATION-MEMORY-LAYER-V1.md`
- `dore-core/tests/memory-layer-contract.mjs`
- `functions/api/dore/memory.js`
- `cloudflare/d1/002_dore_conversation_memory.sql`
- canonical Master Work Register interpretation for `CONV-MEM-V1`

## Findings

1. The D1 schema and scoped-recent GET path are real implementation, not only design prose. Conversation/message/chunk tables and conversation/project indexes exist, and GET rejects a request with neither conversation nor project scope.
2. The static contract test is useful but bounded. It proves expected source/schema strings are present; it does not execute the Cloudflare write path or prove production isolation.
3. Current POST behavior has drifted materially from the earlier documented M1 contract. `ingestMessage()` now requires all of `DORE_SENSORY`, `DORE_MEMORY_VECTOR`, `DORE_MEMORY_ARCHIVE`, and Workers `AI`; it computes a 384-dimensional embedding, writes the R2 archive and Vectorize record, then commits D1 rows. R2/Vectorize are therefore no longer optional hooks on the current write path.
4. The GET path still performs only D1 scoped-recent retrieval; it does not yet perform Vectorize semantic recall. Thus the existence of Vectorize upsert code is not evidence of a working scoped semantic-memory system.
5. POST currently permits a missing project id by normalizing it to `unscoped`. This is weaker than the intended explicit project boundary and must not count as project-isolation proof.
6. Vector namespace is `project_id::conversation_id` truncated to 64 characters. No persisted collision test was found for long identifiers.
7. `dore_memory_chunks` exists in schema but is not currently exercised by the API.
8. Partial-write cleanup exists for R2/Vectorize if a later stage throws, but rollback behavior has not been exercised in persisted acceptance evidence.
9. No evidence in this bounded batch justifies changing `CONV-MEM-V1` from `ACTIVE_PARALLEL / IMPLEMENTING` or promoting it to production-ready memory.
10. No P01 runtime state or subtitle action was changed.

## Current evidence boundary

### Verified repository facts

- D1 conversation/message/chunk schema exists.
- D1 retrieval has mandatory at-least-one-scope behavior.
- exact conversation+project query path exists.
- message dedupe by conversation/content hash/role exists.
- R2 archive and Vectorize embedding write code exists.
- static contract assertions exist.

### Still missing

- one successful production message ingest through the **current** D1+R2+AI+Vectorize path;
- exact production conversation+project replay;
- two-conversation and two-project zero-cross-talk proof;
- rejection or safe handling of absent/incorrect project scope;
- R2 recovery/replay proof;
- actual metadata/scoped Vectorize retrieval and contamination tests;
- namespace collision proof or collision-resistant replacement;
- partial-write rollback diagnostic;
- Workers AI/R2/Vectorize cost/availability evidence under the free-first rule;
- Conversation Runtime consumption of this interface with retrieved-memory provenance;
- authenticated tenant isolation for any future public conversation.

## Disposition

`CONV-MEM-V1`: remain `ACTIVE_PARALLEL / IMPLEMENTING`.

The architectural distinction among history, recalled memory and consolidated knowledge remains sound. The main correction is sequencing/evidence: current code has coupled write ingestion to M2/M3 infrastructure before M2/M3 behavior has been accepted. Future verification should test the implementation that actually exists, not the older D1-only bootstrap description.

## Smallest useful next proof

When this work is resumed without displacing P01, run one production-safe fixture containing two conversations in two projects through the current write path; verify exact D1 replay, R2 recovery, scoped Vectorize retrieval, zero cross-talk, namespace behavior and rollback diagnostics; persist cost/availability measurements and only then reconsider the M1/M2/M3 milestone classifications.
