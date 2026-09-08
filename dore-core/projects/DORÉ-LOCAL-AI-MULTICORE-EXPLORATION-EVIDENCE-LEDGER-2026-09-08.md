# DORÉ LOCAL AI / MULTICORE EXPLORATION — EVIDENCE LEDGER

Date: 2026-09-08
Status: DISCOVERY / READY_FOR_POC
Owner: Doré
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`

## Evidence reconciled

- `docs/dore/DORE-EXPLORATION-MATURE-RESOURCE-BASELINE-2026-09-07.md`
- `docs/dore/DORE-LOCAL-AI-BUILD-BORROW-ADAPT-REJECT-AUDIT-2026-09-07.md`
- `docs/dore/DORE-EXPLORATION-ROUND-MULTICORE-2026-09-07.md`
- current Master Register `CORE`, `EVOLUTION`, `RUNTIME`, `NERVOUS-SYSTEM`, `SEARCH` boundaries

## Classification

The September 7 Local-AI / multicore work is a legitimate architecture-and-resource-selection milestone, but it is not implementation completion.

Current classification:

- mature-resource baseline: `VERIFIED_COMPLETE` as a bounded exploration baseline only;
- Build / Borrow / Adapt / Reject audit: `VERIFIED_COMPLETE` as a bounded audit/decision artifact only;
- multicore/residency architecture: `DISCOVERY / READY_FOR_POC`;
- actual residency manager, virtual-capability router, QMD adapter, wake durability adoption, model benchmark and code-deletion/refactor work: `UNKNOWN_NEEDS_EVIDENCE` until implemented and measured.

These documents must not be promoted into a claim that Doré already has operational multi-core local AI.

## Governing architecture retained

1. Doré remains the authority layer. External projects may provide organs, algorithms, adapters, evaluation methods or runtime primitives, but do not own Doré identity, Knowledge Authority, Context semantics, Reflex, product semantics or project authority.
2. Doré products request virtual capabilities, not physical model names.
3. Multi-core coexistence is a capability-availability property, not a requirement to keep many large models resident in RAM.
4. Minimum sufficient capability is the routing rule: deterministic retrieval/rules first; tiny core next; current resident specialist next; hot-swap a heavier specialist only when required.
5. Local inference promotion is governed by Free Gate, Lightweight Gate, Maturity Gate, Capability Gain and Build/Borrow/Adapt/Reject.
6. Intelligence-per-Resource is a required evaluation dimension alongside quality, latency, memory, load/unload behavior, failure rate and reuse probability.

## Candidate decisions preserved

### High-priority direct POC / source audit

- QMD — local document/hybrid retrieval adapter candidate; Doré SQLite/FTS5 remains deterministic floor and Knowledge authority remains in Doré.
- wake — crash-durable event log / restart-resume / effect-aware replay POC candidate.
- oMLX — EnginePool/LRU/TTL/memory-guard/tiered-cache residency-manager POC candidate on Apple Silicon.
- mlx-serve — strict single-residency comparator.
- macMLX — native Swift/Apple-Silicon inference comparator.
- Osaurus — Mac-native agent/runtime/sandbox source comparison, not a Doré replacement.

### Borrow/absorb rather than wholesale deploy

- vLLM Semantic Router — workload/signals/policies/model-pool/recipe semantics; do not deploy the heavy serving stack solely for routing.
- mnemos / localmem — citation, deterministic recall, write/read separation, restore/consolidation and supersession patterns; do not create a second authoritative Doré memory store.
- Graphiti / LongMemory / grit / MOOSEDev / ASKS — temporal/provenance/knowledge-lifecycle patterns; adoption remains evidence-gated.

### Explicit non-goals

Do not build from zero, absent a demonstrated gap:

- generic local model serving engine;
- generic OpenAI-compatible protocol;
- generic provider gateway;
- complete semantic router;
- generic document semantic search engine;
- generic coding-agent execution loop;
- generic scheduler;
- resident-process loop recovery;
- generic memory framework;
- generic graph platform;
- STT engine;
- generic Mac agent sandbox.

## Missing evidence / engineering gates

The exploration has not yet produced persisted proof for:

- source-level compatibility audit against current Doré runtime/A2A/native-messaging code;
- code-deletion map showing which bespoke Doré infrastructure can safely be removed;
- QMD integration benchmark against current deterministic/fuzzy Search baseline;
- actual wake kill/restart/resume proof on a real Doré job;
- M4/16 GB residency benchmark comparing one-model-at-a-time versus pool/LRU/TTL strategies;
- measured cold-load/hot-swap/peak-RAM/idle-RAM/unload/leak/TTL/OOM/restart behavior;
- local model quality benchmark on Doré-owned Chinese/dialogue/Bible/project-context/tool-use workloads;
- proof that zero commercial API keys/network operation remains viable after selected models are downloaded;
- a machine-readable capability registry binding virtual capabilities to replaceable local endpoints;
- blind cross-product evidence that the selected architecture reduces AI pressure rather than merely adding infrastructure.

LongMemory remains a restored first-tier historical candidate, but repository identity/details require re-verification before implementation or dependency decisions.

## Revisit / supersession interpretation

This exploration does not supersede Doré's existing Runtime, Reflex, Knowledge or A2A architecture. It narrows future engineering by introducing a stronger deletion-and-borrow principle and by separating capability routing from physical model residency.

The earlier intuition that multi-core means many simultaneously resident models is explicitly superseded. Governing interpretation is now:

`many available virtual capabilities → minimum-capability routing → one tiny/pinned core plus hot-swapped specialists as needed → LRU/TTL/memory-guard release`

No existing production subsystem should be removed until a bounded replacement POC proves equal-or-better behavior and preserves project semantics, authority, continuity and rollback.

## Smallest next proof

Run `POC-MC1` on the actual M4/16 GB machine:

1. expose the same virtual capability set through two strategies — strict one-model-at-a-time and pool/LRU/TTL;
2. measure cold load, hot swap, peak/idle RAM, unload correctness, repeated-switch leakage, TTL, OOM protection, restart recovery and local API stability;
3. include deterministic/no-model routing as the baseline;
4. preserve all measurements and failure traces;
5. promote only the smallest strategy that measurably improves Doré capability without increasing ordinary idle/runtime pressure.

This POC is subordinate to the active P01 subtitle critical path and must not interrupt it.
