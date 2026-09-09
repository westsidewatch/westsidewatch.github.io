# DORÉ DESIGN LIVING CURRENT P1 — EVIDENCE LEDGER

Date: 2026-09-09
Status: ACTIVE_PARALLEL / IMPLEMENTED_PROTOTYPE_NEEDS_RENDERED_ACCEPTANCE
Scope: Doré Design motion-language P1 only
P01 impact: NONE

## Bounded evidence

- commit `e76f50785c2a670173bf685f9cbe10d2ae3c7cec` — `DORÉ Design P1: Living Current in Design Lab`
- commit `0a51a7a488ba8f46514b86d472e4a713e7ed12aa` — workspace schema fix marker
- commit `b85608981faa8f5310f9f2ad3caab2eff7469367` — `DORÉ Design P1: keep motion lab workspace schema-valid`
- `dore-design/motion_prototypes.py`
- `dore-design/prototypes/P1-LIVING-CURRENT-NATIVE.md`
- `static/dore-design/prototypes/p1-living-current-native/index.html`
- `static/dore-design/prototypes/p1-living-current-native/styles.css`

## What is implemented

1. P1 Living Current is a real Doré Design implementation prototype, not merely a design note. It is registered as a first-class Design Lab surface and routed through the Design 2 editor/runtime.
2. The prototype tests a bounded spatial hypothesis: the foundational 8:5 horizontal current can use native browser overflow + CSS scroll snap with no added animation runtime.
3. The implementation includes explicit keyboard-focus, reduced-motion and mobile behavior in the prototype contract, and exposes experiment metadata through the Design runtime.
4. The follow-up schema repair removes the non-canonical `prototype` workspace node type and retains only page identity + experiment metadata, keeping the structured workspace schema-valid while rendering the experiment through `render_p1()`.

## Evidence boundary

- Code and wiring prove `IMPLEMENTED_PROTOTYPE`.
- They do **not** prove a rendered/browser acceptance PASS, visual quality, hardware/mobile behavior, or production-homepage adoption.
- The prototype's synthetic gradient/texture cover art is experiment scaffolding. It must not be promoted as the final New Westside visual grammar or as proof of Doré-generated website assets.
- The statement in `P1-LIVING-CURRENT-NATIVE.md` that native primitives are sufficient is therefore a bounded architecture hypothesis supported by implementation, but remains `NEEDS_RENDERED_ACCEPTANCE` until the named acceptance conditions are executed and persisted.

## Classification

- Living Current P1 spatial prototype: `ACTIVE_PARALLEL / IMPLEMENTED_PROTOTYPE_NEEDS_RENDERED_ACCEPTANCE`.
- New motion runtime for P1: `REJECTED_FOR_NOW / NOT_NEEDED_BY_CURRENT_HYPOTHESIS`; revisit only if rendered/hardware acceptance demonstrates a concrete failure.
- Initial non-schema workspace `prototype` node: `SUPERSEDED / REPAIRED` by the schema-valid metadata-only page representation.
- Synthetic prototype cover visuals: `EXPERIMENT_SCAFFOLDING / NOT_CANONICAL_VISUAL_LANGUAGE`.

## Smallest next proof

Run one persisted rendered acceptance covering desktop horizontal scroll/snap, keyboard focus, reduced-motion behavior and explicit mobile behavior against the schema-valid Design Lab surface. If PASS, P1 may be promoted to `VERIFIED_PROTOTYPE`; this still must not be conflated with final New Westside visual-language or homepage production acceptance.

No P01 subtitle runtime, ordering, deployment, audio/transcription dependency, blocker or resume path was modified.