# All-era validation readiness recovery

The previous full city run45336715072 failed at two old assumptions. These changes repair the validation contract, not the models or camera.

1. The all-era foundation loop waited for the requested phase number but did not wait for asynchronous city publication. It could inspect an unfinished phase, fail the nonempty common-mass check and never write `phase-report.json`. The later audit then failed because that report was absent. The loop now additionally waits for `cityGenerationStatus === 'ready'`; its positive mesh, phase-ownership and foundation checks remain.
2. The residential distance test demanded different pixels in every overview. After city framing improved, the first settlement is viewed entirely within the near band, where original pixels are deliberately preserved. The test now requires identical pixels for a near-only scene and changed pixels for scenes with middle/far housing. Every phase must still restore the exact original rendered image and retain housing, landmark and render-cost accounting. The independent GPU fixture still proves the near identity, far pixel change and unchanged geometry/draw costs.

Local residential proof: all18 phases; first settlement near-only;17 actual city distance-layer differences; exact switch restoration; phone and evidence checks. The isolated GPU fixture changes36 far pixels, preserves near pixels and uses identical1 draw/24 triangle counts. These are fixture costs, not whole-city performance measurements.

The complete local foundation browser suite also passed:18 rendered phases,7 staged samples,4450 registered buildings and zero reported errors. It now writes `phase-report.json` successfully. Historical full-timeline acceptance remains false.

This package makes no new visible city change or historical geometry claim. Continue using the terrain preview to review the previous visual work. Full new-head CI is authoritative only after it completes; passing these two local suites is not a claim that every workflow has passed.
