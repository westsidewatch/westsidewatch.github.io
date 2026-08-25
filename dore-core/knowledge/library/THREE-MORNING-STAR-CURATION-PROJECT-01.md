# THREE MORNING STAR CURATION — PROJECT 01

Status: ACTIVE PROJECT / LEARNING-BY-BUILDING
Date: 2026-08-24
Owner: Westside Watch
Editor: Doré
Product: Liming Library / 黎明書局

## Project intent

This project is both a real Liming Library product build and a Doré learning experiment. Doré participates in research, resource discovery, information architecture, editorial preparation, production, verification, and post-project reflection. The purpose is not to assign Doré a new identity, but to let Doré learn through real work, improve its understanding of its role, and progressively become capable of proposing and executing future projects itself.

## Brand rule

Public-facing authorship and product identity remain centered on **Westside Watch / 西望**.

Doré must not become the public-facing brand or dominate the reader experience. Doré's internal reasoning such as “why Doré selected this teacher/resource” belongs in backend provenance, editorial notes, audit records, and learning memory unless explicitly requested for publication.

Doré may appear publicly as an **editor** where editorial credit is appropriate.

Default public hierarchy:

`西望 / Westside Watch → 黎明書局 → collection / teacher / series / work`

Optional editorial credit:

`Editor: Doré`

not:

`Doré recommends / Doré Library / Doré says ...`

## Existing Three Morning Star rule

`名師系列 = 三晨星`.

The Three Morning Star layer is a curated quality tier, not a claim of infallibility or blanket doctrinal endorsement. Seed teachers supplied by the editor are calibration examples; Doré must expand discovery across the biblical world until the library coverage/saturation standard is met.

## Information architecture under discussion

The working shared-resource graph is:

`domain → teacher → series → work/episode → Scripture relationship`

Liming Library presents primarily from the teacher/collection direction.
ONE presents the same underlying resources primarily from Scripture/book/chapter direction.
The resource should be stored once and indexed many ways rather than duplicated into separate product datasets.

Doré's selection rationale remains backend metadata. Public presentation should foreground the work, teacher, Scripture, provenance, language/access status, and Westside Watch editorial curation.

## Project dialogue memory — 2026-08-24

Decisions and principles established during project discussion:

1. Doré learns through experiments, projects, failures, corrections, and real product work. Projects should help Doré understand itself rather than repeatedly assigning it new identities or names.
2. Doré should increasingly participate in building itself: diagnose missing knowledge, seek training/resources, propose structures, execute bounded work, evaluate results, and update its own evidence-based understanding of capability and role.
3. Liming Library is a structured bridge to high-quality external biblical resources, not a warehouse that copies the internet. Externally hosted videos and other reliable resources normally remain at their source; the library stores metadata, provenance, relationships, access/language status, and indexes.
4. External resources are learning material for Doré as well as reader resources. Doré's study of teacher corpora can improve later work such as subtitle proofreading, Scripture recognition, translation, search, and ONE resource alignment.
5. Teacher corpora may include video, existing subtitles, transcripts, PDFs, books/articles, notes, and other legitimate sources. Multiple representations of the same work should be related, not mistaken for independent knowledge claims.
6. Doré must actively discover better and more complete resources beyond editor-provided seeds, trace resources back to official/authorized/high-quality sources, and preserve provenance.
7. Subtitle/accessibility work and Liming Library form one product loop: discover high-quality resource → determine Chinese accessibility → use official Chinese where available → where appropriate and rights-compatible, create/proofread/translate an accessibility layer → connect it back to the same library resource and Scripture graph.
8. Public brand concentration remains 西望 / Westside Watch. Doré is infrastructure, learner, researcher, librarian, worker, and may be credited as editor; it should not displace the brand in public product presentation.
9. Internal Doré reasoning belongs in backend/audit/learning records by default. Public pages should not contain a recurring “Doré why selected” module.
10. This project itself is a prototype for future Doré autonomous project formation.
11. Subtitle output should have a low-friction reader-facing landing point in Liming Library where rights permit: subtitle files are accessibility/derivative assets attached to the original video resource, not isolated Doré artifacts. Public states should distinguish official subtitles, editor-verified/calibrated subtitles, and preliminary subtitles without turning Doré into the public brand.
12. A video URL entered through search does **not** automatically create a subtitle job. Doré must first perform a biblical-domain relevance gate. Subtitle work is a Westside Watch/Liming Library biblical-resource capability, not a general-purpose internet transcription service.
13. A user-submitted biblical resource is also a discovery contribution to Liming Library. Search users should be able to enlarge the library simply by bringing legitimate biblical-world resources to the search box. The system should not treat a useful submitted URL as a disposable one-off query.

## Biblical-domain gate for subtitle work

Before transcription, proofreading, translation, expensive media processing, or publication, Doré must classify the submitted video/resource.

Default decision states:

- `ACCEPT_BIBLICAL` — substantially concerned with Scripture, biblical books/passages, biblical theology, exegesis, biblical languages/text, biblical history/geography/archaeology, church history/theology that materially supports biblical study, Christian spiritual formation/sermons/teaching with substantive biblical content, or another established Liming Library biblical collection domain.
- `REVIEW_AMBIGUOUS` — metadata or available evidence is insufficient, mixed, or only weakly related. Doré may inspect lightweight metadata/transcript samples as needed, but should not silently proceed to full subtitle production.
- `DECLINE_OUT_OF_SCOPE` — clearly unrelated to the Bible/Christian biblical-learning scope. Do not transcribe, translate, generate subtitle files, enqueue publication, or add it to Liming Library merely because a URL was submitted.

Classification should use available evidence in a cost-conscious order: URL/platform metadata → title/description/channel/series context → existing captions/transcript sample where available → limited content inspection if still ambiguous. Full transcription should not be the mechanism used merely to discover that an obviously unrelated video was out of scope.

The gate is semantic rather than keyword-only. A resource does not qualify merely because its title contains “Bible”, “Jesus”, “church”, or a verse token, and a legitimate biblical resource should not be rejected merely because its title is indirect. Doré should preserve the classification, confidence, evidence, and reason in backend provenance so errors can become learning examples.

Reader-facing decline should be brief and brand-appropriate, e.g. that the submitted video is outside the biblical-resource scope and therefore no subtitle was produced. Internal Doré reasoning remains backend by default.

False-positive and false-negative decisions should be retained as training/evaluation cases so Doré improves this gate over time.

## Search-to-library contribution loop

For a URL submitted through any Westside Watch search surface (main site, ONE, Join, Liming Library, or another surface using the shared Doré search runtime), the desired lifecycle is:

`user submits URL → normalize/canonicalize URL → biblical-domain gate → check Library Registry for canonical URL/content identity → if existing, return existing library resource/accessibility assets → if new and ACCEPT_BIBLICAL, create a provenance-preserving candidate/resource record → discover title/creator/series/source/language/Scripture relations/official or authorized alternatives → assess rights and Chinese accessibility → attach to appropriate teacher/series/domain/Scripture graph → where appropriate and rights-compatible, create subtitle/accessibility job → proofread/translate/Scripture-align → attach resulting subtitle asset to the same resource_id → expose through Liming Library and relevant ONE Scripture indexes → retain discovery provenance and quality feedback.`

The submitting user is therefore a **discovery contributor**, not automatically an editor or authority. Submission does not itself confer Three Morning Star status, publication approval, doctrinal endorsement, or permission to redistribute derivative files.

### Deduplication and enrichment

A submitted URL must first be checked against existing canonical resources and known mirrors/variants. If the work already exists, Doré should enrich the existing record rather than create duplicates. A new URL may reveal a better official source, missing language version, transcript, PDF, episode, series relationship, or Scripture relation; these should improve the existing graph.

### Collection status is separate from biblical relevance

`ACCEPT_BIBLICAL` means the resource is in scope for evaluation and possible ingestion. It does **not** mean the resource is automatically Three Morning Star. Doré must separately evaluate collection tier, source quality, provenance, rights, usefulness, and relationship to established collections.

This distinction allows search users to help discover the wider biblical world while preserving the curated meaning of the Three Morning Star layer.

### Subtitle generation is conditional, not blind

For a newly discovered biblical video, Doré should inspect existing accessibility before generating anything:

`official Chinese available → bridge/index official Chinese first`

`good existing Chinese subtitles available and rights-compatible → index/preserve provenance; do not duplicate merely to generate another file`

`Chinese missing or materially inadequate + resource valuable + rights allow derivative/distribution → enqueue Doré subtitle/translation workflow`

`rights unclear/restrictive → preserve discovery and metadata; do not expose a downloadable derivative until permitted`

Thus user discovery can create useful work for Doré without turning the search box into an uncontrolled transcription queue.

### Contribution provenance

Backend records should preserve at minimum: discovery source (`user_search_submission`), first-seen time, submitted canonical URL, subsequent official-source resolution, Doré classification/evidence/confidence, duplicate resolution, collection decision, rights/accessibility decision, and resulting resource/subtitle identifiers. Public identity/privacy of the submitting search user is not required for the library resource.

### Product effect

This loop intentionally converts aggregate search activity into library growth:

`more useful searches → more discovered biblical resources → richer Liming Library → richer Doré learning corpus → better subtitle/search/Scripture alignment → better ONE and Library results → more useful searches`.

Search is therefore both retrieval and a controlled discovery sensor for the library.

## Autonomous-project learning target

Doré should learn a reusable project cycle from this work:

`observe need → define project → state reader/product outcome → inspect existing system → identify knowledge gaps → research/learn → propose information architecture → prepare resources → build → verify → publish under brand rules → observe use/failures → reflect → update knowledge/capability → propose next project`

Future autonomy must remain evidence-based. Doré should not claim a project is complete merely because files or plans exist; it must distinguish proposal, implementation, deployment, content population, verification, and reader-facing completion.

## Doré questions for this project

Before the public layout is frozen, Doré should produce its own editorial/information-architecture answer to:

- What does a reader need to understand at the Three Morning Star collection entrance?
- What is the minimum useful teacher-page hierarchy?
- How should a large teacher corpus be divided into series and works without overwhelming the reader?
- Which metadata is editorial/backend-only and which belongs in public presentation?
- How should Chinese availability, official subtitles, Doré-assisted subtitles/translation, PDF/notes, and original-language sources be signaled without making Doré the brand?
- How should the same resource graph serve Liming Library teacher-first browsing and ONE Scripture-first browsing?
- What should remain visually and editorially consistent with Westside Watch rather than being invented as a separate Doré visual system?

Doré should identify any information-architecture, digital-library, editorial-curation, accessibility, or interface knowledge it lacks. Missing knowledge should generate targeted learning before implementation rather than confident invention.

## Success criterion for Project 01 as an autonomy exemplar

The project succeeds beyond the immediate collection when Doré can later demonstrate, from project evidence, that it can:

1. recognize a product/content need;
2. propose a bounded project rather than a new identity/system;
3. assemble and verify its own source corpus;
4. produce an information architecture compatible with the existing Westside Watch ecosystem;
5. prepare/build content with provenance and rights awareness;
6. distinguish backend editorial intelligence from public brand presentation;
7. verify the live result;
8. diagnose what failed or remains weak;
9. retain the lesson;
10. use those lessons to propose and execute a subsequent project with less human scaffolding.

This file is a living project memory. Material decisions from continuing discussion should be appended or integrated here as the project develops.
