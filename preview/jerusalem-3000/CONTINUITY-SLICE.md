# Canonical Herodian destruction slice

This slice owns the Herodian, Roman destruction and Aelia residue display. It is an integration baseline, not completion of the full historical city.

- Generate parcel architecture once. Keep building IDs, footprints and geometry instances when scrubbing through destruction and back.
- Roads use the same provisional registration linework as the block subdivision. Evidence monuments retain separate object batches and source labels.
- Reserve the currently rendered Temple platform and Antonia footprints before generating residential parcels. These exclusion bounds constrain the reconstruction; they are not archaeological surveys.
- Disable the legacy temporal boxes, calibration city and independently regenerated inheritance models in this slice.
- Ruin is a reversible vertical collapse towards each object's terrain anchor. It is a schematic transformation, not a sourced simulation of individual collapse or debris.
- At Aelia, the prior objects remain as ruins. Roman replacement architecture, burial depths and reuse links require sourced object records and are not implemented by this slice.
- Other periods still use the prior morphology paths. Full-timeline completion must remain false until their object continuity is verified.

## Validation

`node scripts/verify_jerusalem_3000_city_lifecycle.mjs` tests stable identity, reversible transforms, fractional phase boundaries, monument exclusions, evidence filtering and failed-core readiness.

With Playwright installed, serve the repository and run `node scripts/verify_jerusalem_3000_browser.mjs`. `J3K_URL` selects the proposed build or deployed site; `J3K_OUTPUT` selects the evidence directory. The same test is run before merge and after deployment, with desktop/mobile screenshots and a deliberately unavailable city registration to verify that core failures cannot silently fall back to a successful legacy scene.
