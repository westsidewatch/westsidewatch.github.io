# Local wall/water plan registration

M2 slice eight, continuing PR #1271. No new historical wall or tunnel geometry is supplied by this package.

A source registry identifies the Broad Wall footprint and Siloam underground centerline as separate targets in canonical Core. Admission results are retained in each target's metadata and exposed in diagnostics. Current entries are withheld, with explicit missing source plan, survey controls, independent checkpoints, digitized geometry, vertical authority and dating variant.

The compiler fits a uniform scale/rotation from two registered survey controls, preserving image-down coordinates. Independent off-baseline checkpoints test orientation and residuals. Declared plan scale, tolerance, provenance URL/locator/hash, sourced per-vertex canonical elevations and dating variant are mandatory. Modern approximate map points are not survey controls. Degenerate baselines, wrong scale, mirrored alignment, missing/incorrect vertical datum and self-intersecting wall polygons fail.

Success yields a registered-plan candidate, not certified historical geometry or a complete city/hydraulic simulation. Plan hash is a provenance declaration; source-byte verification and archival intake remain separate work before supplying real records. A 3D renderer has not been added.

Fixtures test known transforms and rejection paths with synthetic coordinates and example.org sources. Fixtures never enter production data. Real production entries remain withheld; no line is inferred from a marker or tunnel length.

Existing source/dating controls, houses, temples, lifecycle and era projection continue unchanged. The new registry uses the shared loader once. Evidence explains the intake requirements. Full 18-era browser regression checks the real targets remain withheld.

Next: obtain and archive a reusable source plan with control/elevation authority, check its bytes and dating scope, and digitize one local candidate through this admission path. Missing historical evidence is not filled by arbitrary geometry. M2 and historical timeline readiness remain incomplete.
