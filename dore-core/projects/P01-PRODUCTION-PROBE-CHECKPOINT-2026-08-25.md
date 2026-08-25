# P01 Production Probe Checkpoint — 2026-08-25

Project: `P01-PREFLIGHT-SUBTITLE`
State: `RUNNABLE`
Terminal state: none

## Cycle completed

Added a deploy-targeted verification harness for the existing rights-aware reader-result endpoint.

Evidence:
- `tests/dore-p01-production-probe.mjs` — verifies deployed `dore.video-subtitle-result.v1` schema, real job identity, reader state, rights contract, downloadable VTT behavior when authorized, and mandatory HTTP 403 denial when derivative download is not authorized.
- `.github/workflows/dore-p01-production-probe.yml` — bounded manual production probe using an explicit deployed origin and real subtitle job id.

Commits:
- `f0e4f142e6bd2ae5b67da5e153899a0b89f9af45`
- `68550973cc1593199dec976124846a803dc81d86`

## What this proves

The repository now contains an executable production-verification gate rather than relying on commit existence or unit-contract evidence alone. The probe enforces the rights boundary at the deployed reader surface and will fail if a rights-restricted result leaks a derivative subtitle file.

## What remains unverified

This checkpoint does **not** claim production verification. A real deployed Pages origin and a real D1 `dore_video_subtitle_jobs` id must be supplied by an available deployment/runtime path and the probe must pass against production. After that, the reader Search/result/download path and downstream Stories/Library/ONE paths still require production E2E verification as applicable.

## Next executable action

Discover or obtain the deployed Pages origin and a real current P01 job id from available repository/deployment evidence; run the production probe; persist run URL/log evidence; then continue the Search → result/download → Stories/Library/ONE reader flow.

No human product/editorial decision is currently identified. Missing production target evidence is an execution/deployment discovery task unless repository/account access proves unavailable.
