# DORÉ MULTIWRITE BIBLE STUDY EVIDENCE LEDGER — 2026-09-09

Status: ACTIVE_PARALLEL / IMPLEMENTED_SLICE / NOT_VERIFIED_COMPLETE
Sweep parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Product surfaces: Multiwrite / ONE
Capability boundary: `context.fuzzy-search`
P01 impact: NONE

## Evidence reviewed

- merged PR #521, `DORÉ BI-3: add Multiwrite Bible Study Prepare UI`;
- merged PR #523, `Hotfix Multiwrite new-book and Bible Study entry runtime`;
- merged PR #525, `Multiwrite: move Bible Study to home alongside My Library`;
- `static/dore/dore-multiwrite-bible-study.js`;
- `static/multiwrite/bible-study.js`;
- `static/multiwrite/home-bible-study.js`;
- `static/multiwrite/book.js` / `book.html` / `home-runtime.js` related BI-3 integration;
- `static/one/one-bi3-embedded.js` and ONE loader integration;
- `local/dore-companion-extension/site_bridge.js` + background allowlist path;
- `tests/test_dore_bi3_capability_ui.py`;
- recent BI-3/hotfix commit chronology on 2026-09-09;
- GitHub Actions runs on PR #521 head `1f65f3d4f57b3414ef602ee15e6501e5af5a868b`, PR #523 head `128fb4d215838bfdfc896398e604fa088041e7a8`, and PR #525 head `c06bc8394fc890b7728a919d618505b08a8fb2d0`.

## Original objective

Make Bible Study a Doré capability that can appear inside Multiwrite and ONE without each product building or learning its own search/provider stack. The first bounded product contract is `Prepare`: fuzzy retrieval returns evidence-bearing Context Results, and the product may perform only the typed `Keep / Flow / Present` study actions.

## What is actually implemented

1. A shared, provider-neutral Prepare controller exists at `static/dore/dore-multiwrite-bible-study.js`.
2. The controller propagates `host`, `mode=prepare`, `embedded`, lane and query context rather than exposing QMD/Concord/SWORD/OpenAI/provider identities to the product UI.
3. Multiwrite book and home surfaces both persist a `dore.study-document.v1` document containing `kept` and `flow` evidence items in IndexedDB `studyDocuments`.
4. ONE mounts the same Prepare controller in embedded mode and persists the same StudyDocument schema family.
5. A bounded Westside site bridge now dispatches only allowlisted `context.fuzzy-search` calls through the Companion/native path; it does not expose a general arbitrary local-exec bridge to the page.
6. The UI normalization retains `canonical_reference`, `source_ref`, `evidence_status`, provenance, preview and typed action metadata.
7. `tests/test_dore_bi3_capability_ui.py` contains contract coverage for provider neutrality, action admission, shared DB schema, ONE embedded context and a Node behavior acceptance for query-context propagation + typed Flow dispatch.
8. PR #523 is important negative evidence: immediately after BI-3 integration, production-facing regressions existed in new-book entry, DB-version alignment, local-book opening and panel focus. They were subsequently repaired and regression coverage was added. This means the implementation history is real, but merge existence alone cannot be treated as product-completion evidence.
9. PR #525 moved the Bible Study workspace onto the Multiwrite home surface alongside My Library, with `Keep / Flow` summary rendering and the same `context.fuzzy-search` bridge contract.

## CI reconciliation

The earlier bounded review understated the available CI evidence.

- PR #521 head `1f65f3d4f57b3414ef602ee15e6501e5af5a868b` has persisted successful workflow runs including `Doré Capability Runtime` run `34319916071`, `Multiwrite Import v1` run `34319915999`, `Doré Foundation Tests` run `34319916002`, ONE cross-reference preflight, ONE Global Audit and the A2A control-plane workflow.
- `Doré Capability Runtime` run `34319916071` completed successfully; its recorded steps include minimum-sufficient Bible routing tests, capability runtime tests, zero-metered-cost benchmark and shared-state visual execution probe.
- PR #523 hotfix head `128fb4d215838bfdfc896398e604fa088041e7a8` also has persisted successful `Doré Capability Runtime` run `34320863465`, `Multiwrite Import v1` run `34320863506`, and `Doré Foundation Tests` run `34320863452`. This is stronger evidence that the repaired BI-3/hotfix state passed the capability/runtime gate.
- PR #525 head `c06bc8394fc890b7728a919d618505b08a8fb2d0` has a persisted successful `Multiwrite Import v1` run `34321336202`, but no `Doré Capability Runtime` run is present for that head in the commit-associated workflow evidence. The likely explanation is path gating, but that should not be invented as proof.

Therefore repository/CI implementation evidence is materially stronger than previously recorded, but it still does not establish the full live product path.

## Classification

- BI-3 shared Prepare controller: `ACTIVE_PARALLEL / IMPLEMENTED_SLICE`.
- Multiwrite Bible Study product surface: `ACTIVE_PARALLEL`.
- ONE embedded BI-3 surface: `ACTIVE_PARALLEL`.
- `context.fuzzy-search` Westside site bridge: `ACTIVE_PARALLEL / BOUNDED_CAPABILITY_BRIDGE`.
- Browser-local StudyDocument persistence: `MAINTENANCE` once live flow is proven; not yet a durable cross-device knowledge store.
- BI-4 Live rundown / projection workflow: not implemented by this evidence family; remains outside the verified BI-3 slice.

## Completion evidence boundary

The following are now durably evidenced:

- merged implementation PRs;
- source-level architecture boundaries;
- explicit regression tests and Node acceptance code;
- successful Capability Runtime / Foundation / Multiwrite CI on the original BI-3 head;
- successful Capability Runtime / Foundation / Multiwrite CI on the immediate post-merge hotfix head;
- successful Multiwrite Import CI on the later homepage-integration head;
- hotfix chronology showing concrete runtime defects were found and repaired.

The following remain **not established** by this bounded evidence and therefore must not be claimed:

- one recorded live browser acceptance from Multiwrite page → site bridge → Native Messaging → Doré Core `context.fuzzy-search` → evidence-bearing result → Keep/Flow persistence → reload/readback;
- one equivalent live ONE embedded acceptance proving the same shared capability boundary;
- production proof that provider-neutral fuzzy retrieval quality is acceptable across real study queries rather than only contract fixtures;
- evidence that Present/projection has a real downstream consumer rather than only an admitted action payload;
- cross-device/server-backed StudyDocument durability;
- a final full Capability Runtime run specifically associated with PR #525 head after the homepage relocation.

Therefore BI-3 still must **not** be marked `VERIFIED_COMPLETE` as a live product capability. The stronger CI evidence narrows the missing proof to live end-to-end behavior and the final integrated-head/runtime boundary rather than source-test absence.

## Current quality judgment

Architecturally the slice is stronger than the earlier pattern of embedding retrieval intelligence independently in each product: shared controller + typed result/action contract + bounded site bridge are reusable and reduce provider leakage. The immediate post-merge hotfixes show the product integration was still fragile at the entry/runtime layer, especially around IndexedDB schema coordination and local/static book duality. The successful post-hotfix Capability Runtime run materially improves confidence in the repaired implementation, while the absence of a recorded live browser round-trip still prevents product-completion promotion. The current implementation should be retained and tested, not rewritten from scratch.

## Durable learning / capability retained

`one Doré capability → shared provider-neutral UI controller → host-specific persistence adapter → typed evidence/action contract`

This is a reusable pattern for future Doré product capabilities. The product should know the Doré capability and evidence contract, not the underlying retrieval provider.

## Weaknesses / debt

- three Multiwrite paths now participate in the same IndexedDB version and object-store evolution; schema coordination is a real maintenance surface;
- StudyDocument persistence is browser-local and product-hosted, so it is not yet canonical cross-device memory;
- the bridge depends on the local Companion/native runtime being present; fallback/absence behavior is currently a product runtime concern;
- repository and CI evidence are strong for the implementation slice, but live browser/native/Core round-trip acceptance is not yet durable;
- `Present` is part of the action vocabulary but BI-4/live projection completion is explicitly outside this slice.

## Revisit triggers

Reopen for architecture refinement when any of the following occurs:

1. the same StudyDocument must follow a user across devices;
2. a third product consumes BI-3 and begins duplicating host persistence logic;
3. Core/browser fuzzy-result semantics diverge;
4. BI-4 Live rundown or real Present projection is implemented;
5. repeated IndexedDB migration regressions appear.

## Current disposition

Retain the shared controller and bounded bridge. Do not fork another product-specific search engine. Next proof should be live end-to-end acceptance in Multiwrite and ONE, followed by a decision on whether StudyDocument remains local working memory or graduates to a canonical Doré memory substrate.

## Canonical-register implication

The current Master Work Register has no explicit `MULTIWRITE` / BI-3 row in the bounded 2026-09-09 review. This evidence family therefore represents a missing workstream/history item that should be surfaced in the canonical register as `ACTIVE_PARALLEL`, without displacing P01. Until that register mutation is safely persisted, this ledger is the durable source of truth for the BI-3 evidence boundary.