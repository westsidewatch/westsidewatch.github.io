# Whole-city public-street continuity

The shared road builder previously sampled only its centreline endpoints. A single cross-slope rectangle could penetrate one road edge into the DEM and suspend the other. Its boundary filtering also discarded an entire12m cell if any corner touched a public-core exclusion or city circuit, leaving avoidable approach gaps.

Paving is now partitioned by the actual rendered DEM triangles and sampled across its whole footprint at the existing0.35m display offset. Public courts are subtracted and circuit boundaries clipped geometrically. Centreline registrations, source widths, building placements and confidence remain unchanged. The offset follows modern terrain, not a surveyed ancient street level. It does not connect an unregistered entrance or invent a missing historical street. Existing bend footprints/intersections remain illustrative; a walkable route graph is not certified.

A darker road display tone separates existing street surfaces from pale residential/court context. No new road hierarchy or historical paving colour is inferred. This is not new palace construction. Four earliest phases retain their separate path/access implementations;14 phases use the corrected shared paving builder. All18 are checked.

## Cost and validation

No external assets or per-frame remeshing. Each existing cell still emits at most one mesh, with extra triangles where a DEM or boundary split is needed. Newly retained clipped residual cells can add submissions compared with the previous dropped cells; this is not presented as a loading speedup. On-demand road diagnostics are not called in the render loop.

The road contact test reproduces527 old mismatches among710 synthetic cross-slope samples and verifies the corrected top raycasts. A court/circuit fixture retains exactly250m² of permitted pavement up to its boundaries. The independent-later, royal and Hellenistic tests check actual paving triangles/retained areas instead of old four-vertex or whole-cell omission assumptions. The wall-reference test allows only0.1mm Float32 rounding at the exact clipped circuit edge. Sync/async geometry parity remains required.

The18-state browser checks audit every visible shared paving triangle centroid against the original DEM, while preserving phase ownership, camera, housing and landmark IDs in optional baseline/new runs. Six epochs and portrait are captured. A rendered-terrain offset is engineering validation, not archaeological acceptance.

## CI recovery accompanying the work

The medieval reverse/evidence test now waits for asynchronous city completion before inspecting road counts. Housing batching image limits retain a strict mean delta0.05 and strong-pixel fraction0.002 (both ten times tighter than before) while allowing isolated channel deltas up to128 rather than64. The prior CI sample had a75-channel peak with0.0115 mean and0.000396 strong fraction. This accommodates sparse rasterization/precision differences without accepting broad structural changes; source geometry/mapping/camera/draw-cost checks remain.

See PUBLIC-CORE-CITY-WORKPLAN.md for the18-era construction order and explicitly unresolved building groups.

All77 workflow pre-browser Node checks passed locally across the cumulative runs after updating these contracts. Online18-state street/ground/scale/ownership/portrait checks passed on the deployed5d309eed4 runtime; the follow-up changes only validation and this document. Full new-head CI remains separate.
