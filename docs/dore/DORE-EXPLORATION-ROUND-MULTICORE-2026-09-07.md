# Doré Exploration Round — Multicore Without Multicore Pressure

Date: 2026-09-07
Status: exploration delta over existing Doré Local AI baseline
Target: Mac mini M4 / 16 GB unified memory

## Frozen baseline

This round does not replace prior conclusions.

Doré remains Doré. External projects are substrates, organs, algorithms, and reference implementations; they do not own Doré identity, Knowledge Authority, Context semantics, Reflex, product semantics, or evolution policy.

Preserved architecture:

- LongMemory: candidate Knowledge/Memory substrate, not Doré itself.
- QMD: document/hybrid retrieval substrate.
- wake: durable execution substrate.
- Osaurus: Mac-native agent/runtime/sandbox source reference.
- vLLM Semantic Router: Mixture-of-Models routing architecture source.
- mnemos/localmem/Graphiti/grit/Palimp/MOOSEDev/ASKS: retained complementary reference patterns.
- multi-core means virtual capabilities with minimum-capability selection; not many large models resident simultaneously.
- Free Gate, Lightweight Gate, Maturity Gate, Capability Gain, Build/Borrow/Adapt/Reject remain mandatory.

## New exploration question

How can Doré keep multiple specialist AI cores available while reducing RAM, compute, latency, energy and maintenance pressure on a 16 GB Apple Silicon machine?

## Strong new delta: model residency becomes a first-class scheduling problem

The strongest new finding is that current Apple-Silicon local serving projects have already implemented mature patterns for exactly this constraint.

### oMLX — high-priority A+ source/POC candidate

Role: local inference residency manager and cache-aware multi-model server.

Relevant features:

- Apple Silicon / MLX local serving.
- Multi-model EnginePool.
- LRU eviction when memory pressure rises.
- Per-model TTL auto-unload.
- Manual pin/load/unload.
- Process-level memory guard to avoid machine-wide OOM.
- Supports LLM, VLM, embeddings and rerankers within one serving plane.
- tiered KV cache: hot RAM + cold SSD.
- SSD cache survives model/session churn and can avoid repeated prefix recomputation.
- OpenAI-compatible localhost API.
- Apache-2.0.
- cloud/API payment is not required for the local core path.

Doré decision:

**BORROW + DIRECT POC / A+**

Do not copy its full product/admin UX into Doré. Study or directly POC the EnginePool, LRU/TTL, memory guard and tiered cache behavior.

This materially upgrades the previous single-residency idea:

```text
Virtual capability pool
        ↓
Doré Reflex
        ↓
Residency manager
        ├─ pin tiny/high-frequency core
        ├─ hot-swap specialist
        ├─ LRU evict stale model
        ├─ TTL unload idle model
        ├─ memory guard prevents OOM
        └─ SSD cache preserves reusable prefixes
```

### mlx-serve — focused single-residency reference

Role: small Apple Silicon local server explicitly designed to load exactly one MLX model at a time.

Relevant features:

- hot-swap by requested model name;
- unload previous model automatically;
- auto-unload on inactivity;
- per-request keep_alive;
- model lifecycle event log;
- memory monitoring;
- subprocess isolation for text/vision;
- supports text, vision, embeddings, TTS and STT;
- OpenAI-compatible local endpoint.

Doré decision:

**BORROW / POC COMPARATOR / A**

Use it as the cleanest comparison for strict single-residency on 16 GB. If oMLX's larger feature set is unnecessary, mlx-serve demonstrates a smaller residency-control design.

### macMLX — native Swift inference reference remains important

macMLX remains a useful candidate because its inference engine is Swift-native/in-process, with no Python requirement in its main path, and exposes a local OpenAI-compatible API.

Doré decision remains:

**DIRECT POC / A**

Its value is not routing semantics; its value is low-friction native inference on Apple Silicon.

### Apple official MLX stack — foundation confirmation

Apple's 2026 local-agentic-AI guidance formalizes the stack as MLX → MLX-LM → MLX-LM Server, with local OpenAI-compatible serving and tool calling. This reinforces the decision not to invent a custom low-level inference engine or protocol for Doré.

Doré decision:

**Do not build a custom local inference substrate from zero.**

## New multicore architecture

The previous virtual-core architecture is preserved and refined into two independent decisions:

1. capability routing: which kind of intelligence is required?
2. residency routing: which physical model should be loaded now, kept hot, evicted, or left asleep?

```text
                          DORÉ
                            │
                    Reflex / Authority
                            │
                 Virtual Capability Router
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
     no-model            tiny-hot          specialist
        │                   │                   │
SQLite/FTS/QMD      intent/entity/etc   language/reasoning/
LongMemory             small model       coding/vision/etc
                                                │
                                    Residency Manager
                                                │
                               ┌────────────────┼───────────────┐
                               │                │               │
                             pinned          hot-swap        cold/asleep
                               │                │               │
                         tiny frequent    current task      disk only
                                                │
                                     LRU / TTL / memory guard
                                                │
                                          local MLX runtime
```

This means 'multi-core coexistence' is a capability property, not a RAM residency requirement.

## Pressure-reduction rule

Doré should route by the minimum sufficient capability, not by strongest-model preference.

Decision order:

1. Can deterministic retrieval/rules answer it? If yes, no model.
2. Can a tiny always-hot core classify/extract/rewrite it? If yes, do not wake a large model.
3. Does the current resident specialist already satisfy the task? Reuse it.
4. If another specialist is required, hot-swap only then.
5. Keep a model resident only when observed reuse probability justifies its RAM cost.
6. Unload idle specialists by TTL.
7. Cache reusable prefixes/context blocks when that reduces recomputation without excessive SSD churn.

## Important separation: capability routing vs physical model naming

Doré products must request virtual capabilities only:

- language
- reasoning
- coding
- vision
- research
- embedding
- rerank
- voice
- image
- tiny-reflex

Physical model names stay behind the capability registry. Replacing a model must not alter Doré memory, identity, project context, product behavior or external API surface.

## Relation to LongMemory and QMD

LongMemory and QMD reduce AI pressure before model routing even occurs.

Example: fuzzy Bible-study note in 多寫.

```text
user types note
   ↓
tiny/local reflex or deterministic entity extraction
   ↓
QMD + LongMemory retrieval
   ↓
lightweight rank
   ↓
subtle related result
```

No large language model is required unless the user asks for interpretation, synthesis, writing or deeper reasoning.

Therefore:

**better Knowledge + Retrieval is itself a multicore pressure-reduction strategy.**

## New candidate: oMLX vs mlx-serve vs macMLX decision gate

Do not install all three in production.

Run a focused POC and select the smallest one that satisfies Doré's actual needs.

Required test on M4/16 GB:

- cold model load time;
- hot-swap time;
- peak RAM;
- idle RAM;
- unload correctness;
- repeated switch leakage;
- model TTL behavior;
- OOM prevention;
- local API stability;
- tool-call compatibility;
- embedding/rerank coexistence;
- SSD cache benefit vs write pressure;
- crash/restart recovery;
- zero network/API-key operation after models are downloaded.

Selection preference:

- if strict one-model-at-a-time is enough → prefer smallest single-residency implementation;
- if Doré benefits from tiny pinned models + specialist hot-swap → prefer EnginePool/LRU/TTL architecture;
- if zero-Python native integration materially reduces maintenance → favor macMLX/Swift-native path;
- do not keep multiple inference servers merely for feature accumulation.

## vLLM Semantic Router — preserved, narrowed role

Still A+ as routing architecture reference, but not the physical inference substrate on this Mac.

Borrow:

- Workload → Router → Pool;
- signals and policies;
- model eligibility;
- recipes;
- quality/cost/latency/privacy dimensions;
- versioned MoM contract;
- evaluation methodology.

Do not deploy the heavy vLLM serving stack merely to get these concepts.

Doré Reflex should absorb the routing semantics while the local residency manager handles Apple-Silicon model lifecycle.

## Osaurus — preserved new-exploration result

Osaurus remains valuable for:

- model-agnostic agent identity;
- agent continuity independent of physical model;
- local/offline operation;
- tool/skill selection;
- sandbox/execution;
- scheduling;
- Mac-native integration.

Its key architectural confirmation is preserved:

**models are interchangeable; the harness/identity/context compounds.**

Doré remains the higher-level identity and authority.

## OpenJarvis — preserved new-exploration result

Keep its evaluation idea as a Doré hard metric:

**Intelligence per Resource**.

Every model/core decision should be evaluated on:

- answer/task quality;
- latency;
- RAM;
- load time;
- energy/resource proxy;
- context cost;
- failure rate;
- reuse probability;
- unload/reload overhead.

A larger model is not better if a smaller/deterministic path completes the same Doré task reliably.

## Rejected/low-priority findings this round

- tiny new personal GitHub routers with minimal adoption: useful as examples, not dependencies;
- routing projects centered mainly on paid cloud provider price optimization: not Doré Core candidates;
- MoE projects built around Alibaba/Qwen-specific physical models: architecture may be studied, but those models are not Doré core candidates under the current user decision;
- running many model servers simultaneously: conflicts with the lightweight principle unless benchmark evidence proves a need.

## New hard engineering invariants

1. Doré Sovereignty Gate — external substrates never become Doré authority.
2. Exploration Preservation Gate — old A/A+ findings and new validated findings cannot disappear without explicit supersession evidence.
3. Free Gate — offline/local/no-commercial-key core path.
4. Minimum Capability Gate — do not invoke AI when deterministic capability suffices.
5. Residency Gate — multi-core availability does not imply multi-model RAM residency.
6. Memory Guard — local inference must have a hard machine-protection ceiling.
7. Idle Release — specialist models must be unloadable after inactivity.
8. Model Replaceability — products request virtual capability, never physical model identity.
9. Intelligence-per-Resource Gate — promotion requires measured capability gain per resource burden.

## Next engineering action

POC-MC1: Build a local residency benchmark harness around Doré virtual capabilities.

Compare one-model-at-a-time and pool/LRU strategies on the actual M4/16 GB machine.

Target capability set for the first benchmark:

- tiny-reflex
- language
- reasoning
- embedding
- rerank

Image/vision/voice remain cold specialists until requested.

Acceptance goal:

> Doré can expose several specialist capabilities while keeping ordinary idle/runtime pressure close to a single tiny core plus deterministic retrieval, loading heavier intelligence only when the task proves it needs it.

Core principle:

> Doré becomes more capable by having more available organs, while becoming lighter by refusing to keep those organs active when they are not needed.
