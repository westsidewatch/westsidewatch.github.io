# DORÉ ITALIAN EDITORIAL ATLAS EVIDENCE LEDGER — 2026-09-14

Status: SWEEP-01 EVIDENCE LEDGER
Scope: bounded reconciliation of the Italian Editorial Atlas and its integration into the Doré multi-page design resident. This ledger does not alter or interrupt P01.

## Evidence reviewed

- commit `7c09ab73c9082df2001d00f07814e00671a7a38c` — exposes `Italian Editorial Atlas / 義大利編輯圖譜` as a persistent design-research page in the multi-page editor and adds the `dore.italian-editorial-grammars.v1` registry;
- commit `aca01c80cc0c922f8f5763175ea961744240911b` — extends the Candidate 01 resident deployment verification to compile the Atlas runtime, verify the page appears in the editor, verify the canvas points at the Atlas surface, and verify the grammar registry is served;
- commit `93ba0b4d3ae3b60cd82ab5b6b6923155d77df210` — aligns the Atlas page with the shared workspace canvas contract (`1200×930`);
- `static/dore-design/italian-editorial-grammars.v1.json` — current family/era/composable-grammar registry.

## Classification

### IT-ATLAS-001 — Italian Editorial Atlas research surface

**Current classification:** `ACTIVE_PARALLEL / IMPLEMENTED_RESEARCH_SURFACE`

The Atlas is not merely a research memo. It has a persistent editor-visible page, a canonical JSON registry, a renderer bridge, deployment/runtime verification hooks and a workspace canvas contract. That is sufficient to classify the surface implementation itself as a bounded implemented component.

It is **not** `VERIFIED_COMPLETE` as design education or visual-language learning. The registry itself explicitly distinguishes `researching`, `seed` and `provisional` era states, and current proof does not show that the extracted grammar has passed blind transfer into a real Westside product.

## Original objective

Move Doré design learning away from flattening publications into static “style cards” and toward a more durable model:

`publication family → era → composable grammar → issue-specific invention`

The explicit governing principle in the registry is:

> Stable editorial intelligence, issue-specific visual invention.

The Atlas therefore aims to preserve editorial lineage and material/temporal logic without copying historical covers, mastheads or logos.

## Completion evidence for bounded milestones

The following component milestones are currently evidenced:

1. **Editor exposure — bounded PASS**: the Atlas is registered as `design-research` and appears in the multi-page editor.
2. **Canonical grammar registry — bounded PASS**: `dore.italian-editorial-grammars.v1` exists and is consumed by the Atlas surface.
3. **Resident verification contract — bounded PASS in workflow definition**: the Candidate 01 deploy workflow checks the Atlas editor page, canvas handoff, static surface and grammar registry in the running local resident.
4. **Workspace-canvas compatibility — bounded PASS at implementation level**: the Atlas page now carries the shared `1200×930` canvas contract.

These prove implementation boundaries. They do not by themselves prove the latest workflow run passed, nor do they prove the grammar is visually correct or transferable.

## Current quality judgment

The architecture is materially stronger than a one-card-per-publication model because it separates stable learning from issue-level visual invention and treats layout, image, typography, material, density, sequence, irony and emergence as composable modules.

The strongest currently researched family is `Campo Grafico`, where 1933/1934 entries carry issue evidence and explicit material/sequence observations. Other families remain seed/provisional. This asymmetry is healthy if preserved honestly; it would become a defect only if seed/provisional entries were consumed as equally authoritative finished knowledge.

## Superseded interpretation

The older design-learning tendency to reduce a publication into one static style card or one fixed historical-cover look is `SUPERSEDED` as the preferred learning model for this family.

This does **not** mean historical examples are discarded. They remain evidence and provenance. What is superseded is treating a historical surface as a reusable visual template.

## Missing evidence / open gates

1. **Atlas runtime run evidence:** the workflow definition contains meaningful live-resident checks, but this bounded batch did not find a persisted successful workflow-run artifact/status for commit `aca01c80...`; do not convert workflow assertions into a runtime PASS without run evidence.
2. **Research completeness:** most non-`Campo Grafico` eras remain `seed` or `provisional`; their grammar must not be promoted to canonical mature learning yet.
3. **Blind transfer:** no persisted test yet shows that an Atlas-derived grammar improves a materially different real Westside artifact without copying a source cover or requiring target-specific restatement.
4. **Product acceptance:** no human-accepted digital/print specimen currently proves that Atlas learning should propagate into `VIS-GRAMMAR` or Brand V1.

## Revisit trigger

Revisit when any of the following exists:

- a successful persisted Candidate 01 resident run proving the Atlas checks live;
- one family/era graduates from `researching` to a clearly evidenced mature state;
- a blind transfer experiment applies an Atlas grammar to a real Westside design specimen;
- the Atlas begins duplicating or conflicting with `VIS-LEARN`, `VIS-GRAMMAR` or Storybook art-direction canon.

## Capability retention

This work contributes a reusable design-learning principle:

**learn systems as composable grammar and temporal/material behavior, not as screenshots to imitate.**

That principle is compatible with the existing Westside rule that Doré-derived website assets should be purpose-built from current brand principles rather than cropped historical Doré originals.

## Current disposition

- Atlas implementation surface: `ACTIVE_PARALLEL / IMPLEMENTED_RESEARCH_SURFACE`.
- Editor/runtime integration code: bounded component completion, maintain as regression-protected infrastructure.
- Atlas research corpus: `ACTIVE_PARALLEL`, uneven maturity by era.
- Static style-card interpretation: `SUPERSEDED` as preferred learning model.
- Brand/production propagation: not yet authorized by evidence.

No P01 state or action is modified by this reconciliation.