# DORÉ MEMORY SWEEP 01 — CHECKPOINT 80 — 2026-09-12

Status: COMPLETE / BOUNDED BATCH
Sweep: `MEM-SWEEP-01`
Critical-path constraint: P01 subtitle work was not modified, interrupted or reprioritized.

## Evidence family reviewed

Doré sensory-memory / Product→Brain closed-loop history and current runtime evidence:

- `functions/api/dore/sensory.js` and its first-party D1 capture/dedupe history;
- Search unknown-input bridge commit `44e116f977aa079b56cdb3fe27b599606271c69b`;
- `scripts/dore/sensory-heartbeat.mjs` and current protected claim/reconciliation behavior;
- current `dore-core/memory/sensory-*.json` diagnostics/state;
- `.github/workflows/dore-sensory-bootstrap.yml`;
- `.github/workflows/dore-sensory-seed-test.yml`;
- `.github/workflows/dore-sensory-heartbeat.yml`;
- `.github/workflows/dore-live-sensory-consolidate.yml`;
- historical retirement commit `45f7c96afd0450ec7101b2ec6ad8706cc93fec60`.

## Reconciliation result

A durable first-party sensory substrate is real: D1 capture/deduplication, Search intake, protected heartbeat claim/reconciliation, persisted diagnostics, and one historical Mary signal linked to a consolidated brain node are evidenced.

However, the Mary consolidation cannot be treated as evidence of a generic autonomous research→brain-node loop. The workflow named `Doré Live Sensory Consolidate` explicitly hard-codes the Mary node and directly marks that one signal consolidated. Meanwhile three signals claimed on 2026-08-28 remain `RESEARCHING` with `brain_node=null`, and the latest 2026-09-12 heartbeat reports `changed=false` for the oldest one.

Therefore:

- bounded repair/reconciliation mechanics remain a valid historical completion milestone;
- generic autonomous closed-loop learning remains `UNKNOWN_NEEDS_EVIDENCE`;
- the Mary-specific consolidation workflow is a naming/role `REVISIT_CANDIDATE`, not generic capability proof;
- the unsafe temporary sensory transport is `RETIRED`;
- repeated Mary heartbeat seeding (`heard_count=1289`) is liveness/dedupe evidence, not learning-volume evidence;
- stale `RESEARCHING` signals require an explicit finite retry/failure/escalation policy.

## Durable output

Created:

`dore-core/projects/DORÉ-SENSORY-MEMORY-CLOSED-LOOP-EVIDENCE-LEDGER-2026-09-12.md`

This ledger sharpens the interpretation of existing `CW-001`, `ME-001`, `ME-008`, Search and runtime evidence without deleting the earlier bounded milestone.

## Register disposition

Canonical interpretation to carry forward:

`SENSORY-MEM — ACTIVE / MAINTENANCE + UNKNOWN_NEEDS_EVIDENCE`: capture/dedupe/claim/reconciliation are real; one Mary fixture consolidated; generic autonomous research→brain-node→reader improvement is not yet proved.

No new human/environment blocker was discovered in this batch. Sweep 01 is not yet `VERIFIED_COMPLETE` and continues with the next materially unaccounted evidence family.