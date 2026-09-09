# C04 Refinement — 2026-09-09

User feedback: framework is approximately right, but overall design is inconsistent, design language is not precise/refined enough, style is immature, and the second-page scroll is not smooth.

Corrections applied:
- Keep C04 architecture and Candidate 01 color baseline.
- Do not redesign section colors.
- Make page 2 inherit Candidate 01 editorial vocabulary: typography hierarchy, dawn-gold index treatment, restrained borders, shadow/depth, paper/dark/olive/gold world logic.
- Remove the visual impression that page 2 is a separate tile product.
- Replace direct scroll-event transform writes with requestAnimationFrame interpolation.
- Give each horizontal current a stable continuous coordinate, inertia smoothing, and weighted travel distance.
- Preserve all-landscape layout, 8:5 horizontal rhythm, and the first-layer sequence after page 2.

This is a refinement of C04, not a new candidate.