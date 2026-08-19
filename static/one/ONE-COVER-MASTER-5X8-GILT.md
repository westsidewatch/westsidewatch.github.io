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

The cover artwork must retain the upper and middle field for the illustration. The complete typography stack belongs in the lower field. The production master therefore uses one proportional shift token, `--one-cover-type-shift`, rather than book-specific offsets.

Canonical production parameters:

- desktop typography stack shift: `5.4cqw` downward from the previous baseline;
- mobile typography stack shift: `4.7cqw`;
- very narrow covers inherit the mobile rule and may reduce the shift only to prevent clipping;
- title, English book name, book metadata, separator, chapter number and chapter subtitle move as one system;
- no individual Bible book may introduce a local `top`, `bottom`, `translate`, negative margin or private font-size patch to reposition this stack;
- if the stack clips, fix the shared master or responsive type scale rather than moving one book independently.

The objective is the same as the approved reference: **the image remains dominant and the typography occupies the lower portion without covering the principal action unnecessarily.**

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

It remains an independent Westside Watch theological/brand symbol and may be used once where composition and meaning justify it. It must never be repeated as four corner ornaments.

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
4. the full typography stack sits in the approved lower field and does not unnecessarily cover the main Doré action;
5. corners are quieter than the title and image;
6. no modern star remains in the four corners;
7. the chapter-specific image is the correct canonical asset;
8. desktop and mobile preserve the same identity;
9. Doré originals and Studio · Doré continuations use the same cover grammar;
10. no book-specific positioning patch is required to pass.
