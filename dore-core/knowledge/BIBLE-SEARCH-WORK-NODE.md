# Doré Bible Search — first earned work node

Date: 2026-08-22
Source milestone: `SCRIPTURE_READING_COMPLETE`

## Role

Bible Search is the first external work node earned by Doré. It is not a fork of Doré and not a separate intelligence product. It is a stable service boundary through which ONE, Westside Stories, the Westside Watch site and later consumers can ask Doré Scripture-search questions.

## v0.1 contract

Core implementation: `dore_core.search.BibleSearchIndex`

Supported query modes:
- `reference`
- `text`
- `lemma`
- `morphology`
- `fuzzy`

Every result carries canonical reference, witness identity, language, match score/type, analyses when available and provenance. Fuzzy retrieval returns candidates only and must not be represented as certainty.

## Growth rule

Do not replace this node every time Doré learns something new. Extend the same service boundary as new milestones earn new capabilities: entities/places, chronology, historical context, semantic domains, quotations/allusions, brand vocabulary and later Researcher evidence synthesis.

## Product rule

Consumers must call Doré rather than duplicate Doré's Scripture intelligence locally when practical. Product-specific presentation remains outside Core.
