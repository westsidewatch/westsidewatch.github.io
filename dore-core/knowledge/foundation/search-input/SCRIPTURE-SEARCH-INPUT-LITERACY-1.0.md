# Scripture Search Input Literacy 1.0

Status: FOUNDATION MICRO-UNIT / NOT GRADUATED
Purpose: teach Doré the real-world forms people use when asking for Scripture references.

## Principle

Human Bible-reference input is not a formal citation language. Doré should first learn the stable, common conventions that require no theological reasoning.

This unit is **input literacy**, not autonomous inference. Common book abbreviations, Chinese/Arabic chapter numbers, punctuation variants and multiple references are basic reality and should be accepted directly.

## Required capabilities

Doré must understand at least:

- full Chinese book names;
- common Chinese book abbreviations for all 66 books;
- Arabic chapter numbers: `帖後3`, `羅3`;
- Chinese chapter numbers: `帖後三`, `羅三`;
- explicit chapter wording: `帖後3章`, `帖後三章`;
- single verse: `羅3:12`, `羅3：12`, `羅三12節`;
- verse range: `羅3:12-16`, `帖後3：15-19`;
- chapter-and-verse wording: `帖後3章8節到10節`;
- punctuation/range variants: `-`, `–`, `—`, `～`, `至`, `到`;
- multiple independent references in one query, separated by whitespace, Chinese/English semicolon, comma, slash, newline or similar ordinary delimiters;
- overlapping multi-reference results must be deduplicated.

## Examples that must work

- `羅馬書3：12-16`
- `羅3:12-16`
- `林前 8:9-15`
- `賽三第四節`
- `帖後3章八節到十節`
- `帖後三`
- `帖後3`
- `帖後3：15-19 創世紀2:5-9`
- `羅3:12-16；詩23:1`
- `太5:3-12 約3:16 羅8:28`

## Boundary

This unit does **not** claim that Doré can infer arbitrary typos, ambiguous prose or malformed references. Those failures should later become learning signals for the autonomous-learning system.

A known standard abbreviation is not a reasoning problem and should never be left for Doré to "discover" through trial and error.

## Graduation

Pass only when unseen references using different books and formatting variants transfer without book-specific patches. Multi-reference tests must include two and three references and mixed single/range references.

## Sweep 01 evidence state — 2026-08-27

Current repository implementation is partial and does not yet satisfy this graduation paragraph. Core and browser Search each contain useful reference parsing, but they differ in alias/range grammar and the bounded review found no shared all-66-book, multi-reference, deduplication transfer fixture proving parity or graduation.

Canonical missing-evidence guardrail: `DORÉ-MISSING-EVIDENCE-REGISTER.md#ME-010`.
Detailed implementation reconciliation: `dore-core/projects/DORÉ-SCRIPTURE-SEARCH-INPUT-EVIDENCE-LEDGER-2026-08-27.md`.

Do not issue a completion token for this micro-unit until the shared unseen acceptance corpus passes without book-specific patches.