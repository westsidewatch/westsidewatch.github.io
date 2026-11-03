# B34 — precinct routes before outward infill

## Shared engineering correction across temple periods

An actual original-DEM test found the previous western paving triangles could cut0.265m into the terrain even when their boundary vertices were above it. The ribbon algorithm sampled terrain crossings on the two long edges but bridged the interior terrain diagonals. It did not conform to the rendered surface.

Paving tops now clip each existing ribbon strip to the actual indexed DEM triangles, then evaluate the period-specific paving height at the clipped vertices. The metre frame, DEM vertices, height sampler, sanctuary envelopes and historical object identities stay intact. Existing ground support faces remain; no terrain flattening is introduced. The shared routine serves First Temple royal/temple roads, independent Persian and Hasmonean sanctuary approaches, court-gallery floors and the southern flight. This fixes a common generator defect without transplanting Herodian architecture into earlier periods.

Real original-DEM triangle-centroid tests cover1594First Temple,269Persian and328Hasmonean approach top triangles, with zero terrain intrusion at those samples. These are contact samples, not proof of walkable historical gradients or ancient street placement. Existing gate/doorway/road clearance tests remain in force.

## Western street: separate evidence from the display candidate

The [Western Wall Heritage Foundation](https://thekotel.org/en/10812/2/) describes the street outside the western retaining wall. Its [site account](https://thekotel.org/en/wailing-wall-western-wall/) discusses the excavated southern section and its relationship with Robinson's Arch. These support the existence and external relationship, not this project's exact linework. Later Roman eastern Cardo excavation results are not used as Herodian street vertices.

The old street grammar emitted63paving blocks occupying50m width and an additional invented24m-high wall, partly inside the inherited300×480m platform. It has been replaced by one thin terrain-conforming paving batch. Selected width8m and length357m are authored display budgets, not a digitized excavation plan. No shop fronts, drains or bridge are asserted from these dimensions.

The original geographic candidate at31.777,35.2337 remains in the ledger. The display centre is derived from the rounded platform's west edge, an8m width and0.35m clearance. At the canonical origin this yields x−154.35m, a−31.328m offset from the provisional source anchor. The offset and authority are exposed in `inspectHerodianDimensions().precinctRoutes`; they are not silently registered as surveyed geography. Only this speculative display candidate changes, not the platform, terrain or city.

The route is **inferred** in the ledger and renderer. Observed-only filtering hides it; evidence for the existence of a street does not certify current display vertices. A footprint-only housing exclusion follows the actual route plus1m engineering clearance; it is not an enlarged historical plaza. Visible house-bound checks reject occupancy of the route. `西側街道` gives a close inspection view in the core stages.

## Remaining R1 blockers

- Southern flight to wall/gate/underground passage: unresolved. The current modern DEM display datum and rounded platform do not establish ancient levels. No fake bridge or oversized gate closes this gap.
- Antonia to northern/western porticoes: [Josephus War5](https://penelope.uchicago.edu/josephus/war-5.html) supports the relationship and descending passages, but current endpoint/height registration is not resolved. The present fortress profile is not a source-admitted surveyed footprint; no decorative stair is added.
- Robinson/Wilson structures and the southern pilgrimage junction require dated footprints and level alternatives before execution.
- First Temple royal/court placement and early Second Temple court envelopes remain authored. Main-road links are engineering prototypes, not surveyed ancient routes or demonstrated physical continuity.

R1 is partial; R2 landmark blocks and R3 city gates/walls are not accepted by this repair. All-era spatial acceptance, complete precincts and historical geometry acceptance remain false.
