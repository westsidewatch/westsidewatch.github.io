# DORÉ MEMORY SWEEP — CHECKPOINT 18

Status: PARTIAL / CONTINUE
Date: 2026-08-26
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Primary index: `DORÉ-MASTER-WORK-REGISTER.md`
Previous checkpoint: `DORÉ-MEMORY-SWEEP-CHECKPOINT-17.md`

## Bounded batch — Join product history + Priority-B site-media cutover

Reviewed:
- `join/index.html`
- commit history for `join/index.html`
- commit `0d9554d04bcce49face5283707b9e7bac244d04e` (`feat(dore): complete Priority B site media R2 cutover`)
- current `DORÉ-MASTER-WORK-REGISTER.md`
- Checkpoint 17 next-batch instruction

## Findings and classifications

1. **Join is a live utility/community surface, not an unfinished blank product.** The current page exposes church gathering information, WeChat join QR, Zoom details, contacts, church identity, and explicit DORÉ / ONE / WESTSIDE navigation. Its governing workstream remains `MAINTENANCE`, not `READY` or `DISCOVERY`.

2. **Join gained a direct Doré encounter path in two bounded steps.** Commit `f67da9dec06f5f15dc39778d1092fd575d419bbe` surfaced Doré Search, ONE and main-site entrances; commit `34086ad6c6d5c6f65c64a287a80f29756a4ecc38` added an inline Doré search box. The current page still contains both the portal navigation and `data-dore-search-entry` form using `/dore/dore-search-entry.js?v=20260824a`. This is a legitimate product-history milestone: Join evolved from a church-access card into a cross-product doorway without ceasing to be a utility page.

3. **Priority-B site media private-R2 cutover is a defensible bounded infrastructure milestone.** Commit `0d9554d04bcce49face5283707b9e7bac244d04e` records `status=PASS`, `asset_count=5`, `runtime_cutover=registry-private-r2`, `github_binaries_removed=5`, and `r2_delivery_verified=5`. The diff cuts active site references from local binaries to `/api/dore/assets/site-file?code=...` for the site background, Damascus Gate, Jerusalem wall, temple-stone texture and WeChat QR while explicitly retaining brand SVGs in GitHub and leaving canonical Doré 241 untouched.

4. **Join is direct current-code evidence that the Priority-B cutover remains active.** Its background resolves through `SITE-BACKGROUND`, and its WeChat QR through `SITE-WECHAT-QR`. This supports treating the cutover as historical `VERIFIED_COMPLETE` for the five declared assets while keeping the asset service itself under maintenance/continuous infrastructure stewardship.

5. **The cutover must not be inflated into a Join redesign milestone.** The current page still uses its compact centered card, gold-overlay photographic background, double border, and earlier portal/footer treatment. No evidence in this batch shows a completed application of the later Visual Grammar / Brand V1 work. Join therefore remains `MAINTENANCE`, with later proven grammar as a future enrichment dependency rather than an active redesign claim.

6. **The direct-search/portal additions belong to Join rather than new permanent workstreams.** They should be consolidated into the canonical JOIN product-history entry and not duplicated as separate active projects.

## Historical milestone dispositions

- Join DORÉ/ONE/main portal exposure: `VERIFIED_COMPLETE` as a bounded navigation milestone; ongoing cross-product information architecture remains maintenance.
- Join direct Doré inline-search entry: `VERIFIED_COMPLETE` as a bounded encounter-path milestone; Search quality itself remains governed by SEARCH.
- Priority-B five-asset site-media R2 cutover: `VERIFIED_COMPLETE` as a bounded infrastructure/runtime-placement milestone; asset service maintenance remains continuous.
- Join full visual redesign / Brand V1 propagation: **not completed in this evidence batch**; keep future-facing and dependency-gated.

## Current quality judgment

Join is functionally coherent for its church/community access purpose and now has stronger ecosystem continuity than its earlier state because Search, ONE and the main site are directly reachable. The strongest recent engineering improvement is invisible infrastructure: site-critical binary media no longer depend on active GitHub binary paths for the five migrated assets.

The visual system is intentionally not judged `VERIFIED_COMPLETE` against the newer Westside visual-language work. Its compact bordered-card composition and heavy gold-overlay background may later become a `COMPLETED_REVISIT_CANDIDATE` only when Visual Grammar / Brand V1 has been independently proven and a real same-content redesign can demonstrate material improvement without harming utility.

## Durable learning retained

- Product utility completion, cross-product navigation completion, media-storage migration completion and visual-system completion are separate claims.
- A maintenance surface can accumulate verified bounded milestones without changing its top-level classification to ACTIVE.
- Cross-product doorway work should be consolidated into the owning product row rather than duplicated as a new project.
- Storage migration evidence is strongest when the current product still resolves through the new delivery contract, not merely when an old migration report says PASS.
- Visual redesign should be dependency-gated by proven grammar; do not reopen a functioning utility page merely because newer design research exists.

## Canonical-register correction required

JOIN should remain `MAINTENANCE`, but its current-position text should acknowledge:
- current DORÉ / ONE / WESTSIDE portal navigation;
- current inline Doré Search entry;
- verified Priority-B R2 delivery for its background and WeChat QR as part of the five-asset site-media cutover;
- later visual-language propagation remains future work, not a completed claim.

MEM-SWEEP-01 should record that Join product history / Priority-B site-media evidence has now been reconciled.

## Completed-work ledger candidate

Create a concise completed-work entry for the **Priority-B five-asset site-media private-R2 cutover** on the next safe completed-ledger reconciliation. It should remain separate from `CW-011` (Priority-A ONE media) because the asset sets, product scope and placement evidence differ.

## Next bounded batch

Continue concrete Main or WSS product-history evidence. Prefer WSS if an accessible canonical repository/integration record can be located; otherwise reconcile Main/Journal surface history and its relationship to the verified Priority-B site-media cutover.

Do not interrupt or replace P01.