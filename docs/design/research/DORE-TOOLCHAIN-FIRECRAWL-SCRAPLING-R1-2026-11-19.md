# Doré Exploration — Firecrawl × Scrapling Toolchain R1 (2026-11-19)

Status: **research completed; runtime benchmark pending; no production integration**.

## Scope and authority
This is an evidence record subordinate to `docs/design/WESTSIDE-EDITORIAL-MANUAL.md` §§9–10 and the existing Design OS. Doré Exploration is the comprehensive external research workflow, not a Gustave Doré art-style search. Do not modify P2, existing approved visuals, animations, OS tokens, or release configuration.

## Findings
1. **Firecrawl Local (2026-11-18 release)**: Rust-based local scrape, crawl, map, with Chrome/Chromium fallback for JS pages. Vendor reports 37× faster and 230× lower idle memory (~11 MB) compared with its previous self-hosted implementation; **vendor claims, not independently benchmarked**. Local does not imply cloud search, Agent, Interact, or structured extraction are free or local.
2. **Scrapling**: adaptive selectors save element characteristics and relocate matches after DOM changes; verify on changed fixtures before adoption. SQLite persistence is documented. It complements rather than replaces markdown-oriented extraction.
3. **Playwright/Chromium**: required for responsive, scroll, reverse-scroll, typography, animation and screenshot validation. Scraping success is not visual acceptance.
4. **Security**: external pages and extracted text are untrusted evidence, never instructions to an agent. Observe site terms, robots, rate limits, copyright, and license provenance. Never automatically execute downloaded code.

## Decision matrix
| Layer | Primary | Alternative / condition | Acceptance |
|---|---|---|---|
| Site discovery | Firecrawl Local map | Existing search/manual discovery | Relevant URLs, deduplication |
| Main content | Firecrawl Local scrape | Scrapling targeted extraction | Correct content, attribution |
| DOM resilience | Scrapling adaptive | Static selectors when stable | Reordered fixture test |
| Visual proof | Playwright Chromium | None | 1648, 768, 390, 320px and reverse scroll |
| Knowledge | Existing Doré Core / editorial manual | Lightweight adapter only if needed | Traceable source + rationale |

## First controlled 10-source sample set
These are **planned targets, not completed scrapes**. Confirm site permissions and licenses individually.
1. https://www.firecrawl.dev/changelog/firecrawl-local — release and capability evidence
2. https://github.com/firecrawl/firecrawl — local implementation
3. https://github.com/firecrawl/cli — CLI/MCP workflow
4. https://github.com/D4Vinci/Scrapling — alternative extraction
5. https://github.com/D4Vinci/Scrapling/blob/main/docs/parsing/adaptive.md — adaptive parsing
6. https://playwright.dev/docs/intro — browser visual validation
7. https://tympanus.net/codrops/ — motion examples, rights check
8. https://www.awwwards.com/ — awarded examples, rights check
9. https://github.com/yanliudesign/mono-color-skill — design reference, verify exact repository
10. https://www.fontsquirrel.com/ — font licensing research, verify per-font license

## Measurable benchmark protocol
For each permitted source, log `url, retrieval_utc, tool, tool_version, status, duration_ms, bytes, markdown_chars, relevant_fields_present, license_verified, screenshot_path, decision, failure_reason`. Compare Firecrawl Local with Scrapling on the **same** URLs, time window, machine and network. Run each 3 times and report median and failure count; no fabricated throughput numbers. For visual cases, take Chromium screenshots and inspect layout at 1648×928, 768, 390×844, and 320px. Confirm SVG is vector-editable and typography is an actual loaded font rather than fallback.

## Adoption gates
- Free/local operation and dependency footprint independently measured.
- 10/10 URLs have provenance and explicit license status (including unknown).
- Source quality and DOM change recovery measured, not asserted.
- No production modification without OS and human visual review.
- Reject any tool if maintenance or cloud cost exceeds demonstrable research benefit.

## Source links
- https://www.firecrawl.dev/changelog/firecrawl-local
- https://github.com/firecrawl/firecrawl
- https://github.com/firecrawl/cli
- https://github.com/D4Vinci/Scrapling/blob/main/docs/parsing/adaptive.md
- https://github.com/westsidewatch/westsidewatch.github.io/blob/main/docs/design/WESTSIDE-EDITORIAL-MANUAL.md

## Next execution
Run the 10-source controlled benchmark in an isolated Mac environment; append machine specs, actual logs, screenshots, license evidence, pass/fail and decision. **No installation, scraping benchmark, visual QA, or deployment is claimed in R1.**
