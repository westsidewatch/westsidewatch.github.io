# Doré ↔ ChatGPT A2A — Autonomous Communication Research Map

Date: 2026-09-01
Related project: GitHub Issue #272
Status: research candidates; none are adopted merely by appearing here.

## Open-source release vision

The project becomes a credible standalone open-source alpha when Doré and a peer agent can communicate without a human manually relaying each turn, while preserving safety, evidence, recoverability and explicit human-intervention gates.

Minimum alpha gate:
1. Bidirectional agent endpoint/discovery rather than GitHub files as the only transport.
2. Capability discovery: each agent can advertise what it can do and what it cannot do.
3. Durable task lifecycle: submitted/working/heartbeat/input-required/completed/failed/cancelled, with resumable state.
4. Autonomous learning/recovery loop: blocked -> diagnose gap -> inspect memory/training -> research current authoritative docs/tools -> controlled experiment -> learn -> resume parent goal.
5. Relationship memory and failure memory survive process/session restarts.
6. Observability: transport, execution, product acceptance and learning/recovery evidence are distinguishable.
7. Human intervention gates: explicit user takeover or genuinely human-only/time-critical permission boundary.
8. Interoperability test against at least one agent outside Doré's own implementation.
9. Protocol conformance/security tests and documented threat/permission model.
10. Repeated real-work evidence that the same failure class requires less human intervention.

The stronger beta milestone is autonomous peer initiation: either side can create a legitimate task/message when a trigger occurs, the other can discover/accept/decline it, and the conversation/task can continue asynchronously without a human polling GitHub.

## Current ecosystem to study and selectively reuse

### 1. Linux Foundation Agent2Agent (A2A) Protocol — highest priority
Official project: https://github.com/a2aproject/A2A
Official Python SDK: https://github.com/a2aproject/a2a-python
Inspector: https://github.com/a2aproject/a2a-inspector

Why it matters:
- Open protocol for communication/interoperability between opaque agents.
- Production-ready ecosystem with broad industry adoption.
- A2A 1.0 SDK supports JSON-RPC, HTTP+JSON/REST and gRPC.
- Official Python SDK includes async server/client patterns, optional FastAPI, OpenTelemetry and SQL persistence integrations.
- Ecosystem includes Agent Cards/capability discovery, samples, Inspector and TCK validation.
- Apache-2.0 Python SDK.

Doré hypothesis:
Do NOT rewrite the working dore.mail chain immediately. Build an A2A compatibility/adapter experiment beside it. Map dore.mail task/message/result semantics to A2A Task/Message/Artifact/status concepts, then use Inspector/TCK to expose mismatches.

### 2. A2A Inspector + TCK — immediate validation candidates
Why it matters:
- Inspector can connect to a local A2A agent, inspect Agent Card, validate basic compliance, live-chat and expose raw protocol traffic.
- TCK is intended for implementation compatibility testing.

Doré hypothesis:
A local Doré A2A endpoint should eventually pass Inspector/TCK before public alpha. This is more valuable than inventing our own compliance dashboard.

### 3. LangGraph — durable learning/recovery runtime candidate
Official docs: https://docs.langchain.com/oss/python/langgraph/overview

Relevant capabilities:
- durable execution
- persistence/checkpoints
- long-running stateful agents
- interrupts/human-in-the-loop
- fault recovery and resumability
- explicit graph/state routing

Doré hypothesis:
Model the autonomous-learning loop as explicit durable states rather than ad-hoc retries:
WORK -> BLOCKED -> DIAGNOSE -> LEARN -> EXPERIMENT -> VERIFY -> RESUME_PARENT_GOAL, with HUMAN_REQUIRED as an interrupt rather than generic failure.
Evaluate LangGraph before rebuilding equivalent checkpoint/recovery machinery.

### 4. Temporal — stronger durable-execution candidate for later scale
Official project/docs: https://github.com/temporalio/temporal and https://docs.temporal.io/ai

Relevant capability:
Durable workflows can resume after crashes, network timeouts or long waits for human approval; suited to long-running stateful agent loops.

Doré hypothesis:
Probably heavier than needed for the current Mac-resident phase. Keep as a scale/reliability candidate and compare against LangGraph when persistence moves beyond one machine.

### 5. Model Context Protocol (MCP) — capability/tool boundary, complementary to A2A
Official specification: https://modelcontextprotocol.io/

Relevant concepts:
- host/client/server separation
- explicit capability negotiation
- tools/resources/prompts
- stateful sessions and notifications
- security/consent boundaries

Doré hypothesis:
Use A2A for agent-to-agent collaboration; use MCP-style capability/tool boundaries for what an agent can access. Do not conflate the two protocols.

### 6. OpenAI Agents SDK — orchestration/tracing pattern research
Official open-source SDK: https://github.com/openai/openai-agents-python

Relevant concepts:
- manager/agents-as-tools
- handoffs
- guardrails
- built-in traces/spans for agent, tool and handoff activity

Doré hypothesis:
Study its handoff and observability semantics, but do not make Doré dependent on paid OpenAI API usage. The useful target is architecture/pattern learning and compatibility thinking, not introducing a paid runtime dependency.

### 7. Microsoft Agent Framework — A2A integration reference
Official docs: https://learn.microsoft.com/en-us/agent-framework/

Relevant observation:
Microsoft describes A2A as useful across process/service/organizational boundaries, with agent discovery, remote state and normal distributed-system concerns such as timeouts, retries and versioning.

Doré hypothesis:
Use as an interoperability/reference implementation study, not an immediate dependency.

## Proposed architecture direction

Keep current proven pieces while adding standards around them:

ChatGPT/peer agent
  <-> A2A compatibility endpoint (new experiment)
  <-> Doré relationship/task layer
  <-> durable learning/recovery state machine
  <-> coordination worker/local tools
  <-> product acceptance + evidence

Existing GitHub inbox/outbox remains a durable fallback/audit transport during migration, not necessarily the final real-time conversation transport.

## Research discipline

For every candidate at actual adoption time, re-check:
- current release/maintenance status
- license
- security posture
- local/offline compatibility
- cost/API dependency
- protocol/version compatibility
- migration burden
- whether it actually reduces human intervention

Then run a small controlled experiment. Promote only proven pieces.

## First experiments after Storybook milestone

1. Write a dore.mail.v2 -> A2A semantic mapping table.
2. Expose a read-only local Doré Agent Card/capability endpoint.
3. Implement one minimal A2A task round-trip beside the existing GitHub mailbox.
4. Validate it with official A2A Inspector/TCK.
5. Prototype BLOCKED -> LEARN -> RESUME as a durable state machine using either minimal local code or LangGraph after comparison.
6. Measure whether Doré can recover one known failure (e.g. missing/outdated dependency knowledge) without ChatGPT teaching the second time.

## Open-source readiness statement

Do not wait for perfection. Open-source alpha is appropriate once the minimum alpha gate above is demonstrated end-to-end and documented. The distinguishing feature should not be 'another A2A implementation'; it should be the evidence-driven relationship layer: autonomous learning/recovery, failure memory, human-intervention gates, and measurable reduction of human intervention built on top of interoperable standards.