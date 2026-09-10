# P1 exact motion baseline

Before any Living Water adaptation, P1 is reset to the unmodified upstream interaction.

- Upstream project: `gwen-bo/codrops-grid-to-preview`
- License: MIT
- Demo: `https://tympanus.net/Tutorials/GridToFullPreview/`
- Source files inspected: `src/index.html`, `src/styles/shop.scss`, `src/js/product-grid.js`, `src/js/product-preview.js`

Pinned behavioural invariants for the next adaptation pass:

- 8 items, 4 columns × 2 rows
- 5vw row/column gutter
- two independent 2×2 preview overlays
- left/right product grouping by grid column
- 100ms mouseenter debounce
- cards move inward by ±2.5vw
- preview scale compensates for the 5vw gutter
- cross-shaped clip-path calculated from the preview rectangle on resize
- GSAP timeline with `power2.inOut`
- timeline reverses on mouseleave
- preview gallery cycles images every 0.5s

Do not replace this baseline with custom slice assembly. Adapt content only after this exact interaction has been accepted.
