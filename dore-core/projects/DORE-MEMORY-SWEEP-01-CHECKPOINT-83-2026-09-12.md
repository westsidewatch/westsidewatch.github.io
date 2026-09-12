# DORÉ MEMORY SWEEP 01 — CHECKPOINT 83 — 2026-09-12

Status: COMPLETE / BOUNDED BATCH
Sweep: `MEM-SWEEP-01`
P01 constraint: subtitle critical-path state was not modified.

## Evidence reviewed
- `40e38e21fb621721b01ae1388d19dec97d71ef8a` — Dawn external pointer URL surfaces.
- `8112d1c2dffb1e87d4b3fe3c098085edae5f37dd` — Dawn capability mount registry.
- `dore_core/capabilities/url_surface.py`.
- `dore_core/capabilities/surface_mounts.py`.
- Dawn URL-surface workflow, benchmarks, public Web Surface integration and tests from those commits.

## Findings
1. Dawn now has a real pointer-to-presentation-surface boundary. Routing external pointers does not change relevance, admission or ownership.
2. The real discovery corpus is used as the benchmark substrate, with a 900+ pointer gate and pointer-only surface index.
3. A bounded Project Gutenberg Web Surface is mounted in the public Dawn storefront while source ownership remains external.
4. `SurfaceMountRegistry` corrects a capability-truth ambiguity: routed adapters are not automatically executable. It distinguishes `mounted`, `dormant` and `unavailable`; `SurfacePlan` exposes `mount_state` and `executable`.
5. Current bounded state: `bibliographic-page` is mounted for Project Gutenberg. IIIF, PDF, EPUB/MOBI, Zotero and general-web adapters remain dormant.
6. Classification: URL-surface resolver and mount-truth registry are `VERIFIED_COMPLETE / COMPONENT` implementation milestones. The heterogeneous multi-adapter reading system remains `ACTIVE_PARALLEL / UNKNOWN_NEEDS_EVIDENCE` because most adapter classes are not mounted and this batch found no persisted successful CI/status record for the latest mount-truth commit.
7. Reusable lesson: discovered or routable capability must not be treated as executable capability. Future Doré orchestration and capability registries should preserve this distinction.
8. Dawn collection relevance remains independent. Preview/render success must never promote a candidate or prove editorial fit; existing `RQ-006` remains valid.
9. The prior implicit assumption that route availability proves installed equipment is `SUPERSEDED`; the dormant adapter contracts themselves remain valid future equipment.
10. No new human-decision or environment blocker was found, and P01 state was not changed.

## Smallest next proof
Persist one fresh acceptance run for the mount-truth gate, production-readback one approved Gutenberg item through the Web Surface, then mount one materially different dormant adapter and prove fallback/refusal without mutating discovery/admission state.

## Durable linkage
See `DORÉ-DAWN-URL-SURFACE-EVIDENCE-LEDGER-2026-09-12.md`. Master Register bookkeeping should advance the Sweep frontier through Checkpoint 83 and enrich `DAWN-LIBRARY` with this component milestone.

## Sweep disposition
Sweep 01 remains `ACTIVE_PARALLEL`; this batch does not justify `VERIFIED_COMPLETE`.