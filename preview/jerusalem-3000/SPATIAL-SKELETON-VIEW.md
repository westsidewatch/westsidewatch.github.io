# Stage 2: common spatial skeleton comparison

A new optional 空間骨架對照 panel provides a common plan view for all 18 eras. The fixed window, north direction, scale bar and modern DEM background remain identical when eras change. The terrain canvas draws the existing rendered DEM triangles once and reuses that image; opening the panel does not move the 3D camera, navigate time or generate other eras.

The collector reads the shared ledger and current lifecycle/evidence state. Green outlines are registered district polygons; orange features are registered routes; blue locations represent water/defense; purple locations represent sacred/civic model cores. Bounds-only objects are shown as model centers, not invented footprint outlines. Withheld, unresolved, invalid-frame or out-of-terrain geometry is excluded, with missing drawable geometry explicitly counted. Zero features does not mean historical absence. All geometry remains illustrative/unverified.

A dashed envelope describes only the currently registered occupation layout, never a historical wall or city boundary. It uses existing polygons, component bounds or rotated provisional masses. Optional retained first-Temple models respect their display setting. No district, street, wall or landmark geometry is fabricated to fill a domain. Source relations without their own physical history do not acquire drawn geometry by association.

The existing first three early-era footpath centerlines now publish the same endpoints already used to build their meshes. No path coordinates, house geometry, sources or lifecycle events change. Other generators continue supplying their existing registrations; missing historical spatial foundations remain visible work items.

The view is an engineering baseline for stage 2, not complete city reconstruction. Next spatial work must replace missing/legacy envelopes and routes coherently across the full timeline, retaining the canonical terrain and the distinction between model scope and historical extent. Full foundation/historical acceptance stays false and detail work remains paused.

Validation: common terrain identity, coordinate frame/phase contract, unknown/withheld exclusion, missing geometry, evidence filtering, retained-layer policy, rotated mass envelope and immutable snapshots. Full 18-era desktop/portrait browser regression checks each phase's map state; focused desktop/portrait checks verify canvas fit, localized phase title, fixed-window/evidence return and no timeline navigation. Existing early and lifecycle regressions remain in place. The new collector test runs in city runtime CI.

Two small local JS modules are added. Existing DEM, source registrations and meshes are reused; no new external service, image/terrain download or model generation. No measured bandwidth/token/FPS saving is claimed. The collector runs on request; a hidden panel does not rebuild its scene map.
