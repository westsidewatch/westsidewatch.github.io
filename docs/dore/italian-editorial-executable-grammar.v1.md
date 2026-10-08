# Italian Editorial Grammar — executable image and layout brief v1

Status: experimental specification. This is a new implementation proposal, not a claim that all historic Italian-editorial modules already conform.

## Operating rule
Do not ask an image model to "make it editorial". The design compiler decides a complete page before image generation: focal subject, crop, whitespace, ink roles, layer crossings, typography coordinates, and responsive behavior. The image model receives a **text-free illustration brief**. HTML/CSS renders the real text.

## Inputs
- editorial subject and factual constraints
- intended format and aspect ratio
- available verified subject references and permissions
- site-specific approved palette and type tokens
- image treatment: halftone, engraving, photography, collage, or mixed
- design family and content priority
- desktop/mobile crop constraints

## Design plan, in this order
1. **Visual proposition**: one sentence describing the deliberate spatial tension, not an aesthetic adjective.
2. **Composition grid**: normalized 0–100 coordinates, focal point, subject bounding region, type corridors, crossing regions and safe areas.
3. **Crop instruction**: exactly which edges sever the subject; required minimum subject recognizability; scale relative to canvas.
4. **Negative-space shape**: a connected, located region with approximate area; specify what MUST remain empty and why.
5. **Ink/color roles**: background, subject, text, accent, knockout; strict permitted hex values, max inks, and where each ink is used.
6. **Material technique**: dot screen angles/density for halftone, directional hatch density for engraving, photographic grain if appropriate; no generic filter adjectives.
7. **Type as composition**: live HTML/CSS family, weight, orientation, bounds, line-break policy, stacking order and overlap; no letters in image pixels.
8. **Responsive reinterpretation**: separate mobile art-direction crop; do not merely shrink desktop.
9. **Quality gates**: image integrity, subject fidelity, palette, intentional overlap, legibility, mobile and publication approval.

## Four explicit composition recipes
### A. Overscale collision
- Canvas 3:4. Subject x=35–125, y=10–115, intentionally cropped at right and bottom.
- Vertical headline corridor x=0–21, y=0–100; image crosses into lane around y=65–100.
- Continuous negative space x=20–55, y=3–32.
- Typography z-index above image in crossing region.
- Failure: subject neatly centered, title isolated in a footer bar, empty margin without visual purpose.

### B. Quiet field / isolated fragment
- Canvas 3:4. One small but sharply rendered object occupies x=67–105, y=35–90.
- White field covers roughly 55–65%; text is anchored within x=7–56, y=8–65.
- One intentionally severed object boundary; no scattered ornaments.
- Failure: background filled with extra scenery or arbitrary texture.

### C. Monumental interruption
- Canvas 3:4. One large architectural/organic form x=-20–75, y=-25–120.
- Primary vertical axis is cut at top and bottom; contrasting open column x=75–100.
- Type sits across a controlled contour edge, never over essential facial features.
- Failure: centered symmetrical facade or generic decorative border.

### D. Two-scale encounter
- Overscale foreground x=-20–58, y=25–115; small distant object x=72–90, y=42–63.
- Large uninterrupted negative field between them; type bridges the spatial interval.
- Failure: conventional scenic background with uniformly distributed details.

Coordinates are art-direction defaults, not absolute template law. The compiler must record which values were selected and why.

## Color is a design system, not a filter
Declare per-project ink roles. Example for Olive Mountain ONLY:
- paper #FFFFFF = active knockout/light/whitespace
- primary ink #174B35 = foreground contours and focal darks
- secondary ink #47735E = sparse midground marks, optional
- typography uses approved site CSS, never baked into the image
Do not generalize Olive Mountain's colors to other projects. The zebra reference uses an orange subject ink and a blue text ink: its important transferable principle is **separate color functions and controlled overprint**, not its exact colors.

## Required outputs
- `art-direction.json`: composition geometry, crop, palette, ink roles, reference provenance, type lane, overlap, mobile variant.
- `image-prompt.md`: specific scene, geometry, material and exclusions; absolutely no typography.
- `css-layout-contract.md`: actual live typography and stacking specification.
- `acceptance.md`: pass/fail checklist plus manual editorial sign-off.

## Reference-driven test: zebra poster
The supplied reference has a giant zebra cropped by right and lower boundaries, orange halftone image ink, huge blue vertical type on the left, and a white field. The text-free proof retains much of the image grammar but loses the typography collision. A complete test must therefore compare the image AND its CSS overlay together. Do not use a successful image-only render as evidence that the magazine composition is finished.

## Rejection criteria
Reject generic "Italian magazine style" without coordinates; centered hero portrait; random decorative olive branches; indiscriminate gradients; incorrect brand palette; text embedded in image; uniform margins; hard white footer strips; illegible mobile text; and invented identities. Do not publish without a reviewed visual proof.
