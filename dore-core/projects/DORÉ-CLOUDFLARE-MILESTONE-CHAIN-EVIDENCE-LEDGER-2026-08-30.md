# DORÉ CLOUDFLARE MILESTONE CHAIN — EVIDENCE LEDGER

Status: SWEEP-01 BOUNDED RECONCILIATION
Date: 2026-08-30
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`
Sweep: `dore-core/projects/DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`

## Scope

This bounded pass reconciles the 2026-08-24 Cloudflare/storage/search/service milestone chain as historical work rather than treating every document's `next milestone` section as current resume authority.

Evidence reviewed:

- `dore-core/cloudflare/ASSET-MIGRATION-MILESTONE-PLAN-2026-08-24.md`
- `dore-core/cloudflare/R2-DELIVERY-MILESTONE-2026-08-24.md`
- `dore-core/cloudflare/R2-PRIORITY-B-SITE-MEDIA-MILESTONE-2026-08-24.md`
- `dore-core/cloudflare/JOURNAL-LIMING-MEDIA-MILESTONE-2026-08-24.md`
- `dore-core/cloudflare/STRUCTURED-DATA-RUNTIME-AUDIT-2026-08-24.md`
- `dore-core/cloudflare/SEARCH-RUNTIME-CONSOLIDATION-2026-08-24.md`
- `dore-core/cloudflare/DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md`
- current implementation `functions/api/dore/query.js`
- current Master Register Search / ONE / Join interpretations
- Sweep Checkpoint 19 search service-boundary finding

## Reconstructed milestone chain

### 1. Asset Migration closure

**Historical classification:** `VERIFIED_COMPLETE` for the declared placement/migration milestone.

The closure document records Priority A complete, including Batch 001 and Priority ONE media, with 7/7 Priority ONE assets migrated or deduplicated and verified in R2/D1. It explicitly deferred Priority B and public R2-backed delivery to later milestones.

**Current interpretation:** the completion remains valid; the document's `Priority B deferred` and `next milestone` wording is historical provenance, not current work state.

### 2. Private R2 delivery for ONE

**Historical classification:** `VERIFIED_COMPLETE`.

Production acceptance records private R2 delivery through stable `asset_code` + D1 registry lookup, 7/7 byte-hash verification, active ONE reference cutover, zero active GitHub references to rollback binaries, removal only after verification, and 7/7 post-removal re-verification.

**Durable capability retained:** governed binary placement, stable product-facing asset identity, D1 metadata / R2 binary separation, hash-verified cutover, rollback-before-delete discipline.

### 3. Priority B site-media R2 cutover

**Historical classification:** `VERIFIED_COMPLETE`.

Five large site assets were migrated and runtime-cut over through a separate governed site-media route. The milestone explicitly preserves the placement boundary: code/UI/version-coupled brand assets stay in GitHub; R2 is not a universal dumping ground.

**Supersession finding:** Priority B is no longer deferred. Any older inventory or milestone text that still says `PRIORITY B DEFERRED` is superseded as live status by this later PASS.

### 4. Journal + Liming Library media placement audit

**Historical classification:** `VERIFIED_COMPLETE` for the placement audit; not a media-migration project.

The result was intentionally zero migration: current Journal and Liming Library state had no eligible local binary collection requiring R2 movement. YAML/JSON remained in GitHub because they are versioned editorial/source data.

**Durable lesson:** zero-change can be the correct completion outcome when placement policy says not to move data merely because a storage service exists.

### 5. Structured data-runtime audit

**Historical classification:** `VERIFIED_COMPLETE` for placement/governance.

The audit explicitly kept active 10 MB-class browser indexes on Pages and kept research evidence in GitHub, while reserving D1 for mutable/queryable state and R2 for independently addressable binary/content objects.

**Durable lesson:** storage architecture follows access pattern, mutability, build atomicity and runtime risk—not file size alone.

### 6. Search Runtime Consolidation

**Historical classification:** `VERIFIED_COMPLETE` for the declared browser-lifecycle milestone.

A shared `dore:search-query` extension event was introduced without rewriting Scripture Search semantics. Entity integration was moved onto that lifecycle while existing reference/search/router paths were deliberately preserved.

**Current quality judgment:** still useful architecture, but it is a coordination surface rather than proof of one canonical search-intelligence implementation. Sweep Checkpoint 19 later found browser/Core search-intelligence duplication, so this milestone must not be inflated into universal Search-service convergence.

### 7. Doré Service Layer

**Historical classification:** `VERIFIED_COMPLETE` for the bounded service-contract milestone; `COMPLETED_REVISIT_CANDIDATE` for present-day service-boundary convergence quality.

The milestone declared `/api/dore/query` / `dore.query.v1` as a product-neutral contract for scripture, brain, asset and status routing without replacing the proven browser Scripture engine.

Current repository evidence confirms the endpoint implementation still exists at `functions/api/dore/query.js`. It still returns the declared `dore.query.v1` envelope and delegates Scripture to the browser search dataset, assets to the D1 asset service, status to the canonical status snapshot, and Brain to the knowledge index.

However, a current repository code-search request for literal `/api/dore/query` consumers returned zero matches with `incomplete_results=true`; therefore this pass does **not** claim ecosystem-wide live client adoption from that search. More importantly, Sweep Checkpoint 19 already established that browser Search and `dore_core.search.BibleSearchIndex` contain parallel retrieval/intelligence logic. The historical service-layer PASS is therefore preserved, but its broader architectural promise should be revisited when Search boundary convergence becomes high leverage.

## Superseded live-resume statements

The following historical `next milestone` statements are now explicitly non-governing as live resume instructions because later evidence completed them:

1. Asset Migration closure → `Priority B deferred` / R2 delivery next — superseded by R2 Delivery + Priority B PASS.
2. R2 Delivery → `Priority B shared site/UI images` deferred — superseded by Priority B PASS.
3. Priority B → Journal + Liming media audit next — superseded by Journal/Liming PASS.
4. Journal/Liming → structured data-runtime audit next — superseded by Structured Data Runtime Audit PASS.
5. Structured Data Runtime Audit → Search Runtime Consolidation next — superseded by Search Runtime Consolidation PASS.
6. Search Runtime Consolidation → Doré Service Layer next — superseded by Doré Service Layer PASS.

These documents remain valuable provenance and completion evidence; only their forward-looking resume authority is superseded.

## Completed-work evaluation

### Original objective

Establish a safe Cloudflare-backed placement/delivery/service progression without breaking working Bible Search or deleting binaries before governed replacement paths existed.

### Completion evidence

Strong for the bounded milestones: multiple PASS documents record explicit production acceptance, hash verification, reference cutover, placement decisions and non-destructive constraints. Current `functions/api/dore/query.js` also confirms the service-contract implementation remains present.

### Current quality

Strong in placement governance and destructive-change restraint. More mixed in service-boundary convergence: later implementation growth created specialized APIs and parallel Search logic, so `one stable Doré entry contract` should be treated as an available contract rather than assumed universal architecture.

### What was learned

- stable asset identity should be independent of object path;
- D1 metadata and R2 binaries have distinct roles;
- verified delivery must precede deletion;
- GitHub/Pages remains appropriate for deterministic/versioned source and browser snapshots;
- zero-migration audits are legitimate completions;
- working Search should not be rewritten merely to satisfy infrastructure aesthetics;
- shared lifecycle/service boundaries need later parity/adoption proof if they are to become canonical execution boundaries.

### Weaknesses / debt

- historical forward-looking sections can falsely resurrect already-completed work if read without chronology;
- current client adoption of `/api/dore/query` was not established by this bounded pass;
- parallel browser/Core Search intelligence remains an explicit technical-debt/revisit trigger;
- no reason exists to reopen successful R2 cutovers merely because newer architecture exists.

### Revisit trigger

Revisit the service layer when Search work actively consolidates browser/Core retrieval, when a second or third production product needs common intent routing, or when duplicated service-specific routing begins producing measurable parity regressions.

### Disposition

- R2/placement milestones: keep historically closed and maintain regressions.
- Old `next milestone` clauses: classify as `SUPERSEDED` live-resume authority.
- Doré Service Layer: preserve historical PASS; place service-boundary convergence on the existing Search revisit path rather than creating a competing active project.
- P01: untouched.

## Canonical-register implication

The current Master Register statuses remain materially correct:

- `ONE` remains `MAINTENANCE` with its verified Priority-A R2 delivery milestone.
- `JOIN` remains `MAINTENANCE` with verified Priority-B site-media delivery.
- `SEARCH` remains `MAINTENANCE + DISCOVERY`; this evidence strengthens the existing service-boundary revisit rationale but does not justify a status promotion/demotion.
- `MEM-SWEEP-01` remains `ACTIVE_PARALLEL`.

No P01 subtitle state, runtime, deployment or critical-path action was modified in this pass.
