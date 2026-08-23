# Doré Reflex Consolidation 1.0

Status: GATE RUNNING — PASS requires CI confirmation
Started: 2026-08-22

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
Translated phrase → canonical passage → Hebrew/Greek evidence → lemma/morphology. Verse-level co-attestation is explicitly prevented from becoming a word-level equivalence claim. Word-level upgrade requires explicit `translation_alignment` evidence. Transfer stimuli: `耶西的本`, `虛心`, `太初/起初` pattern.

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

## Current gate state

- RC1: IMPLEMENTED + GATED
- RC2: IMPLEMENTED + GATED
- RC3: IMPLEMENTED + GATED; word-level claims require explicit alignment evidence
- RC4: IMPLEMENTED + GATED
- RC5: IMPLEMENTED + GATED
- RC6: IMPLEMENTED + GATED
- End-to-end workflow: INSTALLED
- Final milestone: **NOT YET DECLARED PASS until the GitHub Actions run is observed green.**

## Learning-loop consequence

Doré Bible Search is the first live internship feeding this reflex layer. Search interactions are stimuli, not automatically trusted facts. Success strengthens reusable routes; failure becomes a capability-class learning signal. ONE, subtitle proofreading, and research work nodes should feed the same reflex system rather than separate answer memories.
