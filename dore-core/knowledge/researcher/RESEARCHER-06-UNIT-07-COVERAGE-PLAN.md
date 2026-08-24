# Researcher 06 — Unit 07 Coverage Expansion Without Test Leakage

Status: IN PROGRESS
Date: 2026-08-24

## Corpus-wide audit result
Against `mandarin-pinyin-lite-v1` and the existing `static/dore/entity-index.json`:
- entity rows: 4,293
- Chinese surfaces: 2,876
- Han occurrences: 14,953
- mapped Han occurrences: 4,602 (`30.78%`)
- unique Han: 774
- mapped unique Han: 39 (`5.04%`)
- fully covered Chinese surfaces: 67 (`2.33%`)
- unmapped unique Han: 735

This is much broader than the one held-out failure. V1 was intentionally tiny and is structurally incapable of general biblical-entity phonetic coverage.

## Learning decision
Do not hand-patch a small list of names. The next experiment must compare v1 with a maintained, comprehensive Mandarin pronunciation dataset/library on the **whole entity corpus**.

Reference candidate: `pinyin-pro`, pinned for the experiment to `3.29.3`.
Reasons:
- public JS library and usable under Node;
- MIT licensed;
- supports tone-free pinyin output and polyphonic handling;
- active package/repository maintenance as observed during this unit;
- appropriate as a research reference before deciding whether Doré should depend on it, vendor derived auditable data, or build a narrower biblical dictionary.

Sources consulted:
- https://github.com/zh-lx/pinyin-pro
- https://www.npmjs.com/package/pinyin-pro

## Boundary
The external library is not yet a production dependency and does not change `mandarin-pinyin-lite-v1`. It is used only as a pinned research reference to answer: "Can systematic pronunciation coverage solve the corpus-wide gap while preserving Doré's provenance/abstention discipline?"

## Next experiment
Run a whole-corpus reference coverage audit with `pinyin-pro@3.29.3`, persist coverage metrics, and compare them against the frozen v1 baseline. Do not consult or optimize against a new final held-out suite during this comparison.
