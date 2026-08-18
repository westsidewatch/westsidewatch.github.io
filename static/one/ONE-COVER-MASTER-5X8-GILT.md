# ONE — Canonical Cover Master: 5:8 Gilt Book Cover

Status: **LOCKED / CANONICAL**

This document supersedes any earlier implementation that allowed the chapter cover to drift toward a square card or picture-frame appearance.

## 1. Cover proportion

The canonical ONE chapter cover is **5:8 portrait**.

Reason: the cover is a book object, not a dashboard card. The vertical proportion supports Doré engraving composition, title hierarchy, mobile scaling and the physical impression of an antique Bible volume.

Implementation rule:

- chapter cover container uses `aspect-ratio: 5 / 8`;
- responsive width may change, but the ratio does not;
- desktop must not widen the cover into a square or landscape card;
- mobile uses the same 5:8 identity;
- image cropping must be deliberate and may not destroy essential figures or theological action.

## 2. Frame concept

The gold treatment is **hot-stamped bookbinding**, not a picture frame.

The border must feel printed/tooled into an old cloth or leather book cover:

- two very fine gold rules;
- low visual weight;
- muted First Light / ONE gold;
- no glow;
- no bevel;
- no relief;
- no plaster, carved-moulding or ceiling-decoration appearance;
- no metallic 3D gradient;
- no heavy Baroque or Rococo mass.

## 3. Corner ornament

The four-corner modern star device is retired.

Canonical corner language:

- extremely small, flat, engraved foliate/acanthus turn;
- one or two restrained leaf gestures only;
- visually attached to the double rule rather than floating as an icon;
- symmetrical by corner but not mechanically perfect in texture;
- worn/broken foil marks may appear subtly to suggest age;
- ornament must disappear into the cover at normal reading distance and reward closer inspection.

The corner must never become the subject.

## 4. Age and material

The gilt is allowed to show restrained age:

- slight discontinuity;
- tiny loss of foil;
- uneven opacity;
- occasional fine abrasion.

Age is texture, not distress decoration. Do not simulate large scratches, fake dirt or theatrical antiquing.

## 5. Morning Star

The Morning Star is not part of the four-corner frame system.

It remains an independent Westside Watch theological/brand symbol and may be used once where composition and meaning justify it. It must never be repeated as four corner ornaments.

## 6. Illustration authority

The cover container and frame never determine chapter artwork identity. Illustration selection remains the responsibility of the canonical cover resolver.

For Revelation 2, the approved Studio · Doré FINAL asset is:

`REV-02-DORE-STUDIO-001` → Book 66, Chapter 2.

No historical Doré plate is assigned to Revelation 2. Therefore the Studio FINAL must resolve there and must not be replaced by an unrelated historical scene.

## 7. Cache/version discipline

Whenever a canonical cover CSS, frame asset or fixed Studio illustration changes, the production page asset version must be advanced or the deployment must otherwise force revalidation. A visually obsolete cached frame/image must not be mistaken for the current master.

## 8. Acceptance test

A cover passes only when:

1. proportion reads immediately as a book at 5:8;
2. gold reads as flat aged hot-stamping, not a picture frame;
3. corners are quieter than the title and image;
4. no modern star remains in the four corners;
5. the chapter-specific image is the correct canonical asset;
6. desktop and mobile preserve the same identity;
7. Doré originals and Studio · Doré continuations use the same cover grammar.
