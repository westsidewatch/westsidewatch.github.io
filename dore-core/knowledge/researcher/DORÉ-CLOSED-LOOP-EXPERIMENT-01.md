# Doré Closed-Loop Experiment 01

Status: READY_FOR_D1_BINDING
Date: 2026-08-23

## Goal

Demonstrate a real learning loop from product input to changed product behavior without a per-question UI/code patch and without a human supplying the answer.

## Loop

`Search input → sensory memory → learning/research queue → heartbeat → brain → Search output`

## Acceptance standard

For one unseen test input:
1. First Search has no reliable brain answer.
2. Search truthfully shows `HEARD/UNKNOWN`.
3. The same input is persisted by the first-party Cloudflare endpoint into D1 and becomes `QUEUED`.
4. Doré Heartbeat claims the signal and marks `RESEARCHING`.
5. Doré performs autonomous research/learning with provenance, counter-checks and examination gates.
6. A product-readable brain node is created or materially updated.
7. The sensory signal advances to the corresponding state and eventually to `CONSOLIDATED` only if the gate is passed.
8. Searching the same input again returns a materially improved, traceable Doré expression/answer.
9. No special-case code for the test question is added between first and second Search.
10. No human supplies the answer during the interval.

## Infrastructure prepared

- `functions/api/dore/sensory.js` — public first-party ingestion/status endpoint.
- `functions/api/dore/sensory-admin.js` — protected Heartbeat queue endpoint.
- `cloudflare/d1/001_dore_sensory.sql` — D1 schema.
- `static/dore/dore-brain-bridge.js` — UNKNOWN → POST sensory signal → QUEUED expression; polls signal state; reads updated brain.
- `DORÉ-EXPRESSION-PROTOCOL.md` — truthful expression semantics.

## Cloudflare binding required

Existing Cloudflare Pages preview project should keep GitHub as source. Production remains GitHub Pages.

In the Cloudflare Pages project:
1. Create D1 database, suggested name: `dore-sensory`.
2. Execute `cloudflare/d1/001_dore_sensory.sql` against it.
3. Bind the D1 database to the Pages project as `DORE_SENSORY` for Preview (and Production only when intentionally enabled later).
4. Add a secret environment variable `DORE_HEARTBEAT_TOKEN` for Preview.
5. Redeploy the latest GitHub commit.

Until step 3 is done, `/api/dore/sensory` intentionally returns HTTP 503 `sensory_memory_unbound`; Doré must remain at UNKNOWN and must not claim the question was saved.

## Privacy rule

The sensory database is first-party infrastructure. Do not expose queue enumeration publicly. Public clients can create a signal and query only a signal ID they already received. Heartbeat queue enumeration/state mutation requires the secret bearer token.

## First test question

Do not preselect a question whose answer has already been written into the brain index. At test time choose a normal biblical/research question that has no current reliable Doré node. Record the exact input before first Search; after that, do not alter product code for that query.

## Success milestone

`DORÉ_CLOSED_LOOP_01_PASS`

Passing this milestone means observable product behavior changed as a consequence of Doré's own learning state, not because a developer patched the requested answer.
