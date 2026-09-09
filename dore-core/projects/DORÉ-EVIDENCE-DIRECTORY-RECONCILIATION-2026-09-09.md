# DORÉ EVIDENCE DIRECTORY RECONCILIATION — 2026-09-09

Status: SWEEP-01 BOUNDED EVIDENCE LEDGER
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
P01 impact: NONE

## Scope reviewed

Complete current `dore-core/evidence/` family:

- `PENPOT-BRIDGE-01-LIVE-EVIDENCE-2026-08-26.md`
- `wake-runtime-local-activation-control-20260905.md`
- `wake-runtime-local-activation-request-20260905.json`
- `wake-runtime-local-activation-pass-20260905.json`

## Findings

### 1. Penpot bridge remains a bounded verified milestone

The evidence supports `VERIFIED_COMPLETE` only for the bridge feasibility milestone: runtime secret access, Penpot Remote MCP initialization/tool discovery, live focused-file resolution, one persistent editable write, and independent readback. The same evidence explicitly records a first typography `Text.getRange()` defect and excludes Visual Constitution completion, visual quality, responsive/print transfer, and finished Westside visual grammar from the completion claim.

**Classification:** bridge milestone `VERIFIED_COMPLETE`; broader `VIS-GRAMMAR` remains `ACTIVE_PARALLEL / BUILDING`.

**Revisit rule:** reopen bridge feasibility only on regression evidence. Future visual work should use small idempotent writes plus readback/export inspection rather than treating successful connection as design-quality proof.

### 2. Wake runtime local activation has current behavioral PASS evidence

The control file explicitly says it is not acceptance evidence and requires three behavioral facts: launchd loaded, durable SQLite state present, and wake-triggered smoke probe passed. The persisted PASS record supplies all three and binds PASS to a concrete current smoke task. It records:

- launchd label `gui/501/org.westsidewatch.dore.wake` loaded;
- plist present;
- 900-second run interval;
- queue directories enabled;
- durable SQLite state present at `~/Library/Application Support/Dore/wake-state.sqlite3`;
- current smoke task `bfaa918c-da37-4202-bf65-226c5a123ef4` reached `passed` in one attempt with return code 0;
- kickstart return code 0;
- wake log processed 1 / passed 1 / failed-or-retry 0 / empty stderr.

The acceptance note is especially important provenance: the current PASS supersedes both an earlier failed v1 activation and a v2 false-positive acceptance defect. Earlier activation attempts must therefore not be allowed to reactivate a blocker or be mistaken for current truth.

**Classification:** local wake-runtime activation milestone `VERIFIED_COMPLETE`; wake/runtime capability itself remains maintenance/continuous infrastructure, not global autonomy evidence.

### 3. Request/control provenance is weaker than terminal acceptance and must not override it

The request artifact remains `status=requested` and the control artifact explicitly denies acceptance status. They are valid provenance for the acceptance contract, not current runtime-state authority. The later task-bound PASS record governs the bounded activation milestone.

**Classification:** request/control artifacts `HISTORICAL / RETAINED`; earlier failed/false-positive activation interpretations `SUPERSEDED` by the task-bound PASS.

### 4. Canonical register interpretation is already materially correct

The Master Work Register already names the wake-runtime local activation milestone and Penpot bridge as bounded evidence while refusing to inflate either into broad autonomy or visual-grammar completion. No status promotion/demotion is warranted from this batch. The useful Sweep action is therefore explicit source-family accounting plus preservation of the wake supersession chain.

## Durable capability retention

- execute an authenticated remote design write against a persistent external design surface and independently read it back;
- distinguish connectivity/bridge proof from visual-quality proof;
- define behavioral activation acceptance before execution;
- bind PASS to the current smoke/task identifier so stale prior tasks cannot satisfy the gate;
- preserve failed and false-positive attempts as superseded provenance rather than current blockers.

## Missing evidence / open debt

- Penpot D4 rendered visual readback/correction and full Search→design-memory→execution→visual-verification remain separate open evidence under `VIS-GRAMMAR` / `ME-015`.
- Wake local activation does not prove cross-machine deployment, broad job classes, long-horizon reliability, or system-wide autonomous operation; those require independent contracts/evidence if later claimed.

## Canonical effect

No P01 state changed. No new human/environment blocker was found. No canonical workstream status change is justified; this ledger makes the current evidence hierarchy and supersession interpretation durable for Sweep 01.
