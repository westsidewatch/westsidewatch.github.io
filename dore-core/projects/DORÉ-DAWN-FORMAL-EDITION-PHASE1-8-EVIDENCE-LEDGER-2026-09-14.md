# DORÉ — DAWN FORMAL EDITION PHASE 1–8 EVIDENCE LEDGER

Status: VERIFIED_COMPLETE / BOUNDED COMPONENT
Date reconciled: 2026-09-14
Sweep: DORÉ MEMORY CONSOLIDATION SWEEP 01
Parent workstream: `DAWN-LIBRARY`

## Classification

`VERIFIED_COMPLETE` for the bounded **Dawn Library Formal Edition Phase 1–8** milestone.

This does **not** promote the whole `DAWN-LIBRARY` workstream to complete. The public catalog/storefront remains `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION` because collection relevance/curation repair, production storefront readback and repeated autonomous-loop identity/dedupe evidence remain open.

## Original objective

Move Dawn Library from an experimental/catalog substrate into a formal edition that can operate against the real canonical catalog, preserve one Dawn-owned Work identity source, support discovery/editorial/personal-state behavior, integrate back into the existing Westside Watch brand/site, and survive a production-equivalent acceptance build without introducing a second runtime authority.

## Strong completion evidence

1. `.github/workflows/dawn-formal-edition-phase8-preflight.yml` defines the final production acceptance gate. It re-runs Phase 4 canonical UI, Phase 5 Editorial World and Phase 6 Personal Dawn gates; enforces the single canonical index and forbidden-runtime-source boundary; performs a production Hugo build; verifies Westside/Dawn static invariants; boots a production-equivalent local site; and executes browser acceptance against both `/dawn-library/` and the formal-edition surface.
2. GitHub Actions run `34727290826`, workflow **Dawn Formal Edition Phase 8 Production Acceptance**, completed on 2026-09-13 UTC with `status=completed` and `conclusion=success` on head `5ceec54484e97db275aa332d35234bb49db94c34`.
3. Commit `3ff2c23a820fe58d197ae5d7bdf41fa35599bdd6` is titled `Dawn Library Formal Edition — Phase 1–8` and explicitly states that it merged the fully accepted Formal Edition after Phase 8 production acceptance run `34727290826` passed all hard gates.
4. The merged implementation includes the Phase 4–7 workflow family and the Phase 8 production-acceptance workflow. Phase 4 itself asserts Dawn canonical identity, a >=10k canonical catalog, bounded 72-item render windows, fuzzy discovery, relation facets, compare state and serialized CollectionContext against the real canonical substrate.

## Current quality judgment

Strong for the declared Formal Edition milestone. This is not a memo-only or branch-only claim: there is a successful terminal production-equivalent workflow followed by an explicit merge to main.

The milestone is narrower than the current total Dawn product. It proves the Formal Edition architecture/integration acceptance at that checkpoint, not that every later catalog item is editorially appropriate, not that current Chinese collection classification is clean, and not that the autonomous storefront loop has proven long-horizon dedupe/readback behavior.

## Durable capability retained

- one Dawn canonical Work identity source across large-catalog discovery;
- bounded rendering over a 10k+ catalog rather than DOM-scale full projection;
- context serialization/restoration for compare/discovery state;
- Editorial World and Personal Dawn gates layered over canonical identity rather than separate book stores;
- single-site Westside brand integration rather than a parallel standalone site;
- production-equivalent Hugo + browser acceptance as the final gate rather than treating component tests as deployment proof;
- explicit forbidden runtime-source checks so discovery/reconciliation sources do not silently become production authority.

## Weaknesses / debt outside the completed milestone

- current `DAWN-LIBRARY` evidence separately proves a Chinese `聖經世界` relevance defect in which modern geopolitical works can be promoted from lexical Israel/Palestine matches; Formal Edition completion does not erase that defect;
- production storefront readback and repeated-loop identity/dedupe proof remain open in the canonical Dawn workstream;
- the milestone proves architecture and integration at its accepted head, not future regression freedom after subsequent changes;
- rights verification and editorial collection fit remain separate judgments.

## Revisit trigger

Reopen the Formal Edition milestone only if a regression breaks canonical identity, large-catalog bounded projection, Editorial/Personal state contracts, brand integration, production build/browser acceptance, or the no-second-runtime-authority boundary.

Do not reopen it merely because Dawn continues to gain books, covers, collections or curation rules. Those belong to ongoing `DAWN-LIBRARY` stewardship.

## Current disposition

Keep **Dawn Library Formal Edition Phase 1–8** closed as a bounded `VERIFIED_COMPLETE` historical milestone and use it as a regression baseline.

Keep `DAWN-LIBRARY` overall `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION` until its independent current open gates are satisfied.

P01 subtitle critical-path state and ordering are unchanged.