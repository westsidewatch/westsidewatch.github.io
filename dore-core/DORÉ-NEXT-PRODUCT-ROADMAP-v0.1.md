# Doré Next Product Roadmap v0.1

Status: ACTIVE / CONTINUATION CHECKPOINT
Date: 2026-08-24

## Why this file exists

This is a cross-conversation continuation checkpoint. If a new ChatGPT conversation starts before the Cloudflare connection is finished, resume from this document together with:

- `dore-core/DORÉ-BRAND-OPERATING-ARCHITECTURE-v0.2.md`
- `dore-core/CLOUDFLARE-R2-ASSET-ARCHITECTURE-v0.1.md`
- `dore-core/knowledge/library/LIMING-LIBRARY-BUILD-PLAN-v0.1.md` (currently evolved to v0.3 content)

Do not reconstruct the roadmap from chat memory when these files are available.

## Current strategic state

Doré is no longer being built as an isolated assistant first and deployed later. Its education, Liming Library construction and real brand work now proceed together.

The active growth loop is:

`Doré learns → Liming Library becomes more ordered → capabilities form → products use them → real use exposes gaps/errors → Doré learns again`

A Doré learning milestone is incomplete when it produces no durable reusable knowledge where such knowledge should exist.

## Workstream A — Doré autonomous learning + Liming Library

This workstream is already active.

Doré continues its Researcher/autonomous-learning education while simultaneously building Liming Library. The library is Doré's first continuous real institutional job and the external evidence of its scholarship.

Learning should progressively leave:
- stable resource identity/coding;
- provenance and authority information;
- Morning Star editorial judgment;
- Spectrum placement;
- Curated Collection relationships;
- Scripture/person/place/event/topic relationships;
- reusable evidence and knowledge for live products.

Doré must complete the Library Science Foundation curriculum before destructive redesign of the existing library coding system.

Long-term test: **多雷學問大不大，先看黎明書局。**

## Workstream B — Next product milestone: Daily Devotional / 每日靈修分享

Daily Devotional is the next full product-production target and the first major end-to-end automation milestone after the Cloudflare/Doré infrastructure work.

It is not merely an AI-written daily article. It is a bounded editorial product operated by Doré across research, writing, visual production, asset management, publishing, product linking and distribution.

### Target production loop

`calendar/church context → topic/Scripture selection → Liming Library research → Doré draft → editorial/theological checks → visual selection/generation → R2 + Asset Registry → Journal publication → ONE/Search integration → social distribution → verification/usage record → feedback into Doré + Liming Library`

### Calendar and church rhythm

Daily Devotional should eventually understand relevant temporal context, including:
- date and weekday;
- Sunday / Lord's Day rhythm;
- major Christian/church calendar occasions where appropriate;
- relevant public holidays when editorially meaningful;
- current Sunday worship / sermon context;
- current Bible-study progress;
- current ONE study context;
- current Journal themes.

Calendar awareness supplies context, not mechanical topic control. Devotional content must not become an automatic repetition of the Sunday sermon or calendar label.

### ONE + Bible Search integration

Daily Devotional must not live only inside Journal.

Desired product relationship:

- **Journal** — full devotional reading and branded presentation.
- **ONE** — relevant chapter/passage pages can surface related/current devotional content and link back to the full piece.
- **Bible Search** — relevant Scripture search results can surface a bounded devotional entry/next step without obscuring the Scripture result.
- **Daily Devotional** — links back into ONE for deeper chapter study and Bible Search for continued Scripture exploration.

Representative user paths:

`Bible Search → Daily Devotional → ONE`

`ONE → Daily Devotional → Bible Search`

This is intended to turn separate products into one Scripture-centered learning ecosystem.

### Social distribution

Daily Devotional should produce platform-appropriate derivatives from one approved source item rather than independently inventing unrelated posts.

Target outputs may include:
- Journal/web canonical item;
- image/card variants;
- short social copy;
- platform-specific formatting;
- publish/prepare queue;
- publication verification;
- usage/performance record where available.

Social publishing must remain behind explicit capability boundaries, credentials and platform permissions. Doré is the editor/operator; platform APIs and policy constraints remain external realities.

### Visual and asset production

Doré is intended to lead and edit the image workflow:

`need identified → search/reuse/generate → provenance/rights check → R2 master → Asset Registry → optimized derivative → product/social use → reuse history`

R2 is the binary source of truth for growing brand media. GitHub retains code, schemas, policy, durable metadata/snapshots and decision history.

## Workstream C — Immediate engineering phase: Cloudflare Connection

This is the current implementation priority because Workstream B depends on it.

The goal is not simply to "use Cloudflare". The goal is to give Doré bounded operational access to the infrastructure already selected for its runtime and brand automation.

### Connection targets

1. **D1 / structured runtime storage**
   - Doré runtime state where appropriate;
   - Asset Registry;
   - Resource Registry / operational resource relationships where appropriate;
   - task/workflow state;
   - publication and verification state;
   - feedback signals.

2. **R2 Standard**
   - original/master editorial images and binary media;
   - shared brand asset library;
   - stable object keys and metadata references.

3. **Workers / Pages Functions**
   - bounded capability gateway between Doré/products and D1/R2;
   - upload/register/retrieve/verify operations;
   - no unrestricted infrastructure access from public clients.

4. **Custom domain + CDN/cache**
   - production asset delivery;
   - `r2.dev` remains development/testing only.

5. **GitHub**
   - remains institutional source of truth for architecture, code, schemas, policies, approved knowledge snapshots and durable decision history;
   - Cloudflare does not replace GitHub.

### First Cloudflare connection acceptance target

Before attempting full Daily Devotional automation, prove a minimal safe round trip:

`Doré/authorized workflow → Worker capability → write/read D1 → upload/read R2 object → create/update registry record → return stable asset/resource reference → verify from a first-party product`

The first acceptance test should use a non-critical test asset and reversible registry data.

## AI/model-cost boundary

Product pages should not need to call ChatGPT directly for every operation. Doré is the intelligence layer and should maximize reuse of governed knowledge, deterministic logic, cached/approved outputs and bounded workflows.

However, Doré must not be equated with "free AI". Cloudflare, D1 and R2 do not themselves provide free general reasoning or image generation. Any fresh model inference/generation requires an actual model/runtime capability and its cost/limits must be governed separately.

Architectural goal:

- products depend on Doré capabilities, not directly on one external chat product;
- Doré's model/provider layer remains replaceable;
- routine operations avoid unnecessary inference;
- approved outputs and Liming Library knowledge are reused rather than regenerated;
- cost is measured rather than assumed to be zero.

## Sequence from this checkpoint

Current intended order:

1. Continue Doré autonomous learning and Liming Library construction in parallel.
2. Begin/continue **Cloudflare Connection** immediately.
3. Establish minimal safe D1 + R2 + registry round trip.
4. Build the smallest Daily Devotional end-to-end vertical slice.
5. Publish canonical Daily Devotional in Journal.
6. Connect Daily Devotional to ONE and Bible Search.
7. Add calendar / Sunday worship / church-rhythm context.
8. Add social-media derivatives and authorized distribution/verification.
9. Feed product-use failures, gaps and editorial corrections back into Doré and Liming Library.
10. Expand automation only after the vertical slice is reliable.

## Product milestone definition

Daily Devotional becomes the first major proof that Doré's faculties can work together in production:

- Researcher
- Librarian
- Journal Editor
- Visual Production / Asset Librarian
- Search/Conversation
- ONE integration
- Calendar/context awareness
- Social/editorial distribution
- Memory/Archivist

Success is not "a devotional was generated." Success is a reliable, reviewable, reusable end-to-end system whose output is connected to the rest of the brand and whose feedback improves Doré.

## Resume instruction for a new conversation

If this work is resumed in a new conversation, first read the three architecture/build-plan files listed at the top and this roadmap. Then determine the latest Cloudflare connection commit/state before proposing new architecture.

**Immediate next task at this checkpoint: implement the first Cloudflare Connection layer and prove the minimal reversible D1/R2/registry round trip.**
