# ONE — Record Index

Status: CURRENT / CANONICAL INDEX
System Atlas identity: `tool:one`

This file is the engineering entrypoint for ONE records under `docs/one/`. It indexes current and historical records; it does not make every older ONE document current.

## Product boundary

ONE is the Bible-study tool surface. Scripture coordinates are the durable content/world reference used to connect events, people, places, periods, themes, maps, media and study resources. ONE should reuse that shared Bible coordinate layer rather than maintaining an unrelated identity scheme.

The current cross-system direction is defined by `docs/CURRENT_MAINLINE.md` and the System Atlas. Paradise Cinema remains the active product mainline while its Bible-media Moment/BiblicalAnchor layer is completed; ONE remains a shared-coordinate consumer during this stage.

## Gospel Harmony records

The three 2026-08-29 reports are retained as provenance:

- `GOSPEL-HARMONY-AUDIT-20260829.md` — preliminary automated audit. It reported 32 structural/reference-column findings and was followed by later audits.
- `GOSPEL-HARMONY-CONSISTENCY-20260829.md` — intermediate consistency pass. It reported zero wrong-column/chapter-bound findings while retaining parser failures and editorial differences.
- `GOSPEL-HARMONY-FINAL-AUDIT-20260829.md` — strongest surviving audit evidence from that date. It inspected 23 Gospel source files and 288 harmony rows, reported zero wrong Gospel-column/chapter-bound findings and zero sermon-label-placement findings, while retaining 6 parser-review findings and 12 duplicate-label/extent cases for editorial judgment.

The final audit remains evidence, not a complete declaration of textual or historical equivalence. Its unresolved parser/editorial findings stay open until later evidence closes them.

## Record rules

1. Current system identity comes from `data/system-atlas.v0.json`.
2. Bible-world identity comes from the shared Bible Index.
3. This README is the current documentation index for ONE.
4. Dated audit reports remain evidence or superseded provenance and do not override newer code/tests by themselves.
5. A future Gospel Harmony specification should have explicit textual/editorial sources and its own acceptance gate before it becomes canonical.

## Reopen trigger

Revisit this record family when ONE receives a new Gospel Harmony specification, a shared Bible-coordinate runtime, or when current code/tests materially contradict the 2026-08-29 final audit evidence.
