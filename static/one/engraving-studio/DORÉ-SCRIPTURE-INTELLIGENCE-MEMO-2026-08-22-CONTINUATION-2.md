# Doré Scripture Intelligence Memo — 2026-08-22 Continuation 2

Status: **WORKING CONVERSATION RECORD — COGNITIVE ARCHITECTURE / SURFACES / TOOL ORCHESTRATION**

This file continues the 2026-08-22 Doré working conversation after `DORÉ-SCRIPTURE-INTELLIGENCE-MEMO-2026-08-22-CONTINUATION.md`. All 2026-08-22 records must be read together, in chronological order, during final pre-build synthesis.

## Early post-foundation work candidates

The current working picture suggests that Doré's first practical responsibilities after Foundation may include three complementary assignments:

1. **Liming Library / 黎明書局 reorganization** through the Librarian faculty;
2. **Westside Stories subtitle proofreading**, likely the simplest bounded external consumer if the Core architecture is sound;
3. **Doré / Visual Director**, formalizing the visual intelligence already developed through ONE.

Subtitle proofreading appears comparatively simple only if the deeper architecture—knowledge, context, provenance, adapters, permissions and memory—is already correct.

## Live sermon interpretation as an early frontstage expression

A concrete church-life vision is real-time sermon interpretation/captioning:

- Cantonese sermon -> Mandarin Chinese subtitles;
- Chinese sermon -> Chinese + English bilingual subtitles;
- other approved language combinations later.

A plausible pipeline is:

`church audio -> speech recognition -> Doré Scripture/church context -> translation / terminology correction -> display`

Doré's advantage over generic live translation should come from knowing Scripture names, book names, church vocabulary, sermon-series context, speakers and likely passage context. It must still preserve uncertainty and must not silently smooth away theological meaning.

This is a model for how Doré can move from backstage infrastructure to frontstage church usefulness through an ordinary computer/projector/secondary-screen surface.

## One Core, many surfaces

Doré should not force every interaction into one dedicated app. It should appear where the work or church activity already happens.

Potential surfaces:

- sanctuary/projector displays for live captions and bilingual sermon access;
- desktop control surface for workers and production staff;
- website / ONE / Liming Library interfaces;
- mobile web for quick resource lookup, schedules and contextual questions;
- QR entry points attached to church spaces, services, courses or printed material;
- post-sermon transcript/search pages;
- email/calendar notifications where explicitly authorized;
- future voice interaction when accuracy, privacy and usefulness are sufficient.

Core principle:

> **Doré should not require people to adapt their lives to Doré. Doré should appear through the surface already natural to the activity.**

This implies a future **Surface Router** inside or adjacent to Core: given a context and action, decide whether assistance should remain invisible/backstage or surface through desktop, web, mobile, projector, notification, voice or another approved interface.

## Tool orchestration — giving Doré hands

Doré may eventually coordinate external tools and services, turning knowledge into bounded real-world action.

Candidate domains include:

- GitHub for repositories, issues, PRs, deployment/project history;
- Cloudflare for domains, DNS, Pages/Workers, routing, deployment/status;
- Google Calendar for church events, teaching schedules and planning;
- Google Drive / Docs / Sheets for approved teaching, planning and operational records;
- Gmail or approved mail systems for retrieval/drafting and explicitly authorized communication;
- Zoom or meeting platforms for links, scheduling context and approved transcript ingestion;
- YouTube/media platforms for sermon/media metadata and publishing workflows;
- storage/CDN/media services for product and church assets;
- speech/translation/TTS providers as replaceable language engines;
- research/search services with evidence/provenance capture.

Doré must never hold one unrestricted 'master key'. External tools should be exposed through narrow adapters with least privilege and explicit authority levels.

A useful action ladder is:

`Know -> Suggest -> Prepare -> Act -> Verify -> Remember`

Reading a calendar, proposing an event, creating an event and deleting an event are different permissions. Likewise, detecting a DNS issue and changing DNS must be separate authority levels.

This implies a **Tool Router + Permission Layer**: Doré determines what capability is relevant, whether it is allowed, whether human approval is required, executes only within scope, verifies the actual result, and records outcome/provenance.

## Emerging real-life integration architecture

The current direction can be summarized as:

```text
DORÉ CORE
   ↓
BACKSTAGE
knowledge / memory / research / library / proofreading / visual direction
   ↓
FRONTSTAGE
live captions / bilingual sermon access / resource discovery / church-facing surfaces
   ↓
CONNECTED ACTION
github / calendar / cloud / communications / media / infrastructure tools
```

These are not separate Dorés. They are increasing levels of presence and authority for one Core.

The cognitive loop therefore continues to develop toward:

`Observe -> Understand -> Judge relevance -> Choose role -> Choose surface -> Choose tool -> Check permission -> Act -> Verify -> Learn`

This is a 2026-08-22 working architecture direction, not yet a final implementation contract.