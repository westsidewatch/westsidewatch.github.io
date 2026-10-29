# All-era metric residential baseline

The prior boundary repair removed out-of-circuit housing but did not complete the occupied street blocks inside the model boundary. The density audit found only 24 illustrative David/Solomon dwellings, narrow Herodian street-front strips and later coarse blocks discarded when any part overlapped a reservation. Enlarging houses or scaling an era to fill its walls would conceal these defects.

## One coordinate and size rule for all eighteen phases

`metric-residential-layout.js` enumerates the complete ordered timeline. Every policy uses the same canonical DEM origin, east-x / south-z metres, one metre per scene unit and unexaggerated elevation. Camera zoom changes projection only. There is no target roof-coverage percentage, count derived from wall area, era-dependent world scale or random density seed. The runtime inspection `inspectMetricResidentialPolicy()` exposes all eighteen policies and the actual root/terrain scales.

All existing early offsets and house dimensions are preserved. Existing generated street-front/block-edge parcel IDs and polygons are preserved; extra parcels use separate `metric-infill` / `metric-parcel` identities. Existing later coarse-block modules remain the same geometrical representation, rather than being rescaled and relabelled as measured houses. Their quantities remain block/module counts, not households. The original foundation and physical-survival acceptance flags remain false.

## Complete existing residential zones rather than enlarge buildings

- Four early phases: append deterministic, non-overlapping illustrative dwellings only within the hull of their existing dwelling cloud. Preserve their old dimensions, original offsets and path clearance; reserve the royal courtyards. An inferred wall does not establish that every enclosed slope was inhabited.
- Four shared middle phases: preserve the original parcel layout, then subdivide the unused parts of the existing authored residential districts. Destruction uses the same layout and schematic ruin projection. Persian residential bounds remain independent; earlier ruins remain opt-in. New layouts do not prove physical reuse.
- Herodian and Roman-destruction phases: preserve the existing houses, then complete residual district interiors instead of stopping at narrow road-front strips. New parcels are checked against roads, sanctuary/fortress reservations and the same authored period enclosure before architecture is generated. The destroyed period reuses this same schematic geometry in place.
- Eight later phases: retain the existing independent district boundaries and block-module dimensions; test roads, religious/public reservations and engineering terrain fit per module, instead of discarding an entire large block. The three final periods retain their common old-city background and explicitly declared outside-wall expansion. Early Aelia's unwalled interval does not inherit a future wall constraint.

The old active Hellenistic adapter scaled a reference city. Its already existing illustrative coordinates are now frozen in a metre registration file; no reference-city scale transform runs on that path. This migration preserves the old coordinates, **not** independent archaeological validation of them. Period-specific registration remains a historical gap.

## Physical modelling limits and source meaning

New small parcel subdivision uses an 18 m span limit within the existing generator's 9–18 m frontage analogy, with 1.6 m access gaps and 0.6 m setbacks. These are explicit engineering parameters for inferred infill, **not measured dimensions of every period's houses**. They never resize an existing house or later block. Room/elite-house variation requires period/district evidence; a wealthy mansion cannot be inferred by scaling a generic small house.

A new candidate with more than 8 m corner-to-corner relief is withheld as needing terrace evidence. This is a conservative engineering admission condition, not an archaeological slope cutoff. Modern GLO-30 includes buildings/vegetation and cannot establish ancient terraces, valleys, empty land or ancient building heights. No terrain is flattened, moved or carved. Land outside the existing residential envelopes remains unresolved rather than automatically populated.

Source context explains why a universal house size/density cannot be certified: the City of David guide distinguishes early ridge settlement, royal/temple development and later western expansion; the official Upper City excavation account describes multiple affluent residences, not a citywide small-house template. The medieval excavation report also documents substantial historic fill that a modern DSM alone cannot reconstruct:

- https://cityofdavid.org.il/wp-content/uploads/2023/03/Traveler_COD_Eng_2022_lowrez.pdf
- https://www.gov.il/en/pages/jerusalem-the-upper-city-during-the-second-temple-period
- https://hadashot.iaa.org.il/Report_Detail_Eng.aspx?id=25701&mag_id=128

## Verification and remaining work

Unit checks cover all eighteen ordered policies, metre/phase/translation invariance, unchanged old parcel dimensions and IDs, unchanged early offsets/dimensions, additive deterministic infill, terrain rejection and the frozen Hellenistic path. Browser checks measure actual roof projections and actual scene scales in all eighteen periods, then cover reverse cache returns, source filters, staged construction, wall boundaries, mobile and generation readiness. Roof projection is measured separately from courts, public buildings, streets and the provisional circuit area; it is not historical population or an archaeological building-coverage ratio.

This completes a shared engineering baseline and increases occupation within supported *model* envelopes. It does not finish historical district extents, true ancient ground, household distribution, all eighteen period-specific dimension catalogues or seventeen physical transitions. Those require source registration and remain visible gaps; fine architectural work stays paused.
