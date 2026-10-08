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

The shared non-Herodian parcel renderer is disabled by the startup-freeze rollback. Its startup audit remains non-mutating and labels those eras `deferred-render-check`. Preserve that boundary until generation can run without blocking interaction and period-specific geometry is reviewed.

The browser gate now checks `production.ok` for the canonical slice and verifies that `productionReady` still requires the complete phase audit. It must not turn the full-timeline readiness flag on merely to pass CI. It renders all 18 phases individually, records visible urban component counts and switching times, and saves each phase screenshot. This catches runtime failures and empty urban layers; it does not certify historical geometry, pixel quality or lifecycle continuity across all periods.

On the current production build, all 18 desktop phase checks pass without console/page errors. The Herodian city contains 1,067 buildings. Screenshot inspection shows the other eras still rely largely on schematic masses. Next implementation work needs bounded non-Herodian generation and reviewed continuity, rather than another global readiness claim.
