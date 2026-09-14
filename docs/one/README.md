# ONE — Record Index

Status: CURRENT / CANONICAL INDEX
System Atlas identity: `tool:one`

This file is the engineering entrypoint for ONE records under `docs/one/`. It indexes current and historical records; it does not make every older ONE document current.

## Product boundary

ONE is the Bible-study tool surface. Scripture coordinates are the durable content/world reference used to connect events, people, places, periods, themes, maps, media and study resources. ONE reuses the shared Bible Index rather than maintaining an unrelated identity scheme.

Canonical Biblical Event identity now lives at `data/bible-index/biblical-event.v1.json`. ONE consumes it through `biblical-event-consumer.v1.json`; the join key is the stable `eventId`, never the display label or alias. ONE does not duplicate canonical event metadata and cannot grant media exactness.

The same event identity is consumed by Paradise Cinema. ONE may hand an event to Cinema with `/cinema/?event={eventId}#cinema-library`; Cinema then resolves only already-admitted official Moments and converts the event entry to its exact Moment deep link. This preserves the boundary: Bible identity can connect surfaces, but it cannot make an unadmitted source exact.

## Current shared-event consumer

- Authority: `data/bible-index/biblical-event.v1.json`
- ONE consumer: `docs/one/biblical-event-consumer.v1.json`
- Cinema consumer: `cinema/resource-graph.js`
- Cross-surface join: canonical `bible:event:*` identity
- Current core identities: Incarnation, Baptism of Jesus, Crucifixion, Resurrection
- Crucifixion and Resurrection remain distinct events even when the current admitted Cinema evidence resolves both to the same official Episode 24.

## Gospel Harmony records

The three 2026-08-29 reports are retained as provenance:

- `GOSPEL-HARMONY-AUDIT-20260829.md` — preliminary automated audit. It reported 32 structural/reference-column findings and was followed by later audits.
- `GOSPEL-HARMONY-CONSISTENCY-20260829.md` — intermediate consistency pass. It reported zero wrong-column/chapter-bound findings while retaining parser failures and editorial differences.
- `GOSPEL-HARMONY-FINAL-AUDIT-20260829.md` — strongest surviving audit evidence from that date. It inspected 23 Gospel source files and 288 harmony rows, reported zero wrong Gospel-column/chapter-bound findings and zero sermon-label-placement findings, while retaining 6 parser-review findings and 12 duplicate-label/extent cases for editorial judgment.

The final audit remains evidence, not a complete declaration of textual or historical equivalence. Its unresolved parser/editorial findings stay open until later evidence closes them.

## Record rules

1. Current system identity comes from `data/system-atlas.v0.json`.
2. Bible-world identity comes from the shared Bible Index.
3. Biblical Event identity comes from `data/bible-index/biblical-event.v1.json`.
4. ONE references canonical event IDs and does not copy event labels, aliases or Scripture ranges into a second authority.
5. Dated audit reports remain evidence or superseded provenance and do not override newer code/tests by themselves.
6. Gospel Harmony specifications require explicit textual/editorial sources and an acceptance gate before becoming canonical.
