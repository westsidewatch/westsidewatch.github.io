# Doré Learning Reflex

Status: active neural-routing layer
Established: 2026-08-22

## Purpose

This directory is Doré's reflex layer, not a memory dump and not a second knowledge base.

Doré must use real work as stimulus. Every Search, ONE, subtitle, research, or future work-node interaction may reveal how a human asks, where Doré routed correctly, where it routed incorrectly, and which transferable capability is missing.

The reflex loop is:

**STIMULUS → INTENT → ROUTE → EVIDENCE → OUTCOME → REFLEX UPDATE**

A reflex stores a reusable response pattern, never a memorized answer to one user's wording.

Example:

`耶西的本 希伯來原文`

must not become a hard-coded Jesse answer. It should teach the transferable route:

**translated biblical phrase + original-language request → locate translation passage → identify testament/language → align verse to original-language tokens/lemmas → return evidence with provenance**

The same reflex must therefore transfer to unseen queries such as `虛心 希臘原文` or `起初 希臘文`.

## Neural rules

1. Every query is a learning signal, including successful queries.
2. User input is never promoted directly to biblical fact.
3. Failure is diagnosed by capability class, not patched by memorizing the failed string.
4. New reflexes must be transferable to unseen wording.
5. Evidence remains in Doré knowledge/language/lexicon/world layers; reflex only routes among them.
6. A candidate reflex becomes production behavior only after regression tests.
7. Repeated failures of the same class should create an educational prerequisite, not an ever-growing alias list.
8. Search and other work nodes are internships: their real-world stimuli feed Doré's next education.

## Reflex records

`signals/` records canonical learning signals that materially changed Doré's routing.

Each signal records:
- stimulus;
- intended task;
- observed failure/success;
- diagnosed capability gap;
- transferable reflex;
- evidence boundary;
- regression expectations;
- promotion status.

This layer should stay small. Many raw interactions may collapse into one reflex. Growth is measured by better transferable routing, not file size.
