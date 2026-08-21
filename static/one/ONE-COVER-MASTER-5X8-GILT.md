# ONE — Canonical Cover Master: 5:8 Gilt Book Cover

Status: **LOCKED / CANONICAL**

This document supersedes any earlier implementation that allowed the chapter cover to drift toward a square card, picture-frame appearance, or per-book typography placement.

## 1. Cover proportion

The canonical ONE chapter cover is **5:8 portrait**.

Reason: the cover is a book object, not a dashboard card. The vertical proportion supports Doré engraving composition, title hierarchy, mobile scaling and the physical impression of an antique Bible volume.

Implementation rule:

- chapter cover container uses `aspect-ratio: 5 / 8`;
- responsive width may change, but the ratio does not;
- desktop must not widen the cover into a square or landscape card;
- mobile uses the same 5:8 identity;
- image cropping must be deliberate and may not destroy essential figures or theological action.

## 2. Approved visual-reference geometry

The approved concept/reference image is now treated as a **measurement reference**, not merely a moodboard.

The cover artwork must retain the upper and middle field for the illustration. The typography uses two shared proportional anchors rather than free-flowing flex-end placement or book-specific offsets.

Canonical production parameters:

- desktop book/title block starts at `64.5%` of cover height;
- desktop chapter block starts at `78.8%` of cover height;
- mobile book/title block starts at `63.5%`, chapter block at `79.2%`;
- very narrow 5:8 covers may use `62.5% / 79.6%` to preserve the same visual hierarchy without clipping;
- the Chinese title, English title and book metadata remain one book/title block;
- the separator, chapter label/number and chapter subtitle remain one chapter block;
- the Morning Star sits higher with the chapter block, preserving a clear lower safe area inside the gilt border;
- both anchors belong only to the shared master; no individual Bible book may introduce a local `top`, `bottom`, `translate`, negative margin or private font-size patch to reposition them;
- if a long title clips or collides, fix the shared responsive type scale or shared anchors rather than moving one book independently.

The objective is the same as the approved reference: **the main Doré action remains dominant while the title sits around the lower third and the chapter information remains clearly inside the lower gilt field rather than sinking toward the edge.**

## 3. One Dawn Gold

All cover gilt is one colour token:

`--one-dawn-gold: #cebd74`

This token is the sole colour authority for:

- Chinese book title;
- English book title;
- book metadata;
- separator rule;
- chapter label and number;
- chapter subtitle;
- double border and corner ornament.

Older independent gold values such as highlight/lowlight variants may remain only as aliases to `--one-dawn-gold`; they must not produce visibly different golds on the cover. Difference in visual weight may come from opacity, size or line weight, not from changing hue.

The transparent frame master is rendered as a mask filled by `--one-dawn-gold`, so the frame and typography cannot drift into different gold colours.

## 4. Frame concept

The gold treatment is **hot-stamped bookbinding**, not a picture frame.

The border must feel printed/tooled into an old cloth or leather book cover:

- two very fine gold rules;
- low visual weight;
- Dawn Gold / ONE gold only;
- no glow;
- no bevel;
- no relief;
- no plaster, carved-moulding or ceiling-decoration appearance;
- no metallic 3D gradient;
- no heavy Baroque or Rococo mass.

The cover uses a nested antique-binding hierarchy: fine outer rules, a broad exposed field of green binding cloth, then an inset foliate gilt panel. When chapter art is present, it is mounted beneath that inset panel rather than bleeding to the physical cover edge; the inward-facing leaves overlap only the image margin. A book-only cover removes the image but preserves exactly the same green field and frame geometry.

Typography has two shared modes within that fixed frame. Illustration covers keep the book and chapter text in the lower field so the central action remains readable. Book-only covers center the complete title group within the empty green field. This is a global two-mode rule, never a per-book positioning exception.

Gold typography and gold ornament must never overlap, touch or visually merge. Illustration-cover text stays inside the dark central safe field above the inward-pointing bottom leaves and between the side-leaf tips. Book-only centered text obeys the same inner safe field. A clear band of uncovered binding or image tone must remain between every glyph and the nearest gilt ornament.

## 5. Corner ornament

The four-corner modern star device is retired.

Canonical corner language:

- extremely small, flat, engraved foliate/acanthus turn;
- one or two restrained leaf gestures only;
- visually attached to the double rule rather than floating as an icon;
- symmetrical by corner but not mechanically perfect in texture;
- worn/broken foil marks may appear subtly to suggest age;
- ornament must disappear into the cover at normal reading distance and reward closer inspection.

The corner must never become the subject.

## 6. Age and material

The gilt is allowed to show restrained age:

- slight discontinuity;
- tiny loss of foil;
- uneven opacity;
- occasional fine abrasion.

Age is texture, not distress decoration. Do not simulate large scratches, fake dirt or theatrical antiquing.

## 7. Morning Star

The Morning Star is not part of the four-corner frame system.

It remains an independent Westside Watch theological/brand symbol and may be used once where composition and meaning justify it. It must never be repeated as four corner ornaments. In the approved lower-field geometry it sits below the chapter text and inside the lower gilt border, never between or on top of title lines.

## 8. Illustration authority

The cover container and frame never determine chapter artwork identity. Illustration selection remains the responsibility of the canonical cover resolver.

For Revelation 2, the approved Studio · Doré FINAL asset is:

`REV-02-DORE-STUDIO-001` → Book 66, Chapter 2.

No historical Doré plate is assigned to Revelation 2. Therefore the Studio FINAL must resolve there and must not be replaced by an unrelated historical scene.

## 9. Cache/version discipline

Whenever a canonical cover CSS, frame asset or fixed Studio illustration changes, the production page asset version must be advanced or the deployment must otherwise force revalidation. A visually obsolete cached frame/image must not be mistaken for the current master.

## 10. Acceptance test

A cover passes only when:

1. proportion reads immediately as a book at 5:8;
2. gold reads as flat aged hot-stamping, not a picture frame;
3. frame and every cover text element visibly use the same Dawn Gold;
4. the book/title block and chapter block sit on the shared approved lower-field anchors and do not unnecessarily cover the main Doré action;
5. title, chapter subtitle and Morning Star remain inside the lower gilt border on desktop and mobile;
6. corners are quieter than the title and image;
7. no modern star remains in the four corners;
8. the chapter-specific image is the correct canonical asset;
9. desktop and mobile preserve the same identity;
10. Doré originals and Studio · Doré continuations use the same cover grammar;
11. no book-specific positioning patch is required to pass.
