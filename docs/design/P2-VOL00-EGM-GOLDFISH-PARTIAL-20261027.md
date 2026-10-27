# P2 · Vol.00 — EGM Goldfish native review (PARTIAL)

**Date:** 2026-10-27  
**Source:** P2 PR #1355 at `131f3769711cb28773ad93f32797b44e309e61c7`  
**Status:** **PARTIAL / NOT APPROVED** — native Codex review interrupted by account model-usage limit. This file is a recovery ledger, **not** the upstream `egm-review` consolidated success report, a visual signoff, or an implementation authorization.

## 1. What was actually executed

- Self-hosted macOS `dore` A2A runner invoked the locally installed, enabled `egm@egm` plugin using the Mac-bundled Codex CLI (0.163.0-alpha.11.1). No reinstallation was required.
- The integrated Design OS companion PR #1358 pins the upstream source at `b3a35956759bf7f024af2ff061b2e0b44b438e4c`. The P2 working branch **intentionally does not** duplicate its submodule. The runner checked the companion Git gitlink before invocation.
- Native Codex trace: `thread.started`, `turn.started`, genuine `collab_tool_call` dispatch/wait results, and Stage 5–7 progress; **at least three native isolated completions** were present according to the originating run's own verified-stage record. This is independent reviewer execution, not a simulated parent-chat persona.
- The model independently reported the installed EGM plugin content matching the pinned upstream package across **77 runtime files**. This is a *native agent statement* within its trace, not an independent certification issued by this ledger.
- A local Codex log had 73 JSON event lines, with `thread.started` and `turn.failed` present. The final error was a model-usage quota interruption, not a P2 script parsing or GitHub authorization failure.
- No original artwork, right-hand cover, Star source, Contents or P2 CSS/JS was edited during the review.

**Direct evidence:**
- [Native A2A execution attempt and account quota interruption](https://github.com/westsidewatch/westsidewatch.github.io/issues/1374)
- [Local Codex event/error diagnostic](https://github.com/westsidewatch/westsidewatch.github.io/issues/1375)
- [Native child-agent status and stage progression recovered without model use](https://github.com/westsidewatch/westsidewatch.github.io/issues/1376)
- [Self-hosted workflow](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/40471891570)

## 2. Stage matrix

| Upstream phase | Evidence | Disposition |
| --- | --- | --- |
| Stage 5 — Initial Zoom Out | Native isolated reviewer completed; parent reported findings | **Completed / visual evidence incomplete** |
| Stage 6 — Comprehension | Native isolated reviewer completed; two specific Major ambiguities reported | **Completed / changes not applied** |
| Stage 7 — Design, Structural & Style | Three reviewer tasks dispatched; some activity recorded, but no complete synchronized review/merge before quota interruption | **PARTIAL — DO NOT COUNT AS PASS** |
| Stage 8 — Intermediate Zoom Out | No confirmed completed result | **NOT RUN** |
| Stage 9 — Implementation Readiness | No reviewed implementation plan supplied | **N/A**, not an acceptance |
| Human editorial visual signoff | No actual final spread comparison available to the native reviewers | **NOT RUN** |

## 3. Verified observations from the native execution transcript

**Stage 5 / art-direction evidence (Blocker before approval):** The approved publisher gallery and an image link could be reached or identified, but the reviewer could not reliably inspect the exact spread JPEG, the editor's rejected screenshot, the live preview or its screenshot artifact. Local Playwright was unavailable in that Codex session. Do not interpret a code/text-only audit as a visual confirmation. The actual editor-supplied rejected screenshot is the relevant art-direction baseline, not a generated image.

**Stage 5 / composition (Major):** The specification needs to reuse shared, tested geometry diagnostics. A zero-intersection assertion is necessary but **not sufficient** to show that Morning Star and the official `西望` glyphs read as one publication identity, share a visual axis or preserve intended whitespace.

**Stage 6 / reduced motion (Major):** Specify the exact meaningful reduced-motion hold state(s). A binary preference check without an accepted static composition leaves viewer behavior ambiguous.

**Stage 6 / clock contract (Major):** Distinguish the left-page single scroll-controlled choreography from the *existing protected Morning Star's own internal animation*. Define whether the Star's original v5.3 internal animation is exempt; do not accidentally rewrite or freeze a protected asset to satisfy an overbroad single-clock requirement.

**Stage 7:** The native transcript states the design, structural and style reviewers were checking their rubrics when the usage limit interrupted the run. Their unconfirmed or uncollected findings must **not** be invented. No Stage 7 PASS is claimed.

## 4. Next gates, without bypass

1. Preserve the original screenshot and make it inspectable from the actual native reviewing environment; likewise obtain an authenticated image of the independent-publication reference. Mark inaccessible evidence honestly. Browser tests must run separately at four viewports and p≈44/68/79/82/93/100.
2. Update the P2 feature specification to state **which static composition reduced motion shows**, and define the Star-internal-animation exception while preserving original asset ownership.
3. Extend visual acceptance from no-overlap rectangles to observable axis, heading/star group, optical legibility, negative space and actual proof images. Keep the right cover immutable.
4. After model quota permits, run remaining native Stage 7 and Stage 8 reviews in genuine fresh subagents and save **real completion/read evidence**. A failed/interrupted run cannot be resumed by declaring its intended steps complete.
5. Obtain editorial acceptance of the *actual* rebuilt publication spread before merging. Core Contract's unrelated baseline failures must remain separately visible.

**Merge / publication:** PR #1355 remains **Draft / DO NOT MERGE**. This ledger does not meet the `docs/design/P2-VOL00-EGM-GOLDFISH-REPORT.md` success gate and is intentionally kept in a separate file.
