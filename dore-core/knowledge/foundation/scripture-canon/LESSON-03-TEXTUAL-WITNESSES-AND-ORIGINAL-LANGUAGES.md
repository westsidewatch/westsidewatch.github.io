# DORÉ Foundation — Scripture Canon
## Lesson 03: Textual Witnesses, Versification, and Original-Language Substrate

Status: **IN PROGRESS**

Student: **Doré / 多雷**

## Lesson principle

A verse address is not the text itself. A translation is not the original-language witness. A lemma is not a surface token. A morphological analysis is not the same kind of claim as the wording of a manuscript tradition.

Doré must therefore learn to ask, before asserting textual detail:

1. Which canonical reference?
2. Which versification system?
3. Which textual witness or edition?
4. Which language?
5. Which token/lemma/morphological dataset?
6. Which part is textual data, and which part is scholarly analysis?
7. What source and license govern each layer?

## 1. Reference identity versus versification

Stable canonical identity and displayed numbering must be separable.

Conceptual model:

```text
canonical passage identity
        ↓
versification mapping
   ↙           ↘
tradition A   tradition B
reference     reference
```

Doré must never assume that different verse numbering automatically means one tradition is wrong. A mapping record should preserve the systems being mapped and the evidence/source for the mapping.

## 2. Textual witness model

A canonical reference may be associated with multiple textual witnesses/editions. Doré must not collapse them into a single timeless string called `the original`.

Initial witness classes:

- Hebrew/Aramaic Masoretic textual data;
- Greek New Testament critical/edited textual data;
- ancient versions and manuscript evidence when later courses require them;
- modern translations as translation witnesses, never mislabeled as original-language evidence.

Each witness/edition requires stable identity, language, textual basis/edition metadata, source, license and version/date where available.

## 3. Token identity

Original-language research should distinguish at least:

```text
surface token
→ normalized token
→ lemma
→ morphology
→ lexical identifier(s)
```

These layers may come from different datasets. Doré must preserve that provenance rather than present a lemma or parsing as though it were simply printed in the biblical text.

## 4. Hebrew and Biblical Aramaic

Foundation goals:

- identify Hebrew versus Biblical Aramaic passages/tokens where the source dataset supports it;
- retain consonantal/vocalized surface forms without destroying Unicode distinctions;
- map tokens to lemmas and morphology with dataset provenance;
- support lexical identifiers without treating Strong's numbering as the meaning of a word;
- preserve ketiv/qere or other textual metadata when the chosen source exposes it;
- distinguish textual wording from later analytical tagging.

## 5. Greek New Testament

Foundation goals:

- preserve Greek surface forms and normalized forms;
- map inflected tokens to lemmas;
- retain morphological parsing with source provenance;
- distinguish the licensed biblical text/edition from morphology produced by another project;
- support lexical identifiers and future semantic/usage research without reducing meaning to dictionary glosses.

## 6. Claim discipline

Examples of classifications:

- `TEXT_EXPLICIT`: wording present in an identified witness/translation at an identified reference.
- `TEXTUAL_DATA`: lemma, morphology, textual variant metadata or versification mapping from an identified dataset.
- `SCHOLARLY_INFERENCE`: conclusion about likely original reading, dating, semantics or historical relationship that requires scholarly argument.
- `TRADITIONAL_INTERPRETATION`: interpretation belonging to a named tradition/source.

Doré must not upgrade `TEXTUAL_DATA` or `SCHOLARLY_INFERENCE` into `TEXT_EXPLICIT`.

## 7. Required machine-readable objects

Lesson 03 introduces these conceptual objects:

```yaml
textual_witness:
  id: witness.example
  language: he|arc|grc|zh-Hant|en
  edition: string
  source_id: source.example
  license_id: string

text_token:
  id: token.example
  witness_id: witness.example
  canonical_ref_id: bible.ref.GEN.1.1
  surface: string
  normalized: string|null
  lemma: string|null
  morphology: string|null
  lexical_ids: []
  provenance: []

versification_map:
  source_system: string
  source_ref: string
  target_system: string
  target_ref: string
  relation: equivalent|split|merged|shifted|disputed
  provenance: []
```

## 8. Research habits taught in this lesson

Doré must learn:

- never cite an original-language claim without identifying its data source;
- never call a modern translation `the Hebrew` or `the Greek`;
- never infer lexical meaning from Strong's numbers alone;
- never erase textual disagreement for the sake of a cleaner answer;
- never call verse-number differences textual contradictions before checking versification;
- prefer explicit uncertainty to invented harmonization.

## Exercises

Doré will eventually be required to demonstrate:

1. map a reference whose numbering differs between traditions without declaring either reference invalid;
2. return a Hebrew token, lemma and morphology while naming the source of each analytical layer;
3. identify a Biblical Aramaic context without treating the whole Old Testament as Hebrew;
4. return a Greek surface form and lemma without confusing inflection with lexical identity;
5. distinguish a textual variant claim from a translation difference;
6. answer `insufficient evidence` when the available dataset cannot support a textual conclusion.

## Lesson completion gate

Lesson 03 is not complete merely because this document exists. Completion requires:

- a witness registry;
- a versification schema/registry;
- original-language ingestion contracts;
- provenance fields per textual/analytical component;
- tests that prevent witness, translation, lemma and interpretation layers from collapsing into one another.

## Maxim

> **Read the text as text, analysis as analysis, interpretation as interpretation, and preserve the path between them.**
