# PR #1352 — P2 editorial award-calibre quality review

Status: **IN PROGRESS / NOT VISUALLY APPROVED**  
Date: 2026-10-21  
Authority: [WESTSIDE-EDITORIAL-MANUAL.md](WESTSIDE-EDITORIAL-MANUAL.md) §6A and the single [Westside Design OS](WESTSIDE-DESIGN-OS.md).  
Skills: [new-westside-editorial-web](../../dore-design/knowledge-lab/skills/new-westside-editorial-web/SKILL.md), visual grammar rubric, `ui.visual-hierarchy`, `ui.motion-forensics`, `ui.critique`, `ui.accessibility`, `ui.visual-verification`.

## Thesis

**One river becomes two doors; one editorial volume appears as cover above contents, held between the star/西望 and Romans 13:12.** Award-calibre recognition is a quality *target*, not a quality *claim*.

## Source of evidence

- User-provided 2026-10-21 screenshots: ~61% and ~71% Church split, ~90% closed spread, 100% opened three-column state, and the newer cover+contents state.
- Actual repository proof CSS/JS and official Vol.00 editorial map.
- Browser screenshot of the **newest candidate after this pass: NOT AVAILABLE YET**. The preview can build/deploy without proving optical quality.

## First critique and coherent corrective pass

| Priority | Defect in supplied view / code | Decision | Owner / acceptance |
| --- | --- | --- | --- |
| **block** | Nearly blank scroll intervals break the causal transition | Retain current proof-only compact handoff; require replay, reverse and reduced-motion test | `static/js/p2-living-water.js`; in-browser scroll checkpoint trace |
| **block** | Full-open Contents copy is far too small relative to the page and has no clear scan hierarchy | Increase Chinese titles, English labels, section numbers and interlude reading sizes, improve rhythm without inventing copy | `static/css/p2-magazine-transition-proof-v3.css`; actual 1648×928 and phone screenshots, check clipping/scroll |
| **important** | The right verse completes in the upper part of a tall navy plane, leaving an unexplained lower half | Move the English/Chinese reading group up to meet the star's axis while extending Chinese/folio to the middle of the field | Same scoped stylesheet; compare 90% and 100% poses |
| **important** | Original 西望 SVG remains disproportionately large and heavy after opening | Reduce the final display height, preserving the original vector proportions, and keep star/glyph synchronized | Same CSS/JS; 90%/100% screenshots |
| **important** | Reduced motion only disabled will-change but did not stop scroll-bound transforms | Snap the five proof stages; star iframe already respects OS reduced-motion preference | Proof JS + original morning-star asset; actual reduced-motion user-agent test |
| **important** | Real rendered browser geometry, contrast, keyboard, 200% zoom and responsive frames not independently observed | Remain unapproved rather than assume screenshots from green CI | Design OS geometry tool and visual verification |

## Award lenses and current score

Internal 10-axis rubric is **NOT SCORED** until the updated preview is actually observed at desktop, tablet and phone. Earlier screenshots expose blockers; they do not support an 18/20 promotion. Awwwards score, Webby score and FWA score **are not provided or inferred**.

Pre-release gate: internal review ≥18/20 with no zero, no unresolved block; additionally all browser, usability and scroll checkpoints must pass. These thresholds are **local Westside gates only**, never official award thresholds.

## Review cycles

1. **Pass 1 — source code and editorial critique:** no-op scroll audited, complete Vol.00 contents preserved, typography hierarchy and two-leaf balance adjusted, keyboard focus and reduced-motion behavior improved. JS syntax check and CI still required.
2. **Pass 2 — deployed side-by-side browser screenshots:** pending direct evidence; measure actual bounding boxes and compare 90% / 100% at 1648×928, 768px, 390px and 200% zoom. Identify clipping or nonfunctional scroll before next approval.
3. **Pass 3 — rejection / refinement:** apply only if pass 2 supplies reproducible defects, not speculative CSS overlays; re-run the same screen and use the same rubric.

**Do not merge** merely because PR is conflict-free or Cloudflare preview/Production Build succeeds.
