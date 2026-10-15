# Engraving Ocean 3D — Phase 2 Research

Status: DISCOVERY / NOT APPROVED / NOT INTEGRATED
Date: 2026-10-15

## Observation and hypothesis
The original continuous-field lab unexpectedly suggested two overlapping 3D cloth-like wave surfaces. The user hypothesizes that directional crossing between upper/lower engraving contours created depth. This is a hypothesis, not yet a measured causal finding. Adding interpolated lines flattened the appearance; uniform duplication also did not reproduce the original impression.

## Variables to isolate
- Local tangent crossing angle Δθ(x,y), not merely global image rotation.
- Overlap extent and position, line density, opacity/occlusion, local curvature.
- Relative phase, directional propagation, camera perspective and temporal stability.
- Avoid treating moiré interference as proof of 3D geometry.

## Research leads (evaluate license and implementation before adoption)
- https://github.com/jbouny/fft-ocean — FFT ocean / projected grid.
- https://github.com/Skittss/FFTOcean — stylized FFT ocean.
- https://github.com/squall01337/abyssal-ocean — ocean WebGL experiment; verify license before reuse.
- https://github.com/reed-soul/SeedOcean — stylized ocean / Gerstner and FFT; verify implementation/license.
- https://github.com/philogb/LIC — line-integral convolution flow visualization.
- https://github.com/aljazfrancic/generative-art-gallery — interference and flow-field examples.

## Proposed controlled experiment
Preserve the original twisting lab. Compare a controlled crossing-angle/overlap study against it while holding all other variables fixed. Measure actual SVG tangent angle distributions and capture time-sequenced renders. If 2D crossing cannot maintain stable depth, test mapping engraving lines onto a real Gerstner/FFT surface. No changes to v2 during research.

## Gate
Phase 2 begins only after Phase 1 flow is accepted and live.
