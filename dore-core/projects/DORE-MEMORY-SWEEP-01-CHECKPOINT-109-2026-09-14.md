# DORÉ MEMORY SWEEP 01 — CHECKPOINT 109

Date: 2026-09-14
Status: ACTIVE_PARALLEL / BOUNDED RECONCILIATION
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
P01 impact: NONE

## Scope

Reconcile the materially new source-intelligence layer merged after Checkpoint 108, without touching the active P01 subtitle critical path.

## Evidence batch

- merged PR #744 — **Doré Source Capability Envelope v1** (`d82e243012638aaff605c3f5e65a138690193a59`);
- merged PR #745 — **Route Cinema runtime probe through Source Capability Envelope** (`0d0cedb46bec187a8cb6f958f9f5895b105a4c8b`);
- existing Universal Source Probe interpretation through Checkpoint 107/108.

## Classification results

### Source Capability Envelope v1

`VERIFIED_COMPLETE / COMPONENT`.

Verified boundaries:

- `dore.source-capability-envelope.v1` is a request-scoped projection over `dore.source-probe.v0`, not a replacement Probe or second source subsystem;
- source authority is preserved while canonical identity authority is explicitly refused (`identityClaimOnly: true`, `canonicalIdentityAuthority: false`);
- observed/declared access modes are normalized provider-neutrally (`static-http`, `browser-runtime`, `mcp`, `api`, `iiif`, `manifest`, `embed`, `local-file`);
- HTTP 401/403/405/406/429 can become a runtime boundary rather than being interpreted as source absence;
- rights claims remain evidence only; `rehost:false` is preserved and rehost/redistribute still require later rights admission;
- editorial canon remains above publish/material-transform/rehost decisions;
- the capability is registered in the canonical Capability Registry;
- the envelope itself is request-scoped, non-persistent and network-free, and retains the Wikisource hard gate.

The resulting shared chain is now:

`Source Authority → Universal Source Probe → Capability Envelope → Identity/Rights admission → Canonical substrate → Surface`

### Cinema capability-routed runtime fallback

`VERIFIED_COMPLETE / COMPONENT` as the first real consumer.

Verified boundaries:

- Cinema calls Probe first and projects the result through `source.capability-envelope`;
- hidden-browser runtime escalation happens only when `runtimeBoundary.required === true`;
- the earlier product-adjacent routing heuristic based directly on raw `needs.includes('runtime-browser-probe')` is removed;
- the A2A native host exposes `source.capability-envelope`;
- no GOOD TV / YouTube / vendor-specific routing branch is introduced;
- the existing Universal Source Probe CI now asserts capability-routed fallback, and PR #745 received a successful Cloudflare Pages branch deployment.

## Retrospective judgment

This is a strong architectural improvement because products no longer need to reinterpret raw Probe evidence independently. The durable learned principle is:

> **capability before product heuristic** — products should consume one provider-neutral capability projection instead of learning site-specific status codes or duplicating source-intelligence decisions.

## Evidence boundary / remaining debt

This batch does **not** prove:

- broad cross-product adoption beyond Cinema;
- live heterogeneous-source parity for Dawn, Multiwrite, ONE, Design and Search;
- a completed rights-admission executor above the evidence-only envelope;
- production exercise of every declared access mode;
- canonical identity admission or rehosting authority, which are intentionally outside this component.

## Revisit triggers

Reopen if:

1. another product adds raw Probe/vendor-specific routing instead of consuming the envelope;
2. a new source class cannot be represented without provider branches;
3. rights or identity authority leaks into the envelope;
4. browser fallback cost/reliability requires shared ranking or cost policy.

## Canonical reconciliation delta

The Master Register's source-intelligence interpretation must now treat Universal Source Probe alone as incomplete history: the family has advanced to a verified request-scoped Capability Envelope with Cinema as the first real capability-routed consumer. `MEM-SWEEP-01` should advance its durable frontier through Checkpoint 109 on the next canonical-register write.

No P01 action or state was modified.
No new `HUMAN_DECISION_BLOCKED` or `ENVIRONMENT_BLOCKED` condition was discovered.
Sweep 01 remains `ACTIVE_PARALLEL`; Sweep-wide `VERIFIED_COMPLETE` is not justified.
