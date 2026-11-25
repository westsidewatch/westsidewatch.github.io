# Housing and period defense boundaries

The housing renderers reserved wall and gate strips but did not consistently constrain occupation to the same period circuit. Road-led parcels or large later district cells could therefore appear entirely outside the displayed perimeter. A common admission guard now checks actual projected mesh surface triangles against the existing, currently selected enclosure, including a two-metre model clearance. A convex hull is deliberately avoided: it would bridge empty courtyards and concave wall-aligned blocks.

The guard runs after owner lifecycle/evidence visibility and before construction presentation. It never moves houses, changes the historical ledger, enlarges a wall to fit generated houses, or reclassifies mistakes as historical suburbs. Rejected illustrative housing is withheld from rendering. Renderer-local generated/eligible counts remain source-owner counts; `inspectHousingBoundary()` and foundation visible bindings describe the final admitted display. Detailed roof polygons are available only with `{includeFootprints:true}`; per-frame diagnostics omit the large rejected-ID list. Decisions are cached by enclosure stage and immutable geometry identity; no city is regenerated on a normal frame or repeat visit.

## Period policy

- David/Solomon uses the existing David enclosure, then its existing northern extension according to the same royal stage. No coordinates or house offsets move.
- The eleven network phases join only matching endpoints of the currently active authored wall families and perimeter returns. Unclosed paths are never silently closed. Ruin and disputed circuits can constrain illustrative occupation without becoming standing walls or accepted archaeological plans.
- Aelia's early interval has gates but no active circuit: its boundary remains unresolved. A later enclosure is not projected backwards into that interval.
- Byzantine and early Islamic circuit changes select the matching stage. The guard rechecks admission on both forward and backward travel.
- Ottoman and later old-city districts use the existing frozen modern-reference envelope. Only districts explicitly marked `extra-mural-expansion` in the two later expansion phases bypass that envelope. The partial modern window remains partial.
- The first three early phases have no complete registered circuit. Their housing is reported as unresolved, rather than forced inside an invented enclosure or a modern wall.

For later block renderers with closed circuits throughout their period, admission also runs per visual housing module during generation. Valid modules in a boundary street block survive; an invalid module does not require removal of the entire block. The final shared guard catches stage-specific differences. The modules and block counts are not historical household counts.

## Validation

`verify_jerusalem_3000_housing_boundary.mjs` covers matching/reversed chains, open gaps, concave notches, complete footprint clearance and owner/evidence visibility restoration. `verify_jerusalem_3000_housing_boundary_browser.mjs` checks the actual rendered roof triangles in all eighteen phases, both royal stages, Aelia's unwalled interval, Byzantine/Islamic stage changes, medieval ruin presentation, reverse-cache returns, evidence filtering and mobile. Declared later extra-mural blocks remain visible. Both checks run in city-runtime CI.

The existing circuits remain authored hypotheses or modern references as previously documented. This is a consistency constraint on the reconstruction, not new archaeological proof. Historical foundation acceptance and all seventeen physical-transition acceptances remain false.
