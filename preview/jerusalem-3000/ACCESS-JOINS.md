# B35 — continuous approach bends before new precinct connections

## Defect and repair

The shared route builder previously emitted an independent rectangle for each centreline segment. At a turn the rectangles overlap on the inside and leave a wedge outside. Coplanar overlap can flicker even when B34 terrain contact is correct. This affects existing First Temple royal/temple approaches and independently authored Persian/Hasmonean sanctuary approaches.

Adjacent segments now share one miter cross-section at the original bend. No centreline point, metre width, building anchor or source chronology changes. Paving strips meet along that cross-section once, with original DEM-triangle clipping retained. Bilinear strip coordinates preserve the two endpoint heights when a raised approach meets a terrain-following part. A near-reversal requires an explicit landing rather than silently folding a ribbon.

Persian and Hasmonean west/east court-gallery branches now start at the actual main-route edge, rather than duplicating paving from its centre. Their existing waypoint junction, outer destination and evidence identity remain explicit; branch topology records both the original junction and rendered edge start. Exact historical street lines remain inferred.

## Inspection

`院門通路` frames the existing approach in the Solomon, Persian and Hasmonean contexts. It stays absent in the David context where the temple approach is not built, and is not backprojected to other periods. Existing `南側入口`, `西側街道`, `安東尼堡` and `院區總覽` controls remain available in their respective contexts.

## Southern interface: measured engineering gap, not a new reconstruction

Actual canonical-standing mesh bounds yield a4.9029m plan gap between the current flight and the rounded platform's south edge. The flight top is193.8020m in the project's relative vertical frame; platform paving is204.2040m, a10.4020m difference. These are model measurements against modern DEM, **not ancient elevations** or excavation dimensions. `inspectHerodianDimensions().accessInterfaces.southern` exposes the actual current measurements and unresolved state.

The existing candidate anchors, wall/gate position and internal passage still need source-specific registration. A bridge, extra staircase or oversized gate would conceal this issue; none is added. Antonia/portico and Robinson/Wilson interfaces also remain unresolved. B35 closes paving-generation defects, not the historical registration gaps documented in [PRECINCT-ROUTES.md](PRECINCT-ROUTES.md).

## Acceptance

- 4623actual rays around a90-degree bend must encounter precisely one paving top inside the intended plan and zero outside; this catches both overlap and holes.
- Original-DEM tests inspect1663First Temple,277Persian and337Hasmonean approach top triangles: each centroid ray encounters one top, with no terrain intrusion in those samples.
- Positive-area triangle-intersection checks reject main-road/gallery-branch overlap while permitting their shared boundary.
- Existing doorway/wall/house clearance, inferred evidence, cached reverse,18-era/17-transition, desktop/portrait and GPU section checks remain required.

These tests do not establish ancient walkability, exact geometry, complete precincts or all-city historical acceptance. Separately owned road junctions outside this repair still need review.
