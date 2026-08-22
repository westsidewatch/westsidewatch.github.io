# DORÉ Foundation Education — Course 01: Scripture Canon

Status: **IN PROGRESS**

Student: **Doré / 多雷**

Program: `DORÉ / Foundation → DORÉ / Researcher`

## Course purpose

Doré's first course is not a devotional summary and not a list of 66 book names. It establishes the canonical reference layer on which later language, history, theology, research, subtitle, visual and MCP work depends.

The goal is a machine-readable, provenance-aware Scripture substrate capable of answering not only “what verse?” but “which textual/canonical object is being referenced, how is it related to other objects, what source supports the relationship, and what remains uncertain?”

## Required competencies

### 1. Canon topology
- Protestant 66-book canon used by Westside Watch as the operational primary canon;
- Old Testament / New Testament division;
- book order, canonical identifiers, common Chinese and English names and abbreviations;
- chapter counts and verse-address normalization;
- awareness that Jewish, Catholic, Orthodox and other canonical traditions differ, without flattening those differences into the Westside operational canon.

### 2. Reference identity
Every canonical unit must have stable identifiers independent of display language. Chinese, English, Hebrew and Greek labels are aliases around the same canonical object, not separate truths.

Initial conceptual identity:

`canon → testament → book → chapter → verse → token`

Later layers may attach pericope, discourse, quotation/allusion and manuscript/textual metadata without changing stable canonical identity.

### 3. Original-language substrate
Doré must eventually support:
- Hebrew Bible token/lemma/morphology research;
- Biblical Aramaic identification and research;
- Greek New Testament token/lemma/morphology research;
- lexical identifiers and mappings;
- textual/version metadata;
- Unicode normalization and stable token identity where source data permits it.

### 4. Canonical entities and relationships
Doré must be able to connect Scripture references to:
- persons;
- places;
- peoples/nations;
- genealogical relationships;
- events;
- objects/institutions where useful;
- quotations and explicit citations;
- parallels and strong intertextual relationships;
- chronology/geography only with evidence and uncertainty preserved.

### 5. Epistemic separation
The canonical layer must never silently collapse these classes:

- `TEXT_EXPLICIT` — stated directly in the selected textual witness/translation;
- `TEXTUAL_DATA` — lemma, morphology, variant or textual metadata from an identified scholarly dataset;
- `CANONICAL_RELATION` — explicit quotation, parallel, genealogy or other defensible relationship;
- `SCHOLARLY_INFERENCE` — research conclusion requiring sources;
- `EDITORIAL_RECONSTRUCTION` — useful Westside/Doré working reconstruction;
- `TRADITIONAL_INTERPRETATION` — interpretation belonging to an identified tradition/source;
- `UNKNOWN / DISPUTED` — evidence does not warrant a single conclusion.

## Source policy for Course 01

Doré will not begin by copying arbitrary Bible websites. Foundation sources must be legally reusable, identifiable, versioned where possible, and suitable for provenance tracking.

Candidate foundation datasets must be reviewed before ingestion for:
- scholarly provenance;
- license and attribution requirements;
- update/version behavior;
- canonical/textual basis;
- machine readability;
- known limitations;
- whether a dataset contains text, analysis, interpretation, or a mixture.

No dataset becomes `canonical truth` merely because it is imported.

## First source candidates

### STEPBible Data
High-priority candidate for structured biblical data: original-language tagged texts, lexicons, proper names, references, morphology and versification resources. Current repository documentation states CC BY 4.0 for the STEPBible Data repository, but individual files/datasets must still retain their own attribution/license metadata at ingestion.

### Open Scriptures Hebrew Bible (OSHB)
High-priority Hebrew candidate. The WLC text is represented as public domain in OSHB documentation, while lemma/morphology data are CC BY 4.0. Doré should preserve the distinction between base text rights and analytical tagging rights.

### MorphGNT / SBLGNT
Candidate Greek New Testament research layer. Morphological parsing/lemmatization and underlying SBLGNT text have distinct licensing terms; Doré must not flatten them into one license record. Ingestion requires explicit provenance per component.

## Data architecture lesson 01

The first object Doré learns is not “Genesis is the first book.” It is **identity with provenance**.

Conceptual example:

```yaml
id: bible.book.GEN
kind: canonical_book
operational_canon: protestant_66
order: 1
testament: OT
names:
  zh-Hant: 創世記
  en: Genesis
  he: בראשית
aliases:
  - Gen
  - Gn
provenance:
  status: foundation
```

A reference then points to the stable identity:

```yaml
id: bible.ref.GEN.32.22
book_id: bible.book.GEN
chapter: 32
verse: 22
```

Language-specific display, versification mapping and textual witnesses are attached rather than baked into the identifier.

## First exercises

Doré must be able to demonstrate, using structured data rather than model memory alone:

1. normalize `創 32:22`, `Genesis 32:22`, and `Gen 32.22` to the same canonical reference;
2. distinguish Jacob, Jabbok and Penuel as different entity types and relate them to the correct canonical context;
3. identify when two traditions number a passage differently rather than treating one as an error;
4. return source/provenance for a Hebrew or Greek lexical/morphological claim;
5. refuse to label an interpretive conclusion as `TEXT_EXPLICIT`;
6. return `UNKNOWN / DISPUTED` when the evidence layer cannot support a unique answer.

## Course build sequence

`source registry → canon schema → book registry → reference normalizer → versification mapping → original-language ingestion → entity graph → cross-reference layer → provenance tests → Course 01 benchmark`

## Current lesson

**Lesson 01: Canonical identity, source provenance and licensing discipline.**

Doré begins Scripture study by learning that knowing a biblical fact includes knowing **what object is being discussed, which source says it, what kind of claim it is, and how confidently it may be asserted.**

Course 01 remains `IN PROGRESS` until the machine-readable source registry and canonical schema exist and the first exercises pass.