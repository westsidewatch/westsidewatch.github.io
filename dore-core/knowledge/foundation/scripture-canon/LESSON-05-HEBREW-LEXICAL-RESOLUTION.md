# Doré Lesson 05 — Hebrew Lexical Resolution

Status: ACTIVE

## Purpose

Doré must not stop at corpus-internal lexical identifiers. A research assistant must be able to resolve a Hebrew token from its OSHB lexical identifier to a human-readable Hebrew lexeme while preserving the original identifier and provenance.

## First training passage

Genesis 15:6, connected in Lesson 04 to Romans 4:3 and Galatians 3:6.

Target lexical resolutions:

- OSHB `539` → אמן (ʾmn)
- OSHB `3068` → יהוה (YHWH)
- OSHB `2803` → חשב (ḥšb)
- OSHB `6666` → צדקה (ṣdqâ)

Prefix markers such as `c/`, `b/`, and `l/` are grammatical/lexical components and must not be silently discarded. Resolution must preserve the raw OSHB value as evidence.

## Required representation

Each resolved lexical item must retain:

1. raw corpus lexical value;
2. parsed prefix components;
3. lexical identifier;
4. Hebrew lexeme;
5. transliteration when available;
6. lexical-source provenance;
7. corpus-snapshot provenance;
8. confidence/status.

## Rules

- Never replace the raw corpus identifier with a guessed lexeme.
- Never infer a Hebrew lexeme merely from an English or Chinese translation.
- A Strong-style number is an identifier, not a definition.
- Lexical equivalence across Hebrew and Greek is not automatic translation equivalence.
- LXX/NT correspondence, semantic overlap, and theological interpretation are separate claim layers.
- Preserve uncertainty explicitly.

## Lesson 05 milestone

Doré passes the first stage when Genesis 15:6 can be rendered as a provenance-preserving lexical witness and compared with Romans 4:3 / Galatians 3:6 without losing either corpus's own lexical analysis.
