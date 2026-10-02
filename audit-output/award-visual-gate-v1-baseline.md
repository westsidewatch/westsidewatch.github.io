# Award Visual Gate v1 — Baseline

Scope: current Westside Watch home layer only. No information-architecture rewrite in this pass.

## P0 — static composition

- The cover currently carries masthead, volume marker, giant title, Chinese line, verse, two entry links, film control and wall motif in one viewport. Preserve all content, but reduce simultaneous visual competition.
- Film begins at 32% on desktop while the title occupies 65%; the overlap is useful, but the transition between paper field and moving image should read as one composition rather than two adjacent panels.
- The four current rows are structurally repetitive. Keep the river system but create stronger rhythm through scale, spacing and editorial hierarchy rather than adding decoration.
- Confluence has the strongest single image gesture. Its surrounding copy should remain quieter so the four-window image carries the scene.

## P0 — typography / whitespace

- Preserve Cormorant Garamond for English display and the established Chinese family, but tighten the number of simultaneous type scales.
- Navigation, eyebrow, metadata and controls need a consistent small-text system.
- Chinese supporting copy should remain visibly secondary to English display type without becoming faint or cramped.
- Increase ceremonial negative space around major transitions instead of filling it with extra labels.

## P1 — material / color

- Preserve temple-stone / living-paper material and Dawn Gold accent.
- Avoid additional opaque panels. Depth should come from image, paper, engraving line and light rather than card UI.
- Reduce sepia/filter stacking where it flattens image depth.
- Gold should mark hierarchy or interaction, not become a general border color.

## P1 — motion

- Motion must follow reading order: cover image breath → title/verse → current flow → confluence assembly.
- Existing perpetual river and track motion should be subordinate to user scroll and pause on direct interaction.
- No motion should be required to make the static composition understandable.
- Reduced-motion mode remains a first-class rendering, not a fallback.

## P1 — interaction

- Replace generic outline-like hover emphasis with editorial state changes: image crop, line reveal, controlled type shift, or Dawn Gold accent.
- Keep focus-visible unmistakable for keyboard use.
- Film pause control should read as utility, not as a third primary CTA.

## Mobile gate

- Do not merely collapse desktop. Recompose cover hierarchy for portrait reading.
- Prevent nav wrapping from becoming the first visual event.
- Keep title, Chinese line and verse readable over the film without heavy opaque overlays.
- Current tiles should preserve editorial cropping and avoid becoming generic horizontal cards.

## Acceptance

A desktop and mobile still frame must each work before motion is evaluated. No new effect is accepted if it increases visual noise, weakens hierarchy, introduces generic card UI, or erases the existing Westside Watch identity.
