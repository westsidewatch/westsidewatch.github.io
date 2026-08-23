# Doré Reflex Consolidation 1.0

Status: **GRADUATED — PASS**
Started: 2026-08-22
Graduated: 2026-08-22

## Purpose

Doré's first consolidation pass over already-earned knowledge. It does **not** duplicate the knowledge base. It connects existing knowledge/capabilities into transferable neural routes.

Graduation principle:

> Doré does not graduate because it remembers an answer. Doré graduates when an unseen stimulus activates the correct evidence route and the result remains bounded by what the evidence proves.

Every route follows:

**STIMULUS → INTENT → ROUTE → EVIDENCE → OUTCOME → REFLEX UPDATE**

## Consolidated tracks

### RC1 — Scripture Reference Reflex
Human references, Chinese/English book names, abbreviations, Chinese chapter numerals and chapter-level requests route to canonical references. Transfer gate includes Matthew and unseen John stimuli.

### RC2 — Text Retrieval Reflex
Strict normalized exact matches suppress containment pollution; containment is secondary; bounded fuzzy retrieval is fallback only and remains candidate evidence. Canonical failure guarded: `馬利亞` must not be polluted by `撒馬利亞` when a strict match exists.

### RC3 — Original Language Reflex
Translated phrase → canonical passage → Hebrew/Greek evidence → lemma/morphology. Verse-level co-attestation is explicitly prevented from becoming a word-level equivalence claim. Word-level upgrade requires explicit `translation_alignment` evidence. Transfer stimuli include `耶西的本`, `虛心/虚心`, and `太初/起初` patterns. Chinese simplified/traditional script variants are normalized as a transferable routing capability rather than phrase-specific aliases.

### RC4 — Cross-Witness Reflex
Canonical passage → aligned witnesses → difference characterization. Missing witnesses are never synthesized and no witness is presumed the winner.

### RC5 — Entity Reflex
Mention → candidate entities → context attestation → resolution. Same-name ambiguity must remain visible until context actually constrains it.

### RC6 — Geography Reflex
Place identity → Scripture attestation → geographic evidence → epistemic separation. `SCRIPTURE_EXPLICIT` and `SCHOLARLY_RECONSTRUCTION` remain distinct evidence classes.

## End-to-end graduation gate

Production gate files:

- `dore_core/reflex.py`
- `tests/test_reflex_consolidation.py`
- `tests/test_dore_bible_search.py`
- `.github/workflows/dore-reflex-consolidation.yml`

The workflow runs both the dedicated six-track transfer suite and the existing Doré Bible Search regression suite.

PASS conditions:

1. RC1 natural-language reference transfer passes.
2. RC2 exact-first retrieval and bounded fuzzy fallback pass.
3. RC3 Hebrew/Greek transfer works while alignment claims stay evidence-bounded.
4. RC4 cross-witness comparison preserves witness identity and uncertainty.
5. RC5 ambiguous entities remain ambiguous until context evidence resolves them.
6. RC6 geography keeps Scripture statements and reconstruction separate.
7. Existing Bible Search regression tests remain green.

No hard-coded answer to one user query is sufficient for graduation.

## Graduation evidence

Observable PR gate: **#233**.

- Run #5 exposed a CI-environment defect: pytest was not installed. The gate correctly failed before testing capability.
- Run #6 installed pytest and exposed a real transfer defect: simplified `这` did not normalize to traditional `這`; result was **13 passed, 1 failed**.
- The Chinese script-variant reflex was corrected at the class level, not with a verse-specific patch.
- Run #7: **Doré Reflex Consolidation 1.0 — SUCCESS**.
- Doré Foundation Tests run #87 on the same head: **SUCCESS**.

The verified green head was `142f2426acf0bdee2bf34cb3addb1a6d5127ad97`, merged to main through PR #233 as `533801ada388029362e9ed21bc2cc6310c84ccbf`.

## Final state

- RC1: PASS
- RC2: PASS
- RC3: PASS at current evidence boundary; word-level equivalence still requires explicit alignment evidence
- RC4: PASS
- RC5: PASS
- RC6: PASS
- End-to-end graduation workflow: PASS
- Foundation regression: PASS

**Reflex Consolidation 1.0 is graduated.**

## Learning-loop consequence

Doré Bible Search is the first live internship feeding this reflex layer. Search interactions are stimuli, not automatically trusted facts. Success strengthens reusable routes; failure becomes a capability-class learning signal. ONE, subtitle proofreading, and research work nodes should feed the same reflex system rather than separate answer memories.
