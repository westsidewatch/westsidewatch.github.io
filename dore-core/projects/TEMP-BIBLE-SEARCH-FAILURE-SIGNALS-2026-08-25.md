# TEMP — Bible Search Failure Signals / External Prompt

Status: TEMPORARY / ACTIVE UNTIL DORÉ SELF-DETECTS, GENERALIZES, REPAIRS, AND VERIFIES
Created: 2026-08-25
Owner: Westside Watch
Executor / steward: Doré

## Why this temporary memo exists

Doré is still in a foundation-building stage. External human prompts remain necessary when real product failures are observed but Doré has not yet demonstrated that it can reliably detect, reflect on, generalize, repair, and verify those failures by itself.

This memo records the observed Bible Search failures as external evidence only. It MUST NOT prescribe Doré's final diagnosis. Doré must produce and persist its own reasoning/judgment about root cause, scope, repair strategy, and regression evidence.

Delete this memo only after the failures below have been independently detected/reconciled by Doré, a systemic diagnosis is recorded, a non-patch repair is verified, and the relevant durable learning has entered canonical Search/Core knowledge and work state.

## Observed real-use failures

### F1 — Relevant biblical concept not retrieved

User query:

`Tablets of the Testimony`

Observed result:

- Expected biblical/KJV-related material was not retrieved adequately.
- In particular, KJV wording such as `tables of the testimony` should be discoverable from a modern-English query using `tablets`.

Why this matters:

- This is not merely an exact-string mismatch.
- It potentially exposes insufficient cross-version lexical association, phrase normalization, biblical-entity/concept association, or ranking/retrieval behavior.
- Doré already has substantial multilingual / multi-version Bible knowledge substrate; the observed weakness appears to be in association/retrieval rather than simple absence of Bible data.

Important constraint:

Do NOT fix this only by adding a one-off synonym such as `tablets = tables`. Doré must decide whether this is one instance of a wider systemic class.

### F2 — Irrelevant English text still produces Scripture results

Observed behavior:

- A random/non-biblical English word combination can still cause Bible Search to display Scripture results.

Why this matters:

- Search is producing false positives instead of abstaining when biblical relevance is insufficient.
- This indicates a relevance-boundary / precision / abstention problem, not simply a fuzzy-search tuning issue.

Expected higher-level behavior:

- Relevant biblical queries should have strong recall.
- Irrelevant queries should have strong precision and should NOT be forced into Scripture results.
- When evidence of biblical relevance is weak, Search must be able to return no confident Scripture match rather than fabricate association.

## Combined signal

These two failures point in opposite directions:

`relevant biblical concept → missed`  (false negative)

`irrelevant non-biblical query → Scripture returned`  (false positive)

Doré must determine whether they share a deeper systemic cause in retrieval relevance, lexical/concept association, ranking/calibration, or another layer.

The expected learning target is NOT a pair of local patches. The desired capability is:

`Observe → classify failure → diagnose → decide isolated vs systemic → generalize → repair architecture/rules/model → regression-test broad classes → persist learning → update canonical work state`

## Required Doré-owned judgment record

Doré should eventually persist its own record containing at least:

- observed failure(s)
- diagnosis
- evidence supporting diagnosis
- confidence / uncertainty
- isolated-vs-systemic scope judgment
- affected query classes
- repair decision
- regression-test design
- regression results
- what durable learning returns to Core/Search

The diagnosis must be Doré's own conclusion. This memo is only an external prompt and evidence checkpoint.

## Suggested benchmark dimensions (not a prescribed implementation)

Doré should consider whether a proper global search benchmark needs coverage across:

- exact Scripture wording
- translation/version lexical variants
- singular/plural / archaic-modern English variation
- spelling/typing noise
- synonymous biblical concepts/entities
- cross-language Chinese↔English retrieval
- indirect biblical concepts
- ranking of exact/equivalent/related results
- truly unrelated random text
- adversarial/noise strings
- explicit abstention when relevance is insufficient

Example relation that should be tested as a concept/version-alignment case:

`Tablets of the Testimony` ↔ KJV `tables of the testimony`

## Priority rule discovered by the human side

A live user-facing core capability failure has very high learning priority. If Doré is performing real Scripture Search work and a real user operation demonstrates failure, the failure signal should outrank ordinary curriculum/research/new-feature work for reflection/diagnosis, subject to safety and active critical-path dependency constraints.

Especially high-value are cases where the underlying knowledge appears to exist but Doré cannot connect or retrieve it correctly, because these expose association/reasoning/retrieval limits rather than missing content alone.

## Completion / deletion tests

- [ ] Doré independently records/reconciles F1 and F2 as real product failures.
- [ ] Doré produces its own diagnosis rather than copying this memo's possible causes.
- [ ] Doré explicitly decides isolated vs systemic scope with evidence.
- [ ] Repair is broader than one-off phrase patching unless Doré proves the case is truly isolated.
- [ ] Relevant-query recall improves on a broader unseen benchmark.
- [ ] Irrelevant-query precision/abstention improves on a broader unseen benchmark.
- [ ] Cross-version lexical/concept retrieval is tested, including `tablets` → KJV `tables`.
- [ ] Existing successful Scripture search cases do not regress.
- [ ] Durable learning is written into canonical Search/Core knowledge/work state.
- [ ] Doré's self-reflection/failure loop can detect a later similar failure without external human prompting.

When all applicable boxes are verified with evidence, delete this temporary memo.