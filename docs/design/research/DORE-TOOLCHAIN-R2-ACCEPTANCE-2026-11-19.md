# Doré R2 — Acceptance checkpoint 1 (2026-11-19)

## Environment
- Python and Playwright available; Chromium executable present.
- Scrapling and Firecrawl CLI absent.
- Container external DNS failed for github.com: `curl: (6) Could not resolve host`.
- Chromium navigation to `file://` blocked by administrator; workaround used `page.set_content()` with a local synthetic fixture.

## Executed browser smoke test
A **synthetic** HTML editorial grid fixture was rendered in Chromium with Playwright. Four viewport tests were executed:
| viewport | expected grid columns | actual | tiles | horizontal overflow | result |
|---|---:|---:|---:|---|---|
| 1648×928 | 3 | 3 | 3 | false | PASS |
| 768×1024 | 3 | 3 | 3 | false | PASS |
| 390×844 | 1 | 1 | 3 | false | PASS |
| 320×700 | 1 | 1 | 3 | false | PASS |

This proves the local browser harness can render and inspect a fixture; it **does not** validate P2, Firecrawl, Scrapling, remote websites, animation, or artistic quality.

## Gate status
- Browser fixture responsiveness: **PASS (4/4)**.
- Remote 10-source extraction: **BLOCKED** (network and tools unavailable).
- Firecrawl vs Scrapling throughput and memory: **NOT TESTED**.
- License provenance: **NOT TESTED**.
- P2 real-page visual QA: **NOT TESTED**.

## Required next run
Use a permitted network-enabled isolated runner. Install and pin verified Firecrawl Local and Scrapling versions, run the same 10 permitted targets three times each, collect exit codes, median duration, content quality, licensing, and resource usage; inspect screenshots of actual source pages. Do not treat this synthetic smoke test as a production acceptance.
