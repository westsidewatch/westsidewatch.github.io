# Scripture Studio — 雙語鉛字硬性規格 V14

**2026-11-09 · status: replaces V13 layout specification; NOT an implemented generator.**
The V13 screenshots are a **failed design acceptance**. Repetition of one ZH + one EN column and breaking of protected clauses to satisfy a predetermined row count are forbidden.

## 0. What 'one line' means

A row/strip is a continuous sequence of alternating Chinese and English material within ONE physical typesetting strip, **not** two separate lines and **not** invariably one ZH block plus one EN block. A work may have many strips. Chinese-reading mode: text top-to-bottom, columns right-to-left. Rotate the exact mother forme 90 degrees for English-reading mode: English horizontal and first, sideways Chinese ornamental.

## 1. Hard acceptance conditions — ALL MUST PASS

**H1 Complete exact scripture.** Both approved Chinese and KJV originals, punctuation and per-language source order must survive intact and compare exactly to the originals. Ornamental counter-language never means omitted or altered text.

**H2 Semantic integrity outranks geometry.** Protected Chinese terms, complete clause fragments and English phrases (e.g. `信道`, `聽道`, `基督的話`, `by hearing`, `by the word of God`) are indivisible. Break only at editorially approved boundaries, with punctuation attached. NEVER cut a character from an intact clause to force column count, balance or fill.

**H3 One mother forme.** Both readings reuse the same canonical mixed typographic geometry rotated as a whole; no separate reflow algorithm. Yin/yang only changes ink/paper contrast, not geometry or source text.

**H4 Genuine interweaving, not one bilingual pair per strip.** Every strip includes both languages. A majority of strips must offer at least TWO language switches when meaningful chunks permit, e.g. `ZH–EN–ZH`, `EN–ZH–EN`, `ZH–EN–ZH–EN` and varied segment counts/lengths. A string of `ZH–EN` columns is NOT artistic interleaving and automatically fails design review. Never manufacture switches by violating H2: if no legal solution exists, return a clear `INSUFFICIENT_APPROVED_BREAKPOINTS` state and request more legitimate phrase boundaries or a different artistic format.

**H5 Reading order.** Chinese-reading: Chinese top first, traditionally vertical right-to-left columns. English-reading: English first, horizontal left-to-right, Chinese sideways decorative. No per-word reversing, letter splitting, or inversion of English reading.

**H6 Strict majority NON 50/50 constraint; a hard gate, not a scoring preference.** Measure each strip's real font-run advance (not character counts and not arbitrary whitespace); Chinese share = zhAdvance / (zhAdvance + enAdvance). Shares in **40–60% count as near-balanced**; outside that range are definitely asymmetric.

| Strips | Minimum asymmetric | Maximum near-balanced |
|---|---:|---:|
| 4 | **3** | **1** |
| 5 | **3** | **2** |
| 6 | **4** | **2** |
| 7 | **4** | **3** |
| 8 | **5** | **3** |
| n | **floor(n/2)+1** | **ceil(n/2)-1** |

All solutions with insufficient non-balanced strips FAIL, regardless of an excellent aesthetic score. Change legitimate allocations / number of strips / canvas geometry; never break protected phrases to meet the ratio.

**H7 Column count is derived, not fixed.** DELETE any 'always 4–8 lines' or 'choose four then partition to quota' policy. Four/six are explicit test cases, not compulsory templates. Derive strips from semantic units and measured length. Do not transfer trailing single characters merely to balance strips.

**H8 No shrinking.** Keep identical nominal Chinese and English font size within the master geometry. OS font family/roles: Chiron Hei HK WS 900 (true heaviest in Chinese-reading) and 200 (true thinnest in English-reading); Bodoni Moda Roman/true Italic/Bodoni Moda SC for English. For more text, add strips, extend physical canvas, or use multiple imprints; NEVER auto-decrease CSS type size, stretch glyphs, crop or omit. Responsive *whole-artwork display* scaling is not lowering source type size.

**H9 Real fill, not empty square.** After H1–H8 pass, examine actual text bounding box relative to the *optical usable* artboard; target about 75%+ occupation in both width/height, without faking it through margins or distorted font scaling. If naturally narrow, adapt format/strip geometry; do not surround a thin column with huge blank square and call it whitespace.

**H10 Fonts and output are real.** Verify OS font files loaded (CSS font-weight alone is not proof), and preview/export consume exactly the same geometry. If fonts unavailable, mark font appearance UNVERIFIED.

## 2. Mandatory algorithm sequence

1. Immutable verified bilingual text and punctuation.
2. Explicit locked semantic spans. NLP candidate segmentation NEVER overrides approved breaks.
3. Search whole-passage multi-strip interleaving possibilities; **allow varying numbers of bilingual switches** per strip and preserve original language order.
4. Measure actual glyph advances at fixed type size; determine needed strips and physical canvas from content.
5. HARD-REJECT violations (missing text, semantic split, repeated single-pair arrangement, majority balance threshold, orientation/size).
6. Only score artistic qualities (asymmetry, ink mass, rhythm, negative space, bounding box fullness) among LEGAL alternatives; show a small set for editorial optical selection.
7. Derive both impressions from one immutable layout; test screenshot and source-consistent export.

**Priority is not an excuse to violate rules:** all H1–H8 are nonnegotiable, while the solver should protect exact text and legitimate semantics before attempting compositional optimization. Where impossible, surface an explicit no-solution state.

## 3. Required machine-readable test output

- `sourceExactZH === true`, `sourceExactEN === true`.
- `protectedBreakViolations === 0`.
- `bandsCount` derived from content, not a constant.
- For every strip: ordered language runs, switch count, source spans, measured zh/en advances and share, and balanced classification.
- `nonBalancedBands >= Math.floor(bandsCount/2)+1` true. **4 bands ≥3 non-balanced; 6 bands ≥4 non-balanced.**
- Every strip mixed; majority have ≥2 language switches; no repeated one-pair mechanical layout.
- `fontSizeOutput === fontSizeInput`; font-load check explicitly records Chiron 200/900 and Bodoni.
- Rotation preserves exact glyph geometry, chinese RTL, English LTR; preview/export use same layout ID.
- Real ink/type bounds relative to artboard and responsive 1648/768/390/320 checks.
- Unsatisfiable => fail visibly; never claim a passed design.

## 4. Examples of automatic rejection

- Four strips of which two are ~50/50: **FAIL**.
- Six strips of which three are ~50/50: **FAIL**.
- A majority of strips `ZH–EN` only: **FAIL**.
- Splitting `基督的話` or `by the word of God` to force counts: **FAIL**.
- Shrinking characters to fill a predetermined square, or leaving a tiny narrow text column in an empty square: **FAIL**.
- Claiming 'Chiron Heavy 900 verified' from fallback font: **FAIL**.

**V13 is superseded.** Implementation requires actual user-visible design proof, not version-number increments.