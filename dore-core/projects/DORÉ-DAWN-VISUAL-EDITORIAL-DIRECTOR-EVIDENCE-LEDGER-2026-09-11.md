# DORÉ DAWN VISUAL EDITORIAL DIRECTOR — EVIDENCE LEDGER

Date: 2026-09-11
Status: ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION / ACCEPTANCE_PENDING
Owner workstream: `DAWN-LIBRARY`
Sweep parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
P01 impact: NONE

## Scope

This ledger reconciles the bounded Dawn Library Phase 2 visual-editorial sequence introduced on 2026-09-11. It does not replace the broader Dawn Library catalog/rights/relevance evidence ledger and does not promote the whole Library workstream to completion.

## Evidence reviewed

- commit `ada854e3c31d3503ac91df9315d2ec3326c8dff8` — Phase 2 Cut 01, Visual Fuzzy Retrieval Foundation;
- commit `58e90894c272a9b1454ac9c1d0104e2e45ea4d03` — Phase 2 Cut 02, graph-bound Editorial Director runtime;
- commit `ed8d9bb578ccc11633b0a14017ece2f0f212ab8e` — Phase 2 Cut 03, live Editorial Director surface consumption;
- commit `873f6548b17b511a650a39e4a3b433bea1d9f85b` — Phase 2 Cut 04, live-content editorial context derivation;
- commit `791d564e250c369a2541c4460340e2cf341c1caa` — Phase 2 Cut 05, multi-surface editorial orchestration;
- `data/resources.json` as the current live editorial-context source;
- `data/dawn_visual_editorial.json` v3;
- `scripts/dore/dawn-editorial-context.mjs` and self-test;
- `scripts/dore/dawn-surface-orchestrator.mjs` and self-test;
- `scripts/dore/build-dawn-visual-editorial-feed.mjs`;
- `layouts/partials/visual-resource-card.html`;
- `.github/workflows/dawn-visual-graph-check.yml`;
- available commit-workflow probes for Cuts 03–05.

## Current evidence-based interpretation

1. Phase 2 now has a real implementation chain rather than an isolated retrieval experiment: **live Library content → derived editorial context → graph-bound visual selection → deterministic generated editorial feed → surface orchestration metadata → Hugo card consumption of the selected visual state**.
2. Cut 04 materially improves the architecture by eliminating the hand-authored query manifest as the active request source. The builder now derives request content from `resources.weekly_theme` plus `morning_star` resources, carries Scripture and visual context forward, and persists `contextSource: resources.weekly_theme+morning_stars` in feed v2/v3.
3. The old `data/dawn_visual_editorial_queries.json` request-manifest path is therefore **SUPERSEDED as the active editorial-context source**. It may remain as historical provenance, but future work must not treat it as the governing source of Dawn editorial intent unless explicitly reactivated.
4. Cut 05 adds a distinct presentation contract rather than mutating Visual Graph identity: `dore.visual-surface-orchestrator.v1` assigns selected VisualWorks into `primary`, `secondary`, and `reading-focus` surfaces with explicit editorial weights and motion semantics (`near-still`, `slow-flow`, `focus`). The contract states that the graph owns identity/relationships while the surface layer owns presentation/motion.
5. The orchestration self-test is meaningful but bounded. It verifies three surface roles, primary weight `2`, deterministic candidate allocation, and no duplicate VisualWork assignment across surfaces for the supplied fixture. It does not prove production motion behavior, responsive layout quality, accessibility, or that every surface is currently consumed by rendered templates.
6. The persisted v3 feed demonstrates the intended split: one selected visual for `dawn-hero`, two for `dawn-river`, and an empty `dawn-focus` slot. An empty focus slot is not itself a defect; it shows the orchestrator can preserve a surface role without fabricating a visual when candidates are exhausted.
7. The workflow trigger was broadened from a hand-maintained list of individual Doré scripts to `scripts/dore/**`, reducing the risk that future editorial-runtime changes bypass the Dawn visual check. The workflow also includes the live-context and surface-orchestration self-tests plus deterministic feed regeneration/diff gating.
8. No workflow runs were returned by the available commit-workflow probes for Cuts 03, 04, or 05 in this reconciliation. Therefore repository implementation and persisted generated output are real, but a successful CI execution remains unverified here.
9. Production storefront readback for the v3 orchestration contract is also unverified. In particular, Cut 05 adds orchestration data but does not by itself prove that hero/river/focus presentation and motion semantics are rendered on the live storefront.
10. This work must not be conflated with the separate Chinese `聖經世界` relevance defect (`RQ-006`). A correct visual-selection/orchestration path does not repair book/catalog editorial relevance, and rights cleanliness still does not equal editorial fit.

## Classification

- Visual fuzzy retrieval foundation: bounded implementation milestone, `COMPLETED / RETAIN` inside the active workstream.
- Graph-bound Editorial Director runtime: bounded implementation milestone, `COMPLETED / RETAIN` inside the active workstream.
- Hand-authored `dawn_visual_editorial_queries.json` as active request source: `SUPERSEDED`; retained only as historical provenance unless explicitly reactivated.
- Live-content editorial-context derivation (Cut 04): `COMPLETED / RETAIN` as a bounded implementation milestone; CI/production acceptance remains separate.
- Multi-surface orchestration contract (Cut 05): `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`; deterministic fixture behavior is implemented, but real surface consumption/motion acceptance is pending.
- Dawn surface consumption of generated director feed: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`, with acceptance evidence still pending.
- Whole Dawn Library visual-editorial system: **not** `VERIFIED_COMPLETE`.

## Missing evidence / acceptance boundary

Before promoting this slice to a verified surface milestone, retain at least:

1. one successful `dawn-visual-graph-check` run containing live-context, orchestration, feed-build and diff gates;
2. one production Dawn Library readback proving the director-selected VisualWork actually renders with the intended card state and metadata;
3. one rendered proof that the v3 `primary` / `secondary` / `reading-focus` surface roles are consumed correctly, including responsive behavior and intended motion semantics rather than only existing as feed metadata;
4. one negative/contrast case proving an unselected visual does not receive the director-selected state;
5. one changed live-content case proving editorial context and selected output follow `resources.json` rather than stale/hard-coded request identity;
6. one candidate-shortage case proving the orchestrator abstains cleanly rather than duplicating or inventing visuals;
7. no regression in rights/authority/surface-preset constraints.

## Revisit trigger

Reopen this architecture if the feed becomes hand-edited, editorial intent drifts back to a parallel manual query source, graph identity drifts from surface identity, selection scores are exposed as authority rather than ranking evidence, live-content changes fail to regenerate deterministically, surface orchestration duplicates identities or fabricates missing candidates, or visual curation begins bypassing rights/authority/surface constraints.

## Durable judgment

Retain the **live content → editorial context → graph-bound runtime → generated feed → surface orchestration → surface consumption** pattern as the stronger reusable Dawn editorial-selection architecture. Cut 04 is a legitimate improvement over the static-request prototype, and Cut 05 establishes a useful identity-versus-presentation boundary. Neither is sufficient for a new global Doré editorial-intelligence completion token until CI and production rendering/motion evidence exist.
