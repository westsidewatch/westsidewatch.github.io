# DORÉ DAWN LIBRARY AUTONOMOUS GROWTH — EVIDENCE LEDGER — 2026-09-10

Status: ACTIVE / EVIDENCE-BOUNDARY LEDGER
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical map: `DORÉ-MASTER-WORK-REGISTER.md`
P01 impact: NONE

## Bounded evidence

Latest persisted autonomous bilingual library-growth evidence reviewed from commit `de776d77ccd3a21f491470988a59d060c70ee5ec` (`chore(dawn): persist autonomous bilingual library growth [skip ci]`).

Observed current bounded state:

- English / Project Gutenberg discovery: candidate queue moved from 117 to 121 with 4 newly discovered candidates.
- English relevance: 5 qualified, 17 deferred, 99 rejected.
- Chinese / Wikisource discovery: candidate queue moved from 202 to 201.
- Chinese relevance: 18 qualified, 91 deferred, 92 rejected.
- Chinese resolver: 5 verified, 4 needs-review, 9 blocked.
- Published library count remained 10 in the persisted loop report.
- Discovery reports preserve the invariant that discovery is metadata-only and does not auto-download full text or auto-promote candidates.
- Relevance reports preserve the invariant that search hit ≠ relevance ≠ verification ≠ curation.

## Reconciliation judgment

1. The autonomous library-growth loop is operational and continues producing persisted bilingual discovery/relevance/resolution evidence.
2. This run is not a new publication-completion milestone: published count remained 10, so candidate churn must not be represented as reader-facing catalog growth.
3. The current Chinese discovery surface still produces obvious lexical false positives. One newly persisted candidate matched by `search:教會` is `司法院院字第1164號解釋`, a judicial interpretation rather than a biblical-world/library work. The layered relevance/resolution gates prevented this from becoming evidence of curation success, but the discovery precision issue is real quality debt.
4. The strongest positive evidence is governance behavior: unverified discovery remains metadata-only; qualified/rejected/deferred distinctions are persisted; resolver states remain explicit; no automatic public promotion is implied by a search hit.
5. Current classification: autonomous bilingual discovery loop = `ACTIVE_PARALLEL / OPERATIONAL`; public catalog growth = `MAINTENANCE / NO_NEW_MILESTONE_IN_THIS_RUN`; Chinese lexical discovery precision = `COMPLETED_REVISIT_CANDIDATE / SEARCH-QUALITY-DEBT`.
6. No human decision or environment blocker is introduced. No P01 ordering/runtime/deployment/audio/transcription state is changed.

## Revisit trigger

Reopen discovery-query quality when any of the following occurs:

- false-positive rate materially increases;
- deferred/rejected queues grow faster than useful qualified candidates;
- repeated obvious non-biblical/legal/administrative results recur from ministry terms;
- candidate-processing cost or review burden becomes material;
- a new Search/relevance capability can improve precision without sacrificing recall.

## Smallest next proof

Add one bounded Chinese negative-relevance regression set covering ministry terms such as `教會`, `福音`, `聖經` against obvious legal/administrative false positives, then persist before/after candidate classification results without weakening the no-auto-promotion invariant.
