# Doré Bible Illustration Motion — Reusable Corpus Program

Status: ACTIVE THIRD WORKSTREAM / DESIGN AND RESEARCH; NO ILLUSTRATIONS CONVERTED YET
Date: 2026-10-15

## Mission and consumers
Build a reusable, faithful **still-illustration-to-motion** pipeline for Gustave Doré's Bible engravings. This is the highest-value component of the third current workstream (Doré Motion Engraving System). Immediate consumers: ONE Bible-study experience and the Emmaus section; later all seven sections and future *Shadow of the Cross* / full Bible narrative cinematics. This is NOT authorization to begin film production now.

## Corpus scale and rights
Plan for 200+ source engravings as a **target corpus, not a verified available inventory**. Audit source edition, image provenance, scan quality, page/caption metadata, and jurisdiction-specific rights for each image; verify any hosting/reproduction restrictions. Do not overwrite or distort source scans. Link to approved external assets where possible, consistent with site asset strategy.

## Canonical record per illustration
Stable illustration ID; biblical book/chapter/verse and scene; Doré original title; edition/source/provenance; asset URL or repository pointer; source dimensions and crop; rights review; subject/background/foreground segmentation and depth layers; subject masks; focal point and text-safe zones; proposed motions and camera limits; loop duration and reduced-motion fallback; motion preset ID; optional future film shot/sequence tags; acceptance status and version. Original scan remains immutable.

## Animation vocabulary (conservative, source faithful)
- Camera: subtle parallax, controlled push/pull, gentle pan; avoid fake full 3D rotation where unseen geometry would be invented.
- Atmospheric: clouds, fog, shafts of light, water, fire/smoke, rain, dust.
- Local subject: minimal fabric, hair, vegetation, distant crowd movement only where credible and does not deform the original drawing.
- Engraving: maintain stable hatching direction, stroke weight, silhouette, texture and facial anatomy. No rubbery warps, jittering crosshatches, sliding layers, visible holes, or mismatched perspective.
- Seamless loops with intentional motion hierarchy, adjustable per image, performance and reduced-motion fallback.

## Proposed shared architecture
1. Non-destructive source ingestion and scene metadata.
2. Depth/mask/semantic-region annotations (reviewed, not blindly assumed).
3. Motion preset library + per-image parameter JSON.
4. Browser renderer integrated with existing Design OS; per-section overrides without global CSS or independent design system.
5. Automated visual regression/performance checks plus human scene-level acceptance.
6. Exportable motion descriptions, masks, camera paths, shot IDs and versioned assets for future cinematic reuse.

## Rollout and gates
A. Audit existing Doré illustration corpus and ONE/Emmaus presentation and asset paths; establish verified inventory.
B. Pilot three distinct engraving types (landscape/atmosphere, figure-centered, architecture/interior) as independent experiments, without touching accepted site pages.
C. Integrate first accepted illustration into ONE and one into Emmaus; measure readability, responsive behavior, loop quality and reduced-motion.
D. Scale in batches across verified corpus, using shared presets and explicit QA rather than bespoke animation code per image.
E. Preserve shot-ready metadata for future film work; film engine, acting, lip sync and full 3D scene reconstruction remain out of scope.

## Relationship to current priorities
1. Complete and deploy Living Water v2 directional flow.
2. Investigate Engraving Ocean 3D independently.
3. Build site-wide Doré Motion Engraving System; **prioritize Bible illustration animation** for ONE and Emmaus, alongside seven-section animated engraved backgrounds.
4. Film engine later; prepare transferable metadata now, do not modify film project.

## Research references
- https://github.com/ai-sci-computing/hatching (research only; README restricts commercial use without written permission; 3D mesh hatching is NOT itself still-image animation).
- https://github.com/CreativeInquiry/ApparentRidges (research lead for future 3D outlines).
- https://github.com/mightyhorst/threejs-hand-sketching (research lead; verify licensing).

## Success criteria
One original scan can produce an approved, restrained motion variant using reusable presets and data, while the original remains unchanged; same pipeline can apply to a growing, rights-cleared corpus, render on site, and retain reusable film-oriented scene metadata.
