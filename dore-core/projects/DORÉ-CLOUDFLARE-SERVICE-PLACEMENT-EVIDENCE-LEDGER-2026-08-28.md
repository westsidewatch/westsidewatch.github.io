# DORÉ CLOUDFLARE SERVICE / PLACEMENT EVIDENCE LEDGER — 2026-08-28

Status: SWEEP-01 BOUNDED EVIDENCE / CURRENT
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`
Sweep source: `dore-core/projects/DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`

## Scope of this bounded pass

Reviewed:

- `dore-core/cloudflare/DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md`;
- live repository implementation `functions/api/dore/query.js`;
- `dore-core/cloudflare/JOURNAL-LIMING-MEDIA-MILESTONE-2026-08-24.md`;
- `dore-core/cloudflare/JOURNAL-LIMING-MEDIA-INVENTORY-2026-08-24.json`;
- current Master Register interpretations for runtime, Search, WSS, ONE, Join, Main, Library ingestion and Sweep 01.

No P01 subtitle-runtime state, deployment, binding, credential, ordering or blocker condition was modified.

## Finding A — Doré product-neutral service contract

### Classification

`VERIFIED_COMPLETE` for the bounded 2026-08-24 service-contract milestone; continuous service evolution remains part of Runtime / product stewardship rather than a permanently frozen endpoint design.

### Original objective

Create one product-neutral Doré query boundary so downstream products can ask Doré through a stable contract rather than importing or reimplementing internal Brain, Asset Registry, status and Scripture routing logic.

### Completion evidence

The milestone memo records `COMPLETE / PASS` and names `/api/dore/query` / `dore.query.v1` as the bounded contract. More importantly, the current repository still contains `functions/api/dore/query.js`, which independently corroborates implementation rather than relying on the memo alone. The function:

- accepts GET `?q=` and POST `{query,type?}`;
- emits schema `dore.query.v1`;
- routes `status`, `asset`, `brain` and `scripture` lanes;
- preserves provenance and an epistemic `boundary` field where available;
- delegates asset queries to `/api/dore/assets/search`;
- reads Brain evidence from `/dore/brain/knowledge-index.json`;
- deliberately delegates Scripture to the proven browser search dataset rather than performing a premature server rewrite;
- falls back from an unmatched Brain question to Scripture instead of inventing an answer;
- explicitly advertises preserved Scripture capabilities: reference, chapter, range, multi-reference, exact text, fuzzy, original-language and entity.

### Current quality judgment

The bounded architectural objective was genuinely reached and remains visible in current code. The strongest design choice is restraint: the service contract unified product routing without pretending that the server already possessed a superior replacement for the mature browser Scripture engine.

The implementation is nonetheless a first-generation routing boundary, not proof of a fully unified Doré cognition/runtime layer. Its classification regexes and Brain matching are deliberately simple; Search still has browser/Core duplication debt recorded elsewhere, and the service endpoint currently delegates Scripture rather than eliminating that split. Therefore the historical milestone should stay closed while future service-boundary convergence remains maintenance/revisit work under existing Search/Runtime lines.

### What was learned / retained

- external products should consume stable Doré contracts rather than internal indexes;
- a stable envelope should carry provenance and epistemic boundaries, not merely answer strings;
- architecture can be improved non-destructively by delegating to a proven specialist instead of rewriting it before parity evidence exists;
- unmatched knowledge questions should fall back or abstain rather than fabricate;
- product-neutral routing is a reusable substrate for WSS and future consumers.

### Weaknesses / debt

- request classification is still regex-driven and therefore not proof of mature intent cognition;
- Brain matching is bounded lexical/containment matching rather than broad semantic reasoning;
- Scripture remains delegated to the browser engine, so the service contract does not resolve the browser/Core Search-intelligence drift documented under `RQ-003`;
- no claim is made here that every live downstream product currently uses `/api/dore/query` as its only Doré boundary.

### Revisit trigger

Revisit if the contract schema changes, a downstream product begins importing Doré internals directly, Search service-boundary convergence is implemented, or live routing evidence shows material misclassification/fallback problems.

### Disposition

Keep the 2026-08-24 service-layer milestone closed as a bounded historical completion. Treat further convergence as maintenance/architecture evolution, not retroactive invalidation.

## Finding B — Journal + Liming media placement audit

### Classification

`VERIFIED_COMPLETE` for the bounded repository-state placement audit; future media ingestion remains governed by the existing R2/D1 placement policy.

### Original objective

Determine whether current Journal and Liming Library content contained local binary media that should move to private R2, while avoiding unnecessary migration of structured editorial/catalog data whose correct master belongs in GitHub.

### Completion evidence

The milestone memo records `COMPLETE / PASS`, and the machine-readable inventory independently records `status: PASS` with:

- Journal local media binaries: `0`;
- Liming Library local media binaries: `0`;
- eligible local binaries: `0`;
- R2 writes: `0`;
- D1 new rows: `0`;
- GitHub binary deletions: `0`.

The inventory explicitly distinguishes `data/volumes/vol-00.yaml`, `data/resources.json` and `content/journal/_index.md` as structured/versioned source material that should remain in GitHub. It also records future R2 namespaces `journal/` and `library/media/`, D1 relationship/governance requirements, and confirms that Doré Original 001–241 plus Search corpus JSON were not touched.

### Current quality judgment

This is a legitimate zero-migration completion, not an empty or skipped task. The quality of the decision comes from refusing a storage migration when the access pattern and asset class did not justify one. Moving JSON/YAML merely because R2 existed would have created competing masters and weakened atomic versioning.

### What was learned / retained

- storage placement should follow asset semantics and access pattern, not platform availability;
- versioned structured editorial/catalog data belongs with code/content when atomic reviewability matters;
- binary media can move to private R2 while D1 owns identity, provenance, rights and relationships;
- zero-change is a valid migration result when evidence says nothing should move;
- source-locked canonical libraries and unrelated Search/corpus data should remain outside a narrowly scoped migration.

### Weaknesses / debt

- the audit describes repository state on 2026-08-24; future Journal/Library media additions can invalidate the zero-binary observation without invalidating the historical audit;
- the next proposed structured data-runtime audit was not discovered as a completed artifact in this bounded pass, so no completion claim is made for Search/corpus runtime placement;
- future owned/downloaded Library media still requires real rights/provenance and D1 relationship enforcement when ingested.

### Revisit trigger

Re-run placement classification when Journal or Liming gains meaningful owned/downloaded binaries, when Resource Master storage/access patterns materially change, or when structured Search/corpus runtime placement is reconsidered.

### Disposition

Keep the 2026-08-24 placement audit closed. Preserve the resulting policy as a maintenance rule; do not manufacture a migration merely to create activity.

## Canonical-register reconciliation

No Master Register status change is warranted from this pass. The current register already captures Cloudflare service/placement milestones inside the reconciled Sweep history and separately preserves the active operational workstreams they feed: Runtime, WSS, ONE, Join, Main, Library ingestion and Search. This ledger sharpens the evidence boundaries without creating duplicate active rows.

The bounded findings also do not create a new blocker, missing-evidence item, superseded item or revisit priority beyond existing Search service-boundary debt and ordinary future placement re-audit triggers.

Sweep 01 remains `ACTIVE_PARALLEL`; this pass does not justify `VERIFIED_COMPLETE`.