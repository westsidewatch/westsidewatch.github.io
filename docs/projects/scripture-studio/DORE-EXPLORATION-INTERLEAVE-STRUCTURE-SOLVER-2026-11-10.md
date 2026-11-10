# 多雷探索 — 找到 V14 缺少的混排結構求解方法

**Date:** 2026-11-10. **Status:** reviewed research + independently tested local algorithm proof, **not an approved Seal design or an integrated production generator**. Reference: 07 古騰夢溪. Supersedes the structural algorithm of V14, not the agreed hard content/type rules.

## Why V14 cannot produce the required rhythm

V14 rowCandidates() constructs only ZH→EN and ZH→EN→ZH. This is a strict code-level limitation: the algorithm cannot generate EN→ZH→EN, ZH→EN→ZH→EN, 4–6-run alternatives, or mixed row signatures even when semantically allowed. A ratio score cannot fix a candidate-generation defect. The global solver then grades alternatives that are intrinsically identical in structure. The V14 output cannot meet the artistic intent of varied cross-axis letterpress.

## Two-stage replacement

**Stage A — structural constrained search.**
- Source model: approved Chinese and English exact text, independently ordered in each language, with verified punctuation and immutable protected phrase spans.
- Candidate grammar: every strip is a sequence of indivisible bilingual phrase-runs; variable starting language, 3–6 runs, and 2–5 switches. Examples: ZH–EN–ZH, EN–ZH–EN, ZH–EN–ZH–EN, ZH–EN–ZH–EN–ZH, EN–ZH–EN–ZH–EN. A row need not have one Chinese half followed by one English half.
- Generate all structurally legal candidates, and reject semantic/word breaks, missing text, repeated single-pair rows, forbidden 50/50 majority, identical pattern for all strips.
- Prefer a real combinatorial constraint solver: Google OR-Tools **CP-SAT**, via [or-tools-wasm](https://github.com/Axelwickm/or-tools-wasm) (Apache-2.0) for a browser editor or native OR-Tools service at build time. Cross-origin isolation / WASM worker deployment needs verification. Do not claim it is installed. A small deterministic beam-search prototype can establish feasibility before adopting heavy WASM.
- Knuth–Plass / [tex-linebreak](https://github.com/robertknight/tex-linebreak) is valuable for whole-paragraph **legal line breaking** after semantic boundaries, but alone it cannot select cross-language interleaving permutations.
- [WebCoLa](https://marvl.infotech.monash.edu/webcola/) and [kiwi.js](https://github.com/IjzerenHein/kiwi.js) optimize geometry/linear constraints, not bilingual phrase grammar. Original kiwi.js repo is archived; do not make it the foundational dependency.

**Stage B — measured optical composition.**
- Measure real glyph bounds at OS-approved Chiron Hei HK WS 200 / 900 and Bodoni Moda / Small Caps / authentic Italic. CSS computed family/weight is not proof of successful font load.
- Set the font size and freeze it. Choose the *number of strips* from available legal phrase boundaries and physical capacity, not a predetermined 4/6 nor a shrinking loop.
- Reject layouts with overly long strips that force large whole-artboard display-scale reduction. Increasing board height alone does not make a design strong; require measurable ink-bounds occupancy in **both axes** and sufficiently varied strip widths/negative spaces.
- If the full bilingual text at this exact font size and semantic locks does not admit a square-like, visually full composition, do **not** falsely announce success. Offer: (1) editorially approve additional authentic semantic breakpoints, (2) adopt the actual natural rectangular plate dimension, or (3) divide into an approved multi-impression sequence. Never silently split protected phrases or omit scripture.
- Yin and Yang must derive from ONE immutable mother forme. Rotation changes reading orientation without recomputing phrase order.

## Local proof performed in this investigation

A standalone JS beam-search candidate enumerator was run in Chromium against the eight existing Scripture Studio presets (with their then-existing editorial locks). The new enumerator **actually generated varied signatures**, including ZEZE, EZEZE, ZEZEZ and ZEZEZE. Seven of eight presets achieved structural completeness and alternating-pattern checks; the Dawn Library candidate returned no legal solution, and was not silently altered. This is **structural feasibility only**. Actual screenshot also showed a narrow central motif with considerable unused board area: **visual-fill acceptance FAILED**. Do not call the test a production-ready generator or say the design reached 07 quality.

With short Romans 10:17 and only four locked English phrases, a high number of multi-switch strips may be mathematically impossible without more meaningful English phrase boundaries. This is a content capacity issue, not solved by arbitrary column-spacing or shrinking. Editable reviewed phrase locks are a core editor feature, not a fallback hack.

## Precise acceptance gates

1. Complete Chinese/KJV quotation preserved exactly, including punctuation and per-language order.
2. Protected phrase/clauses remain whole; any new break requires editorial authorization, not arbitrary token quotas.
3. Each strip has both languages; strictly more than half of strips have >=2 language switches; multiple genuinely different patterns and inter-language positions.
4. Strictly more than half the strips must be outside the 40–60% bilingual measured-advance balance band. 4 strips -> >=3 asymmetric; 6 -> >=4 asymmetric.
5. Typeface OS checked at actual resource/font-face level; Chinese-heavy = 900; Chinese-thin = 200; English respects OS variants.
6. Native font sizes never shrink with longer Scripture. Increase strips/physical board or multi-impression when genuinely necessary.
7. Measure glyph bounds and acceptable artboard optical occupancy in both dimensions; aesthetic review cannot be replaced by only passes of structural tests.
8. The **same geometry** drives live HTML preview, faithful SVG export, yin/yang polarity and 90-degree orientation. Compare screenshots 1648/768/390/320.
9. If impossible, report constraints that conflict; do not manufacture a finished piece.

## Next executable work package

First add an inspectable **phrase-lock editor** for Romans 10:17 and the longer Luke 24:27; identify legitimate additional soft breakpoints with bilingual editorial review. Implement CP-SAT or beam-search constraints over 3–6-run strip permutations, with a two-dimensional optical occupancy filter and true glyph measurement. Validate **one** approved complete Yin/Yang pair before bulk regeneration of HOME + seven realms. Do not modify P2 or production in this phase.

**Evidence and tools:** https://www.npmjs.com/package/or-tools-wasm ; https://github.com/Axelwickm/or-tools-wasm ; https://github.com/robertknight/tex-linebreak ; https://marvl.infotech.monash.edu/webcola/ ; https://github.com/IjzerenHein/kiwi.js ; V14 local HTML code audit and V15 local Chromium proof.

**Important:** This document identifies the needed algorithm and a tested structural proof. It does not claim CP-SAT integration, OS font loading, or a visually satisfactory completed piece.