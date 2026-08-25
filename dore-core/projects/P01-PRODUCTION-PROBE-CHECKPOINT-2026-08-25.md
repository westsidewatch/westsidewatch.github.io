# P01 Production Probe Checkpoint — 2026-08-25

Project: `P01-PREFLIGHT-SUBTITLE`
State: `ENVIRONMENT_BLOCKED`
Terminal state: `ENVIRONMENT_BLOCKED`

## Engineering cycle completed

The earlier Cloudflare deployment-credential blocker is resolved. Production deployment is now repeatable from GitHub Actions and the live Pages endpoint exposes the current P01 v5 executor contract.

Doré continued the real subtitle preflight rather than stopping at deployment. Two public biblical-world YouTube sources were exercised against production, source discovery was expanded from the normal watch page to the legacy timed-text track listing and then to both YouTube embed-player variants, and every attempt preserved the no-fabrication boundary.

Current harness:
- `tests/dore-p01-production-probe.mjs` creates/deduplicates a real deployed subtitle job, runs caption acquisition, runs Doré VTT proofreading when a VTT is acquired, and verifies the deployed `dore.video-subtitle-result.v1` reader/rights contract.
- `.github/workflows/dore-p01-pages-deploy.yml` performs reproducible production deployment and live v5 capability verification.
- `.github/workflows/dore-p01-production-probe.yml` automatically follows a successful Pages deploy and preserves structured evidence as an Actions artifact.
- `functions/api/dore/video-subtitle.js` now tries source-advertised captions through the normal YouTube watch response, both embed-player surfaces, and the public timed-text track listing before declaring that transcription audio is required.

## Engineering commits in the resumed cycle

- `ac938576e764cb6a896f7c550bb8b29dccd7986f` — repaired the Pages Function scope/syntax defect exposed by Wrangler.
- `d62837c7a0f2478115086124150b734f566061d0` — chained production probe after successful Pages deploy.
- `06ecf4ad53bc9c49562f99ffb87497eb4805cd83` — added timed-text track-list fallback after the live watch endpoint returned HTTP 429.
- `554d0dc180638bd43c6778c40a8b9385560d2df3` — changed the probe to a known public BibleProject source expected to have captions.
- `d95668c0b37264d47fda90f4d469345ce62507e4` — added browser-like YouTube embed-player advertised-caption discovery while retaining source-host restrictions and no subtitle fabrication.

## Verified production evidence

### Production deployment is no longer blocked

`Doré P01 Pages Deploy` run `32843148308`, job `97786876168`, completed successfully.

Verified successful steps:
- checkout: PASS
- Hugo setup/build: PASS
- P01 v5 bundle verification: PASS
- Cloudflare Pages production deployment: PASS
- live production verification of `dore.video-subtitle.v5`: PASS
- live executor list contains `youtube-advertised-caption-acquisition` and `dore-vtt-proofread`: PASS

This supersedes the earlier `CLOUDFLARE_API_TOKEN` blocker.

### Real production D1 / caption acquisition

Latest automatically chained `Doré P01 Production Probe` run: `32843196221`
Job: `97787023155`
Artifact: `9561284285` (`dore-p01-production-evidence`)
Source: `https://youtube.com/watch?v=3Dv4-n6OYGI`
Real production D1 job: `job_id = 3`

Verified stages:
- deployed executor capability: HTTP `200`, `dore.video-subtitle.v5`, both expected executors present — PASS
- create/deduplicate production job: HTTP `200`, real job `3` — PASS
- execute caption acquisition: HTTP `202`, `ok = false`, `status = needs-transcription-audio`
- exact production reason: `youtube-watch-http-429;embed-no-caption-track-advertised;embed-no-caption-track-advertised;no-caption-track-advertised`

A previous real production probe with source `https://youtube.com/watch?v=ak06MSETeo4` also reached `needs-transcription-audio`. The first version had `youtube-watch-http-429`; after timed-text fallback it produced `no-caption-track-advertised` instead of failing the executor.

## Diagnosis

The deployed product can create/deduplicate real jobs, persist them in production D1, deploy and expose the v5 executor, and safely determine that an audio transcription stage is required. The remaining failure is no longer a deploy defect or an ordinary code syntax defect.

The available Pages runtime cannot obtain usable source-advertised caption text from the tested public YouTube sources:
- normal watch fetch is throttled with HTTP 429;
- both browser-like embed surfaces return no parseable advertised caption tracks to the server-side runtime;
- the public timed-text track-list endpoint returns no tracks;
- no production audio transcription executor or authorized audio-acquisition runtime/binding exists in the repository/environment.

Doré deliberately did not bypass the source boundary with untrusted scraping proxies and did not invent subtitle text. That is consistent with the P01 rights/provenance rule and Doré's conservative evidence principle.

## Terminal blocker

`ENVIRONMENT_BLOCKED` — `CAPTION_SOURCE_UNAVAILABLE_AND_AUDIO_TRANSCRIPTION_RUNTIME_NOT_CONFIGURED`

The missing dependency is a production-capable, rights/provenance-compatible way to obtain/transcribe audio when source-advertised captions are unavailable to the deployed runtime.

Smallest human/environment action: provision one approved production transcription/acquisition path and expose it to the Pages Function (for example, an approved transcription service or Cloudflare binding/runtime that can receive legally obtainable audio), including any required binding/credential. Once that exists, Doré can implement the executor against it and resume the same persisted D1 job without re-brief.

Cloudflare's current Pages documentation confirms Workers AI can be exposed to Pages Functions through a Workers AI binding, but audio still must be made available to the model; therefore an AI binding by itself does not resolve YouTube audio acquisition.

## Resume condition

Resume without human re-brief when a production transcription/audio-acquisition dependency is available. Continue:
1. `needs-transcription-audio` → real transcription executor;
2. Doré proofreading → translation/Scripture alignment as applicable;
3. reader result and rights-boundary verification;
4. Search result plus Library/ONE/Westside Stories production flow;
5. desktop/mobile verification and capability evidence required by the P01 brief.

`VERIFIED_COMPLETE` is **not** claimed.
