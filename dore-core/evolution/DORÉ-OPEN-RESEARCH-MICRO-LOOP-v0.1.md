# DORÉ Open Research Micro-Loop v0.1

Status: ACTIVE / SAMPLE LOOP
Established: 2026-09-05

## Purpose

This is a deliberately small sample of Doré's ability to grow a useful loop from a recurring need.

When Doré encounters a capability gap, architecture question, recurring failure, or promising research direction, it may run a bounded open-research micro-loop before building anything new.

The open web and mature open-source ecosystem are nutrition for Doré: learn, digest, verify, and retain useful capability. Do not hard-bolt frameworks into Doré merely because they exist.

## Governing filters

Prefer candidates that are:

- free to use;
- open source or openly documented;
- small and understandable;
- low in CPU, memory, storage, network, and background-process cost;
- simple to operate;
- safe and permission-bounded;
- stable and mature enough for real work;
- actively or sustainably maintained;
- easy to replace, remove, or maintain;
- local-first where practical;
- free of unnecessary paid-service or vendor lock-in.

A larger or heavier candidate must show a material behavioral advantage before it can displace a smaller one.

## 1–3 wave progressive search

Doré should stop as soon as sufficient evidence exists. Three waves are a ceiling, not a quota.

### Wave 1 — Landscape

Establish what the current research and mature open-source landscape says about the problem.

Output:
- dominant architecture/research directions;
- mature candidate projects;
- important terminology and evaluation criteria;
- obvious dead ends or heavyweight approaches to avoid.

### Wave 2 — Mechanism

Inspect the strongest small candidates more deeply.

Output:
- architecture and implementation patterns worth learning;
- reusable components or algorithms;
- license/provenance constraints;
- runtime/dependency/maintenance costs;
- evidence of real use, tests, releases, or research results.

### Wave 3 — Doré Fit

Re-rank candidates under Doré's governing filters and current architecture.

For each serious candidate choose one outcome:
- USE — mature component can be used directly behind a Doré-owned interface;
- ABSORB — learn the pattern/code idea and implement only the thin missing layer;
- EXPERIMENT — promising but requires a bounded real-work test;
- WATCH — research direction is valuable but not ready to adopt;
- REJECT — too heavy, costly, fragile, unsafe, locked-in, duplicative, or poorly maintained.

## Digest, do not graft

Default preference order:

1. reuse an existing Doré capability;
2. absorb a small proven pattern;
3. use a tiny replaceable component;
4. run a bounded experiment with a larger component;
5. adopt a framework only when behavioral evidence proves the added weight is justified.

Research notes alone are not capability.

## Loop output

Every completed run should leave a compact research packet containing:

- need / trigger;
- waves actually run;
- sources and provenance;
- shortlist;
- Doré-fit decision: USE / ABSORB / EXPERIMENT / WATCH / REJECT;
- expected cost and maintenance burden;
- proposed capability/loop destination;
- acceptance test if implementation is proposed;
- what was learned even from rejected candidates.

The packet feeds Memory and, when relevant, the Capability Registry and the requesting parent loop.

## Self-creation / nesting rule

This micro-loop may be invoked by Sensory, Memory, Design, Image, Search, Publishing, Product, or another Doré loop.

A child research loop should be created only when the need is recurring or sufficiently distinct that keeping it separate reduces repeated work. Otherwise run this micro-loop once and return the result to the parent.

A child loop must not become permanent merely because it was created. Promote it only after repeated usefulness is behaviorally demonstrated; otherwise merge, retire, or delete it.

## Resource discipline

- No permanent daemon merely to keep this loop alive.
- No continuous polling by default.
- Prefer event/need-triggered execution.
- Bound retries and search waves.
- Cache useful evidence rather than rediscovering it.
- Prefer durable lightweight state over resident processes.
- Avoid duplicate research when Memory already contains fresh verified evidence.

## Acceptance criteria for this sample loop

PASS requires that a real Doré need can trigger the loop and produce:

NEED → 1–3 WAVE SEARCH → FILTER → DIGEST → DECISION → EVIDENCE → MEMORY/REGISTRY RETURN

without requiring a new heavyweight framework or permanent background process.

The first reference sample is the 2026-09-05 investigation of nested/self-improving agent loops, including lightweight graph/state patterns, durable local workflow patterns, harness refinement, regression-gated self-improvement, and external-skill acquisition research.

## Relationship to governing architecture

This micro-loop instantiates the existing Evolution Reflex:

GOAL → ATTEMPT → OBSERVE → DETECT GAP → RESEARCH → EQUIP → EXECUTE → VERIFY → LEARN → TRANSFER.

It also operationalizes the Self-Equipping Rule's SEARCH MATURE EQUIPMENT and STUDY ARCHITECTURE AND CODE PATTERNS stages without changing Doré's governing architecture.
