# Doré Language & Textual Intelligence Foundation

Status: ACTIVE

## Architectural decision

Doré will no longer learn biblical languages, modern languages, and Bible versions as isolated hand-fed curricula. The Hebrew work through Lesson 05B is the validated reference implementation. Its reusable method is now promoted into a universal language/text architecture.

## Universal pipeline

source -> snapshot -> ingest -> normalize -> segment/tokenize -> linguistic analyses -> lexical resolution -> concordance/context -> textual alignment -> intertext -> provenance -> validation/benchmark

Every language or textual witness plugs into this pipeline through an adapter. Language-specific knowledge belongs in adapters and analyzers; evidence, provenance, alignment, validation, and research contracts remain shared.

## First-class language/witness families

- Biblical Hebrew / Aramaic
- Koine Greek
- Septuagint Greek
- Latin
- Chinese
- Cantonese
- English
- additional languages without redesigning the core

## Witness model

A language is not a Bible version. A Bible version is a textual witness expressed in a language.

Examples:
- Hebrew Bible -> Hebrew witness
- Septuagint -> ancient Greek translation witness
- Greek New Testament -> Greek witness
- Vulgate -> Latin translation witness
- Chinese Union Version and other Chinese translations -> distinct Chinese witnesses
- KJV / NIV / other English translations -> distinct English witnesses

Each witness must retain edition/version identity, license/source, snapshot, canonical alignment, and provenance.

## Shared capabilities

1. loss-aware ingestion
2. canonical reference mapping
3. segmentation/tokenization
4. normalization without destroying surface evidence
5. morphology / syntax / lexical analyses when available
6. concordance and context windows
7. cross-language and cross-version alignment
8. quotation/allusion/intertext graph integration
9. uncertainty and claim-class separation
10. reproducible provenance and CI benchmarks

## Language adapters

Adapters declare capabilities instead of pretending every language has the same grammar.

Examples:
- Hebrew: consonantal/pointed forms, prefixes, roots, stems/binyanim, morphology
- Greek: lemma, case/number/gender, tense/aspect/voice/mood, morphology
- Latin: lemma and inflectional morphology
- Chinese: segmentation, traditional/simplified normalization, names/terminology, translation alignment
- Cantonese: speech/transcript segmentation, written vs colloquial forms, Jyutping when sourced, Mandarin/Chinese alignment
- English: tokenization, lemmatization where useful, historical/modern version comparison

## Scaling rule

Use a small audited practicum to validate a method. Once validated, generalize it and run it corpus-wide. Do not manually teach thousands of lexical items, people, places, or verses one by one.

Pattern:

AUDITED SAMPLE -> METHOD -> BENCHMARK -> CORPUS-WIDE INGESTION -> COVERAGE REPORT -> EXCEPTION QUEUE -> METHOD IMPROVEMENT

## Research guardrails

- Surface text is never overwritten by normalization.
- Translation equivalence is not lexical identity.
- Shared gloss is not proof of semantic equivalence.
- A language model's inference is not corpus evidence.
- Ancient translations remain independent textual witnesses.
- Modern translations remain distinguishable editions, not merged paraphrases.
- Cantonese and Mandarin/standard written Chinese are not silently conflated.
- Theology and interpretation may consume linguistic evidence but must remain separately classified claims.

## Immediate build target

Create a universal `LanguageAdapter` and `TextWitness` contract, migrate Hebrew and Greek onto it, then add LXX, Latin, Chinese, Cantonese, and English adapters through the same interface. Corpus-wide benchmarks replace word-by-word lessons.
