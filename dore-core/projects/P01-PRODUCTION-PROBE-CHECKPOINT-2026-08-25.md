# P01 Production Probe Checkpoint — 2026-08-25

Project: `P01-PREFLIGHT-SUBTITLE`
State: `ENVIRONMENT_BLOCKED`
Terminal state: `ENVIRONMENT_BLOCKED`

## Engineering cycle completed

The production probe was upgraded from a manually parameterized reader-result checker into a self-seeding production E2E probe.

Current harness:
- `tests/dore-p01-production-probe.mjs` can create/deduplicate a real deployed subtitle job, run advertised-caption acquisition, run Doré VTT proofreading, and verify the deployed `dore.video-subtitle-result.v1` reader/rights contract. An existing `job_id` remains optional for targeted replay.
- `.github/workflows/dore-p01-production-probe.yml` runs on relevant `main` pushes as well as manual dispatch, defaults to the deployed Pages origin, seeds a public biblical-world BibleProject source, and uploads structured production evidence as a retained Actions artifact.
- The probe waits for deployed schema `dore.video-subtitle.v5` plus both `youtube-advertised-caption-acquisition` and `dore-vtt-proofread` executors before attempting production mutation.
- `.github/workflows/dore-p01-pages-deploy.yml` now provides an explicit, reproducible production deployment path instead of assuming an external Pages integration will refresh itself.

Engineering commits in this cycle:
- `9529ae6c615d3cdd8151e50f6984fa4a8d7cccfc` — self-seeding production probe
- `0f69de451492e0fae5b455442b4b37e35ac3d837` — autonomous push-triggered production probe workflow
- `cfbd2e3a9472cac83d7ff73b7320e0858bf7fef3` — deployment-capability gate
- `aff696fd68f315d872dde5451cf1e076e95ec407` — explicit Cloudflare Pages deployment workflow

## Verified production evidence

### Real production subtitle job

Workflow run: `32831832417` (`Doré P01 Production Probe`)
Job: `97752039352`
Artifact: `9557040549` (`dore-p01-production-evidence`)

Verified:
- production origin reachable: `https://westsidewatch-github-io.pages.dev`
- production POST returned HTTP `202`
- D1 created real subtitle `job_id = 1`
- initial production state: `awaiting-transcription-executor`
- immediate executor action returned HTTP `400` with `supported_video_url_required`

That run revealed that the live endpoint was older than the repository implementation.

### Deployment-capability verification

Production probe run `32831924317`, attempt 2, job `97753436398` polled the deployed endpoint after the repository-side deployment refresh attempt. The live endpoint remained:
- HTTP `200`
- schema `dore.video-subtitle.v2`
- `executors = null`

The repository implementation is `dore.video-subtitle.v5` and contains the caption-acquisition and VTT-proofread executors. Therefore production is not serving current `main`.

### Explicit deployment attempt

Workflow run: `32833024988` (`Doré P01 Pages Deploy`)
Job: `97755705884`
Conclusion: `failure`

Verified successful steps:
- checkout: PASS
- Hugo 0.165.0 setup: PASS
- `hugo --gc --minify`: PASS
- P01 bundle verification for v5 executor/result/router: PASS

Exact blocking step:
- `Deploy production Pages bundle`: FAIL
- workflow environment shows `CLOUDFLARE_API_TOKEN` empty and `CLOUDFLARE_ACCOUNT_ID` empty
- exact log: `CLOUDFLARE_API_TOKEN is not configured`
- process exit code: `78`

This is an infrastructure credential/deployment-boundary failure, not a code defect and not an editorial/product decision.

## Smallest human action required

Provide a production deployment path for the current `main` branch. The smallest durable action is to configure these GitHub Actions repository secrets with Cloudflare Pages deployment permission:

1. `CLOUDFLARE_API_TOKEN`
2. `CLOUDFLARE_ACCOUNT_ID`

The token must be able to deploy the Cloudflare Pages project serving `https://westsidewatch-github-io.pages.dev` (workflow project name currently configured as `westsidewatch-github-io`).

Equivalent one-off recovery: manually deploy the current `main` commit to that Cloudflare Pages project. The durable secrets are preferred because P01 requires repeatable production verification without future human deployment handoffs.

## Resume condition

After production deployment capability is restored, resume without re-brief:
1. rerun `Doré P01 Pages Deploy` and verify live `dore.video-subtitle.v5` executors;
2. rerun the self-seeding production probe and continue real job execution through caption acquisition → proofread → reader result → rights boundary;
3. continue reader-facing Search/result and Library/ONE/Westside Stories production verification required by the Project 01 brief.

`VERIFIED_COMPLETE` is **not** claimed.
