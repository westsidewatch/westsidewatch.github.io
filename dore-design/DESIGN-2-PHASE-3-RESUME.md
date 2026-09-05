# DORÉ DESIGN 2.0 — Phase 3 Resume

Issue: #294
Branch: `dore/design2-phase3-resume`

This branch resumes the direct-manipulation editor upgrade from current `main`, not from the stale `dore-design-2` branch.

## Baseline recovered

The prior 2.0 branch contains the accepted Phase 1–2 command, inspector, canvas and workbench implementation, but it has diverged substantially from current main. Those modules are source material to port forward, not a branch to revive in place.

## Phase 3 target

- Left: Pages / Layers with stable selection state.
- Center: canonical renderer canvas with direct select, drag, resize, marquee multi-select and snapping.
- Right: contextual properties for Page / Text / Image / Selection.
- Keyboard workflow, inline text, align/distribute and undo/redo remain command-backed.
- No editor DOM state becomes canonical document state.
- Multiwrite Homepage remains the first production specimen, but migration/publish parity remains Phase 6.

## Resume rule

Port 2.0 interaction modules onto current main, preserve all 1.9.1 capabilities added since the old branch split, then close Phase 3 before starting snapshot/publish work in Phase 4.
