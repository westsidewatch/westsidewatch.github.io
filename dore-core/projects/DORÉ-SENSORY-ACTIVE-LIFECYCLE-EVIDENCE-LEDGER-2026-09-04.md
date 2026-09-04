# DORÉ SENSORY ACTIVE-LIFECYCLE EVIDENCE LEDGER — 2026-09-04

Status: SWEEP-01 BOUNDED EVIDENCE / MAINTENANCE + REVISIT FINDING
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`
Related: `CW-001`, `RQ-001`, `ME-001`, `CORE`, `MEM-SWEEP-01`

## Scope reviewed

This bounded pass reviewed the current sensory/reflex persistence family without touching the active P01 subtitle critical path:

- `dore-core/memory/sensory-active.json`;
- `dore-core/memory/sensory-heartbeat-diagnostic.json`;
- `dore-core/reflex/REFLEX-CONSOLIDATION-1.0.md`;
- `dore-core/reflex/GATE-RUN-1.0.md`;
- `dore-core/reflex/signals/001-translated-phrase-to-original-language.md`;
- existing `DORÉ-SENSORY-DIAGNOSTIC-PERSISTENCE-EVIDENCE-LEDGER-2026-08-31.md`;
- existing `RQ-001 — Sensory-loop broader robustness evaluation`.

## Findings

### 1. Reflex Consolidation 1.0 remains legitimately closed

The reflex family still contains strong bounded completion evidence: RC1–RC6 passed, the end-to-end graduation workflow passed, Foundation regression passed, and the translated-phrase→original-language learning signal was promoted through that evidence. `GATE-RUN-1.0.md` is only an observable gate marker and must not be interpreted as a capability change by itself.

Current disposition: retain Reflex Consolidation 1.0 as `VERIFIED_COMPLETE`; no reopen is justified from this batch.

### 2. The sensory runtime is alive, but active-signal lifecycle semantics are incomplete

`sensory-active.json` currently contains four persisted signals. One historical signal (`馬利亞有幾位?`) is `CONSOLIDATED`. Three later signals remain `RESEARCHING`:

- Search/conversation explanation prompt, claimed 2026-08-28;
- Scripture phrase `耶和華啊,我終日等候你`, claimed 2026-08-28;
- explicit memory-test prompt containing `初光金`, claimed 2026-08-28.

The fresh 2026-09-04 heartbeat still reports the first of these as `RESEARCHING`, `changed=false`, with no newer research transition since 2026-08-28. The heartbeat itself is healthy (`ok=true`) and continues to reconcile consolidated state, so this is not evidence that the sensory transport is down.

The important distinction is therefore:

- **transport / heartbeat health:** retained;
- **historical repair milestone:** retained `VERIFIED_COMPLETE`;
- **active-signal terminal lifecycle / aging policy:** not demonstrated;
- **heterogeneous signal quality:** still evidence-gated.

### 3. New maintenance debt: RESEARCHING can remain indefinitely without an explicit stale/terminal disposition

Current persisted evidence exposes no bounded aging contract that turns a long-lived `RESEARCHING` signal into one of: resumed research, retryable failure, superseded test fixture, explicit abstention, consolidated learning, or retired diagnostic. A healthy heartbeat can therefore continue reporting an old `RESEARCHING` item without making the queue state more informative.

This is not a blocker and does not invalidate the sensory repair. It is a lifecycle/observability gap under the already-triggerable robustness work in `RQ-001`.

Preferred future contract when dependency-safe:

`CLAIMED/RESEARCHING → progress evidence OR bounded retry → CONSOLIDATED / ABSTAINED / FAILED_RETRYABLE / SUPERSEDED_TEST / RETIRED_DIAGNOSTIC`

with explicit timestamps/reasons and no automatic claim that a timed-out item was learned.

### 4. Diagnostic/test prompts should be distinguishable from organic learning signals

At least one current active item is explicitly a memory-test prompt (`初光金`), and another is a synthetic one-sentence conversation behavior probe. Their presence in the same active list as organic Scripture/search signals is useful for diagnostics but weakens interpretation of the queue unless source/class metadata distinguishes test fixtures from real reader/product stimuli.

A future robustness pass should preserve diagnostic value while adding a signal class/source field or equivalent provenance so test fixtures cannot be mistaken for organic learning demand.

### 5. Classification

- Reflex Consolidation 1.0: `VERIFIED_COMPLETE`, retain closed.
- Sensory repair / D1 reconciliation milestone: `VERIFIED_COMPLETE`, retain closed.
- Rolling heartbeat/probe evidence persistence: `MAINTENANCE` with existing Git-churn revisit debt.
- Active-signal aging / terminal lifecycle semantics: `COMPLETED_REVISIT_CANDIDATE` under `RQ-001` as an implementation-quality gap of the completed sensory milestone.
- Test-vs-organic signal provenance: `COMPLETED_REVISIT_CANDIDATE` under `RQ-001`.
- Broad heterogeneous-signal learning quality: `UNKNOWN_NEEDS_EVIDENCE` / `ME-001`.

## Revisit trigger

Do not interrupt P01. Revisit when sensory robustness work is dependency-safe, Nervous System observability is being formalized, or stale active items begin obscuring real reader/product learning signals.

The revisit should add lifecycle aging/terminal-state evidence and signal-class provenance, then verify that no legitimate in-flight research is silently dropped and no test fixture is promoted into durable learning without evidence.

## P01 boundary

No P01 runtime, deployment, audio/transcription dependency, credential, binding, ordering, blocker or resume state was changed.

## Sweep disposition

This batch adds a bounded maintenance/revisit finding and accounts for the current reflex/sensory active-state family. Sweep 01 remains `ACTIVE_PARALLEL`; no new `HUMAN_DECISION_BLOCKED` or `ENVIRONMENT_BLOCKED` condition is established.