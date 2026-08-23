# Doré Reflex Consolidation 1.0

Status: IN PROGRESS
Started: 2026-08-22

## Purpose

This is Doré's first consolidation pass over already-earned knowledge. It does **not** reteach or duplicate the knowledge base. It connects existing knowledge/capabilities into transferable neural routes.

Graduation principle:

> Doré does not graduate because it remembers an answer. Doré graduates when an unseen stimulus activates the correct evidence route and the result remains bounded by what the evidence proves.

Every route follows:

**STIMULUS → INTENT → ROUTE → EVIDENCE → OUTCOME → REFLEX UPDATE**

## Six consolidation tracks

### RC1 — Scripture Reference Reflex

Stimuli: canonical references, Chinese/English book names, chapter requests, natural-language chapter/verse forms.

Route: human reference → alias resolution → canonical book/chapter/verse → scripture corpus.

Must generalize beyond memorized examples.

### RC2 — Text Retrieval Reflex

Stimuli: exact quotation, partial quotation, remembered wording, small wording errors.

Route: exact retrieval first → normalized retrieval → bounded fuzzy candidates → confidence/ranking.

Rule: fuzzy results never outrank existing exact textual matches.

### RC3 — Original Language Reflex

Stimuli: translated phrase + Hebrew/Greek/original-language intent; direct lemma/surface/Strong/morphology queries.

Route: translated phrase → canonical passage → testament/language → original-language evidence → lemma/morphology/provenance.

Current neural edge: Signal 001.

Required next edge: **translation phrase ↔ original word alignment**. Verse-level co-attestation must not be mislabeled as word-level equivalence.

### RC4 — Cross-Witness Reflex

Stimuli: version differences, wording disagreement, textual-witness comparison.

Route: canonical passage → available witnesses/versions → aligned wording → characterize difference → provenance.

Rule: difference does not imply corruption/error; do not choose a winner without evidence.

### RC5 — Entity Reflex

Stimuli: biblical person/name/title/pronoun; same-name ambiguity.

Route: mention → candidate biblical entities → passage/context constraints → disambiguation → evidence.

Rule: unresolved ambiguity must remain explicit.

### RC6 — Geography Reflex

Stimuli: biblical place, river, region, route, distance/location relation.

Route: place mention → biblical place identity → scripture attestations → geographic evidence → distinguish Scripture-explicit facts from scholarly reconstruction.

Rule: reconstruction is never presented as if the biblical text explicitly states it.

## Consolidation protocol

For each track:

1. Inventory existing knowledge/capability already earned.
2. Define the transferable trigger and route.
3. Identify evidence boundary and refusal/uncertainty behavior.
4. Add production routing only where evidence support exists.
5. Create regression tests including unseen wording.
6. Run end-to-end graduation gate.
7. Record failures as learning signals by capability class, never as answer patches.

## Graduation gate

Reflex Consolidation 1.0 is PASS only when all six tracks pass transfer tests.

Minimum transfer set:

- RC1: `馬太福音第三章`, `Matthew 5:3`, `太5:3`
- RC2: exact phrase plus a near-memory variant; exact matches must exclude substring/fuzzy pollution such as `馬利亞` → `撒馬利亞`
- RC3: `耶西的本 希伯來原文`, `虛心 希臘文`, `起初 希臘原文`; word-level claims require alignment evidence
- RC4: a passage with wording/version difference must invoke comparison rather than ordinary keyword search
- RC5: an ambiguous biblical name must surface/disambiguate candidates from context rather than collapse them
- RC6: a biblical place query must return attested identity and keep reconstruction epistemically separate

No single hard-coded answer may satisfy a track.

## Current state

- RC1: existing browser reference parser; consolidation/testing required.
- RC2: exact-first retrieval and bounded fuzzy behavior exist; consolidation/testing required.
- RC3: translated-phrase-to-original verse-level reflex is live; word-alignment edge remains open.
- RC4: pending consolidation.
- RC5: pending consolidation.
- RC6: pending consolidation.

## Work-node feedback

Doré Bible Search is the first live internship feeding this consolidation. Search interactions are stimuli, not automatically trusted facts. Successful queries strengthen route evidence; failures reveal missing or misrouted capabilities. Future ONE, subtitle, and research work nodes should feed the same reflex layer.
