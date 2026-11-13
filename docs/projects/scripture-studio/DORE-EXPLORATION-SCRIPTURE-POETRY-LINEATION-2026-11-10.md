# 多雷探索｜聖經詩歌分行優先的經文印記排字
**Date:** 2026-11-10 · **Scope:** Scripture Studio poetic structure, Isaiah 62:6, OS true font-weight correction.
**Status:** verified research and engineering decisions; NOT implementation/deployment or visual acceptance.

## 1. Correct OS fonts and weight range

Canonical OS runtime `static/css/westside-design-os.css` uses `--ws-type-display-zh: "Chiron Hei HK WS"` with ordinary role tokens `--ws-weight-zh-air:200`, `--ws-weight-zh-standard:400`, `--ws-weight-zh-anchor:600`. These semantic site roles must not be confused with **the actual extrema of the selected variable font**. Chiron Hei HK official font documentation: **ExtraLight 200; Heavy 900; no 100 instance**. Variable font weight axis 200–900. Scripture artwork experiment should explicitly select Chiron 900 for Chinese-readable strong type and Chiron 200 for sideways Chinese countertype in English-readable state; record that they are **specialized art choices** and do not change global anchor token from 600. English follows `--ws-type-display-en: Bodoni Moda`, actual Roman/Italic/Small Caps as user selections. Need to check font network and glyph instance, not simply computed CSS.

References:
- https://github.com/chiron-fonts/chiron-hei-hk/blob/release/README.en.md
- https://chiron-fonts.github.io/usage/package/
- Local repository docs/design/WESTSIDE-EDITORIAL-TYPOGRAPHY.md and runtime static/css/westside-design-os.css

## 2. Root cause: generic word segmentation is not Bible versification/poetic lineation

The current V16 mix of custom phrase chunks and geometry-driven segmentation has no knowledge of Hebrew poetic parallelism, verse-level poetic lines, stanzas or approved punctuation. Chinese `Intl.Segmenter`/jieba can locate word boundaries but cannot identify religious referents or the syntactic attachment of `呼籲耶和華的`; English NLP also cannot reliably parse archaic KJV. `晝夜必不靜默` is an intelligible image/clause and should stay together by default; `呼籲耶和華的，` is a nominalized direct address and should be protected as one unit unless an editor approves an alternative. Design may split at lesser boundaries only AFTER preserving original biblical literary form.

**High-level priority:**
1. Authorized translation's actual source structure (verse, paragraph, poetry `q1/q2/q3`, stanza `b`, editorial lineation if formally present)
2. Per-translation sentence/clause and Hebrew poetic parallelism, reviewed by an editor
3. Protected phrases + punctuation and grammatical attachments
4. Optional **soft** artistic line breaks inside allowed zones
5. Optical density, interleaving count/ratio and 2D composition — never override rules 1–3.

Note: **USFM does not itself know/compute where a line should break**. It records **publisher-provided** poetic lines. Importing plain-text Chinese Union/KJV does not magically restore q1/q2. An available USFM edition may use different line breaks per edition/translation. Do not copy licensed paragraph/lineation from an unrelated translation into CUV without review. Verify provenance and rights for each bilingual text/lineation source.

## 3. Existing standardized solution: USFM → USJ + lines

USFM / USX / USJ preserve scripture structural data:
- `\\v` verse marker; `\\p` paragraph
- `\\q1`, `\\q2`, `\\q3` poetic lines and indentation
- `\\b` blank line / stanza spacing
- associated markers `\\qr`, `\\qc`, `\\qm#` in special layouts.

**Preferred open-source parser:** [Bridgeconn/usfm-grammar](https://github.com/Bridgeconn/usfm-grammar), MIT, supports USFM 3, USJ, USX, web/Node/Python, tree-sitter syntax validation. It is a grammar/parser, not a Bible dataset or poetic analysis model.

**Fallback/conversion choice:** [unfoldingWord/usfm-js](https://github.com/unfoldingWord/usfm-js), USFM↔JSON and verse objects. Confirm exact version and licensing before vendoring. Neither supplies by itself approved CUV poetic lineation.

Potential advanced optional: inspect original Hebrew accentuation/parallel structure when a passage's source has no line markup; scholarly/editorial review remains essential. No automatic AI guesses shall become scripture structure authority.

Sources:
- https://docs.usfm.bible/
- https://ubsicap.github.io/usfm/poetry/
- https://github.com/Bridgeconn/usfm-grammar
- https://github.com/unfoldingWord/usfm-js

## 4. Isaiah 62:6 protected Hebrew-poetry-aware segmentation — editorial candidate

Chinese (Traditional modern-punctuation CUV as currently used in project):
`耶路撒冷啊，我在你城上設立守望的，他們晝夜必不靜默。呼籲耶和華的，你們不要歇息，`

**Proposed human-review baseline clauses (NOT an assertion that this is the exact q1/q2 markup in any specific licensed edition):**
- A. `耶路撒冷啊，`
- B. `我在你城上設立守望的，`
- C. `他們晝夜必不靜默。`
- D. `呼籲耶和華的，`
- E. `你們不要歇息，`

**Hard protected by default:** `呼籲耶和華的，` (vocative participant address; not `呼籲` | `耶和華的`), `他們晝夜必不靜默。` (one continuous clause), `我在你城上設立守望的，` (predicate+object cohesion). Optional shorter `晝夜` segmentation only if editorial review grants it. Preserve full stop and comma exactly.

KJV original:
`I have set watchmen upon thy walls, O Jerusalem, which shall never hold their peace day nor night: ye that make mention of the LORD, keep not silence,`

**Proposed protected clauses:**
- `I have set watchmen upon thy walls, O Jerusalem,`
- `which shall never hold their peace day nor night:`
- `ye that make mention of the LORD,`
- `keep not silence,`

Default protection of `ye that make mention of the LORD,`, analogous to Chinese `呼籲耶和華的，`, and `day nor night` in clause. Matching between Chinese/KJV is **semantic**, not mechanical one-to-one or identical word order. The final verse boundary remains distinct from lineation.

Be careful: even this example splits only into five ZH and four EN protected clauses. It may not supply enough approved breakpoints for a 7-strip, >=2-switch-each graphic. Under V14 rules such a variant should display **unsatisfiable**, not arbitrarily split sacred clauses. More poetically responsible solution: *use a smaller number of larger, varied strips while preserving the strophic hierarchy*, an expanded artboard, a sequential impression, or an editor-approved secondary break.

Cross-check available text/lineation sources:
- https://wd.bible/verse/isa.62.6.kjv
- https://bible.org/seriespage/isaiah-62

## 5. New data model: first-class scriptural structure

```json
{
  "reference":"Isaiah 62:6",
  "translation":"CUV-Traditional",
  "verbatim":"...",
  "source_provenance":{"format":"USFM|USJ|manual-reviewed","edition":"","rights":""},
  "literary_form":"poetry",
  "verse_ids":["Isa.62.6"],
  "poetic_lines":[
    {"id":"l1","level":"q1","source_start":0,"source_end":0,"strength":"hard","reviewed":false}
  ],
  "protected_spans":[
    {"start":0,"end":0,"text":"","reason":"vocative|predicate|parallelism","approved_by":""}
  ],
  "candidate_soft_breaks":[],
  "review_state":"needs_editor_review"
}
```

All offsets/line IDs in actual records must be calculated against the **real immutable translation string**, not placeholder zeros. A line is never autogenerated merely to match a target row count.

## 6. Parser → compositor boundary

1. Import a legally usable CUV/KJV source with **actual** USFM/USJ/USX poetic markers; if not available, show `poetry structure missing — manual review required`. Avoid guessing all verse text is poetry just because book=Isaiah; literary structure may vary within books.
2. Parse structure with Bridgeconn usfm-grammar; retain verse ID, q markers, indentation, book/chapter, original words/punctuation.
3. In editor display *semantic poem lines* and protected phrases. Distinguish **hard** biblical/approved boundaries from optional **soft** artistic breaks.
4. Constraint solver may interweave ZH and EN segments only at legal breakpoints; preserve original order within each language; start from sentence/stanza grouping.
5. Derive strips and geometry **from** legal segments. Never demand 7 strips when source supplies only 4–5 legitimate segments; reject infeasible 50/50 or multi-switch majority targets visibly.
6. Verify exact source reconstruction, protected-span intactness, q-line boundary compliance, real font loading (200/900), and optical occupancy; screenshot dual orientation and export from canonical geometry.

## 7. Hard acceptance

- None of `呼籲耶和華的`, `ye that make mention of the LORD`, `基督的話`, or parallelisms are broken by a font/geometry constraint without editorial exception.
- Imported poetry lines are preserved and identified by source edition; a new design overlay does not masquerade as original q markup.
- Same exact translation (including spaces and punctuation) and verse source returned after all lineation/interweaving.
- A semantically legal design that cannot satisfy V14 numeric geometry constraints reports **NO_POETICALLY_LEGAL_LAYOUT** and offers format choice; **never** violate scripture syntax.
- OS font 200 true lightweight, 900 actual heavy, Bodoni variants; verified actual font resource loading. No fallback claimed as font verification.
- UI exposes source-poem structure and any editor-authorized overrides with version provenance.

## 8. Research conclusion

The right open-source path is **USFM structural poetry markup + Bridgeconn usfm-grammar (browser/Node) + supervised semantic locks + existing constrained bilingual compositor**. Ordinary segmentation (jieba, Intl.Segmenter) remains a *fallback candidate tool for prose*, never the authority for Biblical poetic lines. No parser independently guarantees the quality or licensing of specific Chinese/KJV source data.

Implementation not yet completed. Do not present a new image or new generator version as passing this review until the actual source structure and font load have been tested.
