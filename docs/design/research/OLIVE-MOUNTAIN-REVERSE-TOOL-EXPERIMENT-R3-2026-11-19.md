# P2 Olive Mountain — reverse research experiment R3 (2026-11-19)

## Goal
Reverse-test the Doré acquisition pipeline against the **actual research-source categories used by Olive Mountain**, without changing P2: award references, motion/flip implementations, and historical botanical engraving sources. This is a source-access test, not a claim that Firecrawl or Scrapling executed.

## Live source-access observations
| Source | Existing Olive Mountain relevance | Observed access | Evidence and decision |
|---|---|---|---|
| https://tympanus.net/codrops/ | GSAP / card flip / reversible motion examples | Web fetch returned HTTP 403 | Access-restricted in this channel; no extraction or copying. Try permitted browser viewing later, or use official public repositories/docs |
| https://www.awwwards.com/ | Award-level visual benchmark | Web retrieval succeeded; site exposes Interaction Design, CSS animations, GSAP, Scrolling, illustration categories | Metadata discovery works. Do not infer that a featured site is reusable source code or licensed asset |
| https://www.metmuseum.org/art/collection | Museum collection provenance and public-domain artwork research | Web retrieval succeeded; Open Access Images and research links discoverable | Candidate provenance workflow. Rights must be verified per object; homepage alone grants no reuse rights |

## Reverse questions and outcome
1. Can the acquisition layer locate relevant design categories? **YES**, Awwwards categories are discoverable.
2. Can it distinguish source types? **YES**, award metadata versus museum collection versus implementation articles require different extraction schemas.
3. Can it handle inaccessible pages? **YES as a workflow decision**, Codrops 403 is recorded rather than falsely counted as a scrape success.
4. Can it retrieve editable botanical SVG and verify licenses? **NOT YET TESTED**.
5. Can it reproduce the actual 12-card flip/scroll behavior and compare screenshots? **NOT YET TESTED**.
6. Did Firecrawl or Scrapling run? **NO**; neither is installed in the current execution environment.

## Source-to-design evidence schema
Record `source_url, category, original_author, license_url, license_status, technique, reusable_asset_url, original_dimensions, animation_direction, reduced_motion, desktop_capture, mobile_capture, approved_for_p2`.
The default for `approved_for_p2` is false until manual visual review.

## Practical decision
Use accessible Awwwards metadata for discovery, official technical repositories for implementation, and museum collections for source/rights research. A 403 is a hard stop for that acquisition path, not a reason to bypass site restrictions. The current adapter is staged in `tools/dore-exploration/dore_acquire.py`; a real Firecrawl/Scrapling test remains blocked until those runtimes are available.

No P2 HTML, CSS, JS, SVG, approved cards, animations or deployment settings changed.
