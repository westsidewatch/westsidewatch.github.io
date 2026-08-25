# P01 PREFLIGHT — AUTONOMOUS SUBTITLE PRODUCT RUN

Status: READY / EXECUTE TO TERMINAL STATE
Date: 2026-08-24
Owner: Westside Watch
Executor: Doré
Parent: THREE MORNING STAR CURATION — PROJECT 01

## Instruction to Doré

Run this preflight as Doré's own product-engineering cycle. Do not wait for step-by-step human implementation instructions and do not turn the work into a sequence of micro-reports. Read the existing repository, Doré foundational principles, Project 01 memory, current Search/Subtitle/Library/ONE/Westside Stories architecture, and production conventions. Determine the implementation path yourself.

Continue until one of only three terminal states is reached:

1. `VERIFIED_COMPLETE` — the complete reader-facing flow is implemented and production behavior has been verified;
2. `HUMAN_DECISION_BLOCKED` — a genuine product/editorial/rights/credential/safety decision cannot be resolved from existing principles/evidence;
3. `ENVIRONMENT_BLOCKED` — a concrete unavailable permission/runtime/deployment dependency prevents further execution and the exact blocker plus smallest human action is recorded.

Ordinary uncertainty, unfamiliar code, missing technical knowledge, failing tests, layout bugs, or implementation difficulty are **not** reasons to stop. They are learning/debugging work.

## Existing starting point

The repository already contains the first half of the path: video URL recognition at the unified Search entrance, video subtitle routing/job infrastructure, external subtitle proofreading worker, Liming Library resource binding, and biblical-domain gating. Inspect and verify the actual current implementation rather than trusting this summary blindly.

## Required product outcome

A reader can submit a video URL through the shared Doré Search entrance and receive the appropriate end-to-end outcome.

Target lifecycle:

`video URL → canonicalize/deduplicate → biblical-domain decision → existing/new resource discovery → subtitle/accessibility assessment → subtitle job where appropriate → Doré transcription/proofreading/translation/Scripture alignment as applicable → usable subtitle result → collection decision → reader-facing result → Liming Library linkage when applicable → ONE Scripture relationship when applicable → Westside Stories tool pathway → production verification`

## Product rules already decided

- Biblical relevance and library collection value are separate decisions.
- Three Morning Star standards remain Doré's established curated standard; this preflight must not redefine or lower them.
- A biblical sermon/video may receive subtitle service without becoming a Liming Library curated work.
- A useful previously unknown biblical-world resource submitted through Search should become a controlled discovery contribution rather than a disposable query; deduplicate and enrich existing resources where possible.
- Existing official/high-quality Chinese accessibility should be preferred over unnecessary duplicate generation.
- Rights/provenance must govern whether derivative subtitle files can be publicly downloadable.
- When a subtitle result is legitimately downloadable, reduce the distance between result and use: provide a clear reader-facing subtitle download/result surface.
- If the work belongs in Liming Library, the result should expose the relevant Liming Library work/subtitle page rather than forcing the reader to understand transcription internals.
- The completed result experience should also expose Westside Stories as the full tool for readers who regularly need video/subtitle workflows, with an appropriate App information/download pathway.
- If a work does not merit Library collection, do not pollute the Library merely to create a permanent result. Provide the correct non-collection result state.
- If the submitted video is outside the biblical-world scope, decline subtitle generation cleanly.
- ONE should consume Scripture relationships where the resource genuinely maps to books/chapters/passages; do not manufacture weak Scripture links merely to populate ONE.
- Public brand remains Westside Watch / 西望. Doré may appear as editor where appropriate; internal Doré reasoning stays backend by default.

## Frontend responsibility

Doré owns the reader-facing implementation for this preflight, not only backend/API work. Inspect the existing visual system and implement the necessary Search result states, subtitle access/download surfaces, Library linkages, and Westside Stories pathway while preserving Westside Watch visual language and responsive behavior.

Do not wait for humans to specify exact HTML, component names, button placement, CSS values, or repository paths. Research and decide those from the existing product.

Verify desktop and mobile behavior, overflow/alignment, readable hierarchy, loading/error/decline states, long titles/URLs, and accessibility basics. A backend-complete but unusable frontend is not `VERIFIED_COMPLETE`.

## Learning responsibility

When the work requires engineering knowledge Doré does not yet demonstrate, identify the exact gap and learn it in context. Examples may include JavaScript/TypeScript, frontend architecture, APIs, Workers, D1/SQL, R2/assets, Git/GitHub, tests, deployment, responsive layout, app integration, or data modeling. Do not create a detached curriculum.

Record evidence distinguishing:

- already-demonstrated capability;
- capability learned and verified during this run;
- capability merely encountered but not yet demonstrated;
- human correction/decision still required.

## Autonomous-runtime observation

This preflight also tests Doré's execution continuity. Record where the current environment requires an external trigger to continue accepted work. Do not falsely claim background autonomy. If execution cannot persist without another invocation, preserve resumable state so the next invocation can continue from evidence rather than requiring a human re-brief.

Where feasible within the existing architecture, improve project execution state/heartbeat/resume mechanisms without destabilizing production. Treat inability to continue asynchronously as an observed capability/runtime gap, not as evidence that the product engineering itself is complete.

## Verification standard

Do not equate commit existence with completion. Verify, as applicable:

- unit/integration/static checks;
- API behavior and state transitions;
- canonicalization/deduplication;
- accepted / ambiguous / declined biblical-domain cases;
- existing-resource and new-resource cases;
- library-collected and non-collected subtitle cases;
- downloadable and rights-restricted cases;
- Search reader-facing result;
- Liming Library destination when applicable;
- ONE linkage when applicable;
- Westside Stories pathway;
- desktop/mobile responsive behavior;
- deployment/production behavior;
- regression risk to ordinary Scripture Search.

If production cannot be deployed from the available environment, reach `ENVIRONMENT_BLOCKED`, record exactly what has been verified before deployment, and specify only the smallest missing action.

## Final evidence

At terminal state, update this file or a linked run record with:

- terminal state;
- commits/PR/deployment identifiers;
- tests and production checks actually run;
- reader flows verified;
- defects found and repaired;
- capabilities learned/demonstrated;
- unresolved risks/blockers;
- lessons that should feed Doré foundational memory;
- whether this preflight supports or weakens the hypothesis that Doré can independently build and maintain a complete Westside Watch product flow.

Do not report completion before this evidence exists.
