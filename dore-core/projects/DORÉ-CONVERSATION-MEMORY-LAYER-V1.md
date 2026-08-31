# DORÉ Conversation Memory Layer v1

Status: ACTIVE / IMPLEMENTING
Established: 2026-08-25
Purpose: give Doré durable, scoped conversational memory without confusing raw history, recalled memory, and consolidated knowledge.

## Governing distinction

1. **History** = what Doré actually heard or said.
2. **Memory** = history selected for retrieval into a current context.
3. **Knowledge** = researched/consolidated conclusions that have earned durable status.

GitHub remains the canonical audited knowledge/evidence/project layer. Cloudflare becomes the runtime conversational-memory layer.

## Storage architecture

### D1 — structured identity and retrieval scope
Binding currently reused: `DORE_SENSORY`.

New records:
- `dore_conversations`
- `dore_messages`
- `dore_memory_chunks`

Required retrieval dimensions:
- `actor_id`
- `project_id`
- `conversation_id`
- time/order

Retrieval MUST NOT begin with unscoped global semantic similarity.

### R2 — raw transcript/archive object storage
Current binding: `DORE_MEMORY_ARCHIVE`.

The current base write path mirrors each accepted message as JSON under:
`conversations/{project_id}/{conversation_id}/{message_id}.json`

D1 stores the archive pointer. Current ingestion fails with `memory_archive_unbound` if the R2 archive binding is absent.

### Vectorize — semantic recall
Binding: `DORE_MEMORY_VECTOR` when semantic indexing/recall is enabled.

Vectorize is additive, not a replacement for D1. The intended order is:

`identity/scope filter in D1 metadata -> vector similarity inside allowed scope -> prompt/context assembly`

The implementation currently names Cloudflare Workers AI model `@cf/baai/bge-small-en-v1.5` for 384-dimensional message embeddings. On the current base ingestion path, Workers AI + Vectorize are a semantic adapter rather than a hard prerequisite: if semantic indexing is disabled or the adapter is unavailable/fails, the D1+R2 message write can still succeed and returns semantic-adapter status. Separate M5/M6 semantic-response and cross-conversation features still require their semantic runtime when invoked.

## Current API

`POST /api/dore/memory`

Stores a message with `conversation_id`, `project_id`, `actor_id`, `role`, and `content`. Duplicate content in the same conversation+role is deduplicated by SHA-256.

**Sweep-01 implementation reconciliation (2026-08-31):** repository history shows more than one dependency shape. An earlier snapshot observed a write path coupled to D1 + R2 + Workers AI + Vectorize. The current `functions/api/dore/memory.js` has since reduced the base-ingest hard dependency surface: `DORE_SENSORY` + `DORE_MEMORY_ARCHIVE` are mandatory, while `AI` + `DORE_MEMORY_VECTOR` are handled by `optionalVector(...)`. Semantic indexing failure does not roll back an otherwise successful D1+R2 message write. Therefore older text saying the current POST hard-requires all four bindings is superseded by the present implementation.

`GET /api/dore/memory?conversation_id=...&project_id=...&limit=24`

Returns recent D1 history only inside the supplied scope. At least one scope is mandatory. Conversation + project is the preferred strongest boundary. The current GET path does **not** perform semantic recall; semantic/cross-conversation recall is provided by separate Full Memory paths.

## Anti-cross-talk rules

1. Never use vector similarity as the first/only selector across all Doré history.
2. Prefer exact current `conversation_id`.
3. If cross-conversation recall is required, restrict first to the active `project_id`.
4. Global consolidated knowledge may be consulted separately; it must not masquerade as remembered conversation.
5. Retrieved context must retain provenance: message id, conversation id, project id, actor/role, time.
6. Public multi-user operation requires an authenticated user/tenant boundary before this memory layer can be considered safe for production public conversation.

### Current implementation cautions discovered by Sweep 01

- POST currently falls back to `project_id='unscoped'` if a project id is absent. This is weaker than the intended explicit project-scoping contract and must not be treated as proof of project isolation.
- Vector records are written with a namespace derived from `project_id::conversation_id`, truncated to 64 characters. Collision behavior for long identifiers has not been acceptance-tested.
- `dore_memory_chunks` exists in schema but is not yet exercised by the current base API.
- `memory-layer-contract.mjs` is now partly stale as a dependency description: it treats both R2 and Vectorize as optional hooks, while current code makes R2 mandatory and Vectorize optional. It remains useful for static schema/scope/policy assertions, not as complete current-runtime proof.
- The contract test is primarily a static source/schema assertion. It does not prove production write/replay, rollback integrity, namespace isolation, semantic retrieval, or tenant isolation.

## Prompt assembly target

Future Conversation Runtime prompt/context packet:

`constitution/authority + current user turn + current-conversation recent window + scoped semantic recalls + project state + relevant consolidated knowledge + tool evidence`

The system should prefer the smallest sufficient context rather than dumping all historical text into every model call.

## Free-first rule

Doré must not purchase storage, embeddings, AI inference, or vector capacity merely for convenience. Cost Frontier must move from FREE to WATCH/APPROACHING_LIMIT before a paid proposal is made. Current core ingestion requires D1+R2; optional semantic indexing and semantic recall add Workers AI/Vectorize usage. Cost verification must therefore distinguish core storage from semantic-adapter consumption rather than silently treating all layers as either mandatory or free.

## Implementation phases

### M1 — scoped history foundation
- D1 schema
- record/retrieve API
- mandatory retrieval scope
- duplicate protection
- CI contract tests

Repository structure and bounded production diagnostics exist, but production-ready/full-memory acceptance remains unverified.

### M2 — archive activation
- R2 immutable raw transcript archive
- recovery/replay test

Current POST requires R2 archival before D1 commit, with archive cleanup attempted if the subsequent D1 write fails. Independent recovery/replay and broader failure-injection acceptance remain open.

### M3 — vector recall
- embedding path
- chunking contract
- Vectorize metadata: actor/project/conversation/message
- ID+scope+vector retrieval
- contamination/"conversation cross-talk" regression suite
- cost/latency measurements

Current base POST can create a message embedding and Vectorize record when the semantic adapter is available; later Full Memory milestones implement semantic response and cross-conversation recall. Message-chunk infrastructure remains unused by the base API, and production-ready/cost/scale evidence remains incomplete.

### M4 — Conversation Alpha integration
- Conversation Context Builder reads this memory layer
- meeting contributions cite retrieved memory provenance
- meeting close persists durable conversation decisions
- consolidation promotes only warranted conclusions to GitHub knowledge/project records

The earlier Conversation Internal Alpha milestone remains separately verified; that milestone must not be conflated with production completion of this memory layer.

### M5–M7 — bounded Full Memory milestones
Merged work adds memory-aware semantic response, same-project cross-conversation recall with foreign-project exclusion, and resumable/idempotent history import plus deletion lifecycle. These are legitimate bounded implementation milestones documented in `DORÉ-CONVERSATION-MEMORY-EVIDENCE-LEDGER-2026-08-27.md`; they do not make the whole layer production-ready.

### M8 — full-history backfill
Named next stage after M7. Representative real-history backfill and fresh-conversation consumption remain open evidence.

## Completion gates

V1 is not complete until:
- real production bindings accept a message through the **current** D1+R2 core write path;
- exact conversation+project retrieval replays it;
- a different conversation cannot retrieve it under strict scope;
- a missing/incorrect project scope cannot silently contaminate another project;
- R2 archive write and recovery/replay are verified;
- semantic recall, when enabled, uses explicit allowed scope and passes cross-conversation contamination tests;
- current namespace construction is shown collision-safe for allowed identifier lengths, or replaced with a collision-resistant namespace key;
- partial-write failure/rollback behavior is exercised for D1+R2 and semantic-adapter failure behavior is separately exercised;
- D1/R2 and Workers AI/Vectorize cost and availability assumptions are explicitly measured under the free-first rule;
- M8 representative full-history backfill is verified;
- Conversation Runtime consumes the scoped memory interface with provenance across a fresh session;
- no public user isolation claim is made without authentication/tenant tests.

## Sweep-01 disposition — 2026-08-31

Classification remains `ACTIVE_PARALLEL / IMPLEMENTING`. The architecture direction is valid and Full Memory M1–M7 represent real bounded progress. Current implementation has also reduced the base-ingest hard dependency surface relative to an earlier snapshot: D1+R2 are the current core, semantic indexing is optional on base write, while semantic-response/cross-conversation capabilities use AI+Vectorize when invoked. The next useful proof remains M8 representative history plus negative-scope, recovery, collision, rollback, cost/latency and fresh-session integration evidence. The static contract test should be updated so its R2/Vectorize dependency assertions match current code. This work remains subordinate to P01.
