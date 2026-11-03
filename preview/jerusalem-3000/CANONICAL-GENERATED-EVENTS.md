# Canonical generated city lifecycle events

The Herodian parcel generator previously registered scalar built/destroyed fields without declared lifecycle events, while the renderer independently animated destruction. Its road mesh IDs were not present in the shared ledger. This package atomically normalizes the finished generated batch and binds both houses and roads to shared event visibility.

Scope: generated blocks/parcels, their finished building IDs, their existing district parent and the eight provisional registration roads. It does not overwrite sourced anchor objects, the other named source districts/networks, or the withheld eastern access. Existing geometry, DEM sampling, confidence, IDs and ruin projection remain unchanged. Normalized parcel-to-block and building-to-parcel/block/district references now use registered IDs.

Each selected record receives an illustrative generation event in herodian-jesus, schematic building ruin (or non-building transform) in roman-destruction, and unresolved fate in aelia. These are model policies, not excavated dates or verified ruin/survival measurements. District events describe the generated envelope, not a historically verified district creation date. No burial or reuse link is inferred. Roads preserve provisional geometry/source authority; registration does not certify ancient alignment.

The candidate ledger is validated before publishing maps or binding finished meshes. Duplicate IDs, conflicting existing events, missing parents, unknown mesh IDs and missing building geometry reject the whole batch. Every bound component receives a stable object/component ID. Existing shared source events remain untouched. The renderer reads current shared events for houses and infrastructure, so edited event state can hide either and restoration uses the same geometry.

Foundation lifecycle snapshots now enumerate withoutDeclaredEventIds in addition to their count. This exposes unresolved source/scope gaps across all 18 eras without manufacturing construction events. Full foundation acceptance and stage 1 remain incomplete.

Tests exercise the real generator, late conflict/mesh/geometry failure rollback, parent chains, eight road bindings, live house and road event gates, source-anchor preservation, later unknown fate and exact reverse identity/transforms. Full browser regression requires zero unbound components in both canonical rendered phases and retains the existing all-era terrain, evidence and trace assertions. New coverage runs in city runtime CI.

No new source downloads, external services, image or model requests. One small local JS adapter module is added. No measured traffic/token/FPS saving is claimed. Architecture detail remains paused.

Browser acceptance: the actual excluded/terrain-fitted scene publishes 2,294 records including 1,067 houses and eight roads. Both canonical phases bind all 23,460 visible components, with zero unbound or out-of-phase components. Roman-destruction records have zero missing declared events. Seven remaining Herodian source relations/withheld entries are explicitly listed in all-era-event-proof.json; they were not given invented construction dates. Startup before phase selection is hidden and tested. Full 18-era desktop/portrait regression passes, errors=[], fullTimelineReady=false.
