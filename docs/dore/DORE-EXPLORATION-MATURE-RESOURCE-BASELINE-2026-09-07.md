# Doré Exploration — Mature Resource Baseline

Recorded: 2026-09-07

## Purpose

This is the canonical baseline from the restored earlier Doré Exploration results plus the latest exploration rounds. Future exploration should start from this baseline rather than restart from zero.

## Core conclusion

Doré should not choose one external “memory system” as its brain.

Doré retains its own:

- Architecture
- Semantics
- Relations
- Provenance
- Decisions / History
- Reflex
- Knowledge authority

Mature open-source projects are treated as organs, algorithms, reference implementations, adapters, and nutrition that Doré can absorb.

Target architecture:

```text
Sources / Projects / Conversations / Research
→ QMD Adapter + Core SQLite/FTS5 deterministic floor
→ Recall Router
→ Doré Knowledge Context
→ Temporal / Relations layer
→ Context Assembler
→ Reflex Router
→ Task Execution
→ Hard / Semantic Gates
→ Durable Event Log / Work State
→ Consolidation / Learning
→ Knowledge and Skill evolution
```

## Restored + new candidate map

### QMD

Role: local document / knowledge retrieval.

Status: A+ candidate for adapter/direct use.

Use for: lexical + semantic + hybrid document search and reranking.

Boundary: QMD does not decide current truth, project semantics, decisions, or knowledge authority.

### LongMemory

Role: restored high-priority reference from earlier exploration.

Important ideas: provenance, temporal/supersession, graph, project context, bounded context, MCP.

Status: keep as a first-tier historical candidate; repository identity/details require re-verification before implementation decisions.

### Graphiti

Role: primary mature reference implementation for temporal knowledge graphs.

Absorb: episode → entity → relation → temporal validity → supersession → provenance → hybrid retrieval.

Status: A+ source-level reference; do not automatically deploy the whole stack.

### mnemos

Role: citation-first retrieval/context recovery.

Absorb: citation, read-only-by-default patterns, working-set restoration, context-compaction recovery, canonical consolidation.

Status: A candidate for POC.

### localmem

Role: lightweight deterministic recall.

Absorb: separate write/read lanes, FTS5/entity graph, no-model recall path, workspace isolation/dedup.

Status: A source-level absorption candidate.

### memkeeper

Role: deterministic retrieval floor plus optional intelligence.

Absorb: BM25 baseline, optional local semantic layer, optional rerank, graceful degradation.

Status: A architecture reference.

### grit

Role: compact SQLite temporal/graph/hybrid retrieval reference.

Absorb: append operation log, bi-temporal state, BM25/vector/graph fusion, budgeted traversal.

Status: watch/source-study candidate; maturity must be checked before dependency adoption.

### Palimp

Role: provenance/safety/local knowledge reference.

Absorb: provenance, temporal/as-of thinking, safe memory-as-data boundary.

Status: source-level reference.

### MOOSEDev

Role: knowledge lifecycle / typed project knowledge.

Absorb: typed decisions, constraints, lessons, ontology, lifecycle, provenance, supersession.

Status: important bridge from project experience to structured knowledge.

### ASKS

Role: knowledge formation/compilation.

Absorb: source → interpret → validate → compile.

Status: important reference for Doré Exploration → Knowledge Admission.

### Mem0

Role: mature production memory benchmark/reference, not Doré's knowledge authority.

Use: compare retrieval/memory quality and production patterns.

Status: benchmark/reference; do not make it Doré Core.

### engram

Role: retrieval evaluation and memory experiments.

Absorb: recall@k, known-answer regression sets, graph activation/dreaming ideas.

Status: evaluation reference.

### agent-memory-kit

Role: minimal evidence-gated episodic memory.

Absorb: no evidence → no episodic-memory admission.

Status: rule/pattern absorption.

### wake

Role: durable autonomous runtime.

Absorb/test: crash-durable event log, kill/restart resume, effect-aware replay, timeline/fork ideas.

Status: A+ POC candidate for Doré autonomous loops.

### Lite-Harness

Role: agent run/attempt/recovery model.

Absorb: attempts, sessions, approvals, ordered events, pause/resume/recover.

Status: architecture reference; likely too large for wholesale adoption.

### Letta / procedural-memory research

Role: background consolidation, memory blocks, skill learning.

Absorb later: dreaming/consolidation and procedural skill evolution.

Status: reference, not current Core dependency.

## Capability ownership

| Doré capability | Primary candidate/reference | Decision |
|---|---|---|
| Document search | QMD | Adapter/direct-use candidate |
| Deterministic recall | Doré SQLite/FTS5 | Keep in Core |
| Hybrid/semantic retrieval | QMD | Enhancement, not life-support layer |
| Context citation/recovery | mnemos | Absorb/POC |
| Knowledge authority/model | Doré | Never outsource |
| Provenance | LongMemory/MOOSEDev/mnemos patterns | Absorb |
| Temporal validity/supersession | Graphiti + LongMemory/grit patterns | Deep absorption |
| Relations | Graphiti/localmem/grit | Absorb |
| Knowledge formation | ASKS + MOOSEDev | Absorb |
| Memory benchmark | Mem0 | Benchmark |
| Retrieval benchmark | engram/QMD patterns | Build Doré eval |
| Durable runtime | wake | High-priority POC |
| Run/recovery model | Lite-Harness | Reference |
| Procedural learning | GAIA/ProcMEM/Letta patterns | Later phase |
| Consolidation/dreaming | Letta/engram patterns | Controlled background ability |
| Hard gate | Deterministic tests/invariants | Keep small and local |

## Architecture principles established by exploration

1. Durable event history should sit below mutable/current knowledge.
2. Current knowledge is a projection, not the raw historical record.
3. Bi-temporal validity and supersession belong in the knowledge model.
4. Retrieval is multi-signal; exact lexical retrieval remains a deterministic floor.
5. Vector/semantic retrieval is an optional second channel, not a replacement for lexical retrieval.
6. Context assembly must be token-budgeted and provenance-aware.
7. Knowledge and instruction must remain distinct.
8. Admission/write governance is separate from retrieval.
9. Memory categories should distinguish semantic, episodic, procedural, decisions, failures/outcomes.
10. Reflex routing should support retrieve-or-skip, skill-or-skip, explore-or-skip, tool/action decisions.
11. Autonomous loops should persist durable work state; correctness must not depend on a resident process staying alive.
12. Rollback/evaluation should have a deterministic hard floor plus semantic judgment for gray areas.
13. Compaction/summarization must not silently destroy goals, accepted/rejected decisions, open work, execution state, rollback points, or provenance.
14. External projects are nutrition/components, not a replacement brain.
15. Future Doré Exploration must compare new candidates against this baseline and report only genuine improvements or missing capabilities.

## Next engineering exploration gate

Perform source-level **Build / Borrow / Adapt / Reject** audits for:

- QMD
- LongMemory
- Graphiti
- mnemos
- localmem / memkeeper
- wake
- MOOSEDev
- ASKS

For each, determine:

- components that can be used directly
- algorithms/schema that can be absorbed
- dependencies to avoid
- overlap with existing Doré capabilities
- engineering work that can be deleted because a mature solution already exists
- local resource cost and failure/degradation behavior
- license and maintenance maturity

## Exploration baseline rule

Future “多雷探索” on Doré Core / memory / context / retrieval / autonomous runtime must start from this document as the existing baseline. It should not restart the landscape survey from zero. New findings are valuable only when they improve, replace, validate, or expose a gap in this baseline.
