# DORÉ CAPABILITY EMBODIMENT RESEARCH — 2026-09-05

Status: ACTIVE_PARALLEL / ARCHITECTURAL
Parent: `dore-core/architecture/DORE-CAPABILITY-EMBODIMENT-2026-09-05.md`
P01 impact: NONE

## Question

How can Doré gain many more abilities without becoming a collection of permanently loaded agents, prompts, tools and runtimes whose communication and resource costs rise with capability count?

## Current answer

Build Doré around sparse capability activation, typed shared state, lazy loading, progressive compilation of learned workflows into cheaper reflexes, and replaceable providers.

Engineering projects may be separate. Runtime cognition remains one Doré.

## Research families

1. Sparse Mixture-of-Experts routing: selective activation, routing stability, semantic specialization and adaptive expert count.
2. Adaptive computation: early exit / token-selective depth / compute proportional to difficulty.
3. Triggered/lazy skill systems: OpenHands skills/microagents; filesystem/capability registries; minimal prompt packs.
4. Plugin/function filtering: expose only relevant functions to a reasoning model.
5. Persistent memory architectures: separation of active attention from long-term durable memory.
6. Agent orchestration as a boundary case: supervisors/handoffs are useful for true isolation or concurrency but should not become the default for faculties of one Doré.
7. Event/state architectures: typed artifacts and job state rather than free-form recursive chat.

## Doré-specific hypotheses to test

H1. A small capability router can keep median active capability count bounded even while registry size grows substantially.

H2. Typed artifacts between visual stages will reduce model calls/context size versus Image-agent <-> Design-agent conversation while improving reproducibility.

H3. Repeated workflows can be compiled downward from deliberative L2 execution to semantic/deterministic L1/L0 execution after regression evidence.

H4. Provider schemas and heavy model runtimes can remain unloaded until a route explicitly requires them.

H5. Capability additions can have near-zero effect on unrelated task latency if manifests remain compact and skill bodies are lazy-loaded.

## Required benchmark

Create a benchmark with at least three task families:
- visual production;
- Scripture/research;
- deterministic maintenance/engineering.

Measure:
- active capability count;
- loaded instruction/context bytes;
- model calls;
- tool calls;
- latency;
- cache hit rate;
- peak resident memory when measurable;
- task correctness/quality;
- routing error rate.

Compare:
A. broad/eager loading;
B. multi-agent conversational handoff where applicable;
C. sparse capability route + typed shared state.

Do not promote architectural claims without measured evidence.

## Immediate visual experiment

Use the first Doré Image acceptance asset as the first benchmark packet:

`product need -> visual.direct -> visual.grammar -> image.generate -> image.critic -> design.compose -> design.verify`

No free-form internal agent conversation. Persist typed artifacts and telemetry.

The second comparable visual task must test whether validated steps compile downward and require less deliberative compute.

## Guardrail

Do not confuse application-level sparse routing with modifying or training the underlying foundation model. MoE/adaptive-computation research is architectural inspiration unless and until Doré has a justified model-training program with separate evidence, hardware and safety/resource gates.