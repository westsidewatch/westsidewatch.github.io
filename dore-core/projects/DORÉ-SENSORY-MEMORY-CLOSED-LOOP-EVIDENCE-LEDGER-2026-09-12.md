# DORÉ SENSORY MEMORY / CLOSED-LOOP EVIDENCE LEDGER — 2026-09-12

Status: ACTIVE / SWEEP-01 EVIDENCE
Primary register: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`
Related: `CW-001`, `ME-001`, `ME-008`, `SEARCH`, `RUNTIME`, `CORE`

## Bounded question

What is actually proved today about Doré's first-party sensory-memory loop from unknown Search input through durable research/consolidation, and which older claims must remain bounded?

## Verified substrate

1. **First-party durable capture exists.** `functions/api/dore/sensory.js` writes normalized unknown queries to the `DORE_SENSORY` D1 binding, fingerprints them with SHA-256, deduplicates repeated inputs and increments `heard_count` instead of creating duplicate signals.
2. **Search has a real Product→Brain intake bridge.** Commit `44e116f977aa079b56cdb3fe27b599606271c69b` wired unmatched non-Scripture Search input to `/api/dore/sensory`, exposed live state in the reader surface, and polls for a later `CONSOLIDATED` signal/brain-node result. This is stronger than the older architecture state in which Product→Brain had no writable ingestion path.
3. **Protected heartbeat transport exists.** `scripts/dore/sensory-heartbeat.mjs` requires `DORE_HEARTBEAT_TOKEN`, talks to protected `/api/dore/sensory-admin`, reconciles already-linked consolidated nodes, and claims at most one new signal as `RESEARCHING` per heartbeat.
4. **Current production diagnostics are live.** At `2026-09-12T01:36:24Z`, the seed diagnostic returned HTTP 200 with `state=CONSOLIDATED`, `deduplicated=true`, `schema_reconciled=true`, and `heard_count=1289`; the claim diagnostic records success; the heartbeat diagnostic reports `ok=true` against the deployed Pages base.
5. **One historical bounded signal is durably consolidated.** `sensory-active.json` links signal `5cf2c608-e66f-4176-a3f8-b3284819158a` (`馬利亞有幾位?`) to `research.nt.mary-count` with state `CONSOLIDATED`.

## Critical provenance correction

The historical Mary consolidation is **not evidence of a generic autonomous research→brain-node faculty**.

`.github/workflows/dore-live-sensory-consolidate.yml` is a one-off workflow whose Python body explicitly constructs the `research.nt.mary-count` node, its questions, concepts, answer body, Scripture references and provenance, then directly marks the Mary sensory signal `CONSOLIDATED`. It does not consume an arbitrary claimed sensory signal and autonomously produce a new evidence-bearing brain node.

Therefore the defensible interpretation of `CW-001` is narrower:

- **verified:** D1 capture/dedupe, protected claim transport, reconciliation mechanics, one bounded Mary consolidation fixture, and repeat production diagnostic health;
- **not verified:** generic autonomous unknown-input research, generic brain-node creation, broad heterogeneous signal completion, or `DORÉ_CLOSED_LOOP_01_PASS`.

This correction does not invalidate the historical repair milestone; it prevents that bounded fixture from being promoted into a stronger learning claim.

## Current stale-state evidence

`sensory-active.json` currently contains three signals claimed on 2026-08-28 that remain `RESEARCHING` with `brain_node=null`:

- `3973e981-e7e2-4e09-b0ef-6ab22ba1544f` — Search dialogue question;
- `5a7c7590-004c-4903-9e28-d322c42bec90` — Scripture-language query;
- `4a2ab8d9-0bc4-4952-8dc2-ba60a8b09ed8` — memory-test phrase `初光金`.

The latest heartbeat diagnostic still points at the first of these, reports `changed=false`, and shows its state as `RESEARCHING`. This is direct evidence that the transport can keep running while a claimed signal remains unresolved; it is not evidence that the research stage completes.

## Workflow lineage classification

- `.github/workflows/dore-sensory-bootstrap.yml` — **historical/bootstrap diagnostic**, retained; it documents the first-party-only D1 requirement.
- `.github/workflows/dore-sensory-seed-test.yml` — **bounded acceptance fixture**, retained; Mary-specific, not generic capability proof.
- `.github/workflows/dore-sensory-heartbeat.yml` — **ACTIVE / maintenance transport**, currently scheduled every five minutes; it repeatedly seeds the Mary fixture, claims/reconciles state, and persists diagnostics.
- `.github/workflows/dore-live-sensory-consolidate.yml` — **COMPLETED / fixture-specific / REVISIT_CANDIDATE for naming and role clarity**. Its name sounds generic, but implementation is Mary-specific and should not be treated as the autonomous learning executor.
- Commit `45f7c96afd0450ec7101b2ec6ad8706cc93fec60` explicitly retired an unsafe temporary sensory transport — **RETIRED**, superseded by the first-party Cloudflare/D1 path.

## Quality / efficiency judgment

The first-party capture and dedupe layer is useful and lightweight. The main current inefficiency is that the scheduled heartbeat repeatedly posts the same Mary acceptance question; by 2026-09-12 this produced `heard_count=1289`. That is useful as liveness/dedupe evidence, but it is not proportional evidence of learning quality and can obscure whether novel signals progress.

The more important missing behavior is a generic research executor that consumes a claimed signal, produces evidence/provenance under Doré's research gates, creates or updates a product-readable brain node, links that node back to the signal, and lets Search render the improved answer on re-query without query-specific code.

## Current classification

`SENSORY-MEM`: **ACTIVE / MAINTENANCE + UNKNOWN_NEEDS_EVIDENCE**.

Historical repair/consolidation mechanics remain accepted as a bounded completed milestone. Generic autonomous closed-loop learning remains unproven.

## Smallest next proof

Without touching P01, run one fresh unseen non-fixture query through:

`Search unknown input → D1 signal → heartbeat claim → generic evidence-bearing research executor → brain node with provenance/status → signal consolidation → fresh Search re-query renders the node`.

Acceptance must also show a finite stale-state/error policy so a signal cannot remain `RESEARCHING` indefinitely without retry, failure classification or escalation.

Until that proof exists, do not use the Mary fixture, heartbeat liveness, repeated `heard_count`, or workflow names as evidence of generic autonomous learning.