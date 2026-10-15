# Doré Editorial Engraving Asset Engine

Status: THIRD CURRENT WORKSTREAM — PLANNED, NOT IMPLEMENTED
Date: 2026-10-15

## Scope
Doré Motion is a reusable site-wide engraved-visual production engine, not only an animation tool. It must support: (1) animated engraving backgrounds for seven sections; (2) subtle, source-faithful animation of Doré Bible illustrations for ONE and Emmaus; (3) editorial engraving illustrations and ornaments for Westside Watch magazine; (4) small three-dimensional engraved objects for site UI and articles. Later film use is a downstream beneficiary, not current production scope.

## Three interoperable capabilities
1. Motion Engraving — layered 2D engravings, parallax, ambient lighting/weather, region masks, reduced-motion fallback.
2. 3D Engraved Objects — reusable 3D mesh assets with curvature-aware line shading, controlled lighting, orbit camera and static/animated export. Candidate motifs: olive branch, lamp, scroll, coin, vessel, column, key, trumpet. Each requires an original or rights-cleared model.
3. Editorial Engraving — composition templates for covers, article illustrations, section dividers, ornamental details, hero compositions and consistent multi-angle asset variants.

## Asset contract
Each asset has a stable ID, source/provenance/rights, source model or immutable image, scene and camera parameters, light/material/engraving preset, output variants (SVG/PNG/WebP/video or web renderer where appropriate), alt text, safe-area metadata, reduced-motion alternative, usage mapping and version. Export must not claim vector SVG where renderer only outputs raster; vector paths require explicit extraction.

## Architecture
One modular rendering and asset pipeline governed by the existing Design OS, with per-page and per-section parameter overrides; do not establish a second typography/color/CSS authority. Separate immutable sources, reusable motion/shading presets, composition layouts and output assets. Batch generation and visual QA, responsive and performance budgets.

## Phased acceptance
A. Finish approved Living Water v2 directional flow.
B. Investigate engraved Ocean 3D independently.
C. In third workstream, pilot one animated Doré Bible illustration, one animated background and one engraved 3D object; confirm style consistency, reuse rights, performance and reduced motion.
D. Integrate accepted results into ONE, Emmaus and one magazine editorial page; then scale to seven sections and growing illustration corpus.
E. Preserve transferable masks/cameras/shots for possible future film use; no film project modification now.

## Research caution
ai-sci-computing/hatching is publicly readable but its README restricts commercial use; do not copy its code into site production without permission. Other 3D NPR implementations need separate license and capability checks.

## Long-term R&D asset designation
Doré Motion is a **strategic, long-term, cumulative research-and-development asset of Westside Watch**, not a one-off visual effect or a project that ends with a single release. Maintain it through versioned algorithms, reusable source and scene metadata, evaluated open-source dependencies and licenses, stable asset IDs, visual regression baselines, documented experiments (including failures), and production-ready presets. Each milestone must deliver independently usable site value while adding transferable capabilities. Immediate production benefits (Living Water, seven sections, ONE, Emmaus, magazine) take priority; a future Bible-film pipeline is a potential beneficiary but must not become a blocker or distort near-term acceptance criteria. Keep governance within the existing Design OS and existing project register, avoiding a competing design system.
