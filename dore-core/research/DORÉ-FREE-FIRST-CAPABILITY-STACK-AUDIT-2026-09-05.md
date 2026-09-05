# DORÉ FREE-FIRST CAPABILITY STACK AUDIT

Status: ACCEPTED FOUNDATION / BUILD MAY PROCEED
Date: 2026-09-05

## Decision

Doré Capability Embodiment may proceed under the existing `FREE-FIRST` rule.

The selected software foundations are open source and do not require a paid SaaS subscription merely to use their code. The architecture must nevertheless keep **software license**, **model/runtime cost**, and **optional hosted-service cost** separate. Open-source software does not make a cloud model, GPU rental, hosted database, or provider API free.

## Accepted open-source cards

| Resource | Role | License/status | Doré decision |
|---|---|---|---|
| Pydantic AI | typed agent/tool runtime, deferred/on-demand capabilities | MIT | preferred reference/runtime integration where useful |
| mcp-agent | simple routing / MCP workflow reference | Apache-2.0 | benchmark/reference; do not duplicate if Doré stdlib router suffices |
| DSPy | optimization / cognitive compilation experiments | MIT | later evolution-plane adapter; not hot-path dependency |
| Hermes Agent | trace-to-skill/self-improvement patterns | MIT | study and selectively digest; do not adopt whole agent runtime |
| MCP Registry | external server discovery metadata | Apache-2.0/MIT transition; docs CC-BY-4.0 | later discovery adapter, not core dependency |
| agentgateway | gateway, routing, policy, telemetry | Apache-2.0 | reserve for scale; do not install now |
| Agent Lightning | offline agent training/evolution | MIT | future evolution plane only after enough traces exist |
| Graphiti | temporal knowledge graph | Apache-2.0 | reserve; only add if existing Doré memory proves insufficient |

## Free-first interpretation

### Always allowed in the foundation
- Python standard library routing/state code;
- local deterministic functions;
- local files / Git-backed capability manifests;
- open-source libraries above when their dependency cost is justified;
- self-hosted local models whose **model license** is separately approved;
- existing free-tier infrastructure while observable limits remain inside Doré Cost Frontier policy.

### Not silently allowed
- paid model APIs;
- paid embedding APIs;
- paid vector databases;
- GPU rentals;
- paid hosted agent/evaluation services;
- model weights with incompatible research-only/non-commercial restrictions;
- a free tier that becomes a hidden hard dependency with no local fallback.

Any such boundary must remain optional and enter `HUMAN_PAID_DECISION` under Doré Operating Nervous System.

## Stability rule

Future stability is not achieved by trusting one framework. Doré therefore owns the following narrow contracts:

1. `CapabilityManifest` — portable capability description.
2. `RouteDecision` — selected small working set.
3. `TaskState` / typed artifacts — communication inside one Doré.
4. provider/skill references — lazy boundaries, never provider identity.
5. evidence/promotion records — Doré-owned learning history.

Frameworks sit behind these contracts and may be replaced. Doré must not persist framework-specific objects as its durable memory/evidence format.

## Dependency strategy

Phase 1 intentionally begins with **zero new runtime dependencies** for the core router. Python stdlib implements the first deterministic/lexical sparse route. This establishes baseline behavior and a benchmark before Pydantic AI, embedding routers, DSPy, MCP, or other packages are introduced.

A dependency may be added only when it beats the baseline on at least one measured dimension without unacceptable regressions:
- routing quality;
- latency;
- context footprint;
- implementation complexity;
- observability;
- reliability;
- replaceability.

This prevents open-source dependency accumulation from becoming a new form of armour stacking.

## Model/image warning

Doré Image remains the one major area where **software can be free while execution is not automatically free**. ComfyUI/diffusers-style runtimes can be local/open-source, but actual image models have distinct licenses and hardware requirements. M1 must approve the exact resident renderer + model + license before generation becomes a verified Doré capability.

No paid image API is part of the required foundation path.

## Construction order

1. stdlib compact registry + typed shared state + bounded router;
2. benchmark dormant growth and unrelated-task isolation;
3. lazy instruction/provider loader;
4. visual capability path with one shared task state;
5. resident free/local renderer reconnaissance;
6. compare mature open-source adapters against baseline;
7. add only demonstrably useful dependencies;
8. later evolution plane: trace -> candidate -> regression -> promotion -> cognitive compilation.

## Acceptance

The stack is considered compatible with Doré's free-first architecture because the base system can operate without metered external AI services and every heavier component is optional, replaceable, and subject to explicit cost/license gates.

This is not a promise that all future inference is costless. It is a guarantee that **Doré Core does not structurally require payment in order to possess, route, retain, or execute deterministic capabilities**.
