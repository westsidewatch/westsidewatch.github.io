# DORÉ Corpus Reader Specification v0.1

Status: **FOUNDATION IMPLEMENTATION SPEC**

## Purpose

Doré has completed first direct readings in Biblical Hebrew, Biblical Aramaic, and Greek. The next step is not manual verse-by-verse note taking. It is a reproducible reader that can traverse the pinned original-language corpora and transform source records into Doré's provenance-preserving knowledge contract.

## Reader pipeline

```text
Pinned upstream snapshot
        ↓
Source adapter
        ↓
Native reference parser
        ↓
Canonical reference mapper
        ↓
Token reader
        ↓
Language resolver
        ↓
Surface preservation
        ↓
Lemma / morphology analytical layers
        ↓
Per-layer provenance
        ↓
Validation
        ↓
Doré corpus record
```

## Adapters

### OSHB adapter

Input: `openscriptures/morphhb@3d15126fb1ef74867fc1434be1942e837932691f/wlc/*.xml`

Responsibilities:

- parse OSIS book/chapter/verse/token structure;
- preserve source-native OSIS references;
- preserve Hebrew/Aramaic surface data without destructive normalization;
- ingest lemma and morphology only as analytical layers;
- resolve Biblical Aramaic at passage/token level rather than blindly inheriting file-level `xml:lang="he"`;
- retain textual metadata exposed by source where supported;
- attach WLC provenance to textual surface and OSHB/OSHM provenance to analysis as appropriate.

### MorphGNT/SBLGNT adapter

Input: `morphgnt/sblgnt@aaed91e57c8e4a8dc9a2383e129ca5e75fe6393d/*-morphgnt.txt`

Responsibilities:

- parse source-native book/chapter/verse code;
- preserve inflected surface form;
- preserve normalized form when supplied;
- ingest lemma and morphology as analytical metadata;
- distinguish SBLGNT textual edition provenance from MorphGNT analytical provenance;
- map source-native references to Doré canonical IDs.

## Required output record

```yaml
token_id: stable-id
canonical_ref_id: bible.ref.GEN.1.1
source_native_ref: string
witness_id: string
language: he|arc|grc
order: integer
surface: string
normalized: string|null
analyses:
  - type: lemma|morphology|lexical_id
    value: string
    source_id: string
    confidence: number|null
provenance:
  textual_surface:
    source_id: string
    corpus_snapshot: string
validation:
  status: pass|warn|fail
  messages: []
```

## Language boundary rule

Book identity must never determine token language by itself.

For mixed-language books/passages, language assignment must be explicit and auditable. Daniel and Ezra are required foundation tests. Any unresolved boundary must produce `warn/review`, never a fabricated language label.

## Failure behavior

Reader must fail closed when:

- canonical reference cannot be mapped;
- source snapshot differs from pinned version without upgrade approval;
- textual surface has no provenance;
- analysis is present without analytical provenance;
- a token is silently discarded;
- Hebrew/Aramaic language resolution is required but unresolved and downstream code attempts to assert a language as fact.

Warnings are permitted for non-critical optional metadata, but warnings must remain queryable.

## Reading order

The ingestion engine may process corpora efficiently, but canonical identity and source-native order are both preserved.

Foundation completion requires full coverage of:

- 39-book Protestant Old Testament operational registry through OSHB where source coverage supports it;
- Biblical Aramaic passages represented distinctly;
- 27-book New Testament through pinned MorphGNT/SBLGNT;
- zero silent token drops;
- Lesson 03 provenance test suite passing.

## Principle

> Doré may read quickly. Doré may not read carelessly.
