# Doré Cloudflare Structured Runtime Evidence Ledger — 2026-08-26

Status: DURABLE SWEEP-01 EVIDENCE
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Primary index: `DORÉ-MASTER-WORK-REGISTER.md`

## Purpose

Preserve the bounded Cloudflare structured-data placement and Doré Search runtime-consolidation evidence reviewed during Memory Consolidation Sweep 01, while keeping current Search quality and P01 execution claims separate.

## 1. Structured-data runtime placement audit

Source: `dore-core/cloudflare/STRUCTURED-DATA-RUNTIME-AUDIT-2026-08-24.md`

**Classification:** `VERIFIED_COMPLETE` for the bounded placement/governance audit.

The audit explicitly passed after deciding not to move the active deterministic browser indexes merely because they are large. The governing placement remains:

- GitHub + deterministic generators → versioned browser indexes on Pages → Doré browser Search;
- D1 → mutable/queryable registry and operational state;
- R2 → independently addressable binary/content objects.

The declared hot-path browser indexes included `search-index.json`, `original-index.json` and `entity-index.json`; their placement decision was to keep them on Pages rather than misuse R2 or D1 as generic blob storage.

**Current-quality judgment:** strong for the declared architectural decision. The milestone proves a deliberate storage/runtime boundary, not that Search itself is product-complete or that later structured datasets can never move.

**Retained capability:** choose storage by access/mutation semantics rather than file size; protect a working public runtime from aesthetic infrastructure migration.

**Revisit trigger:** material Search delivery redesign, repository-size pressure, changed browser-index generation strategy, or a service architecture that demonstrably improves reliability/performance without weakening regression protection.

## 2. Search runtime consolidation

Source: `dore-core/cloudflare/SEARCH-RUNTIME-CONSOLIDATION-2026-08-24.md`
Implementation evidence: commit `2426bbd64c9d87e2b69448c3e27dd80d8cd0e367` (`feat(dore): consolidate production search runtime`).
Current-code evidence:

- `static/dore/dore-search-runtime.js` still exposes the shared `dore:search-query` lifecycle and binds submit observation once;
- `static/dore/dore-entity-search.js` still subscribes to `dore:search-query` and treats entity identity context as additive rather than replacing Scripture Search;
- current `static/dore/search/index.html` still loads the runtime before the existing search routers/engine and loads entity search as a runtime subscriber afterward.

**Classification:** `VERIFIED_COMPLETE` for the bounded browser lifecycle/compatibility milestone.

The consolidation created one supplemental extension boundary without rewriting the proven Scripture engine. Existing reference, range, chapter, multi-reference, fuzzy/exact, original-language, chapter-reading, Brain/status/asset and graceful-degradation paths were intentionally preserved.

**Current-quality judgment:** the shared lifecycle remains materially current because its implementation and script ordering are still active in the product. This is stronger evidence than a historical PASS memo alone.

**Retained capability:** extend a working product through a stable compatibility event rather than accumulating independent submit hooks or replacing the core engine prematurely.

**Weakness/debt:** the milestone does not prove semantic intent understanding, universal relevance calibration, or product-level Search cognition. Current real-use Search false-positive/false-negative evidence and the still-TAUGHT cognition gate remain governed separately by `SEARCH` and its revisit/evaluation work.

**Revisit trigger:** browser/service boundary replacement, event-contract changes, entity-routing regressions, or a future server-side search path that is ready to prove equivalence against the protected browser behavior.

## 3. Service-layer chronology boundary

`dore-core/cloudflare/DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md` and current `functions/api/dore/query.js` confirm that `dore.query.v1` followed the shared runtime milestone and remains implemented. That bounded Service Layer v1 completion was already reconciled by Sweep Checkpoint 16 and is not duplicated here as a new completed-work claim.

The current service still declares Scripture as a protected/delegated browser-search lane while Brain, Asset and Status have explicit service behavior. This corroborates the historical non-destructive sequencing decision.

## 4. Historical next-step language

The August 24 Cloudflare milestone documents contain chronological `next milestone` statements such as:

`Structured Data Runtime Audit → Search Runtime Consolidation → Doré Service Layer → first external worker`.

These statements are useful product history, but their sequencing authority is now **satisfied/superseded** by the later completed milestones and the canonical Master Work Register. They must not reactivate an old infrastructure sequence ahead of the current P01 critical path.

Classification of the documents themselves: retained historical evidence, not retired. Classification of their old `next milestone` instructions as current priority authority: `SUPERSEDED`.

## 5. Current operational boundary

No top-level Master Work Register status change is required from this evidence family:

- `SEARCH` remains `MAINTENANCE + DISCOVERY`, not `VERIFIED_COMPLETE`;
- current Search relevance/cognition gaps remain open independently of the historical runtime milestones;
- the Cloudflare structured-runtime milestones are reusable infrastructure history rather than a new active workstream;
- P01 remains the active critical path and was not modified by this reconciliation.

## Completed-work reconciliation candidate

A later safe completed-ledger reconciliation may add a concise entry for the **Search structured-data placement + shared runtime consolidation** milestone family, provided it preserves the boundary that runtime architecture completion is not Search product/cognition completion.

## Sweep conclusion for this evidence family

The structured-data placement audit and shared Search runtime consolidation are both defensible historical `VERIFIED_COMPLETE` bounded milestones whose architecture remains materially visible in current code. Their old sequential `next milestone` language is no longer current priority authority. No new human or environment blocker was discovered in this evidence family.

## Sweep 01 reconciliation note — 2026-08-29

A later Sweep checkpoint (Checkpoint 25, Journal/Liming media placement) incorrectly stated that no evidence of the named structured data-runtime audit had been found in that bounded pass. That statement is superseded by this durable ledger and the underlying `STRUCTURED-DATA-RUNTIME-AUDIT-2026-08-24.md`, which already establish the bounded audit as `VERIFIED_COMPLETE`.

The corrected interpretation is:

- Journal/Liming binary-media zero-migration remains independently `VERIFIED_COMPLETE` for its own bounded placement question;
- the Search/corpus structured-data runtime audit is **not missing** as a historical architecture milestone; its 2026-08-24 placement/governance decision is `VERIFIED_COMPLETE`;
- this does **not** mean future structured datasets can never move, and it does not make Search product/cognition complete;
- any future revisit is triggered by materially changed access patterns, delivery architecture, repository pressure, or measurable reliability/performance benefit—not by an unresolved historical audit claim;
- no P01 state, dependency, priority, deployment, binding or credential was modified by this reconciliation.

## Sweep 01 bounded revalidation — 2026-08-30

This run re-read the canonical Sweep file through Checkpoint 25 and the current Master Work Register, then revalidated this ledger against the contradiction introduced in Checkpoint 25.

**Classification and evidence judgment**

1. `STRUCTURED-DATA-RUNTIME-AUDIT-2026-08-24.md`: retain `VERIFIED_COMPLETE` for the bounded storage/governance decision.
2. `SEARCH-RUNTIME-CONSOLIDATION-2026-08-24.md`: retain `VERIFIED_COMPLETE` for the bounded shared browser lifecycle/compatibility milestone.
3. Historical Cloudflare `next milestone` sequencing: retain as provenance, but current priority authority is `SUPERSEDED` by later milestones and the Master Work Register.
4. The Checkpoint 25 sentence that the structured data-runtime audit was not found is itself superseded evidence, not a new missing-evidence item.
5. No top-level Master Work Register status change is warranted: its current Cloudflare/service-placement interpretation is already compatible with this corrected evidence boundary, and `SEARCH` correctly remains `MAINTENANCE + DISCOVERY`.

**Completed-work evaluation**

- Original objective: prevent storage-fashion migrations and add a single extension-compatible browser Search lifecycle without replacing the proven Scripture engine.
- Completion evidence: explicit PASS audit, implementing commit, and current runtime/script-order evidence retained in this ledger.
- Current quality: still strong for the bounded architecture; deliberately insufficient for Search cognition/product-complete claims.
- Retained capability: select storage by semantics/access pattern; extend proven runtimes through stable compatibility boundaries.
- Debt: browser/Core search-intelligence parity and semantic intent/relevance remain separate open work already governed under Search.
- Revisit trigger: material delivery architecture change, repository pressure, event-contract regression, or measurable reliability/performance gain from a new service boundary.
- Current disposition: keep both bounded milestones closed; do not reactivate the old Cloudflare sequence; do not create a false missing-evidence blocker.

No P01 subtitle critical-path state, deployment, credential, binding, ordering or blocker was modified in this bounded pass.
