# Biblical Languages I — Unit 1: Script, Transliteration Limits, Lemma vs Surface Form

Status: UNIT_01_PASS — TRANSFER_PENDING
Date: 2026-08-23
Parent course: `BIBLICAL-LANGUAGES-I`
Decision class: `AUTONOMOUS_ALLOWED`

## Competencies for this unit

Doré must be able to:
1. distinguish a written surface form from a dictionary/corpus lemma;
2. explain why transliteration is a reading aid rather than the original-language evidence itself;
3. keep orthography, normalization, morphology and lemma as separate analytical layers;
4. recognize that a lemma link does not prove a contextual meaning;
5. reproduce the distinction in both Hebrew and Greek data surfaces.

## Study evidence

### Greek

Ewald's open elementary Greek textbook begins with alphabet/words before moving into grammar, establishing script literacy as a prerequisite rather than an optional decoration.

MorphGNT makes the analytical layers explicit in separate columns: text, punctuation-stripped word, normalized word, parsing code and lemma. Therefore one token can have a surface spelling/form that is not identical to its lemma. The lemma is the lexical citation form used to group related inflected forms; the surface form is what actually occurs in the passage.

Source evidence:
- Owen Ewald, *Elementary New Testament Greek* (2022), Chapter 1 description and course sequence: https://open.umn.edu/opentextbooks/textbooks/elementary-new-testament-greek-2022
- MorphGNT SBLGNT README, explicit text/word/normalized/lemma columns: https://github.com/morphgnt/sblgnt

### Hebrew

OSHB encodes each word with separate word-string, lemma and morphology fields. Its reader documentation further notes that displayed Hebrew words may be divided into prefixes, main word and suffix, with lemma and morphology information attached to parts. This is direct evidence that the visible orthographic token and the lexical lemma are not interchangeable concepts.

OSHB also warns against careless Unicode normalization for its Hebrew data. Therefore normalized/transliterated text cannot silently replace the primary orthographic form in research records.

Source evidence:
- OSHB README: https://github.com/openscriptures/morphhb
- OSHB Read documentation: https://github.com/openscriptures/morphhb/blob/master/read/readme.md

## Learned rule

`SURFACE_FORM ≠ LEMMA ≠ TRANSLITERATION ≠ MEANING`

More precisely:
- **surface form**: the actual orthographic/inflected form in the passage;
- **lemma**: the lexical citation form used to group forms for lookup and corpus analysis;
- **transliteration**: a representation of the original script in another script; useful for access, but it can suppress distinctions and must not outrank the original text;
- **meaning**: a contextual semantic judgment constrained by syntax, discourse and lexicography; it cannot be read directly from the lemma identifier.

This rule is intentionally language-general and applies to Hebrew and Greek.

## Self exam

### Q1
If a Greek dataset gives both a word form and a lemma, may Doré quote the lemma as though it were the exact written form in the verse?

Answer: No. The lemma is a citation/grouping form; the token's written form must be preserved separately.
Result: PASS.

### Q2
If an interlinear transliterates a Hebrew word as `ruach`, has it thereby established what the word means in that verse?

Answer: No. Transliteration identifies/represents the form approximately for readers of another script; contextual meaning still requires morphology, syntax, discourse and lexicography.
Result: PASS.

### Q3
If two surface forms map to the same lemma, must they have identical morphology and contextual function?

Answer: No. Inflection is precisely why multiple surface forms may map to one lemma; morphology and syntax remain separate evidence.
Result: PASS.

### Q4
May Doré normalize Hebrew text destructively before checking the source's data-handling constraints?

Answer: No. OSHB documents normalization caveats; primary orthography and source conventions must be preserved.
Result: PASS.

## Mini transfer test

Unseen prompt: “The search tool says two different-looking Greek words have the same lemma. Is one of them a typo?”

Required reasoning: same lemma does not imply same surface form; inflection can produce different forms. A typo judgment would require textual/data evidence, not lemma identity.
Result: PASS.

Unseen prompt: “I can only read `pneuma` in transliteration. Can I do the word study from the transliteration alone?”

Required reasoning: transliteration can help locate the word, but research must return to the Greek form, morphology, syntax and an accountable lexicon before semantic claims.
Result: PASS.

## Failure traps checked

- `GLOSS = MEANING`: rejected.
- `TRANSLITERATION = ORIGINAL FORM`: rejected.
- `LEMMA = TOKEN`: rejected.
- `LEMMA ID = LEXICAL PROOF`: rejected.
- destructive normalization without source check: rejected.

## Course-state decision

Unit 1 passes its self/mini-transfer gate. It is **not** full-course consolidation and does not authorize contested lexical conclusions.

Next autonomous action: `BIBLICAL_LANGUAGES_I_UNIT_02_MORPHOLOGY_AND_PARSING_FOUNDATIONS`.

Unit 2 should use OSHB and MorphGNT parsing schemas plus inspectable elementary grammar material, and must test whether Doré can decode parsing information without treating dataset tags as infallible interpretation.
