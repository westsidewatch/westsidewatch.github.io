# Doré Autonomous Loop — Global Component Benchmark

Date: 2026-09-01
Status: engineering decision record

## Goal
Compare the now-engineered Doré loop against mature public agent/workflow/runtime projects and standards, then adopt missing pieces without replacing working Doré capabilities.

## Current engineering loop
`Goal -> Plan -> Act -> Observe -> Gap -> Research -> Experiment -> Verify -> Promote -> Resume`

The active real-work feedback pair is **A2A <-> Storybook**. New Westside visual construction is the current parent workload.

## External comparison

### Linux Foundation / AAIF A2A 1.0
Adopt: canonical Agent Card, Task/Message/Artifact lifecycle, state mapping, future HTTP+JSON/JSON-RPC compatibility, Inspector/TCK validation.
Do not treat A2A as scheduler/runtime: it is the inter-agent protocol layer.

### Microsoft Agent Framework autonomous handoff
Adopt pattern: `NO_USER_INPUT` is a continuation event; autonomous execution continues until handoff, termination condition, or turn budget. Doré already has the first half; this benchmark adds an explicit termination/budget policy.

### LangGraph
Adopt pattern: separate thread checkpoint state from cross-thread durable store. Doré JSON files currently mix these concerns. Add an explicit durable checkpoint/event store with transactional writes.

### Temporal
Strength: strongest crash/replay durability and timers. Cost: external server/worker architecture is excessive for one local Mac today. Keep as escalation path when lightweight durability reaches a measured limit.

### DBOS
Strength: lightweight durable workflows/queues with checkpointing and recovery, much less infrastructure than Temporal. Current Python path still assumes a database service for normal production use. Adopt its workflow/step/idempotency concepts now, not a new database dependency yet.

### Prefect
Strength: mature open-source orchestration, retries, work pools, observability. It is broader and heavier than the current local single-host loop. Keep as candidate for multi-machine orchestration, not baseline.

### PydanticAI durable execution
Important ecosystem signal: durable-agent integrations now explicitly span Temporal, DBOS, Prefect and Restate. Doré should keep its runtime semantics engine-neutral and serializable. Adopt this compatibility principle now.

### OpenHands
Adopt: repository-local skills, scoped procedural knowledge, tool/runtime separation, evidence-producing coding loop. Doré already has skill registry; strengthen provenance and verification gates.

### APScheduler
Adopt later only when calendar/cron/timer jobs become first-class. launchd + resident loop is sufficient for current continuous control. Avoid adding a scheduler merely to poll every 30 seconds.

### watchfiles
Adopt later for event-driven local file wakeups when polling becomes a measured bottleneck. Keep current polling as fallback.

### OpenTelemetry
Adopt now at schema level: trace/span IDs, event categories, timing, status and correlation IDs. Do not require an exporter or hosted telemetry service. JSON/Git telemetry remains the free observation transport.

### SQLite WAL
Adopt now. It is in Python stdlib, local, transactional and appropriate for one-machine durable checkpoints, leases, deduplication and event journal. It closes a real gap left by multiple independent JSON state files.

## Missing links found and engineering decisions

1. **Transactional checkpoint/event store** — missing. Add `durable_store.py` using SQLite WAL.
2. **Execution lease / duplicate suppression** — incomplete. Add lease + idempotency keys to durable store.
3. **Retry/backoff policy** — only partially encoded in runtime. Add explicit `retry_policy.py` with no-information-gain blocking, exponential backoff and retry budget.
4. **Termination / autonomy budget** — missing as explicit component. Add `loop_guardrails.py`: autonomous turn budget, wall-clock budget, HUMAN_GATE classifier and terminal states.
5. **Trace correlation** — telemetry exists but no standard trace/span correlation. Add local OpenTelemetry-compatible field conventions without new dependency.
6. **Durability escalation rule** — missing. Record measurable thresholds for moving from SQLite/local runtime to DBOS/Temporal/Prefect.
7. **A2A conformance validation** — adapter exists, but Inspector/TCK is not yet executable in the Mac runtime. Keep as acceptance candidate and require isolated validation before declaring protocol compliance.
8. **Event-driven wakeup** — not necessary yet. watchfiles remains optional; polling is a deliberate fallback.
9. **Scheduled jobs** — not necessary for the current continuous race loop. APScheduler stays candidate until a real scheduled workload appears.
10. **Research source freshness** — catalog must store not only candidate names but role/adoption status; refreshed by real work before use.

## Baseline selected now
`launchd + Python stdlib resident runtime + SQLite WAL durable store + dore.mail/Git audit transport + A2A-shaped semantics + Storybook/Vite lab + repository Skills + explicit retry/guardrail policy + Git telemetry`

This baseline is free, local-first, inspectable, reversible, and keeps the current Doré system running while leaving clean escalation points to DBOS/Temporal/Prefect.

## Escalation thresholds
Move beyond SQLite/local runtime only when at least one is observed and recorded: multi-host execution is required; concurrent durable workflows regularly exceed one local worker; process crash replay causes repeated side effects despite idempotency; scheduled/long-sleep jobs dominate workload; local telemetry cannot explain failures; or database/queue contention becomes a measured bottleneck.

## Rule
No framework is adopted because it is fashionable. A component is promoted only when it solves an observed Doré gap better than the current mechanism and passes a small real experiment.
