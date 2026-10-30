# Public precincts and unlocated planning reserves (B14)

The gray rectangles were not all missing buildings. The renderer treated both real public precincts and arbitrarily placed future programme envelopes as unbuilt land, while housing excluded both. B13 only handled the six Islamic/later eastern courts.

This change separates those meanings before neighbourhood generation:

- All eight later contexts replace the original269,150m² eastern placeholder with the existing frozen modern mapped142,646m² site envelope. This is a bounded display reference, not an ancient perimeter certification.
- Byzantine southern church reservation shrinks from52,500m² to the existing8,037m² Nea model/forecourt envelope; the building still follows its post543 date.
- Unlocated western public-building, cotton-service and early-Islamic administrative programmes retain their original source records in `planningReservations`. They no longer assert that an entire neighbourhood was vacant. Existing inferred residential typologies fill eligible land; this is not proof those particular lots were residential.
- Real sacred precincts, landmark envelopes, named gatehouses and access constraints remain protected. Public contexts use the public stone palette, rather than the gray unbuilt code. No new historical ground elevation is asserted.
- Aelia/Byzantine eastern site uses a DEM-following archaeological context surface and explicitly unresolved internal use. No Islamic upper court, kiosks, dome or Aqsa is copied backward. The IAA debris inspection supports multi-period material presence, not a complete internal plan: https://publications.iaa.org.il/atiqot/vol56/iss1/14/ . Absence of a reconstructed building does not establish historical emptiness.

The reservation audit retains original source polygons and areas, active areas, and non-spatial programme statuses. Source JSON is immutable. The generation test reinstates the unlocated exclusions and verifies the repaired version produces additional actual blocks. It also checks all original later reservations remain accounted for. Browser checks visit all18 eras and reject residual gray unbuilt colour coding; they do not certify all public buildings have been reconstructed.

No DEM vertex, scale, metre parcel policy or existing landmark dimension is changed. Logarithmic depth, exact court/temple terrain exclusion, shared phase caching, enclosure and external callouts remain in place. No remote runtime service or asset is added. The eight later contexts still have uncertain internal plans; all18 historical geometry acceptance flags and17 physical inheritance reviews remain unaccepted.
