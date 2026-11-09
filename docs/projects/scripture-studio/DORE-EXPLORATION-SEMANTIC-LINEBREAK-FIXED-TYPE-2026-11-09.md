# 多雷探索：Scripture Studio 中英正確斷句與固定字號自動增行

Date: 2026-11-09. Status: research decision, NOT a completed generator. Scope: V11 repair while retaining 07 mixed-type principles.

## V11 root-cause audit

- The existing zhTokens() handles editorial preset chunks or Intl.Segmenter(word). Word boundaries do not guarantee meaningful syntactic/Scripture phrases.
- V11 tokenizes English with a whitespace regex. Whole words remain but English phrases such as 'by the word of God' may be broken at arbitrary points.
- allocate() creates independent Chinese and English partitions using arbitrary size weights. segmentFlow() then forces equal numbers of language groups into every band. This gives repeated EN/ZH, EN/ZH layout instead of designed varied rhythm.
- fit(root) begins at 57px, decrements font size until both dimensions <=505px. This is precisely the forbidden shrinking behavior. Delete this adjustment; increase row/strip count and when necessary artwork dimensions.
- Existing tests checking concatenated source strings are necessary but not sufficient to verify syntax, punctuation, protected Biblical phrases, or optical composition.

## Open-source comparison

| Need | Verified source | Role | Limit |
| --- | --- | --- | --- |
| Base word and sentence segmentation | MDN Intl.Segmenter | Browser native since 2024; no package | Not syntax/theology |
| Chinese lexical segmentation | fengkx/jieba-wasm (MIT), messense/jieba-rs (MIT) | Browser WASM, user dictionary and custom sacred terms | Does not know biblical clause boundaries |
| English syntactic phrase candidates | spencermountain/compromise (MIT) | Phrase match, nouns and verbs, POS | KJV archaic grammar may be misclassified |
| English POS/sentence alternative | winkjs/wink-nlp (MIT) | Lean browser NLP | Additional package and model; do not include with compromise without benchmark |
| Unicode break legality | foliojs/linebreak (MIT) and Unicode UAX #14 | Safe break opportunities and punctuation | Not semantic correctness |
| Balanced whole-passage lines | robertknight/tex-linebreak (Knuth-Plass) | Global badness minimization, candidate approach | Justification library, not bilateral Chinese/English semantic composer; verify license before vendoring |

Sources:
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter
- https://github.com/fengkx/jieba-wasm
- https://github.com/messense/jieba-rs
- https://github.com/spencermountain/compromise
- https://github.com/winkjs/wink-nlp
- https://github.com/foliojs/linebreak
- https://github.com/robertknight/tex-linebreak
- https://www.unicode.org/reports/tr14/

## Recommended minimum implementation

Start with native Intl.Segmenter + editorial protected phrase dictionary + custom whole-passage dynamic programming (DP) multiline arranger. Use UAX #14 legality as baseline. Test jieba-wasm with Traditional Chinese and Scripture-specific dictionary; adopt if it materially improves custom-edited passages. Evaluate compromise against KJV before using it for any automatic phrase boundaries. Do not claim generic NLP makes theologically accurate decisions.

Text data is separated into:
1. Exact immutable CUV/KJV source and citations, no rewriting.
2. Protected semantic spans for each language, identified by source start/end offsets, with manual no-break locks. Examples: 信道, 聽道, 基督的話, 'by hearing', 'by the word of God'. Breaks at other syntactic positions get editorial penalties or are forbidden as selected.
3. Shared mixed-type composition: all rows contain both Chinese and English, but rows have differing numbers of segments, lengths, balance and crossings. Source-order preservation checked separately in each language. English leads when English is the primary readable direction.

## No shrink policy

Fix the native Chinese and English nominal font size, consistent with OS. Measure actual glyph runs using loaded Chiron and Bodoni before layout.
Try row counts r, r+1, r+2 until each protected unit fits a legal interwoven strip at the chosen type size. Optimize the whole composition using DP: minimize semantic break penalties + overflow + uneven density + repeated structural pattern + orphans.
A fixed square at fixed physical type size cannot fit an arbitrarily long full bilingual passage. When row growth exhausts square capacity, enlarge intrinsic artwork dimensions or use another imprint/page. On-screen responsive scaling of the whole artwork is allowed but must not change canonical glyph size or delete content.

## Hard acceptance gate

1. Exact text-preservation across all eight existing passages and additional short/long cases (both languages).
2. Zero broken protected words/phrases; quote punctuation attached appropriately; English KJV archaic terms guarded.
3. Every visual strip truly mixes languages, but differing segment counts and lengths, avoiding fixed EN/ZH repetition.
4. Font size remains identical short vs long; longer input means more strips or larger output canvas.
5. Native Chinese columns right to left, rotated English orientation, 200/900 actual Chiron font verified, Latin OS Bodoni verified.
6. One canonical geometry for preview/export, actual browser captures at 1648/768/390/320.
7. If no legal layout exists, the editor asks to enlarge the artwork or create an additional impression instead of shrinking or omitting words.

Decision: remove V11 arbitrary weight-based allocate/splitOrdered and fit shrinking loop. Retain proven native vertical-rl and 90-degree mother-form rotation. No public/live changes or claim of completed implementation.