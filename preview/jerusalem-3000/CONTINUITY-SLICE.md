# Canonical Herodian destruction slice

This slice owns the Herodian and Roman destruction display. It is an integration baseline, not completion of the full historical city.

- Generate parcel architecture once. Keep building IDs, footprints and geometry instances when scrubbing through destruction and back.
- Roads use the same provisional registration linework as the block subdivision. Evidence monuments retain separate object batches and source labels.
- Reserve the currently rendered Temple platform and Antonia footprints before generating residential parcels. These exclusion bounds constrain the reconstruction; they are not archaeological surveys.
- Disable the legacy temporal boxes, calibration city and independently regenerated inheritance models in this slice.
- Ruin is a reversible vertical collapse towards each object's terrain anchor. It is a schematic transformation, not a sourced simulation of individual collapse or debris.
- At Aelia, canonical Herodian architecture is hidden. The established era morphology renders a separate provisional layer. Roman replacement architecture, burial depths and reuse links still require sourced object records; this is not verified object continuity.
- Other periods still use the prior morphology paths. Full-timeline completion must remain false until their object continuity is verified.

## Validation

`node scripts/verify_jerusalem_3000_city_lifecycle.mjs` tests stable identity, reversible transforms, fractional phase boundaries, monument exclusions, evidence filtering and failed-core readiness.

With Playwright installed, serve the repository and run `node scripts/verify_jerusalem_3000_browser.mjs`. `J3K_URL` selects the proposed build or deployed site; `J3K_OUTPUT` selects the evidence directory. The same test is run before merge and after deployment, with desktop/mobile screenshots and a deliberately unavailable city registration to verify that core failures cannot silently fall back to a successful legacy scene.

## Current rendering boundary (2026-10-08)

The former all-era synchronous parcel renderer was disabled by the startup-freeze rollback. A bounded first-temple/Babylonian slice now uses the shared parcel pipeline on demand. Its startup audit remains non-mutating and labels those eras `deferred-render-check`. The other non-Herodian eras retain that boundary pending bounded generation and period-specific geometry review.

The browser gate now checks `production.ok` for the canonical slice and verifies that `productionReady` still requires the complete phase audit. It must not turn the full-timeline readiness flag on merely to pass CI. It renders all 18 phases individually, records visible urban component counts and switching times, and saves each phase screenshot. This catches runtime failures and empty urban layers; it does not certify historical geometry, pixel quality or lifecycle continuity across all periods.

On the current production build, all 18 desktop phase checks pass without console/page errors. The Herodian city contains 1,067 buildings. Screenshot inspection shows the other eras still rely largely on schematic masses. Next implementation work needs bounded non-Herodian generation and reviewed continuity, rather than another global readiness claim.

## Bounded shared first-temple slice

`shared-era-runtime.js` generates late-first-temple architecture only when that phase or Babylonian destruction is requested. Architecture generation yields after at most four parcels or an 8 ms elapsed batch budget; a single parcel remains synchronous. Cancellation occurs when leaving the slice, releases staging geometry, and never attaches a partial city. The ready city is retained for exact return visits.

Both phases use the same building IDs, meshes and footprints. Babylonian destruction samples its own time boundary rather than the Roman destruction boundary. Standing structures collapse towards their terrain anchors; roads remain as infrastructure. The prior independent inheritance model and temporal boxes are disabled in this slice. This is schematic object inheritance, not sourced burial/reuse depths or simulated individual debris.

The registration transforms the existing provisional road/district scaffold using the legacy first-temple envelope. Every generated building remains inferred. The caption explicitly discloses that roads, parcels and residences are not archaeologically registered. No full-timeline readiness claim is made, and the startup phase audit still defers historical validation.

`node scripts/verify_jerusalem_3000_shared_era.mjs` compares batched geometry with the synchronous builder, checks deterministic IDs and inherited phase membership, cancellation cleanup, surfaced errors and independent destruction boundaries. The browser test adds rapid cancellation, shared-identity and reverse-transform checks, legacy-layer exclusion, desktop/mobile shared screenshots and the existing all-18-phase smoke test.

## Persian retained fabric (2026-10-08)

The first-temple shared runtime also accepts direct entry into `persian-nehemiah`. It registers the same building IDs in that phase as a hypothetical retained ruin layer, with the complete Babylonian collapse held fixed. No new first-temple geometry is generated when switching from destruction to Persian rebuilding.

The Persian morphology remains a separate provisional reconstruction. The “前代遺存 · 推定” button enables comparison with earlier ruins; it is off by default and remains subject to evidence filtering. Roads are withheld in this successor layer because their Persian continuity has not been established. Buildings retain their terrain anchors without invented burial depths. The layer does not identify which ruins actually survived, which buildings were reused, or the sourced Persian settlement envelope.

Browser validation checks identity preservation, ruin state, coexistence with successor morphology, evidence filtering, hiding the overlay, and direct Persian entry on mobile. This advances the lifecycle interface; Persian replacement architecture and sourced burial/reuse links remain unfinished. Full-timeline readiness remains false.

## Bounded Persian replacement (2026-10-10)

Persian residential fabric now uses the same bounded parcel/architecture generator as the first-temple city, with the existing smaller provisional Persian envelope. On completion it replaces legacy era morphology, temporal boxes and the separate inherited city model. Partial batches remain hidden and cancel when leaving the phase; cached meshes and IDs are restored on return. Direct Persian entry builds both the successor and earlier retained layer without requiring a prior visit.

Persian objects have distinct phase-specific IDs. No proximity-based predecessor/reuse links are invented. The optional earlier ruin layer still uses the original first-temple IDs and full collapse. Both layers are inferred and hidden by the observed evidence filter. The transformed road/district scaffold is still not a sourced Persian survey; the historical settlement envelope, Nehemiah wall variants and burial/reuse records remain unfinished. Full timeline readiness stays false.

## Bounded Hellenistic–Hasmonean expansion (2026-10-11)

The next expansion phase uses the same bounded generator and existing provisional Hellenistic footprint. Completed architecture replaces legacy morphology, temporal boxes and the independent inheritance model. Direct entry builds only the requested expansion city; it does not eagerly generate first-temple/Persian geometry. Leaving cancels staging, and returning reuses completed IDs and meshes.

Persian and expansion buildings have distinct phase-specific IDs. No spatially guessed reuse links or historical parcel continuity are asserted. Evidence filtering keeps both provisional cities out of the observed-only view. Roads and district extents still require sourced period-specific registration. This step replaces the runtime rendering path, not historical certification or full-timeline completion.

The browser gate checks Persian/expansion round trips, phase isolation, cancellation/retry, identity/transform preservation, observed filtering, and direct mobile expansion entry without eagerly building earlier cities.

## Begin with the earliest settlement

The earliest phase has its own small ridge/spring scene instead of scaled Herodian roads and parcels. A mapped modern Gihon spring point anchors illustrative dwellings upslope; modern DEM triangles ground the footings and narrow footpath. Fourteen dwellings is a scene design choice, not a historical house count. Their shapes, roofs and positions remain inferred. No fortification or monumental footprints are supplied for this stage.

A close camera makes the small settlement readable. Leaving restores the prior broad-city camera and minimum orbit distance. Legacy residential and temporal/inheritance layers are disabled only for this early phase. Observed-only mode hides the illustrative settlement. Source context and limitations are stored in `data/settlement/earliest.v1.json`; neither the modern map point nor DEM proves ancient ground levels or excavated house locations.

Node validation checks rendered triangle sampling, footings, phase/evidence isolation and disposal. Browser validation checks desktop/mobile initial views, no legacy overlap and all 18 era renders. The earliest scene remains a landscape-constrained illustration requiring archaeological footprint work.
