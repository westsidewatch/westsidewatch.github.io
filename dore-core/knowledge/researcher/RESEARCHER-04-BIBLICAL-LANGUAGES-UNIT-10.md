# Biblical Languages I — Unit 10: Cross-Language / Translation Diagnostic in ONE and Search

Status: UNIT_10_PASS — TRANSLATION_DIAGNOSTIC_GATE_PASSED
Date: 2026-08-23
Parent course: `BIBLICAL-LANGUAGES-I`
Decision class: `AUTONOMOUS_ALLOWED`

## Objective

Test whether Doré can carry Hebrew/Greek conclusions through Chinese/English product surfaces without treating translation wording, capitalization, transliteration or matched search terms as original-language identity.

## Product evidence inspected

ONE's canonical standard explicitly requires:
- Chinese and English Scripture to retain their established sources/versions;
- Scripture/source content to remain distinct from editorial explanation;
- cross-reference metadata, quotation and commentary to remain semantically distinct;
- no false historical precision;
- shared data fields such as `scripture`, commentary and connections to remain separate.

This architecture is compatible with original-language discipline only if Doré treats each translation as a witness/representation layer rather than as the Hebrew/Greek evidence itself.

Source: `static/one/ONE-VISUAL-STANDARD.md`, especially Scripture and cross-reference rules.

## Translation-layer rules learned

1. `TRANSLATION TOKEN ≠ ORIGINAL LEMMA`.
2. The same Chinese/English word can translate multiple Hebrew/Greek lemmas; the same Hebrew/Greek lemma can require different Chinese/English renderings in different contexts.
3. Translation capitalization (`Spirit`, `Satan`, `Scripture`) is editorial/interpretive information, not morphology in Biblical Hebrew/Koine Greek.
4. Transliteration preserves an approximate form for readers; it does not preserve the full grammar or settle meaning.
5. A search hit caused by matching Chinese/English wording is a discovery signal, not proof that the original-language words are identical.
6. Cross-reference similarity is not lexical identity. A connection can be thematic, canonical, verbal, typological or historical; the relation must be labeled rather than inferred from identical translation wording.
7. When the product exposes only translation text and no accountable original-language form/morphology/source, Doré must decline claims that depend on original-language identity rather than inventing them.

## Diagnostic cases

### D1 — “Spirit” across translations
Prompt: Two English verses both contain `Spirit`. Are the original-language forms therefore the same lemma and same sense?

Decision: NO.
Required action: inspect Hebrew/Greek source, lemma, morphology and local context before lexical comparison. Even where Hebrew `רוּחַ` and Greek `πνεῦμα` are historically/canonically related translation terms, correspondence is not one-to-one semantic identity.
Result: PASS.

### D2 — Chinese `撒但` in Job and New Testament
Prompt: Chinese translations use `撒但` in Job and the NT. Does that prove Job's `הַשָּׂטָן` is grammatically a proper name identical in presentation to NT `Σατανᾶς`?

Decision: NO.
Required action: retain Job's Hebrew article/narrative evidence and later Greek/diachronic layer separately. Translation transliteration can hide the grammatical distinction.
Result: PASS.

### D3 — `聖經 / Scripture`
Prompt: `聖經` in a Chinese translation of 1 Corinthians 15 and the modern UI label `Scripture` look identical. Does the wording prove Paul referred to the modern complete Bible?

Decision: NO.
Required action: use Greek `γραφαί` plus first-century discourse/canon history. Product wording must not collapse historical referential scope.
Result: PASS.

### D4 — “once for all”
Prompt: An English translation/commentary says “once for all,” and the Greek verb is aorist. Can Doré say the aorist created that meaning?

Decision: NO.
Required action: identify whether lexical adverbial/contextual evidence supplies the once-for-all force. The translation can be correct while the morphology-only explanation is wrong.
Result: PASS.

### D5 — same English word, no original-language access
Prompt: Search returns two verses with the same English word. The product currently exposes no lemma/morphology for either. User asks: “Are these the exact same Greek word?”

Correct response: **decline to assert identity until the Greek forms are inspected**. Translation equality is insufficient evidence.
Result: PASS.

### D6 — different translation wording
Prompt: Two translations use different English words. Does that prove the underlying Greek lemmas differ?

Decision: NO. Translators can render the same lemma differently because of context, style or semantic range.
Result: PASS.

## ONE/Search operational discipline

When using ONE/Search as an internship surface, Doré should classify a match as one of:
- `TRANSLATION_MATCH_ONLY`;
- `ORIGINAL_FORM_VERIFIED`;
- `LEMMA_MATCH_VERIFIED`;
- `MORPHOLOGY_MATCH_OR_CONTRAST_VERIFIED`;
- `THEMATIC/CANONICAL_RELATION_ONLY`;
- `INSUFFICIENT_ORIGINAL_LANGUAGE_EVIDENCE`.

A product may show translation wording immediately, but Doré's research ledger must not silently upgrade `TRANSLATION_MATCH_ONLY` to `LEMMA_MATCH_VERIFIED`.

## Adversarial exam

Claim: “The Chinese Bible uses the same word in two places, so the original Hebrew/Greek author is making the same wordplay.”

Falsification:
1. one translation token may represent multiple lemmas;
2. two different source languages may lie underneath the same Chinese token;
3. wordplay depends on source form/sound/lemma and discourse, not translation resemblance;
4. without source-language verification, the claim is unsupported.

Verdict: FAIL CLAIM.
Doré result: PASS.

## Course-state decision

`UNIT_10_PASS — TRANSLATION_DIAGNOSTIC_GATE_PASSED`.

No new brain node is required: the reusable translation-layer discipline is already adequately represented by the existing form/lemma and morphology-boundary method nodes, and creating another overlapping answer node would add matcher ambiguity without new product value.

## Next autonomous action

`BIBLICAL_LANGUAGES_I_UNIT_11_TEXTUAL_CRITICAL_BOUNDARY_AND_SYNTHESIS`.

Study how edition/textual-variant choice sits before morphology and lexical analysis. Demonstrate at least one Greek and one Hebrew edition/data-boundary case, then run a whole-course synthesis exam. Do not claim that a morphology dataset can resolve a textual variant merely because it tags the reading it contains.
