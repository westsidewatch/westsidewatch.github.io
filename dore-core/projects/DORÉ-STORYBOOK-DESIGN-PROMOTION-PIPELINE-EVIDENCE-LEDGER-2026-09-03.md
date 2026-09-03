# DORÉ STORYBOOK → DORÉ DESIGN PROMOTION PIPELINE EVIDENCE LEDGER — 2026-09-03

Status: SWEEP_01 / VERIFIED_BOUNDED_RECONCILIATION
Related workstreams: `VIS-GRAMMAR`, `EVOLUTION`, `MEM-SWEEP-01`
P01 impact: none

## Evidence reviewed

- commit `8f1b0584b2055bb9b32cb8e07b1d580b862133fa` — `feat(dore): close Storybook design promotion loop`;
- coordination result commit `789793762e0cadb9506a3ad5861e7bdd0c4c14e7`;
- promoted candidate `new-westside-living-current-v1` / `Living Current / 活水流域`;
- Storybook evidence, promotion gate, candidate registry, editable workspace wiring, candidate gallery and judgment endpoint recorded by those commits.

## Current classification

- Storybook → Doré Design promotion pipeline v1: `VERIFIED_COMPLETE` as a bounded design-infrastructure milestone.
- `Living Current / 活水流域`: `ACTIVE_PARALLEL / CANDIDATE`; it is not a production-baseline replacement.
- New Westside visual grammar as a whole: remains `ACTIVE_PARALLEL / BUILDING`.

## Completion evidence

The canonical acceptance result is terminal `PASS` on attempt 1 and records:

- transport `PASS`;
- execution `PASS`;
- product monitor `PASS`;
- Storybook build success;
- 4 test files / 8 tests passed;
- deterministic Storybook evidence generated;
- promotion gate `PASS` with all named checks true for the promoted candidate, including build, render, function, accessibility, visual stability, responsive behavior, design distinctness, Westside fit, provenance completeness, editable bindings, immutable baseline protection, renderer/story availability and material distinctness;
- promotion acceptance code `DORE_STORYBOOK_PROMOTION_V1_PASS`;
- candidate gallery `PASS`;
- editable canvas `PASS`;
- feedback roundtrip `PASS`;
- baseline 262 immutability preserved;
- live local Doré Design health reported version `1.9.0`, `promotion_pipeline=storybook-to-dore-design-v1`, and one promoted candidate visible through the candidate registry.

## Important evidence boundary

The broader Storybook evidence summary contained at least one aggregate `RESPONSIVE_PASS=false` across the whole multi-candidate observation set. That does **not** invalidate the promoted `Living Current` candidate because the candidate-specific promotion gate separately records `RESPONSIVE_PASS=true` and passed the canonical promotion acceptance. The aggregate observation layer and the candidate promotion gate must therefore remain distinct evidence scopes.

This milestone proves that Doré can move one bounded, evidence-bearing design candidate from Storybook research into the editable Doré Design candidate system without mutating the locked baseline. It does **not** prove:

- that `Living Current` is the final or preferred New Westside homepage;
- that the live public homepage should be replaced;
- that current New Westside visual grammar is mature enough for Brand V1 propagation;
- that Doré has general visual judgment across arbitrary products;
- that D4 rendered visual readback/correction has been closed globally.

## Retrospective evaluation

### Original objective
Create a real promotion path from research/prototyping in Storybook into Doré's editable design workspace, while preserving provenance, baseline immutability, responsive/accessibility checks and a reversible candidate state.

### Current quality
Strong for a first bounded infrastructure milestone. The result is substantially better evidence than a design screenshot or commit-only claim because it combines build/test/render evidence, a machine-readable promotion gate, runtime registry exposure, editable bindings and feedback roundtrip acceptance.

### What Doré learned / retained

- treat design research and production baseline as separate states;
- promote candidates through explicit gates rather than copying screenshots by hand;
- preserve provenance and candidate identity across Storybook → editable workspace;
- keep an immutable known baseline while allowing materially distinct experiments;
- record human/Doré judgment separately from machine promotion eligibility;
- distinguish aggregate observation failures from candidate-specific promotion eligibility.

### Weaknesses / debt

- only one candidate has crossed the full promotion path;
- promotion eligibility is not equivalent to editorial/art-direction approval;
- the aggregate Storybook observation suite still contains responsive failure(s) outside the promoted candidate;
- current evidence is local-runtime acceptance, not public production rollout evidence;
- the visual grammar project still needs purpose-built Doré-derived asset families and real cross-product digital/print proof before broad propagation.

### Revisit trigger

Revisit the pipeline if a second materially different candidate cannot promote without one-off code changes, if candidate judgment cannot feed a durable learning loop, if baseline immutability regresses, or when Brand V1 propagation requires cross-product candidate promotion.

### Disposition

Keep the Storybook → Doré Design promotion pipeline v1 closed as `VERIFIED_COMPLETE` bounded infrastructure and maintain it as reusable design-production capability. Keep `Living Current` as a candidate until comparative visual/editorial judgment and downstream product evidence justify promotion beyond candidate state.

## Canonical reconciliation note

Sweep 01 should treat this as a newly verified sub-milestone under `VIS-GRAMMAR` / design-production infrastructure, not as completion of `VIS-GRAMMAR` itself. The Master Work Register should retain `VIS-GRAMMAR` as active/building while naming the promotion pipeline v1 as closed bounded infrastructure. No P01 state or dependency is changed.