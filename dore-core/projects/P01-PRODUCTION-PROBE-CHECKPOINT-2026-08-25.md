# P01 Production Probe Checkpoint — 2026-08-25

Project: `P01-PREFLIGHT-SUBTITLE`
State: `ACTIVE`
Terminal state: none

## Cycle completed

The production probe has been upgraded from a manually parameterized reader-result checker into a self-seeding production E2E probe.

Current harness:
- `tests/dore-p01-production-probe.mjs` can now create/deduplicate a real deployed subtitle job, run advertised-caption acquisition, run Doré VTT proofreading, and verify the deployed `dore.video-subtitle-result.v1` reader/rights contract. An existing `job_id` remains optional for targeted replay.
- `.github/workflows/dore-p01-production-probe.yml` now runs on relevant `main` pushes as well as manual dispatch, defaults to the deployed Pages origin, seeds a public biblical-world BibleProject source, and uploads structured production evidence as a retained Actions artifact.
- The probe now waits for the deployed `dore.video-subtitle.v5` executor capability before attempting mutation, so CI cannot confuse a deployment race with an endpoint defect.

Engineering commits in this cycle:
- `9529ae6c615d3cdd8151e50f6984fa4a8d7cccfc` — self-seeding production probe
- `0f69de451492e0fae5b455442b4b37e35ac3d837` — autonomous push-triggered production workflow
- `cfbd2e3a9472cac83d7ff73b7320e0858bf7fef3` — deployment-capability gate after the first production race was observed

## First real production evidence

Workflow run: `32831832417` (`Doré P01 Production Probe`, run 1)
Job: `97752039352`
Artifact: `9557040549` (`dore-p01-production-evidence`)
Conclusion: `failure`, but it produced the first real production job and a precise deployment-race diagnosis.

Verified evidence from the run:
- production origin was reachable: `https://westsidewatch-github-io.pages.dev`
- a real production POST succeeded with HTTP `202`
- D1 created real subtitle `job_id = 1`
- initial production job state: `awaiting-transcription-executor`
- the immediate executor POST returned HTTP `400` with `supported_video_url_required`

Diagnosis:
- the probe ran before the newer v5 action-based executor code had reached the deployed Pages origin. This is a deployment ordering race, not a need for human re-brief and not yet an environment terminal state.
- the repair is now encoded in the probe itself: it must observe deployed schema `dore.video-subtitle.v5` plus both `youtube-advertised-caption-acquisition` and `dore-vtt-proofread` executors before seeding/resuming the production job.

## What this now proves

P01 no longer requires a human to discover or paste a `job_id` merely to exercise production. Doré can create a real production job and preserve structured evidence autonomously. The first run also demonstrated useful failure learning: production deployment ordering is now an explicit executable gate rather than an implicit assumption.

This checkpoint does **not** claim `VERIFIED_COMPLETE`.

## Next executable action

Let the deployment-capability-gated production run complete. If the v5 executor is observed, continue the same real `job_id` through caption acquisition → proofread → reader-result/rights verification and persist exact production evidence. If that stage exposes a genuine executor defect, diagnose and repair it rather than stopping. After production subtitle execution passes, continue the reader Search/result and downstream Library/ONE/Westside Stories production verification required by the Project 01 brief.

No human product/editorial decision is currently identified.
