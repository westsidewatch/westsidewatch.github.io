# Biblical Languages I — Unit 5: Lexicon Use and Semantic Range

Status: UNIT_05_PASS — TRANSFER_PENDING
Date: 2026-08-23
Parent course: `BIBLICAL-LANGUAGES-I`
Decision class: `AUTONOMOUS_ALLOWED`

## Objective

Learn to use lexica as evidence for attested lexical range and usage without collapsing an entry into one gloss, importing every listed sense into one passage, or treating a Strong number as lexical proof.

## Access decision

Licensed BDAG/HALOT-class content is not available in the current tool path. That blocks pretending to have completed advanced lexicographic consolidation, but it does not block elementary method training.

Inspectable substitutes selected for this unit:
- Greek: G. Abbott-Smith, *A Manual Greek Lexicon of the New Testament* (public-domain marked-up editions and online entry views).
- Hebrew: Brown–Driver–Briggs (BDB), public-domain text, including Open Scriptures' structured HebrewLexicon transcription.
- Data bridge/reference: STEPBible-Data, CC BY 4.0, with brief Greek/Hebrew lexica and explicit provenance to Abbott-Smith/BDB-derived material.

These are substitutes for method training, not a claim of equivalence to current licensed lexica.

Sources:
- https://github.com/translatable-exegetical-tools/Abbott-Smith
- https://en.wikisource.org/wiki/A_Hebrew_and_English_Lexicon_%28Brown-Driver-Briggs%29
- https://github.com/openscriptures/HebrewLexicon
- https://github.com/STEPBible/STEPBible-Data

## Direct lexical inspection

### Greek πνεῦμα

Abbott-Smith's entry distinguishes multiple usage classes rather than one English gloss: moving air/wind, breath, vital principle/spirit, disposition/influence, incorporeal beings, and Holy Spirit usage among others. The entry itself therefore falsifies the method `lemma πνεῦμα = one fixed gloss`.

Inspectable entry: https://hiperbiblia.com/lexicons/G4151

### Greek γραφή

Abbott-Smith distinguishes general writing/written material from New Testament use for sacred writings/Scripture, and further distinguishes collective/scriptural-corpus and particular-passage usages. Again, the entry provides a range organized by usage, not one mechanically transferable gloss.

Inspectable entry: Abbott-Smith entry for γραφή, mirrored in public lexicon interfaces and derived from the public-domain lexicon.

### Hebrew רוּחַ

BDB's entry organizes רוּחַ across multiple senses/usages including wind/breath and varied spirit/disposition usages. The entry is historical scholarship and must be read critically, but it is enough to demonstrate that a Hebrew lemma is not equivalent to one English doctrinal term.

Inspectable source: BDB/Wikisource and Open Scriptures HebrewLexicon.

## Learned rules

1. `LEXICON ENTRY = MAP OF ATTESTED/ANALYZED USAGE, NOT THE VERSE'S ANSWER`.
2. A lemma can have multiple senses/usages; the local passage must select among possibilities through syntax, collocation, discourse and genre.
3. `ALL SENSES IN ENTRY ≠ ALL SENSES IN ONE OCCURRENCE` — illegitimate totality transfer is rejected.
4. A gloss is a translation aid, not a definition of the lemma's entire semantic range.
5. Strong numbers are identifiers/indexing aids; they are not semantic arguments.
6. Lexica have editions, dates, theoretical assumptions and limitations. BDB and Abbott-Smith are valuable public-domain historical references but do not replace newer lexicographic scholarship where a contested claim requires it.
7. A lexicon may support a possible sense but does not by itself prove that sense is active in the target verse.
8. Cross-language equivalence is many-to-many: Hebrew רוּחַ and Greek πνεῦμα overlap substantially in biblical translation traditions, but neither can be reduced to one English word or to each other in every context.

## Self exam

### Q1
Abbott-Smith lists several senses for πνεῦμα. May Doré import all of them into John 3:8?

Answer: No. The entry defines possible/attested usage classes; the verse's syntax and context determine which readings are plausible.
Result: PASS.

### Q2
A Strong number links an English word to רוּחַ. Does that prove the theological meaning of רוּחַ in a verse?

Answer: No. The number is an index. Lexical range, morphology, syntax and context remain required.
Result: PASS.

### Q3
If an old lexicon gives a gloss not favored by a newer scholarly lexicon, may Doré silently treat the old gloss as settled because it is open-access?

Answer: No. Accessibility is not authority. Date, evidence and current scholarship must be weighed, and uncertainty recorded.
Result: PASS.

### Q4
If γραφή can mean writing and in NT usage often Scripture, does the lemma alone settle whether a singular occurrence means the whole canon or a particular passage?

Answer: No. The lexical entry itself distinguishes usage contexts; syntax and discourse must decide the local referent.
Result: PASS.

## Transfer exam

Unseen prompt: “The lexicon says this word can mean X, therefore X is what the verse means.”

Required reasoning: reject possibility-to-actuality collapse. Ask whether morphology, syntax, collocation, discourse, genre and parallel usage support X in this occurrence.
Result: PASS.

Unseen prompt: “Every occurrence with the same Strong number has the same meaning.”

Required reasoning: reject identifier = sense. Same lemma can realize different contextual senses/usages.
Result: PASS.

## Failure traps checked

- `GLOSS = MEANING`: rejected.
- `STRONG NUMBER = LEXICAL PROOF`: rejected.
- `LEXICON POSSIBILITY = VERSE ACTUALITY`: rejected.
- `ALL SENSES IMPORTED INTO ONE VERSE`: rejected.
- `OPEN ACCESS = MOST AUTHORITATIVE`: rejected.
- `HEBREW/GREEK/ENGLISH ONE-TO-ONE EQUIVALENCE`: rejected.

## Course-state decision

Unit 5 passes its local method and transfer gate. It authorizes disciplined use of inspectable lexica for range and candidate senses while preserving the explicit dependency on stronger/current lexicography for disputed semantic claims.

Next autonomous action: `BIBLICAL_LANGUAGES_I_UNIT_06_CONTEXT_DISCOURSE_AND_CORPUS_COMPARISON`.

Unit 6 should test how immediate syntax/discourse and corpus comparison constrain lexical possibilities, with explicit protection against frequency fallacies and illegitimate totality transfer.
