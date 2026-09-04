# DORÉ ONE — SCRIPTURE-FIRST / CROSS-REFERENCE EVIDENCE LEDGER

Date: 2026-09-04
Status: DURABLE_EVIDENCE_LEDGER
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
P01 impact: NONE

## Scope

This ledger consolidates a bounded ONE product-history milestone around Scripture-first cross-reference reading. It does **not** claim ONE as globally complete and does not change the active P01 subtitle critical path.

## Primary evidence

### 1. Scripture-first acceptance milestone

Commit `9469563d6eb2d6365508080c435f3ad995216256` — `chore(dore): persist v5 Scripture-first acceptance evidence`.

The persisted work-node report changed from v4 `NOT_READY / FAIL` with failure `one_visible_crossref_intelligence` to v5 `AVAILABLE / PASS`, added capabilities `one_scripture_first_crossref_ui`, `crossref_click_to_explore`, and `crossref_readable_desktop_layout`, and retained governance that the million-edge graph remain traceable while Scripture text appears before technical metadata.

Classification: `VERIFIED_COMPLETE_SUBMILESTONE / ACCEPTED_PRODUCT_DIRECTION` for the bounded Scripture-first/click-to-explore/readable-layout acceptance packet.

Boundary: the same evidence explicitly says this is **not** completion of permanent issue `#281`; therefore it must not be inflated into overall ONE completion.

### 2. Subsequent layout maintenance

Commit `6b263c93b2c0fefe3ef0aa752f004672fe9e6207` — merge of PR #292, `fix(one): restore full-width cross-reference leaf`.

The patch updates `static/one/index.html` / layout CSS to restore a full-width cross-reference leaf, preserve a multi-column desktop connection grid, collapse responsively, and keep the cross-reference intelligence surface spanning the reading area.

Classification: `COMPLETED_MAINTENANCE` following the accepted v5 direction. This is evidence of post-acceptance product correction, not evidence that the whole product is finished.

## Consolidated interpretation

1. ONE has a real completed bounded milestone: Scripture-first cross-reference reading reached an explicit persisted PASS acceptance state.
2. The accepted product direction is human-readable Scripture before graph/technical metadata, click-to-explore flow, traceable graph provenance, and readable desktop/mobile proportions.
3. Later layout repair should be retained as maintenance evidence and as a regression lesson: accepted behavior can still suffer presentation regressions after the acceptance packet.
4. Overall ONE remains active/partially evidenced. Permanent issue #281 and broader ONE completion are outside this milestone.
5. A future revisit is justified only if later production shows regression in Scripture-first ordering, graph traceability, click-to-explore behavior, or readable responsive layout. A general desire to keep improving ONE does not reopen this completed submilestone.

## Evidence debt / revisit candidate

`UNKNOWN_NEEDS_EVIDENCE`: durable automated regression proof for the accepted Scripture-first ordering and full-width responsive cross-reference presentation is not established by this bounded commit evidence alone. This is a revisit candidate, not a blocker and not grounds to invalidate the accepted milestone.

## Disposition

- Retain bounded acceptance milestone as completed.
- Retain later layout repair as completed maintenance.
- Do not mark ONE globally `VERIFIED_COMPLETE` from this evidence.
- Do not supersede the Scripture-first direction unless later canonical product evidence explicitly replaces it.
- Do not modify P01 subtitle/runtime/deployment state.