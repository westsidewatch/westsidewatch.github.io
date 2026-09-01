# DORÉ SENSORY RESEARCH LIFECYCLE EVIDENCE LEDGER — 2026-09-01

Status: SWEEP-01 BOUNDED EVIDENCE / MAINTENANCE FINDING
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`
Related: `CORE`, `MEM-SWEEP-01`, `CW-001`, `RQ-001`, `ME-001`, `ME-008`

## Scope reviewed

This bounded pass reviewed the current sensory research-lifecycle evidence without changing the active P01 subtitle critical path:

- `dore-core/memory/sensory-active.json`;
- `dore-core/memory/sensory-heartbeat-diagnostic.json`;
- `dore-core/memory/sensory-claim-step-diagnostic.json`;
- `dore-core/memory/actions-probe-diagnostic.json`;
- the existing sensory persistence/revisit interpretation in `DORÉ-SENSORY-DIAGNOSTIC-PERSISTENCE-EVIDENCE-LEDGER-2026-08-31.md`, `RQ-001`, `ME-001` and `ME-008`.

## Evidence observed

### 1. Historical consolidation milestone remains valid

`sensory-active.json` still contains the earlier real signal `馬利亞有幾位?` in `CONSOLIDATED` state with a durable `brain_node` (`research.nt.mary-count`) and consolidation timestamp. Nothing in this batch contradicts the already verified sensory-loop repair/consolidation milestone.

### 2. Multiple later signals remain in `RESEARCHING` without durable completion evidence

The current active-memory snapshot contains three later signals still recorded as `RESEARCHING`, each with `brain_node: null`:

1. `你好,多雷。請用一句話說明你在搜索頁面裡如何與我對話。` — claimed 2026-08-28T01:30:18.670Z;
2. `耶和華啊,我終日等候你` — claimed 2026-08-28T21:54:09.540Z;
3. `多雷,請記住今天的測試詞是「初光金」。請只回答:我已記住初光金。` — claimed 2026-08-28T22:01:08.999Z.

As of the 2026-09-01 diagnostic pass, none of these three entries has a persisted consolidation timestamp or linked brain node in `sensory-active.json`.

### 3. Transport/claim observability is healthy, but it does not prove research-lifecycle completion

The current heartbeat diagnostic is `ok: true` and continues to read a `RESEARCHING` signal successfully. The current claim-step diagnostic records `outcome: success` with HTTP 200, and the Actions probe is also `ok: true` with a fresh 2026-09-01 run id/timestamp.

Therefore this evidence does **not** support an `ENVIRONMENT_BLOCKED` classification for the sensory system. The deployed probe/claim/heartbeat path is alive. What remains unproven is the downstream lifecycle from claimed `RESEARCHING` state to durable research result / consolidation / explicit terminal failure or expiry.

### 4. Current diagnostics are biased toward liveness rather than lifecycle closure

The heartbeat currently reports one `RESEARCHING` signal with `changed: false` and a stale underlying signal `updated_at` from 2026-08-28 while the diagnostic itself refreshes on 2026-09-01. This makes an important distinction visible:

- the diagnostic workflow itself is continuously alive;
- the underlying research item can remain unchanged for days;
- a green heartbeat must not be interpreted as evidence that the research task is progressing or will terminate.

This complements, rather than replaces, the 2026-08-31 finding about high-frequency diagnostic commit churn.

## Classification

- sensory transport / claim / heartbeat observability: retain `CORE/CONTINUOUS` and the bounded historical repair milestone as `VERIFIED_COMPLETE`;
- current unresolved `RESEARCHING` items: `ACTIVE / UNKNOWN_NEEDS_EVIDENCE` at the individual lifecycle level;
- research-lifecycle timeout / retry / terminal-state semantics: `MAINTENANCE / UNKNOWN_NEEDS_EVIDENCE`;
- broad sensory robustness remains governed by `ME-001` / `RQ-001`;
- public product expression of real `QUEUED` / `RESEARCHING` states remains governed by `ME-008`.

No current evidence warrants calling these items `BLOCKED`, `FAILED`, `CONSOLIDATED`, or `VERIFIED_COMPLETE`.

## Quality judgment

The system is stronger than a simple broken-loop diagnosis: it can durably claim signals, expose live state and preserve at least one real consolidated result. The current weakness is lifecycle accountability. Long-lived `RESEARCHING` states can coexist with continuously green diagnostics without a durable reason code, retry count, lease/timeout policy, terminal failure state, or consolidation proof.

That is an observability/state-machine debt, not a reason to invalidate the original repair milestone.

## Revisit trigger / smallest useful future evidence

Do not interrupt P01 for this maintenance item. When dependency-safe, the smallest useful proof is a bounded lifecycle fixture covering at least:

1. claimed → researching → consolidated;
2. claimed/researching → retry with persisted attempt count;
3. researching → explicit terminal failure/abstention/expiry with reason;
4. stale lease recovery without duplicate research execution;
5. multiple simultaneous signals so one continuously selected heartbeat item cannot hide stranded peers.

Persist per-signal timestamps/state transitions and verify that a green heartbeat is reported separately from research-progress/closure status.

## Canonical-register disposition

The current Master Register classification does not require a status change from this batch: it already treats sensory memory as continuous core work, the historical repair as closed, later `RESEARCHING` evidence as in-flight rather than complete/blocked, and diagnostic persistence as maintenance/revisit debt. This ledger sharpens the evidence boundary: **liveness is not lifecycle closure**.

## P01 isolation

No P01 code, runtime state, deployment, binding, credential, job ordering, blocker state or resume state was modified. The existing approved production audio-acquisition/transcription environment dependency remains the governing P01 blocker.

## Sweep disposition

This source-family batch is now durably accounted for. It adds a lifecycle-maintenance finding but does not justify `MEM-SWEEP-01 = VERIFIED_COMPLETE` and does not create a new human/environment blocker.