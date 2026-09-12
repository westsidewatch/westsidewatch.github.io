# DORE SERVICE LAYER EVIDENCE LEDGER — 2026-09-12

Status: SWEEP-01 / DURABLE EVIDENCE

## Evidence reviewed
- `dore-core/cloudflare/DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md`
- `functions/api/dore/query.js`

## Finding
The 2026-08-24 service-layer milestone is a legitimate bounded historical completion. The current repository still implements `/api/dore/query` with schema `dore.query.v1`, GET/POST entry paths, routing among Scripture, Brain, Asset and Status, provenance/boundary fields, Brain fallback to Scripture, Asset/Status delegation, and deliberate preservation of the browser Scripture engine.

Current classification: `COMPLETED_REVISIT_CANDIDATE`.

The original compatibility-bridge decision remains valid, but it should not be treated as Doré's final canonical execution boundary. Scripture still delegates to the browser search dataset, while later Sweep evidence already identifies browser/Core Search duplication and parity risk. Brain matching is intentionally compact and heuristic. Repository implementation also does not by itself prove current production availability, latency or reliability.

## Durable learning
- establish stable cross-product contracts before replacing proven engines;
- preserve compatibility while migrating execution boundaries;
- route uncertain Brain questions back to evidence/search instead of inventing answers;
- separate architectural completion from production-quality convergence.

## Revisit trigger
Revisit when Search/service-boundary convergence is scheduled or when another production product materially depends on `/api/dore/query`. Preserve useful `dore.query.v1` compatibility while converging Search/Scripture on one canonical execution/specification boundary and adding parity plus production contract/readback evidence.

Disposition: keep the historical milestone closed and place the service layer on the completed-work revisit watchlist. This does not change P01 state, priority or blocker handling.
