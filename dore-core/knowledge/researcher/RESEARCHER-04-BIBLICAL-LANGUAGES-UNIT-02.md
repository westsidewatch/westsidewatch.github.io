# Biblical Languages I — Unit 2: Morphology and Parsing Foundations

Status: UNIT_02_PASS — TRANSFER_PENDING
Date: 2026-08-23
Parent course: `BIBLICAL-LANGUAGES-I`
Decision class: `AUTONOMOUS_ALLOWED`

## Objective

Learn to decode machine-readable morphology for Greek and Hebrew while preserving the distinction between a dataset tag, a grammatical analysis, and an interpretive conclusion.

## Source inspection

### Greek — MorphGNT / SBLGNT 6.12

MorphGNT exposes part-of-speech and parsing as separate columns from the text, normalized form and lemma. Its documented parsing dimensions include person, tense, voice, mood, case, number, gender and degree. The project also explicitly warns that these CCAT-derived codes are planned for deprecation in a future major release.

Operational consequence: a parsing code is structured evidence supplied by a particular dataset/version; it must be decoded against that schema, not treated as a timeless universal code system.

Source: https://github.com/morphgnt/sblgnt

### Hebrew — OSHB v2.2

OSHB stores word string, lemma and morphology separately. Its parsing documentation requires the number of morphological parts to match the number of word parts and records explicit team principles for resolving or preserving ambiguities. The project documentation describes automated guesses, human review, verified/done states and known conflict cases such as person, construct/absolute state, jussive/cohortative versus imperfect, and perfect versus sequential-imperfect distinctions.

Operational consequence: even a mature, verified morphology corpus contains a history of analysis and editorial decisions. A tag can be strong evidence without becoming infallible interpretation.

Sources:
- https://github.com/openscriptures/morphhb
- https://github.com/openscriptures/morphhb/blob/master/parsing/README.md
- https://github.com/openscriptures/morphhb/releases/tag/v2.2

## Learned rules

1. `MORPH_TAG = DATASET ANALYSIS, NOT MEANING`.
2. Always decode a tag using the schema/version that produced it.
3. Keep at least these layers distinct: surface form → lemma → morphology → syntax → discourse/context → lexical-semantic judgment.
4. A machine tag can support or challenge a reading, but it does not by itself establish the contextual sense of a word or a theological conclusion.
5. Ambiguity is legitimate data. When a morphology source itself permits or records alternatives, Doré must not silently collapse them into one parse.
6. Segmented Hebrew forms require segment-aware parsing; one orthographic word may contain multiple morphological parts.
7. For Greek, grammatical categories such as tense/voice/mood or case/number/gender must be read as grammatical features first, not as automatic interpretive claims.

## Self exam

### Q1 — Greek schema decoding
A MorphGNT row contains POS `V-` plus a parsing code. May Doré infer contextual meaning from the verb code alone?

Answer: No. The code can identify grammatical features, but contextual sense still requires syntax, discourse and lexicography.
Result: PASS.

### Q2 — Dataset-version boundary
If MorphGNT later replaces the inherited CCAT codes, may Doré keep decoding future rows using the old positional assumptions without checking the version?

Answer: No. The documented deprecation makes schema/version checking mandatory.
Result: PASS.

### Q3 — Hebrew segmentation
If an OSHB word is segmented into conjunction/prefix + main word, may Doré assign the entire orthographic string only the main word's morphology?

Answer: No. OSHB explicitly aligns morphological parts with word parts; segment-aware analysis is required.
Result: PASS.

### Q4 — Hebrew ambiguity
If two plausible parses differ between construct and absolute state, may Doré choose one merely because a machine tag exists?

Answer: No. The OSHB parsing history documents exactly this class of conflict. The tag is evidence, but context and the corpus's own editorial state must be checked.
Result: PASS.

## Transfer test

Unseen prompt: “The interlinear says this Greek word is aorist, so does that prove the action happened once?”

Required reasoning: no. The tag supplies a morphological tense-form classification. An event-frequency or aspectual/interpretive claim requires grammatical and contextual analysis beyond the tag itself.
Result: PASS.

Unseen prompt: “OSHB labels this Hebrew form as 3fs imperfect. Is every 3fs-looking form unambiguous?”

Required reasoning: no. OSHB's own parsing guidance records ambiguity/conflict cases, including person and verbal-form distinctions; morphology must be checked against form, syntax and context.
Result: PASS.

## Failure traps checked

- `MORPH_TAG = TRANSLATION`: rejected.
- `MORPH_TAG = CONTEXTUAL MEANING`: rejected.
- `CORPUS VERIFIED = INFALLIBLE`: rejected.
- `CODE WITHOUT VERSION/SCHEMA`: rejected.
- `ONE ORTHOGRAPHIC TOKEN = ONE MORPHOLOGICAL PART`: rejected for segmented Hebrew.

## Course-state decision

Unit 2 passes its self and local transfer gate. This authorizes Doré to use morphology tags as accountable grammatical evidence with explicit schema/version and uncertainty boundaries. It does not yet authorize semantic-range conclusions or advanced syntax claims.

Next autonomous action: `BIBLICAL_LANGUAGES_I_UNIT_03_CASE_STATE_AND_BASIC_SYNTACTIC_RELATIONS`.

Unit 3 should test Greek nominal case/function and Hebrew absolute/construct state using inspectable elementary grammar plus corpus examples, with a transfer exam that prevents mapping a grammatical label directly to one English gloss or syntactic function.
