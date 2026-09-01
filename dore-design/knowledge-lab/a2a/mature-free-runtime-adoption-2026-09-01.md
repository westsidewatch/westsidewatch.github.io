# Doré A2A — Mature Free Runtime Adoption

Date: 2026-09-01
Status: active adoption policy

## Decision
Doré should reuse mature open-source foundations instead of rebuilding agent infrastructure. Keep the current working `dore.mail` coordination path while adding compatibility layers incrementally. No paid hosted service is required for the baseline.

## Adopt now

### 1. Linux Foundation A2A Protocol + official Python SDK
- Upstream: `a2aproject/A2A`, `a2aproject/a2a-python`
- License: Apache-2.0
- Role: agent cards/capability discovery, task lifecycle, messages/artifacts, HTTP+JSON / JSON-RPC interoperability, streaming and asynchronous notification semantics.
- Doré use: build an adapter beside `dore.mail`; do not rewrite the proven mailbox first.
- Validation: use A2A Inspector/TCK as compatibility tests.

### 2. LangGraph OSS patterns/runtime
- Upstream: `langchain-ai/langgraph`
- License: MIT for OSS package.
- Role: durable graph state, checkpoints, persistence, resume-after-interruption, explicit state-machine orchestration.
- Doré use: model Driver lifecycle and parent-goal checkpoint/resume. Start with patterns and a small isolated local prototype before replacing the resident worker.
- No LangChain requirement: LangGraph can be used independently.

### 3. OpenHands Skills pattern
- Upstream: `OpenHands/OpenHands`
- License: MIT.
- Role: repository-local reusable skills, triggerable procedural knowledge, scripts/hooks, versioned capability accumulation.
- Doré use: evolve `knowledge-lab/skills/registry.json` toward portable skill packages with provenance, trigger, procedure, verification, scope and limits.

## Candidate later, not baseline dependency

### Temporal self-hosted
- Role: stronger durable execution when Doré needs multi-process/distributed workflows, timers, queues and crash recovery beyond the local worker.
- Free path: open-source self-hosting; local development server is available.
- Decision: do not add this operational weight yet. Re-evaluate when the lightweight Driver/worker reaches a concrete durability limit.

## Free-baseline rule
1. Prefer Apache-2.0/MIT/open-source components and local/self-hosted operation.
2. Do not introduce paid hosted APIs merely to implement orchestration.
3. A mature component is a candidate, not dogma: verify current maintenance, compatibility, license and fit at adoption time.
4. Preserve provenance and upstream version for anything copied/adapted.
5. Run the smallest isolated experiment before promotion into Doré Core.
6. Do not sacrifice a proven Doré capability merely to become standards-compliant.

## Target architecture

`Human Goal -> Durable Driver -> A2A task/state layer -> Doré + research/design/tool capabilities -> Observe -> Decide -> Act -> checkpoint -> next action`

ChatGPT conversation is observation/command UI, not a required execution heartbeat.

## Immediate real-work acceptance
Use New Westside × Storybook as the integration workload. The system passes only when the parent goal continues without a new human message, unknown gaps enter research/experiment/verification, verified lessons become reusable skills, and the parent goal resumes. Locked homepage #262 remains untouched.
