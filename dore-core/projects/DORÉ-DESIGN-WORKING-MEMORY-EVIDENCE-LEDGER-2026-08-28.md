# DORÉ DESIGN WORKING MEMORY — EVIDENCE LEDGER

Date: 2026-08-28
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01`
Status: ACTIVE / EVIDENCE-BOUNDED

## Bounded sources reviewed

- `docs/dore/DESIGN-WORKING-MEMORY.md`
- `.github/workflows/dore-design-agent-acceptance.yml`
- `dore-core/evidence/PENPOT-BRIDGE-01-LIVE-EVIDENCE-2026-08-26.md`
- current `VIS-GRAMMAR` interpretation in `DORÉ-MASTER-WORK-REGISTER.md`

## Reconciliation

### 1. The Design Working Memory target is broader than its current CI proof

`DESIGN-WORKING-MEMORY.md` defines four gates:

- D1 Design Scope;
- D2 Truth State;
- D3 Consolidation;
- D4 Penpot Visual Verification;

and a first operational acceptance exam that requires Doré Search conversation → current design brief → Penpot execution → visual readback → correction loop → verified design state.

The current `dore-design-agent-acceptance.yml` is useful but narrower. It checks Python syntax, deterministic D1–D3 truth/consolidation behavior, Penpot-action routing, MCP-client build and fail-closed behavior when MCP is unavailable. It does **not** execute the D4 visual readback/correction contract and does not prove the full Search-to-design acceptance exam.

Therefore CI success for this workflow must not be interpreted as Design Working Memory completion.

### 2. Penpot bridge feasibility is separately verified

`PENPOT-BRIDGE-01-LIVE-EVIDENCE-2026-08-26.md` proves a bounded infrastructure milestone:

`Doré Core → runtime secret → Penpot Remote MCP → live design context → execute_code → persistent editable object → independent readback`.

That milestone is legitimately `VERIFIED_COMPLETE` for bridge feasibility only. It explicitly does not prove typography/foundation completion, visual quality, export fidelity, responsive/print transfer or finished Westside grammar.

### 3. Current design-memory classification

- D1–D3 deterministic memory/truth/consolidation machinery: real implementation progress with automated acceptance coverage.
- Penpot remote bridge feasibility: `VERIFIED_COMPLETE` bounded infrastructure milestone.
- D4 visual verification/correction loop: `UNKNOWN_NEEDS_EVIDENCE`.
- full Search conversation → inherited design memory → execution → visual readback → correction → verified state exam: `UNKNOWN_NEEDS_EVIDENCE`.
- overall Design Working Memory: `ACTIVE`, not `VERIFIED_COMPLETE`.

### 4. Durable lesson

A design system has three distinct evidence layers that must not be collapsed:

1. **memory truth** — can Doré distinguish observations, references, proposals, attempts, decisions, corrected/final/verified states?
2. **execution connectivity** — can Doré persist editable objects into the external design surface?
3. **visual competence** — can Doré inspect the actual rendered composition, diagnose visible mismatch, revise, and verify the result against current design intent?

Passing one layer is not evidence that later layers pass.

This reinforces the governing Visual Grammar rule already established by Sweep 01: tool/API success, editable/vector output and layer creation are production properties, not proof of visual quality.

## Missing-evidence candidate

A future canonical missing-evidence item should track the still-unproven D4/full operational exam. The smallest useful proof is one bounded real Westside design task using current confirmed visual memory, followed by actual visual readback, at least one evidence-driven correction when required, and a persisted final verification artifact. This work must remain subordinate to the P01 critical path.

## Canonical-register disposition

No workstream status change is justified by this batch. `VIS-GRAMMAR` should remain `ACTIVE_PARALLEL / BUILDING`. This ledger narrows the evidence boundary around design-memory/design-agent claims and should be referenced by the Master Work Register during the next safe canonical-register edit.

P01 subtitle state/action was not modified.