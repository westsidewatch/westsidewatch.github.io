# Whole-city terrain readability

The city and surrounding land shared a pale stone range. Directional hillshade alone left some enclosed valleys almost as bright as exposed slopes. This package separates muted earth from building stone and adds bounded terrain enclosure shading to the existing DEM presentation across all18 phases.

For each DEM vertex, eight directions sample the existing grid at approximately90,180 and360m. The highest positive horizon angle per direction contributes to an average enclosure value. Enclosed low terrain receives additional darkening; an exposed summit receives none from this term. Missing directions at the grid boundary are excluded, never replaced by fictitious terrain. Solar-facing slope shading and the existing absolute20m contour lines remain.

This is a visual depth cue, not a physical lighting simulation or historical surface reconstruction. Earth colours do not encode vegetation, rivers, ancient ground levels or evidence classes. No DEM position, normal, height sampler, origin, datum, building footprint or camera is changed. In particular this does not repair unresolved ancient city coverage, nor manufacture more historical buildings.

## Cost

The enclosure values and vertex colours are calculated once when the single terrain mesh is loaded. No added mesh, texture, shader pass, per-frame horizon calculation or remote data request. The same terrain is reused across epochs. Lookup distances are rounded to existing grid vertices; the30m source cannot supply fine rock faces or ancient street levels.

## Verify and inspect

`verify_jerusalem_3000_terrain_presentation.mjs` tests a synthetic bowl, crest and flat plane, actual DEM shading, exact position/sampler/scale invariance, contour levels and resource restoration. Architectural-ground and regional-terrain checks retain the terrain/temple masking and named mountain/valley relationships.

`verify_jerusalem_3000_terrain_readability_browser.mjs` visits all18 phases at the completed display stage, checks phase ownership and original vertical scale, captures six representative epochs and phone layout, and verifies no page errors. Supplying `J3K_TERRAIN_BEFORE` routes the previous presentation module into a baseline page and verifies identical camera, target, registered housing and landmark IDs against the new presentation. Surface UUIDs are session-local; compare grid authority across pages instead.

Default city overview should now distinguish the limestone city from surrounding slopes and valley recesses without a specialist switch. Next work remains public-building coverage and street interfaces from registered source plans; this rendering change does not complete that construction.
