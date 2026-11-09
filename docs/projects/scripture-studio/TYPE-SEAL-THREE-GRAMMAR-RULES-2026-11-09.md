# Scripture Seal — Three compositional grammar laws / 三條鉛字語法

**Date:** 2026-11-09
**Status:** user-approved direction for the Scripture Studio generator; not an approved completed artwork.
**Reference:** study 07, *Dream Pool of Gutenberg* / 古騰夢溪, Onion Design.
**Supersedes:** V1–V5 independent side-by-side Chinese/English layout, two separate stamp solvers, and the erroneous conception that each language takes its own row or dedicated half.

## Rule 1 — One forme, two reading orientations / 同一印版，兩個閱讀方向

There is **one** source letterpress composition, not two independent poster designs. Rotating the entire forme 90 degrees produces two viewing states with fixed relative glyph positions. Do not reflow after rotation.

- Chinese-reading orientation: Chinese is conventionally vertical and legible; Latin type appears vertical/sideways and functions primarily as visual type material.
- English-reading orientation: English is normally horizontal and legible; Chinese vertical characters appear sideways and serve primarily as visual material.

Yin/yang paper-versus-ink reversal is a separately controlled visual polarity, not a substitute for rotating the same composition.

## Rule 2 — Primary reader / 次要語言作印面構成

Only one language needs to be immediately readable in a given orientation. The counter-language retains its real glyphs and type runs, yet is allowed to function as texture, density, spacing and type-shape contrast. Do not falsify Scripture quotations: all words must remain exact source excerpts, with complete source available in a separate readable Folio/biblical text surface.

## Rule 3 — **Same interleaved typographic run** / **中英在同一排交替咬合**

**Mandatory:** Chinese and English must be **interleaved within the same compositional line/run**, not assigned to separate rows, columns or page halves.

Conceptual input example (editor-selected, not a claim of an original Bible translation):
`信道 | faith | 從聽道 | cometh`

This is a **single alternating sequence** with four typed segments (ZH, EN, ZH, EN). The sequence is laid out with shared position/advance calculations and intentional optical adjustments in **one** mother forme. The actual Chinese and English phrases may not be word-for-word translations in the same order; editorial selection of interleaving is an artistic composition decision, never an instruction to alter canonical Scripture.

- Every next segment's position is computed **from the measured advance and ink bounds of preceding segments**, including rotated-run geometry; it is not drawn in a wholly independent rectangle.
- The interleaved **one-row** logic refers to a common typesetting sequence/track; local registered returns or additional lines can exist for long texts, but must be meaningful and obey the same shared interleaving logic. Do not cheat by placing all Chinese fragments in a Chinese row and all English fragments in a Latin row.
- Preserve Chinese semantic spans and English whole-word/phrase spans; never blindly split Chinese by character count or drop English words. Characters may be positioned individually within a vertical Chinese run, but the semantic span stays intact.
- For design exploration, support an explicit editable run order and segments: `[{lang:"zh",text:"信道"}, {lang:"en",text:"faith"}, {lang:"zh",text:"從聽道"}, {lang:"en",text:"cometh"}]` with order, direction, optical offsets and citation mapping. Derive the rotated viewing mode from the **same recorded geometry**, not from separate layout functions.
- Preview, editable editor, print-ready SVG and the negative/positive impression must read the same immutable master layout data. Rendering a rotated clone, not regenerating with different line breaks, is the acceptance check.

## Implementation test before the next art preview

1. A debugger can display the **actual single interleaved run** as ordered ZH / EN / ZH / EN pieces inside one SVG group (not two parent-language groups).
2. Translating the entire group via a 90-degree transform changes the primary readable language without changing pairwise distances among letters or fragment segments.
3. A visual test must show neighboring ZH↔EN fragment transitions along the same line/run, not a two-column arrangement disguised by overlap.
4. No broken Chinese word/semantic grouping, missing text, accidental clipping or distorted Latin glyphs.
5. Yin/yang changes only palette/ink polarity (unless an explicitly documented mirrored print workflow is separately justified).
6. Use one shared canonical layout object for on-screen SVG and exported SVG; inspect actual screenshots including 390px.
7. First test a *short piece*, then long Luke 24:27, then HOME + seven realms, without handcrafting eight independent posters.

## What this document prevents

- The false solution `Chinese vertical block | English horizontal block`.
- The false solution `Chinese row / English row`.
- The false solution `one Chinese-only stamp + one independently rendered English-only stamp`.
- The false solution `rotate English alone in the independent English block`.
- Decorating an unresolved type layout with frames, texture, lines or generated images.

**Design aim:** Modern, rigorous and minimal artwork. Start with black-on-white character form, measured typography and balanced negative space. The artistic result, not the novelty of an algorithm, determines acceptance.
