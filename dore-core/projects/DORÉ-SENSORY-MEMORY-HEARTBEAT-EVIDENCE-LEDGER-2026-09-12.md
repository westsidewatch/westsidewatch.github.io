# DORÉ SENSORY MEMORY / HEARTBEAT EVIDENCE LEDGER — 2026-09-12

Status: ACTIVE / BOUNDED EVIDENCE
Sweep: `MEM-SWEEP-01`
P01 constraint: no subtitle runtime, blocker, ordering, binding or resume condition was modified.

## Evidence reviewed

- `dore-core/memory/sensory-active.json`;
- `dore-core/memory/sensory-seed-diagnostic.json`;
- `dore-core/memory/sensory-heartbeat-diagnostic.json`;
- `dore-core/memory/sensory-claim-step-diagnostic.json`;
- `dore-core/memory/actions-probe-diagnostic.json`;
- persisted heartbeat commit `92113c7ec8e1c03b7d1713db8067de83e94637cf`;
- persisted Actions probe evidence associated with run `34695645542` and SHA `2fd77985f40941a636aa8fc5d119bd0d1b85da78`.

## Bounded findings

1. The sensory-memory path has real repeated production heartbeat evidence. The latest persisted heartbeat successfully reached the Pages production base, reconciled one already-consolidated signal, and completed its claim step without error.
2. Deduplication is active for the consolidated `馬利亞有幾位?` signal: repeated seeding returns the same signal identity/state and increments observed/heard evidence rather than creating a duplicate work item.
3. `sensory-active.json` is not a globally complete memory state. At the reviewed snapshot it contains four signals: one `CONSOLIDATED` and three still `RESEARCHING`. Therefore repeated heartbeat success must not be promoted into a claim that all sensory signals autonomously progress to terminal consolidation.
4. The heartbeat itself reported `changed: false` for the reviewed Search-conversation signal, while reconciling one consolidated signal. This proves observation/reconciliation continuity, not autonomous research completion for unchanged `RESEARCHING` items.
5. The Actions probe is live and persisted (`ok: true`) for run `34695645542`; this is useful execution-plane observability evidence but does not by itself prove every scheduled/Actions pathway or every downstream capability.
6. The current durable classification is `CORE/CONTINUOUS / ACTIVE` for sensory-memory continuity and observability. The bounded heartbeat/dedupe behavior is verified as a component behavior; terminal research-to-consolidation autonomy across representative signals remains `UNKNOWN_NEEDS_EVIDENCE`.
7. No superseded/retired sensory implementation is justified by this batch. Preserve signal identity/dedupe and heartbeat diagnostics as regression evidence.
8. No new `HUMAN_DECISION_BLOCKED` or `ENVIRONMENT_BLOCKED` condition was discovered.

## Revisit / next proof

The next meaningful proof should not be another identical heartbeat alone. Persist at least one representative currently-`RESEARCHING` signal progressing through claim/research/consolidation to terminal durable memory without human re-brief, while preserving dedupe, provenance and scope; also persist a negative/no-change heartbeat case and a retry/failure case so continuity is not inferred only from success-path probes.

## Canonical-register delta

When the next canonical bookkeeping edit is applied, the Master Register should:

- advance `MEM-SWEEP-01` frontier through the latest standalone checkpoints rather than stopping at Checkpoint 79;
- record the sensory-memory heartbeat/dedupe component as bounded real runtime evidence under `CORE`/`RUNTIME`, without promoting broader `DORÉ_ALIVE_1.0` or autonomous-memory completion;
- preserve P01 as `BLOCKED / ENVIRONMENT_BLOCKED` with its existing approved audio/transcription dependency unchanged.
