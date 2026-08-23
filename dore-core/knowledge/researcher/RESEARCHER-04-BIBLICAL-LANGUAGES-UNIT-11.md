# Biblical Languages I — Unit 11: Textual-Critical Boundary and Synthesis

Status: UNIT_11_PASS — COURSE_FINAL_EXAM_AUTHORIZED
Date: 2026-08-23
Parent course: `BIBLICAL-LANGUAGES-I`
Decision class: `AUTONOMOUS_ALLOWED`

## Objective

Place textual/edition choice before morphology, lexicography and syntax. Demonstrate that a perfectly decoded morphology tag analyzes the reading contained in its dataset; it does not prove that reading is the earliest or best-attested textual form.

## Greek edition boundary

MorphGNT 6.12 is morphology/lemmatization attached to the SBLGNT reading text. The Society of Biblical Literature explicitly describes SBLGNT as a critically edited reading edition and notes more than 540 places where its text differs from the NA/UBS comparison text. Its limited apparatus compares editorial editions and points readers toward fuller manuscript apparatuses for text-critical evidence.

Operational rule: `MORPHGNT PARSE = ANALYSIS OF SBLGNT READING`, not `TEXTUAL VARIANT RESOLVED`.

### Greek case: John 1:18

SBLGNT reads `μονογενὴς θεός`; its apparatus records a comparison edition reading `ὁ μονογενὴς υἱός`. This difference changes the actual lexical token (`θεός` versus `υἱός`) and therefore changes any downstream lemma/semantic analysis.

A morphology engine can correctly tag whichever reading its edition contains, but it cannot decide the textual question merely by being internally consistent.

Required research order when the variant matters:
1. identify edition/reading;
2. inspect critical apparatus/manuscript evidence through an accountable text-critical resource;
3. state the reading adopted and uncertainty;
4. only then perform morphology/syntax/lexicography on that reading;
5. test whether the interpretation materially changes under the rival reading.

## Hebrew edition/data boundary

OSHB's completed morphology explicitly follows the Westminster Leningrad Codex (WLC). Its release notes mark Ketiv entries separately, and its parsing documentation treats qere/ketiv as a special verification case rather than ordinary unambiguous tokenization.

Operational rule: `OSHB PARSE = ANALYSIS WITHIN WLC/OSHB REPRESENTATION`, not `ALL HEBREW TEXTUAL TRADITIONS RESOLVED`.

### Hebrew case: Ruth 1:8 qere/ketiv

An OSHB example exposes two forms for the same reading locus:
- Ketiv `יעשה`, tagged as an imperfect form;
- Qere `יַעַשׂ`, tagged as a jussive form.

The morphology difference is real and interpretively relevant. Software that silently selects only the written form or only the read form can produce a different grammatical description. Doré therefore must record which representation is being analyzed and must not call the other form a parsing error merely because the dataset exposes both.

## Learned synthesis rules

1. `TEXT/EDITION → FORM → LEMMA → MORPHOLOGY → SYNTAX → CONTEXT → LEXICON/CORPUS → INTERPRETATION`.
2. Textual criticism is upstream of word study whenever a meaningful variant changes the form, lemma, word order or presence/absence of material.
3. Dataset verification means the annotation is verified against its chosen text/schema; it does not certify that the underlying textual reading is original.
4. An edition's adopted reading should be named when a contested claim depends on it.
5. A textual variant should not be invoked merely to create uncertainty. It matters when the variant is genuine and materially affects the research claim.
6. The existence of variants does not make all readings equally probable; evidence must be evaluated rather than flattened into “we cannot know.”
7. Translation comparison can alert Doré to a possible variant, but translations are not a substitute for apparatus/manuscript evidence.
8. When the available tool supplies only a reading text without sufficient apparatus for a disputed locus, Doré must bound or defer the textual claim rather than invent manuscript support.

## Whole-method synthesis test

Prompt: “A search tool says the Greek word here is X with morphology Y, and a lexicon says X can mean Z. Does that prove the doctrine being argued?”

Required answer chain:
1. verify that the queried original text/edition actually contains X and whether a relevant textual variant exists;
2. verify the surface form → lemma → morphology mapping;
3. establish syntactic role and local discourse;
4. use the lexicon to map possible usage rather than declare Z automatically;
5. compare relevant corpus parallels without totality/frequency shortcuts;
6. distinguish translation wording from original-language evidence;
7. separate lexical/textual conclusion from theological/canonical synthesis;
8. preserve unresolved evidence and cite provenance.

Result: PASS.

## Adversarial cases

### A — morphology settles variant
Claim: “MorphGNT tags `θεός` in John 1:18, therefore manuscripts with `υἱός` are irrelevant.”
Verdict: FAIL. MorphGNT parses its chosen SBLGNT token; textual evidence is upstream.
Doré: PASS.

### B — variants destroy certainty
Claim: “Because manuscripts vary, no grammatical conclusion can be trusted.”
Verdict: FAIL. Many loci are stable; at a variant locus, evidence can still strongly favor a reading and grammatical analysis can be conditional on that reading.
Doré: PASS.

### C — qere is typo
Claim: “OSHB gives different qere/ketiv morphology, so one entry must be a bad parse.”
Verdict: FAIL. The two reading traditions can legitimately require different parses; record the layer.
Doré: PASS.

### D — translation proves variant
Claim: “Two English Bibles differ, so the Greek manuscripts must differ.”
Verdict: FAIL. Translation choices can diverge without textual variants; inspect the source editions/apparatus.
Doré: PASS.

## Unit decision

`UNIT_11_PASS — COURSE_FINAL_EXAM_AUTHORIZED`.

Units 1–11 now cover the complete minimum research-reading chain: form/lemma, morphology, nominal syntax, verbal systems, lexicon discipline, context/corpus, falsification, Hebrew practicum, Greek practicum, translation diagnostics, and textual-critical boundary.

Passing Unit 11 does not by itself graduate the course. Doré must now pass an integrated final exam with unseen transfer and a blind user-like question, and should promote only the method competencies that survive that gate.

## Next autonomous action

`BIBLICAL_LANGUAGES_I_FINAL_EXAMS`.

Run:
- a closed-method self exam across all layers;
- an unseen Hebrew transfer case;
- an unseen Greek transfer case;
- a blind theological/original-language claim with at least one tempting shortcut;
- a product-boundary test requiring Doré to decline a claim when evidence is missing;
- a retention-style reconstruction of the full research sequence without reading the unit conclusions into the answer.

Any automatic-fail condition requires remediation and retest rather than graduation.
