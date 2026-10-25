# Independent Aelia / Byzantine / early Islamic spatial skeletons

This package replaces the three eras' legacy rectangular mass grids with independently authored district/path layouts on the existing canonical DEM. One JSON configuration drives district registration, route registration, coarse occupied cells, reservations, ledger events and the common spatial skeleton view. No Herodian footprint is scaled or reused to produce these layouts.

## Source context and geometric authority

The IAA's Western Wall Plaza report describes the Eastern Cardo's Roman north–south alignment and later street-side construction/narrowing. The Bet Ha-Bad report describes the modern street's relationship to the Roman/Byzantine Western Cardo. The Nea Church project supplies context for a southern Byzantine Cardo connection. The IAA study of Umayyad streets supplies context for access between the eastern cardo and the southern administrative complex:

- https://publications.iaa.org.il/ha-esi/vol138/iss1/57/
- https://hadashot.iaa.org.il/Report_Detail_Eng.aspx?id=27699
- https://jerusalemfoundation.org/old-project/nea-church/
- https://publications.iaa.org.il/atiqot/vol120/iss1/11/

These sources constrain relationships and broad direction. The model coordinates, envelopes, transverse connector, block partitions, road width and 6m model height are author-designed illustrations, not measurements extracted from archaeological plans. No excavated city boundary, historical wall circuit or exact church/administrative building footprint is claimed. All geometry stays inferred/geometryVerified=false. Periods are composite snapshots, not proof that every illustrated element existed simultaneously throughout the date range; Byzantine southern access emphasizes a later context, and early Islamic southern access emphasizes an Umayyad context.

## Coherent rendering and ledger integration

Aelia has two authored district envelopes and three paths. Byzantine has four envelopes and three paths including a southern western-axis continuation. Early Islamic has four envelopes and three paths, including a southern administrative access context. Reserved precinct/core areas remain unfilled rather than receiving invented landmark buildings.

The existing district-constrained subdivision creates low coarse terrain-following cells, with road clearance and reservation exclusion. These are registered blocks, never semantic individual buildings. Their bottom/top vertices sample the same DEM; no independent flat ground, artificial ancient terrace or source height reconstruction is introduced. Each phase owns distinct IDs, and later object fate is unresolved rather than an invented reuse link.

The shared later publisher stages district/road/block records atomically, validates district parents and mesh bindings, and assigns stable per-object component IDs even where a road has many segments. Rebuilding preserves ledger event edits and definition checks. Scene cleanup retains owned-record behavior. Other later renderers remain unchanged.

The main scene suppresses the old arbitrary Herodian inherited overlay for Aelia. All three independent eras now own their scene; their unused legacy inheritance rules remain auditable instead of being treated as verified survival. Evidence filtering, common skeleton mapping and source/limitation panels use the same registration.

## Validation and remaining work

Real-data tests cover three different phase envelopes, common origin/schema, road clearance, reservation exclusion, slope-fitting/upward caps, non-semantic blocks, fixed IDs/geometry on rebuild, evidence return, invalid source/geometry rejection, district-parent rollback and cleanup. Existing eight-later-batch, inheritance and foundation tests remain. Full 18-era desktop/portrait browser checks verify nonempty district/path maps, zero unbound components and no legacy overlay in these three phases. Whole historical foundation acceptance remains false.

Remaining later eras, archaeological linework, complete city limits, defensible dated subphases, wall/water networks and public building geometry still require coherent work. Detail carving remains paused.

One local JS module and a roughly 13KB JSON are added; the JSON is fetched once through the existing shared loader. Geometry is generated locally on entering the selected phase, with no new image/model/terrain service or measured bandwidth/token/FPS saving claim.

The three eras share one camera window fitted to the union of their authored envelopes, with portrait-aware framing and refitting on resize. Moving between them keeps the comparison scale rather than independently zooming each city. Leaving the group restores the prior view. Coarse blocks/roads use an owned opaque material so legacy construction-opacity mutations cannot leak into this layer; the material is released with the phase geometry.

Browser evidence: Aelia publishes 37 records with 229 visible components; Byzantine 60/284; early Islamic 63/266. All visible components are bound, with zero unbound or out-of-phase IDs. The map reports 2/4/4 district envelopes and three routes for each phase. These counts describe generated design scope, not historic buildings or complete cities. Full 18-era desktop/portrait regression passes, errors=[], fullTimelineReady=false. Focused mobile return/filter checks and the shared-loader single-request assertion also pass. Roof triangle-centroid spot checks on the actual DEM show positive clearance for these layouts; they are not a full ancient-ground or every-face clearance certification.
