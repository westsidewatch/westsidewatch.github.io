# Doré image–type composition contract v1

Reference observations: zebra editorial poster supplied in conversation, followed by a text-free orange/white zebra proof. The proof successfully preserves dramatic crop and spot-ink halftone, but without the reference's left-edge vertical blue headline, its visual hierarchy is materially weaker. Therefore text and image must share a **layout contract**, while typography remains live HTML/CSS.

## Coordinate system
All placement values are percentages of the artwork container; origin (0,0) at top left, 100 × 100 at bottom right. CSS must use the same container coordinate system as the image generation brief. Do not confuse viewport coordinates with image coordinates.

## Contract: zebra editorial reference (demonstration only)
- canvas: portrait 3:4
- image layer: zebra head occupies approximately x=46–100, y=3–63; shoulder and torso sweep through x=0–100, y=37–100; natural open white field x=20–54, y=5–33
- typography lane: x=0–22, y=0–100, vertical oversized headline; text rendered by CSS, never pixels
- intentional overlap: the zebra torso enters the type lane around y=55–100
- foreground stacking: headline ABOVE the zebra where they cross, while preserving readable glyph contours
- label: small editorial issue marker near x=27, y=3
- print roles: one ink for image, a distinct second ink for type; white is the third active compositional component (unprinted paper)
- crucial difference: the blue title is not merely placed in empty space. It *collides* with the orange body and forms an independent vertical structure.

## Contract: Olive Mountain adaptation
- Retain the same spatial conflict, scale, crop, image/text separation and printing logic, but **do not import the reference's orange/blue palette**.
- artwork: deep olive #174B35, optional supporting olive #47735E, pure white #FFFFFF; text uses CSS with site-approved typography.
- CSS typography: Chinese display Chiron Hei, English Bodoni Moda Regular; never rasterize words into the generated image.
- CSS controls the size, orientation, z-index, overflow, mobile breakpoints, safe-area and responsive line breaks.
- The illustration prompt must include the intended title corridor, crossing region and negative-space geometry, but not ask the model to draw any lettering.
- If the speaker has no verified portrait reference, do not fabricate a recognizable speaker face.

## Validation
1. Check image-only asset has no letters or labels.
2. Check subject extends past at least one deliberate crop boundary.
3. Check negative space is contiguous, not a glued-on white caption bar.
4. Check the CSS headline intersects the image in a *designed* area without becoming illegible.
5. Check mobile crop and line breaks at narrow widths; avoid face occlusion.
6. Check Olive Mountain green/white palette, no gold, blue or orange leakage.
7. Review image and HTML/CSS **together**; image-only review is insufficient for editorial composition.

## Implementation contract
Keep the illustration and type layers separate in DOM. Prefer a single relative cover container with an object-fit image and an absolutely positioned typographic overlay; expose CSS custom properties for title lane, overlap, type rotation and mobile adjustments. Preserve accessible HTML text and alt text. Avoid baking decorative rules into images.

This document is a design contract, not proof that the current site already implements it.
