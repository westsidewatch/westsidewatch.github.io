# Biblical Languages I — Source Discovery and Minimal Stack

Status: SOURCE_STACK_SELECTED
Date: 2026-08-23
Parent: `RESEARCHER-04-LIVE-TEST-BIBLICAL-LANGUAGES.md`
Decision class: `AUTONOMOUS_ALLOWED`

## Discovery objective

Select a minimal, inspectable stack that can support the first learning units without pretending that one interlinear, Strong-number index, AI answer, or denominational commentary is sufficient authority.

## Evaluation rubric

Each source was evaluated for competence/authority, provenance/edition, pedagogical level, claim scope, inspectability/citability, framework/limitations, and assigned role.

## Selected minimal stack

### G1 — Owen Ewald, *Elementary New Testament Greek* (2022)

Role: `TEXTBOOK` — Greek foundations.
Publisher/provenance: Seattle Pacific University Library; open textbook; CC BY-NC-SA 4.0.
Authority: author is a classical-languages professor with long-term Greek teaching experience; university-library publication.
Pedagogical level: elementary; Chapter 1 begins with alphabet, words/names and nominal sentences; later chapters progress through clauses, cases, tense, mood, voice, participles and complex sentences.
Inspectability: open PDF/metadata through SPU and Open Textbook Library.
Limitation: pedagogical grammar, not an independent lexicon or textual-critical authority.
Sources:
- https://digitalcommons.spu.edu/open_books/2/
- https://open.umn.edu/opentextbooks/textbooks/elementary-new-testament-greek-2022

### G2 — Joseph R. Dongell, *Elementary New Testament Greek* (2014)

Role: `COUNTERPOINT + PRACTICE` — alternate Greek pedagogy and explicit tools/exegesis orientation.
Publisher/provenance: First Fruits Press, Asbury Theological Seminary; CC BY-NC 3.0.
Authority: seminary-published instructional grammar.
Pedagogical level: elementary; designed around parts of speech, grammar, verb system, vocabulary and actual NT examples.
Inspectability: full text openly downloadable from Asbury.
Limitation: a first-course grammar and explicitly dependent on stronger lexicon/exegetical references for advanced claims.
Source: https://place.asburyseminary.edu/academicbooks/6/

### H1 — Open Scriptures Hebrew Bible (OSHB) v2.2

Role: `PRIMARY_SOURCE + MORPHOLOGY/PARSING REFERENCE + PRACTICE`.
Provenance: Open Scriptures Hebrew Bible Project; Westminster Leningrad Codex text with OSHB lemma/morphology data; lemma/morphology CC BY 4.0, WLC text public domain.
Authority: long-running collaborative morphology project; v2.2 release states the morphology for the entire Hebrew Bible is completed and verified following the WLC.
Inspectability: repository exposes word-level text, lemma and morphology; morphology codes and parsing principles are documented.
Limitations: computational tagging is evidence to inspect, not an infallible grammatical judgment; README itself documents normalization/data-handling caveats.
Sources:
- https://github.com/openscriptures/morphhb
- https://github.com/openscriptures/morphhb/releases/tag/v2.2

### G3 — MorphGNT: SBLGNT Edition 6.12 (Tauber, 2017)

Role: `PRIMARY_SOURCE SUPPORT + MORPHOLOGY/PARSING REFERENCE + PRACTICE`.
Provenance: James K. Tauber, ed.; SBLGNT text combined with MorphGNT analysis; version 6.12; DOI 10.5281/zenodo.376200.
Authority: citable dataset with explicit column definitions and parsing codes.
Inspectability: repository exposes book/chapter/verse, POS, parsing code, text, normalized form and lemma.
Limitations: SBLGNT text remains under its EULA; MorphGNT parsing scheme notes that inherited CCAT codes are planned for deprecation in a future major release. Parsing remains an analysis layer, not a lexicon.
Source: https://github.com/morphgnt/sblgnt

### H2 — Beginning Biblical Hebrew (Cook & Holmstedt, 2013)

Role: `TEXTBOOK` — Hebrew pedagogical anchor.
Publisher/provenance: Baker Academic; faculty publication page at University of Toronto, Department of Near & Middle Eastern Civilizations.
Authority: authored by specialists in Biblical Hebrew; described as field-tested for more than a decade and informed by Hebrew linguistics.
Pedagogical level: beginning; short grammar lessons, workbook exercises and Hebrew reader.
Inspectability: bibliographic/description level is openly inspectable; full textbook is not open-access in the current tool path.
Limitation: full instructional content is not presently machine-inspectable here. Therefore it may anchor the bibliography/course design, but Doré must not claim to have studied inaccessible chapters.
Source: https://www.nmc.utoronto.ca/research-publications/faculty-publications/beginning-biblical-hebrew-grammar-and-illustrated-reader

### L1/L2 — Academic lexica (required, access boundary recorded)

Roles: `REFERENCE`.
Greek target: BDAG-class NT Greek lexicon.
Hebrew target: HALOT/Holladay-class Hebrew-Aramaic lexicon.
Evidence of curricular use: Asbury Greek materials explicitly teach use of BDAG; Asbury Hebrew syllabi list Holladay/HALOT alongside BHS and syntax references.
Current limitation: full licensed lexicon content is not available through the present open tool path. Doré may record the requirement and bibliographic role but must not fabricate lexicon entries or page-level claims.

## Selection decision

The operational minimum for Units 1–2 is:
- Greek pedagogy: Ewald 2022, checked against Dongell 2014 where useful;
- Greek primary/morphology surface: MorphGNT/SBLGNT;
- Hebrew primary/morphology surface: OSHB v2.2;
- Hebrew textbook anchor: Cook & Holmstedt, with an explicit content-access boundary;
- lexicon layer remains a required dependency for semantic-range units and cannot be replaced by morphology datasets.

This stack is sufficient to begin script/form/lemma and elementary parsing work. It is **not** sufficient to consolidate semantic-range or contested lexical claims until accountable lexicon access is inspected.

## Failure / boundary ledger

- `FULL_HEBREW_TEXTBOOK_CONTENT`: unavailable in current tool path; do not pretend chapter study occurred.
- `LICENSED_LEXICON_CONTENT`: not available; blocks later lexical-semantic consolidation, not Unit 1.
- `MORPHOLOGY_DATA != LEXICON`: explicitly preserved to prevent Strong-like gloss substitution.

## Next action

`BEGIN_BIBLICAL_LANGUAGES_I_UNIT_01_SCRIPT_FORM_LEMMA`
