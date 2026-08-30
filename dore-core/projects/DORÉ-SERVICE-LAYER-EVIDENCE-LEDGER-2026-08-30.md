# DORÉ SERVICE-LAYER EVIDENCE LEDGER — 2026-08-30

Status: SWEEP-01 BOUNDED RECONCILIATION
Related canonical work: `CORE`, `RUNTIME`, `SEARCH`, `WSS`, `LIBRARY-INGEST`, `STEWARDSHIP`
Source sweep: `dore-core/projects/DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`

## Evidence reviewed

- `dore-core/cloudflare/DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md`
- current implementation `functions/api/dore/query.js`
- current `functions/api/dore/` route family inventory
- current canonical `DORÉ-MASTER-WORK-REGISTER.md`
- existing completed-work interpretation for the first Westside Stories external-worker integration

## Historical milestone judgment

**Classification:** `VERIFIED_COMPLETE` for the bounded Doré service-contract milestone established on 2026-08-24. The broader Doré runtime/service platform remains `CORE/CONTINUOUS` / `ACTIVE` stewardship.

### Original objective

Create one product-neutral Doré entry contract so products can ask Doré for Scripture, Brain, asset, or status work without coupling every consumer directly to Doré's internal storage/index implementations or prematurely replacing the proven browser Bible Search engine.

### Completion evidence

1. `DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md` records `COMPLETE / PASS`, endpoint `/api/dore/query`, schema `dore.query.v1`, GET/POST input forms, intent lanes, stable envelope fields, and explicit non-destructive compatibility rules.
2. The current repository still contains `functions/api/dore/query.js`, which implements the declared `dore.query.v1` envelope and `scripture`, `brain`, `asset`, and `status` routing.
3. Current implementation preserves the original compatibility boundary rather than silently rewriting Bible Search: Scripture requests delegate to `/dore/search-index.json`; Brain loads the canonical `/dore/brain/knowledge-index.json` and falls back to Scripture when no sufficiently confident node is found; asset requests delegate to `/api/dore/assets/search`; status requests delegate to `/dore/status/current.json`.
4. The current `functions/api/dore/` family contains the later product/runtime surfaces that grew around the service boundary, including asset, brain, conversation, memory, learning-event and library routes. This confirms the service layer was not merely a dead design memo.
5. The later Westside Stories first-external-worker milestone independently demonstrates the durable architectural lesson: external products should consume stable Doré service contracts rather than internal indexes. That milestone remains separately closed as `CW-012` and does not need to be merged into this service-layer completion claim.

## Current quality judgment

The original bounded milestone remains sound. It established a useful compatibility seam at the right time: one stable response envelope and routing boundary, while explicitly refusing a premature server-side Scripture rewrite that could regress the public Search product.

However, the current `query.js` implementation is intentionally thin and should not be misread as a complete canonical intelligence layer. Its routing classifiers are regex/heuristic based, Brain matching is bounded string/concept matching, and Scripture execution is still delegated to the browser-search dataset rather than centralized behind one server retrieval implementation. Checkpoint 19 separately identified browser/Core Search duplication and service-boundary drift; this service milestone does not erase that debt.

## What Doré learned / capability retained

- expose product-neutral contracts instead of making every product import internal indexes;
- preserve proven behavior during architecture transitions rather than rewrite for elegance alone;
- standardize provenance, confidence and epistemic boundary fields at service edges;
- explicit delegation can be a valid architecture milestone when the delegated subsystem is intentionally still canonical;
- historical service-contract completion and later intelligence consolidation are different work items.

## Weaknesses / debt

- `dore.query.v1` is primarily a routing/envelope contract, not proof of universal query understanding;
- Search execution remains split between browser/public-search logic and Core/service-side logic, so parity can drift;
- current intent classification is heuristic and not equivalent to the still-unpassed Search cognition `CONCEPT_PASS` / `PRODUCT_PASS` gates;
- this bounded review did not find a dedicated current automated regression suite specifically asserting the whole `/api/dore/query` contract across all four lanes;
- endpoint existence in repository is not by itself fresh production availability evidence; live deployment should be checked when a consumer depends on a changed contract.

## Revisit trigger

Reopen/refactor when any of the following becomes true:

- `RQ-003` Search service-boundary convergence work begins;
- a second or third external product requires richer shared query semantics;
- `dore.query.v1` schema or delegation targets change materially;
- repeated production evidence shows lane misclassification or parity drift;
- a canonical server-side Scripture/Search execution layer becomes demonstrably safer than the current compatibility delegation.

## Disposition

Keep the 2026-08-24 service-layer milestone closed as `VERIFIED_COMPLETE` historical infrastructure. Do **not** treat it as proof that Search cognition, unified retrieval, or all Doré service execution is complete. Continue broader service/runtime evolution under existing active workstreams.

## Missing-evidence candidate retained from adjacent Cloudflare placement work

The Journal/Liming media-placement milestone explicitly deferred Search/corpus and Doré Brain/runtime structured-data placement to a later **structured data-runtime audit**. This bounded repository search found no clearly named completed audit artifact. That future decision remains `UNKNOWN_NEEDS_EVIDENCE`, but it is not a blocker to the service-layer milestone and does not justify moving JSON/YAML/runtime data merely because D1/R2 exist. The smallest useful future proof is an access-pattern/source-of-truth audit covering update frequency, atomicity, size, latency, provenance, rollback and competing-master risk before any structured-data migration.

## Sweep disposition

This batch introduces no new human/environment blocker and does not modify or interrupt P01. The canonical Master Register's current high-level statement that Cloudflare service/placement milestones have been reconciled remains consistent with this evidence; no status change is required from this bounded pass.
