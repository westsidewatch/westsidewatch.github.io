# Learning Signal 001 — translated phrase → original language

Date: 2026-08-22
Source work node: Doré Bible Search
Status: PROMOTED / VERIFIED THROUGH REFLEX CONSOLIDATION 1.0
Promotion evidence: `dore-core/reflex/REFLEX-CONSOLIDATION-1.0.md`, PR #233, Doré Reflex Consolidation run #7 SUCCESS, Doré Foundation Tests run #87 SUCCESS.

## Stimulus

`耶西的本 希伯來原文`

Observed variant: `耶西的本 希伯來文`

## Human intent

The user is not searching for the literal full Chinese string. They are asking for the Hebrew underlying a translated biblical phrase.

## Failure

The browser search treated the whole query as ordinary Chinese keyword text. Original-language indexes were only loaded when the query itself already contained Hebrew/Greek, a Strong-like identifier, or morphology syntax.

Doré therefore possessed both translation and original-language corpora but failed to route between them.

## Diagnosed gap

`BIBLICAL_QUERY_UNDERSTANDING.TRANSLATED_PHRASE_TO_ORIGINAL`

This is a routing/query-understanding gap, not a missing-Jesse fact.

## Transferable reflex

When a query contains an original-language intent marker (for example `希伯來文`, `希伯來原文`, `希腊文`, `希臘文`, `原文`, `Hebrew`, `Greek`):

1. remove the intent marker from the retrieval phrase without discarding it;
2. locate exact translated-text passages first;
3. infer expected source language from explicit request and testament;
4. lazy-load the original-language index;
5. reverse-align each matched verse to original surface forms and lemmas already attested for that canonical verse;
6. show the translated verse plus original evidence and provenance;
7. do not claim that every token in the verse is the exact lexical equivalent of the user's phrase unless word-level alignment evidence exists.

## Evidence boundary

Verse-level co-attestation is evidence that an original token occurs in the matched verse. It is **not yet word-level translation alignment**. Until Doré learns/earns word alignment, output must label the Hebrew/Greek material as original-language terms attested in the verse rather than falsely claiming an exact one-to-one translation mapping.

## Regression gate

Required transferable cases:

- `耶西的本 希伯來原文`
- `耶西的本 希伯來文`
- `起初 希臘原文`
- `虛心 希臘文`

The first two must locate the translated passage containing `耶西的本` and expose Hebrew evidence from that verse. Passing only the Jesse wording is not graduation.

## Reconciliation note — Sweep 01

This signal was originally persisted as `candidate reflex; regression required`. That status became stale after Reflex Consolidation 1.0 graduated. The historical failure and diagnosis remain valid provenance, while promotion is now bounded by RC3 and the end-to-end transfer/regression evidence in PR #233. This does not upgrade verse-level co-attestation into word-level translation alignment, and it does not prove production-wide Search relevance quality.