# DORÉ CINEMA BIBLICAL EVENT CLOSURE — EVIDENCE LEDGER

Date: 2026-09-14
Status: BOUNDED_VERIFIED_COMPONENT
Workstreams: `CINEMA`, `ONE`, `SCRIPTURE-CANON`
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01`

## Evidence reviewed

- merged PR #772 — `ONE + Cinema: shared Biblical Event consumer v1`;
- merged PR #773 — `Paradise Cinema: close Biblical Event migration layer`;
- merge commits `8fea87638cf08067e14fbcbeb80fa9eb82118574` and `21fcd5475b2a4a9e5376c5513a5bb97ef5fb7506`;
- `data/bible-index/biblical-event.v1.json` authority move;
- `docs/one/biblical-event-consumer.v1.json` consumer contract;
- `cinema/data/bible-journey.v0.json`, `cinema/resource-graph.js`, `cinema/event-entry.js`;
- acceptance additions for shared consumer identity and Biblical Event closure.

## Verified bounded milestone

The Biblical Event identity migration is now closed at the repository/contract layer:

1. `data/bible-index/biblical-event.v1.json` is the shared Biblical Event authority for ONE and Paradise Cinema; the Cinema-private duplicate authority is removed.
2. ONE consumes stable `bible:event:*` identifiers without copying canonical labels, aliases or Scripture ranges.
3. Cinema consumes the same Bible Index authority and can resolve an admitted exact Moment from a canonical event entry.
4. Core Journey stations for Incarnation, Baptism, Crucifixion and Resurrection now carry canonical `eventId` values directly rather than deriving primary event identity from `world` aliases.
5. The empty `cinema/data/bible-journey-moment.v0.json` compatibility layer is removed. Editorial exact-Moment exceptions remain explicit as `exactMomentOverrides` on the Journey payload.
6. The authority boundary remains intact: Biblical Event identity does not itself grant media exactness; exact playback still requires an already-admitted official Moment.
7. Crucifixion and Resurrection remain distinct canonical event identities even where the current admitted media happens to resolve both to Episode 24.
8. PR #773 adds an explicit Biblical Event closure acceptance and updates the Holy Light Cinema gate to require the legacy compatibility files to stay absent.

## Classification

- shared Biblical Event authority migration: `VERIFIED_COMPLETE / COMPONENT`;
- ONE + Cinema shared-consumer contract: `VERIFIED_COMPLETE / COMPONENT`;
- old Cinema-private Biblical Event authority: `SUPERSEDED / REMOVED`;
- old Journey-Moment compatibility file: `SUPERSEDED / REMOVED`;
- alias/world-derived primary station event identity: `SUPERSEDED`;
- Paradise Cinema whole-product heterogeneous-provider reliability and production playback/readback: remains `ACTIVE_PARALLEL / UNKNOWN_NEEDS_EVIDENCE`.

## Retrospective evaluation

### Original objective

Remove duplicated Biblical Event truth and migrate ONE/Cinema to one stable Bible Index authority without allowing Scripture identity to manufacture media precision.

### Completion evidence

Both migration steps were merged to `main`; the repository diff removes the private/compatibility files, adds canonical event IDs and shared consumer contracts, and adds explicit acceptance coverage in the Cinema workflow.

### Current quality

Strong as an identity/authority closure. The migration reduces duplicate truth, removes an empty compatibility schema, and makes the exactness boundary explicit. It is materially better than the earlier alias-derived / Cinema-private arrangement.

### Durable learning

Shared domain identity should live at the Bible Index layer, while product surfaces consume identifiers and relationships rather than replicate canonical labels/aliases/ranges. Media exactness must remain a separate admission problem from biblical identity.

### Remaining weakness / debt

Repository closure does not prove production provider reliability, live event-entry playback/readback, or heterogeneous-source correctness. The current media corpus may legitimately map more than one distinct event to the same admitted episode, so product UX still needs to preserve event distinction clearly.

### Revisit trigger

Reopen this component only if a new consumer needs Biblical Event identity, the shared schema changes, or regression evidence shows private/alias-derived authority reappearing. Do not reopen merely to redesign Cinema UI.

## Sweep disposition

This closes a historical migration layer and should be retained as a regression-protected component milestone. It strengthens the `CINEMA` current-position narrative but does not promote Paradise Cinema as a whole to `VERIFIED_COMPLETE`.

P01 impact: NONE. No subtitle code path, blocker, binding, credential or ordering was changed.
