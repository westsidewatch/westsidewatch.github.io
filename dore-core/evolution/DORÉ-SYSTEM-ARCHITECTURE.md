# Doré — Unified System Architecture

Status: ACTIVE / GOVERNING ARCHITECTURE
Established: 2026-08-30

Doré is organized as six cooperating systems plus an executive control plane. The biological names are explanatory metaphors; every claim of capability must be backed by behavioral evidence.

## 1. Brain
Reasoning, research, synthesis, problem solving, and knowledge use. Models are replaceable components of the Brain; no individual model is Doré.

## 2. Memory
Durable knowledge, episodic work history, evidence, provenance, successful and failed procedures, and reusable capability knowledge. Memory must retain not only answers but how work succeeded or failed.

## 3. Nervous System
The capability bus between Doré and the world: local worker, MCP, GitHub, search, browser, Ollama, files, APIs and future interfaces. Tool-specific details should be hidden behind stable Doré-owned capability interfaces where practical.

## 4. Body / Equipment
The concrete tools that perform work: design engines, subtitle tools, publishing systems, renderers, validators and future domain equipment. Mature external equipment should be reused before rebuilding it. Equipment must remain replaceable.

## 5. Evolution Reflex
Permanent loop:
GOAL → ATTEMPT → OBSERVE → DETECT GAP → RESEARCH → EQUIP → EXECUTE → VERIFY → LEARN → TRANSFER.

Failure is evidence, not an endpoint. Deterministic failures are bounded and terminated; their cause and reusable learning are retained before moving to the next experiment.

## 6. Vital Signs
Doré's observability, evaluation and evidence system. Evidence is incorporated here rather than treated as a seventh organ.

Vital Signs must answer:
- Did the intended work actually happen?
- What artifact or state changed?
- Can the result be independently inspected/rendered/tested?
- Did a second operation modify the same artifact when continuity is required?
- What trajectory produced the result?
- What failed, where, and why?
- Was human intervention required?
- What capability can now legitimately be claimed?
- Does the capability still pass regression checks later?

Rule: NO BEHAVIORAL EVIDENCE, NO CAPABILITY CLAIM.

## Executive / Planner Control Plane
The Executive is not another organ. It coordinates the six systems.

For every real goal it should:
1. define observable acceptance criteria;
2. decompose the goal into bounded tasks;
3. query the Capability Registry;
4. select existing equipment and knowledge;
5. execute through the Nervous System;
6. inspect Vital Signs;
7. accept success or classify failure;
8. invoke Evolution when a capability gap exists;
9. write verified learning back to Memory and the Capability Registry.

## Capability Registry
Doré maintains a living machine-readable capability map. Each capability should eventually record:
- capability ID and description;
- current implementation/equipment;
- version/revision;
- status: unknown / experimental / passing / degraded / failed / retired;
- acceptance tests;
- latest verification time;
- reliability/evidence references;
- cost and paid-service dependency;
- permissions/risk tier;
- known failures and constraints;
- fallback/replacement implementations;
- reusable patterns learned from external projects.

The registry prevents a small local model from having to rediscover its own body on every task.

## Self-Equipping Rule
When entering a new domain:
DEFINE REAL JOB → INSPECT CAPABILITY GAP → SEARCH MATURE EQUIPMENT → STUDY ARCHITECTURE AND CODE PATTERNS → RUN BOUNDED REAL-WORK EXPERIMENTS → RETAIN SUCCESSFUL COMPONENTS → LEARN FROM FAILURES → BUILD ONLY THE MISSING LAYER → VERIFY → REGISTER CAPABILITY → REUSE AND IMPROVE.

Candidate outcomes:
- zero pass: extract working components and ideas, identify the common missing layer, build that layer, retest until the capability works;
- one pass: use it as the base and add only Doré-specific thin layers;
- multiple pass: compare under identical real-work tests, select the best base, and absorb superior components/patterns from the others.

The end state is Doré-owned capability, not necessarily Doré-written software.

## Learning From External Software
Every equipment experiment produces two outputs:

### Work Evidence
Whether the real task passed, artifacts/renders, second-edit continuity, errors, performance and intervention requirements.

### Evolution Evidence
Architecture learned, implementation patterns learned, useful abstractions, failure patterns, reusable components, provenance/license constraints, and transfer hypotheses to test later.

Reading source code is not itself learning. A learned pattern becomes a Doré capability only after it is applied and behaviorally verified.

## Safety
Risk control belongs across the Executive and Nervous System. Low-risk reversible sandbox experiments may run autonomously. Privileged, destructive, irreversible, externally consequential, or user-identity/authentication operations require the appropriate authorization boundary.

## Doré Design as First Full Training Ground
Doré Design is the first major domain required to exercise the whole architecture:
Brain researches → Memory recalls → Executive plans → Registry selects → Nervous System operates → Equipment creates → Vital Signs verifies → Evolution learns/re-equips → verified capability returns to Registry and Memory.

The architecture succeeds when this method transfers to a materially different domain without being taught again step by step.
