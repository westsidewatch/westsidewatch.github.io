# DORÉ LIGHT FAMILY IMPLEMENTATION RECONCILIATION

Date: 2026-09-07
Parent workstreams: VIS-GRAMMAR, MEM-SWEEP-01
P01 impact: NONE

## Bounded evidence reviewed

- `functions/api/dore/penpot-light-family-v01.js`;
- `functions/api/dore/penpot-light01-threshold-prototype.js`;
- `.github/workflows/dore-penpot-light-family-v01.yml`;
- `.github/workflows/dore-light01-threshold-gate.yml`;
- commit `6596aad55d2f71e138e285087593ba7038c1ca1b` (`feat(dore): produce LIGHT family v0.1 in Penpot`);
- commit `f529ccedfa27b56deae3324eb5537e432a018e75` (`ci(dore): verify LIGHT family production in Penpot`);
- `DORÉ-VISUAL-ASSET-SUITE-LEDGER-2026-09-06.md` through Checkpoint 51.

## Reconciliation finding

The prior repeated statement that no reusable LIGHT source assets existed is too strong and is superseded by direct repository evidence.

A real purpose-built LIGHT family implementation exists. `penpot-light-family-v01.js` defines six reusable SVG assets (`LIGHT-01` through `LIGHT-06`) across FULL / FRAGMENT / TRACE strengths and sends them through the Penpot MCP production route. The companion workflow invokes the deployed endpoint and asserts `ok === true`. A separate threshold prototype produces a named `LIGHT-01 / THRESHOLD / PROTOTYPE` board and deliberately reports `prototype_created_not_visual_pass`.

This is meaningful implementation evidence, but it is not yet the full visual acceptance packet required by the New Westside grammar contract.

## Current classification

- LIGHT family v0.1 implementation: `ACTIVE / UNKNOWN_NEEDS_EVIDENCE`.
- Penpot production route for LIGHT assets: implemented; runtime PASS not independently persisted in this reconciliation.
- LIGHT-01 threshold prototype: implemented, explicitly **not** a visual PASS.
- Bethlehem-star family: still `READY`; no source implementation found in this bounded batch.
- Full purpose-built Doré-derived website asset suite: remains `ACTIVE_PARALLEL / BUILDING`.
- Brand V1 propagation: remains gated.

## Why this is not VERIFIED_COMPLETE

The current code proves that a six-asset LIGHT family was authored and wired to Penpot, but the required acceptance evidence is still incomplete:

1. no persisted browser screenshot/readback of the generated family was found in this batch;
2. no identical-real-content Journal/Search comparison was found;
3. no desktop/mobile acceptance packet was found;
4. no print-equivalent proof was found;
5. no accessibility/performance acceptance was found;
6. no critique/revision record was found;
7. no cross-product transfer decision to ONE / Join / Liming Library was found;
8. the Bethlehem-star companion family remains unimplemented in the evidence reviewed here.

## Retrospective judgment

Original objective: create a reusable purpose-built light grammar rather than decorate the interface with original Doré plates or generic engraving filters.

Completion evidence: source implementation and production workflow exist, including six named vector assets and a separate threshold prototype.

Current quality: architecturally useful and materially beyond a concept card, but visually under-proven. The implementation is dominated by geometric SVG paths/gradients and cannot yet be judged as a mature Doré-derived light language without rendered review and critique.

Durable learning: implementation existence and visual acceptance must remain separate gates. Repository code can move an item from `READY` to `ACTIVE`, but only rendered evidence can move it toward completion.

Weakness / debt: the prior Sweep checkpoints repeatedly treated the LIGHT family as nonexistent because they inspected ledgers/inventory but did not follow the dedicated Penpot endpoint/workflow evidence deeply enough.

Revisit trigger: first persisted rendered LIGHT-family readback, first Bethlehem-star implementation, or first identical-content Journal/Search application.

Current disposition: retain and evaluate; do not discard, promote to Brand V1, or treat as visual PASS yet.

## Smallest next proof

Persist one rendered Penpot/browser readback of the six LIGHT assets, apply a selected variant to identical real Journal or Search content beside the current production control, and record a visual critique. In parallel, implement the Bethlehem-star family under the same provenance contract.

## P01 isolation

No P01 subtitle ordering, deployment, credentials, audio, transcription, runtime, or blocker condition was changed.