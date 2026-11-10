# B15: roof-module shape quality

A low-area block could previously remain over100m long. `partitionOverviewBlock` stopped at900m² or rejected a split if a child was below120m², without checking length. Irregular planning residuals therefore produced narrow full-height courtyard walls and long diagonal roof faces on the modern DEM. The result resembled a cut through the city. It is a display-generation artifact, not a sourced valley or historic street.

The common overview generator now:

- Checks diameter as well as area; normally subdivides coarse visual modules until at most32m across.32m is an engineering display bound, not measured ancient housing.
- Allows small pieces when division is required by length. Narrow strips are divided without introducing extra access gaps; declared street reservations remain upstream.
- Uses a solid cap for shapes under6m wide instead of forcing a courtyard into a needle. Pieces under1.5m wide remain exposed ground rather than pretending to be usable buildings. These engineering thresholds do not establish historical lot sizes.
- Reports maximum displayed module span, slender solid modules, omitted sliver area and projected roof area. Counts are not historical building counts.

No DEM positions, terrain scale, period footprint, historic landmark/gate dimension or source parcel is enlarged or moved. Authored block/object IDs stay with their existing ledger; only their visual subdivisions change. Ineligible fragment meshes can disappear while the remaining part of the registered block stays. The metre parcel generator used by the early/shared/canonical phases is retained. All18 selected phases are checked through the same overview interface; the8 later coarse owners receive the new length subdivision.

`verify_jerusalem_3000_module_shapes.mjs` reproduces a124m narrow strip, checks it is subdivided without being erased, checks a tapered tip, and builds all8 later owners with their actual selected enclosure/reservation/coverage registrations. Actual generated modules must satisfy the span bound. The omitted tip area must remain below1% of projected roof area in each context. Existing containment, terrain sampling, all18 evidence/phase visibility, portrait and17-transition checks remain required. This is not historical geometry acceptance or a complete repair of illustrative street layouts.

There are more visual modules and vertices in affected blocks. No download, FPS, memory or token savings are claimed. No external runtime asset or terrain request is added. Geometry continues to use the existing persistent phase cache.

At the local Crusader comparison pose, visible projected roof area changes from387849.85m² to387832.42m² (about0.0045% decrease); visible visual modules1703→2472. Thin mesh count is not a housing-population metric. The separate omitted-tip counter is430.24m²; it cannot be equated with net roof loss because courtyard/solid and admission/subdivision changes also affect coverage. The before/after comparison uses the same selected phase, camera and original terrain.
