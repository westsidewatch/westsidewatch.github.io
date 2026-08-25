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

D1 stores the archive pointer. The API is intentionally able to operate without R2 during the free-first bootstrap stage.

### Vectorize — semantic recall
Planned binding: `DORE_MEMORY_VECTOR`.

Vectorize is additive, not a replacement for D1. The intended order is:

`identity/scope filter in D1 metadata -> vector similarity inside allowed scope -> prompt/context assembly`

Phase 1 does NOT fabricate embeddings or silently choose a paid embedding dependency. Vector retrieval is activated only after a free-first embedding path, metadata contract, contamination tests, and cost frontier are established.

## Current API

`POST /api/dore/memory`

Stores a message with explicit `conversation_id`, `project_id`, `actor_id`, `role`, and `content`. Duplicate content in the same conversation+role is deduplicated by SHA-256. If R2 is bound, the raw message is also archived.

`GET /api/dore/memory?conversation_id=...&project_id=...&limit=24`

Returns recent history only inside the supplied scope. At least one scope is mandatory. Conversation + project is the preferred strongest boundary.

## Anti-cross-talk rules

1. Never use vector similarity as the first/only selector across all Doré history.
2. Prefer exact current `conversation_id`.
3. If cross-conversation recall is required, restrict first to the active `project_id`.
4. Global consolidated knowledge may be consulted separately; it must not masquerade as remembered conversation.
5. Retrieved context must retain provenance: message id, conversation id, project id, actor/role, time.
6. Public multi-user operation requires an authenticated user/tenant boundary before this memory layer can be considered safe for production public conversation.

## Prompt assembly target

Future Conversation Runtime prompt/context packet:

`constitution/authority + current user turn + current-conversation recent window + scoped semantic recalls + project state + relevant consolidated knowledge + tool evidence`

The system should prefer the smallest sufficient context rather than dumping all historical text into every model call.

## Free-first rule

Current implementation uses the already-bound D1 path and makes R2/Vectorize optional. Doré must not purchase storage, embeddings, AI inference, or vector capacity merely for convenience. Cost Frontier must move from FREE to WATCH/APPROACHING_LIMIT before a paid proposal is made.

## Implementation phases

### M1 — scoped history foundation (NOW)
- D1 schema
- record/retrieve API
- mandatory scope
- duplicate protection
- optional R2 archive hook
- CI contract tests

### M2 — archive activation
- bind/create R2 only if available within accepted free-first constraints
- immutable raw transcript archive
- recovery/replay test

### M3 — vector recall
- choose embedding path
- chunking contract
- Vectorize metadata: actor/project/conversation/message
- ID+scope+vector retrieval
- contamination/"conversation cross-talk" regression suite
- cost/latency measurements

### M4 — Conversation Alpha integration
- Conversation Context Builder reads this memory layer
- meeting contributions cite retrieved memory provenance
- meeting close persists durable conversation decisions
- consolidation promotes only warranted conclusions to GitHub knowledge/project records

## Completion gates

V1 is not complete until:
- real D1 production binding accepts a message;
- exact conversation retrieval replays it;
- a different conversation cannot retrieve it under strict scope;
- R2/Vectorize status is explicitly reported rather than assumed;
- Conversation Alpha consumes the scoped memory interface;
- no public user isolation claim is made without authentication/tenant tests.
