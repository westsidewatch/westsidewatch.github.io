# Doré Local AI — Build / Borrow / Adapt / Reject Audit

Date: 2026-09-07
Status: engineering baseline
Machine target: Mac mini M4 / 16 GB unified memory

## Hard gates

Order of evaluation:

1. Free Gate
2. Lightweight Gate
3. Maturity Gate
4. Capability Gain
5. Build / Borrow / Adapt / Reject

### Free Gate

A Doré Core dependency must remain useful with all commercial API keys removed and the network disconnected.

- Core capability must not require paid API/SaaS/credits.
- A localhost API is a protocol, not a paid service, and is allowed.
- External APIs are optional escalation only and must be OFF by default.
- Free tiers/trials/credits do not count as a free foundation.
- Software license and model license are audited separately.
- No hidden telemetry/network dependency may be required for core operation.

Final acceptance: **Doré Local Core works offline, without commercial API keys, with zero recurring AI inference cost.**

## Architecture decision

Do not search for one universal local model. Doré uses multiple specialist cores selected by Reflex/Router. Doré itself owns Knowledge, Context, product semantics, decisions/history, routing policy and evaluation. Models are replaceable capability organs.

## Audit results

### 1. Osaurus — BORROW + ADAPT / A+

Free Gate: PASS for local path. MIT. Native Swift/Apple Silicon. Explicitly supports fully offline local models; cloud providers are optional.

Borrow/source-study:
- macOS-native agent harness patterns
- agent persistence and per-agent state
- local model/provider abstraction
- tool/skill selection
- Agent DB
- self-scheduling
- sandbox/execution isolation
- local server/CLI lifecycle

Do not build from zero until compared against Osaurus:
- generic Mac agent harness
- generic agent database
- generic tool-selection harness
- generic self-scheduling primitive
- generic local agent execution shell

Do NOT replace Doré with Osaurus. Doré retains Knowledge Context, Reflex, semantics, project authority and product integration.

Engineering action: source-level compatibility audit against current Doré runtime/A2A/native messaging architecture.

### 2. OpenJarvis — BORROW / A

Free Gate: PASS for local path. Apache-2.0. Can run backend/frontend on local hardware and use localhost/Ollama.

Borrow:
- local-first/cloud-escalation architecture
- evaluation dimensions: quality, latency, energy, FLOPs/resource cost
- personal assistant/research/code/monitor composition patterns
- local model backend abstraction

Do not adopt whole framework: Python + Rust + Node/frontend stack is heavier than Doré needs on a 16 GB always-on Mac.

Key Doré metric to absorb: **Intelligence per Resource** rather than benchmark score alone.

### 3. QMD — DIRECT/ADAPT / A+

Free/local role: local document/knowledge hybrid retrieval adapter.

Direct/Adapt:
- document indexing
- lexical + semantic/hybrid retrieval
- reranking where useful
- local knowledge collections

Doré retains SQLite/FTS5 deterministic floor and Knowledge authority. QMD results are evidence, not current truth.

Do not build another generic semantic document search engine before QMD integration is evaluated.

### 4. mnemos — BORROW + possible component use / A

Free Gate: PASS. MIT. One cgo-free Go binary; no network, telemetry, Python, Docker, Qdrant or Ollama required. SQLite FTS5/BM25 default; optional local semantic/hybrid search.

Borrow:
- exact source citation (`file#section`, line ranges)
- read-only default
- secret-scanned/path-confined writes
- recall/capture/restore/consolidate lifecycle
- working-set restoration after compaction
- durable-fact admission discipline

Do not create a second authoritative Doré memory database. Integrate patterns or adapter surfaces with Doré Knowledge Context.

### 5. localmem — BORROW / A

Free Gate: PASS. Local SQLite/FTS5; no network/account/telemetry; no LLM on recall path.

Borrow:
- strict read-lane/write-lane separation
- deterministic recall
- workspace/global tiers
- dedup
- weak-result labeling
- lessons/failure memory
- temporal supersession patterns

Reject as complete Doré retrieval engine: lexical limitations are acknowledged by the project and Doré already requires fuzzy/semantic/CJK retrieval.

### 6. wake — DIRECT POC / A+

Free Gate: PASS. Apache-2.0. One local Go binary. Tested on macOS/arm64.

POC directly:
- crash-durable event log
- kill/restart/resume
- effect-aware replay
- timeline/fork/diff
- unmodified agent/subprocess execution

Do not build another resident-daemon-based loop recovery system first.

Important caveat: Codex live-model adapter is explicitly not fully human-validated upstream; test Doré's actual Codex/local-agent path ourselves.

### 7. vLLM Semantic Router — BORROW/ADAPT, NOT FULL DEPLOY / A+

Free Gate: source/architecture PASS (Apache-2.0); deployment-fit gate: FAIL for full heavy stack on M4/16 GB.

Borrow:
- Workload → Router → Model Pool architecture
- signals
- policies
- model eligibility
- recipes
- Mixture-of-Models composition
- privacy/location/cost/quality routing concepts
- router evaluation methodology

Do not deploy vLLM GPU-serving infrastructure merely to obtain routing logic.

Do not build a complete semantic router from zero; adapt the minimum concepts to Doré Reflex.

### 8. Portkey Gateway — CONDITIONAL BORROW / B

Software is open-source/lightweight and can unify model endpoints, but its ecosystem is strongly provider/cloud-oriented.

Allowed only if Doré can run the selected gateway path locally with:
- no Portkey hosted account
- no paid provider key
- no required telemetry
- no external control plane

Borrow if needed:
- request normalization
- retry/fallback
- endpoint health
- provider error normalization

Do not make it a Core dependency until a localhost-only POC passes Free Gate. If a thin local adapter is simpler than the gateway after audit, reject the dependency.

### 9. LiteLLM — REFERENCE / B-

Useful mature provider abstraction but broad enterprise/cloud surface is larger than Doré's local-first need.

Borrow ideas only unless Portkey/local adapters fail. Do not let cloud-provider abstractions define Doré architecture.

### 10. Graphiti — BORROW ALGORITHMS/SCHEMA / A

Use as mature temporal-knowledge reference, not a required Doré service.

Absorb:
- episode → entity → relation
- validity windows
- supersession
- provenance
- temporal/current-vs-history retrieval
- hybrid graph retrieval concepts

Keep Doré's lightweight SQLite-centered Knowledge authority. Avoid introducing a heavyweight graph-service dependency solely for these semantics.

## What Doré should stop building from zero

Unless source-level audit proves a real gap, stop/reject new bespoke implementations of:

- generic local model serving engine
- generic OpenAI-compatible protocol
- generic multi-provider retry/fallback gateway
- complete semantic model router
- generic document semantic search engine
- generic coding-agent execution loop
- generic agent scheduler
- resident-process loop recovery
- generic memory framework
- generic temporal graph platform
- STT engine
- generic Mac agent sandbox

## What Doré must continue to own

- Knowledge authority
- Architecture/Semantics/Relations/Provenance/Decisions-History model
- temporal current-state projection
- Knowledge Admission Gate
- Context Retrieval/Assembly policy
- Reflex policy
- product/task semantics
- privacy/free/offline policy
- capability registry
- model evaluation history
- hard/semantic/evolution gates
- user intent and project authority

## Minimal target stack for first engineering POCs

Do not install everything. Test the smallest useful composition:

```text
Doré Core
  ↓
Knowledge Context + Reflex
  ├─ deterministic → SQLite/FTS5
  ├─ fuzzy/document → QMD adapter
  └─ AI required → specialist-core routing policy
                         ↓
                 local model endpoints
                 (existing local provider first)

Durability sidecar/runner POC → wake
Citation/consolidation patterns → mnemos
Agent/runtime source comparison → Osaurus
MoM routing design source → vLLM Semantic Router
```

Gateway rule: **do not add Portkey/LiteLLM until multiple real local endpoints create enough adapter complexity to justify a gateway.** This deletes a dependency from the immediate plan.

## Immediate engineering sequence

### POC-1 — Runtime deletion audit
Compare current Doré runtime/A2A/native messaging/scheduling code against Osaurus + wake. Identify code that can be removed or replaced by a mature primitive. Do not change product semantics.

### POC-2 — Retrieval integration
Keep SQLite/FTS5. Add/evaluate QMD adapter for fuzzy/hybrid retrieval. Import mnemos citation/restore concepts without creating a competing authority store.

### POC-3 — Specialist-core router
Implement the smallest Doré-specific policy surface using vLLM Semantic Router's Workload/Signals/Pool/Recipe model. Do not deploy full vLLM infrastructure.

Initial capabilities:
- language
- reasoning
- coding
- vision
- research
- embedding
- rerank
- voice
- image

Routing should prefer deterministic/local paths and load AI only when needed.

### POC-4 — Language/Reasoning benchmark
Benchmark non-Alibaba-family open-weight candidates on the actual M4/16 GB machine. Gemma 4 is baseline, not assumed winner.

Test with Doré-owned corpus:
- natural Chinese dialogue
- long conversational continuity
- ambiguous references
- Chinese/English switching
- writing
- Bible research
- project-context grounding
- tool calling/structured output
- refusal to invent missing context

Measure:
- quality
- latency
- peak/steady RAM
- model load time
- tokens/sec
- energy/resource proxy
- failure rate

### POC-5 — Durable loop
Run one bounded real Doré job under wake. Kill it intentionally, resume it, verify effects are not duplicated, and verify the event record independently.

## Promotion rule

A mature project/component is promoted only if it:

1. passes Free Gate;
2. reduces Doré-maintained code or clearly improves capability;
3. does not take over Doré Knowledge/Context authority;
4. works acceptably on M4/16 GB;
5. degrades safely when optional AI/network components are unavailable;
6. beats the current baseline in a reproducible Doré-owned evaluation.

Core principle:

> Mature open source is Doré's nutrition and organs, not a replacement brain. Every adopted component should make Doré more capable while reducing the amount of bespoke infrastructure Doré must carry.
