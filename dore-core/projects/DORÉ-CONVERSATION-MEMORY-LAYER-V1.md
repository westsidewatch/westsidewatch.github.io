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
Planned binding: `DORE_MEMORY_ARCHIVE`.

When bound, each message can be mirrored as immutable JSON under:
`conversations/{project_id}/{conversation_id}/{message_id}.json`

D1 stores the archive pointer.

### Vectorize — semantic recall
Planned binding: `DORE_MEMORY_VECTOR`.

Vectorize is additive, not a replacement for D1. The intended order is:

`identity/scope filter in D1 metadata -> vector similarity inside allowed scope -> prompt/context assembly`

The implementation currently names Cloudflare Workers AI model `@cf/baai/bge-small-en-v1.5` for 384-dimensional message embeddings. This is implementation evidence only; no production semantic-recall acceptance has yet been persisted.

## Current API

`POST /api/dore/memory`

Stores a message with `conversation_id`, `project_id`, `actor_id`, `role`, and `content`. Duplicate content in the same conversation+role is deduplicated by SHA-256.

**Sweep-01 implementation reconciliation (2026-08-27):** the live repository implementation has advanced beyond the original M1 bootstrap contract and now hard-requires `DORE_SENSORY`, `DORE_MEMORY_VECTOR`, `DORE_MEMORY_ARCHIVE`, and `AI` before a new POST can succeed. It writes an R2 archive object and a Vectorize embedding before committing the D1 conversation/message rows, with rollback attempts if a later write fails. Therefore R2/Vectorize are no longer optional on the current write path, even though older text and tests still describe them as optional hooks.

`GET /api/dore/memory?conversation_id=...&project_id=...&limit=24`

Returns recent D1 history only inside the supplied scope. At least one scope is mandatory. Conversation + project is the preferred strongest boundary. The current GET path reports whether Vectorize/R2 bindings exist but does **not** yet perform semantic recall.

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
- `dore_memory_chunks` exists in schema but is not yet exercised by the current API.
- The contract test is primarily a static source/schema assertion. It does not prove production write/replay, rollback integrity, namespace isolation, semantic retrieval, or tenant isolation.

## Prompt assembly target

Future Conversation Runtime prompt/context packet:

`constitution/authority + current user turn + current-conversation recent window + scoped semantic recalls + project state + relevant consolidated knowledge + tool evidence`

The system should prefer the smallest sufficient context rather than dumping all historical text into every model call.

## Free-first rule

Doré must not purchase storage, embeddings, AI inference, or vector capacity merely for convenience. Cost Frontier must move from FREE to WATCH/APPROACHING_LIMIT before a paid proposal is made. The current hard dependency on Workers AI/R2/Vectorize therefore requires explicit runtime/cost verification rather than being silently treated as free or optional.

## Implementation phases

### M1 — scoped history foundation
- D1 schema
- record/retrieve API
- mandatory retrieval scope
- duplicate protection
- CI contract tests

Repository structure exists, but production acceptance remains unverified.

### M2 — archive activation
- R2 immutable raw transcript archive
- recovery/replay test

Current POST code attempts R2 archival as a required write, but no persisted recovery/replay acceptance was found in Sweep 01.

### M3 — vector recall
- embedding path
- chunking contract
- Vectorize metadata: actor/project/conversation/message
- ID+scope+vector retrieval
- contamination/"conversation cross-talk" regression suite
- cost/latency measurements

Current POST code creates a message embedding and Vectorize record, but no semantic-retrieval path or contamination acceptance is yet evidenced. Message-chunk infrastructure remains unused.

### M4 — Conversation Alpha integration
- Conversation Context Builder reads this memory layer
- meeting contributions cite retrieved memory provenance
- meeting close persists durable conversation decisions
- consolidation promotes only warranted conclusions to GitHub knowledge/project records

The earlier Conversation Internal Alpha milestone remains separately verified; that milestone must not be conflated with production completion of this memory layer.

## Completion gates

V1 is not complete until:
- real production bindings accept a message through the **current** write path;
- exact conversation+project retrieval replays it;
- a different conversation cannot retrieve it under strict scope;
- a missing/incorrect project scope cannot silently contaminate another project;
- R2 archive write and recovery/replay are verified;
- Vectorize recall uses explicit allowed scope and passes cross-conversation contamination tests;
- current namespace construction is shown collision-safe for allowed identifier lengths, or replaced with a collision-resistant namespace key;
- partial-write failure/rollback behavior is exercised;
- Workers AI/R2/Vectorize cost and availability assumptions are explicitly measured under the free-first rule;
- Conversation Alpha consumes the scoped memory interface with provenance;
- no public user isolation claim is made without authentication/tenant tests.

## Sweep-01 disposition — 2026-08-27

Classification remains `ACTIVE_PARALLEL / IMPLEMENTING`. The architecture direction is valid, but repository implementation and earlier documentation/test language had diverged. Current code has effectively coupled M1 write ingestion to M2/M3 infrastructure before M2/M3 acceptance evidence exists. The next useful proof is therefore not merely a D1-only fixture: it is one production-safe two-conversation/two-project fixture through the current D1+R2+AI+Vectorize write path, followed by exact D1 replay, R2 recovery, scoped vector retrieval, zero cross-talk, namespace-collision checks, and rollback diagnostics. This work remains subordinate to P01.