# DORÉ DESIGN 2 — ARRANGE CAPABILITY EVIDENCE LEDGER — 2026-09-05

Status: BOUNDED_RECONCILIATION_COMPLETE
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register extension: `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-SPARSE-CAPABILITY-RUNTIME-2026-09-05.md`
P01 impact: NONE

## Bounded evidence reviewed

- recent Design 2.0 arrange implementation sequence through `1e9a9edf633c4e51b060fac57c023ad819bb368e`;
- `4d2311f26336ef82b5415b133064ce0edc639c4b` — native arrange operations;
- `bdb39dd28e4cbe894c7df5f93734bd86c848f1ed` — distribute spacing, canvas-center and z-order controls;
- `7df2176f7de75c95f78aca3906ca2fc255738795` — complete arrange command payload preservation;
- `a966469103713ccce50a3cbad045bec6b2ca8ed9` — complete arrange contract coverage;
- `96a81ffeaf2bf0a170827a729eb5089174de5539` — durable capability-slice record;
- `1e9a9edf633c4e51b060fac57c023ad819bb368e` — geometry/persistence smoke checks;
- immediately preceding Design 2.0 layer/geometry/group/alignment implementation commits in the same bounded product slice.

## Current classification

### Design 2.0 native arrange capability
`ACTIVE_PARALLEL / VERIFIED_COMPLETE_SUBMILESTONE`

A coherent native structured-workspace arrange slice now exists. The durable contract records align left/center/right, align top/middle/bottom, center-to-canvas horizontally/vertically, distribute horizontally/vertically, fixed-gap stack operations, z-order movement, group/ungroup, and persistence of geometry mutations through `/api/workspace` without adding a new runtime dependency.

This is a legitimate completed submilestone inside an active Design workstream. It is not evidence that Doré Design 2.0, the visual-production system, or the shared control plane is globally complete.

## Completion evidence

1. Repository implementation commits introduce native arrange/group/alignment/layer operations rather than only documenting them.
2. Follow-on fixes preserve the complete arrange command payload through the workspace path instead of dropping geometry-control fields at a boundary.
3. Contract coverage and a focused static smoke test pin key geometry formulas and verify that the native path reaches the persistent save surface.
4. The durable product note explicitly records the implemented operation set and names Frame + Asset/Image editing as the next product slice.

The strongest bounded claim supported here is repository-level implementation plus focused contract/smoke coverage. No live end-user interaction packet or commit-associated CI run receipt was reviewed in this batch, so live product acceptance remains separate evidence.

## Current quality judgment

The slice is materially stronger than an editor surface that exposes only raw coordinates or ad-hoc canvas manipulation. It moves ordinary layout work into named, reusable structured operations and keeps workspace JSON—not a renderer-specific scene graph—as the persistence authority. That aligns with the already-reconciled renderer-neutral asset/shape doctrine.

The main weakness is acceptance breadth, not missing basic operation coverage. Static smoke checks are useful regression evidence but should not be treated as proof of interactive correctness across mixed-size selections, nested groups, hidden/locked nodes, undo/redo, keyboard-driven flows, responsive canvas sizes or real production documents.

## Durable learned principles

- Named semantic layout operations are preferable to forcing agents/users to synthesize coordinate arithmetic repeatedly.
- Arrange commands must preserve their full payload across UI/control/workspace boundaries; partial command forwarding is a real failure mode.
- Geometry mutation should persist through the same canonical workspace authority used by the rest of Design 2.0.
- Renderer-neutral workspace state and semantic arrange operations reinforce one another: the canvas remains a projection, not the data authority.
- Static/contract tests can verify mathematical and persistence invariants, but live interaction remains a separate acceptance layer.

## Revisit / supersession judgment

- Manual coordinate-only arrangement as the default Design 2.0 workflow is now `SUPERSEDED` for the implemented operation family.
- Renderer-owned z-order/group state remains superseded by canonical workspace state.
- The arrange slice itself should be retained as a completed submilestone and reopened only for concrete interaction defects, nested/group semantics, undo/redo integration, accessibility/keyboard requirements or performance evidence.

## Smallest next proof

Persist one bounded interactive acceptance packet using a real Design workspace that demonstrates:

1. mixed-size multi-select align + distribute;
2. center-to-canvas and fixed-gap stack;
3. z-order and group/ungroup state surviving save/reload;
4. hidden/locked node behavior remaining correct;
5. one before/after exported visual proving the semantic operation changed the intended geometry without corrupting unrelated state.

Do not require this proof before continuing the next Frame + Asset/Image product slice; retain it as the acceptance boundary for promoting arrange from repository-complete submilestone to live-product verified behavior.

## P01 isolation

No P01 subtitle/runtime/deployment/binding/credential/audio-transcription state, ordering or blocker was modified by this reconciliation.
