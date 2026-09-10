# DORÉ MEMORY SWEEP 01 — CHECKPOINT 51

Date: 2026-09-10
Status: ACTIVE_PARALLEL
P01 impact: NONE
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
Evidence ledger: `DORÉ-DAWN-LIBRARY-AUTONOMOUS-STOREFRONT-EVIDENCE-LEDGER-2026-09-10.md`

## Bounded evidence reviewed

- commit `b317fb245cb89f2ac9e028f78e80a1762ad939ab` — switch Chinese storefront publication generation to the already verified Chinese catalog;
- commit `918fb28210708ecfa5741bdbce674a47291cb6e5` — correct WS Export's role from presumed Chinese OPDS catalog to on-demand EPUB/PDF publication service;
- commit `6cad3eefe44673e50fc3dc2d928da89f86badc46` — later persisted Dawn autonomous-growth state;
- Checkpoint 50 and the current Dawn Library evidence ledger.

## Reconciliation findings

1. Checkpoint 50's Chinese `verified: 0` state is now superseded by newer persisted evidence. The latest bounded resolver report in commit `6cad3eef...` records 202 Chinese candidates, 19 relevance-qualified, `verified: 5`, `needs-review: 4`, and `blocked: 10`.
2. This is a legitimate first bounded Chinese verification milestone, but not Chinese or bilingual maturity. The proper classification advances from `ACTIVE / UNKNOWN_NEEDS_EVIDENCE` to `ACTIVE_PARALLEL / BOUNDED_PASS_EVIDENCE` for the resolver path only.
3. The WS Export integration was also corrected at the architecture boundary. Chinese Wikisource does not expose the assumed Ready-for-export OPDS path used earlier. The implementation now uses the already rights-verified Chinese catalog as authority and generates WS Export publication links on demand.
4. Therefore WS Export must be treated as a publication/export mechanism, not as source-rights authority or canonical discovery catalog. Rights/provenance remain anchored to the verified Chinese Wikisource edition.
5. The correction is a healthy example of supersession rather than failure: the earlier OPDS assumption is `SUPERSEDED`; the current verified-source → on-demand-export boundary is the governing interpretation.
6. `LIBRARY-INGEST` remains separate and still lacks its authenticated D1 ingest/readback proof. Dawn storefront/catalog progress must not be used to close that milestone.
7. No new human decision or environment dependency was introduced by this batch.
8. No P01 subtitle state, ordering, runtime, credential or blocker action was modified.

## Durable updates

- Updated `DORÉ-DAWN-LIBRARY-AUTONOMOUS-STOREFRONT-EVIDENCE-LEDGER-2026-09-10.md` with the first persisted Chinese verified resolver evidence and corrected WS Export authority boundary.
- The canonical Master Register `DAWN-LIBRARY` row's earlier `verified: 0` wording is now stale relative to this checkpoint and should be reconciled to `5 verified` at the next safe canonical-register write; this checkpoint is the governing newer evidence until that row is rewritten.

## Smallest next proof

1. Production storefront readback.
2. Repeated-loop source identity/dedupe regression.
3. Representative bounded Chinese rights/source audit beyond the first five verified titles.
4. Preserve `LIBRARY-INGEST` as a separate proof obligation.

Sweep 01 remains `ACTIVE_PARALLEL`; this checkpoint does not justify `VERIFIED_COMPLETE` and introduces no genuine `HUMAN_DECISION_BLOCKED` or new `ENVIRONMENT_BLOCKED` condition.
