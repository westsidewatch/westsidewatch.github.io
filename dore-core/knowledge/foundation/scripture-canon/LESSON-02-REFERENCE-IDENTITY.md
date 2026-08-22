# DORÉ Scripture Canon — Lesson 02: Reference Identity

Status: **COMPLETED — DATA LAYER CREATED**

## What Doré learned

A Scripture reference is an address to a stable canonical object, not a display string.

Therefore:

- `創 32:22`
- `創世記 32:22`
- `Genesis 32:22`
- `Gen 32.22`

must normalize toward the same identity:

`bible.ref.Gen.32.22`

The display language is presentation. The canonical identity is infrastructure.

## Canon registry

`BOOK-REGISTRY-PROTESTANT-66.yaml` now supplies the operational Westside Watch 66-book topology with stable OSIS-style book keys, order, testament, chapter count, Traditional Chinese and English names, and initial aliases.

This registry describes the operational canon. It does **not** assert that all Christian or Jewish traditions have the same canon/order/versification.

## Normalization contract v0.1

Input stages:

1. Unicode normalize;
2. trim/collapse whitespace;
3. recognize book alias without losing the original input;
4. parse chapter/verse/range separators (`:`, `.`, full-width variants where safe);
5. resolve alias to canonical book ID;
6. validate chapter against registry;
7. validate verse only against an identified versification dataset — never invent verse maxima from model memory;
8. emit normalized reference plus provenance and warnings.

Conceptual output:

```yaml
input: "創 32:22"
normalized:
  id: bible.ref.Gen.32.22
  book_id: bible.book.Gen
  chapter: 32
  verse: 22
resolution:
  matched_alias: 創
  registry: BOOK-REGISTRY-PROTESTANT-66.yaml
warnings: []
```

## Ambiguity rule

An alias is not accepted merely because it looks plausible. If an alias can map to more than one object in the active language/context, Doré must request or infer context only when evidence warrants it; otherwise it returns ambiguity.

## Versification rule

Canonical reference identity and verse numbering are related but not identical. Doré must preserve the source versification system and explicit mappings when numbering differs among textual/canonical traditions.

## Source lesson

Course 01 source review confirmed the importance of component-level licensing:

- STEPBible Data repository documentation describes its data repository as CC BY 4.0 with attribution and change-record expectations.
- Open Scriptures Hebrew Bible states that the Westminster Leningrad Codex base is public domain while its analytical work is CC BY 4.0.
- MorphGNT distinguishes its morphological parsing/lemmatization license from the underlying Greek text. The current Faithlife SBLGNT repository separately states SBLGNT is CC BY 4.0. Doré therefore records the actual component and authoritative source rather than inheriting a stale aggregate license statement.

This is itself part of Doré's education: **research includes checking the current authoritative source rather than trusting an old summary.**

## Pass condition

Lesson 02 passes at the schema/data-design level when:

- stable book IDs exist for all 66 operational books;
- multilingual aliases are presentation/resolution data rather than identity;
- chapter bounds are machine-readable;
- verse validation is explicitly deferred to sourced versification data;
- ambiguity is representable rather than silently guessed.

All conditions are now represented in the foundation files.

## Next lesson

**Lesson 03 — Versification, textual witnesses, Hebrew/Aramaic/Greek substrate.**

This is where Doré moves from knowing the Bible's address system to reading the source-language research layer behind those addresses.
