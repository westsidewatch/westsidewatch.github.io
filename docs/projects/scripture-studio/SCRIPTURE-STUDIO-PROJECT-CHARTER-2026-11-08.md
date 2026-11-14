每次啟動 Scripture Studio 工程，必須先讀取工程章程、編輯手冊、Design OS、V14 硬性規範、三條鉛字語法、既有多雷探索與版本／驗收記錄，盤點並優先調用工程已具備且實際可用的聖經原文及 USFM 詩行解析、V16–V18 語義鎖定與合法斷句、雙語同帶交錯、真實字型量測、可變版心求解、SVG／HTML 輸出、瀏覽器跨尺寸檢查及 GitHub 工具，沿用已驗證成果並先做來源與權限核查，只有確認缺口後才增補能力，不得另造已存在工具、擅改經文或硬約束、以生成圖片代替工程、未驗收便宣稱達標。

# SCRIPTURE STUDIO — 經文作品編輯與出版系統
## 正式工程立項 / Project Charter · 2026-11-08

**Status:** PROJECT ESTABLISHED — PLANNING / SPECIFICATION, not built or live
**Project ID:** WS-SCRIPTURE-STUDIO
**Repository:** westsidewatch/westsidewatch.github.io
**Planning branch:** draft/p2-0104-olive-entry-20261105 (PR #1385), no permission to merge or change production
**Parent governance:** Westside Design OS, Editorial Manual, Master Site Architecture, existing Doré Design Editorial Studio, existing publishing workflow
**Product goal:** one visual editor and governed publishing pipeline to make distinctive Scripture artworks and distribute Scripture Folio expressions to first-layer realms and the canonical Bethlehem daily publication.

## 1. Decision / 范圍

The Scripture Seal typographic artwork and its downstream section applications are **one formal engineering project**, not disconnected design experiments. The system must become an editor, not a collection of hand-written daily banners.

Three interlocking capabilities:
1. **Scripture Seal / Scripture Folio** — produce the original, square, paired yin/yang typographic bilingual signature and derive a restrained legible daily/section Folio DNA. Art may interweave vertical Chinese and horizontal KJV and may sacrifice immediate reading in its completed expressive seal, but the verified Scripture text remains available and correct.
2. **Scripture Editor** — a visible editing and proofing environment that directly manipulates a real HTML/CSS/SVG-decorated publication surface: passage selection, editorial excerpt/keyword selection, OS typography composition, yin/yang/folio choice, interactive motion/still, responsive preview, version history, citation, approval and destinations.
3. **伯利恆一日 / Bethlehem — A Day daily Scripture calendar** — recurring date-indexed editorial product: date/season and exact selected passage → 1 artwork-level emphasized verse/phrase/selected keywords → complete main Scripture reading (e.g. all 3 selected verses) → faithful reflection → editorial approval → scheduled daily publishing → permanent archive/date navigation.

**Naming:** 伯利恆一日 / Bethlehem is the canonical Journal WATCH column; `A Day` is its daily/live content form. "每日靈糧" is a functional description, never a new thirteenth Journal column. "Scripture Calendar / 聖經日曆" is a product format within Bethlehem, not a peer branch.

## 2. Editorial model and authenticity

A daily entry may choose a three-verse passage yet display only one verse, part of a verse, or several precise words as the **work-level first-eye design**. The **full three verses remain visible** in the Scripture main text with source and translation specified. Reflection/understanding is separate human editorial interpretation, not canonical Scripture.

Calendar relevance may derive from church seasons, lectionary/feast days when applicable, recognized local holidays/observances, church theme and ordinary Bible reading. Date authority is **America/Toronto** including DST; the system should not invent a liturgical attribution when none is approved.

Every biblical excerpt is linked to a verified immutable quotation and exact reference. No AI-generated, rewritten or paraphrased Bible verses masquerading as scripture; translations and copyright/license checked before public use. Editorial/scholarly verification and a responsible human approval step are mandatory, especially for theological reflection.

## 3. Editor UX — direct, visual, not a raw data entry form

**Left / Content:** calendar context, passage selector, verified source, selected verses and excerpt with optional Chinese/KJV alignment; reflection writing/annotations.

**Center / Real publication canvas:** actual Scripture Seal / Folio artwork preview with same source content/render system as public output; drag/adjust approved typography and layout within OS constraints; show actual section host/context rather than a detached unrelated mockup.

**Right / Inspect & Publish:** design DNA settings (approved presets rather than arbitrary colors/fonts), size/layout, language orientation, animation still/key pose and reduced-motion preview, citation, rights/provenance, destination, scheduling, publishing checklist and approval status.

**Top / Preview & mode:** desktop (1648), tablet (768), mobile (390/320), light/branch role, before/after, print still, replay/scrub and reversible animation proof. Protect source content from design edits.

**One source object:** verified passage, excerpt, reflection, layout recipe and publishing record are separate but linked immutable/versioned concerns. A visual edit never silently changes quoted Scripture, and an editorial edit never silently erases artwork versions.

**Integration:** extend the established `dore-design/publishing/EDITORIAL-STUDIO-ARCHITECTURE.md` visible-editor principles, its author/provenance boundaries, and shared publishing capabilities. Avoid an independent full-page editor framework unless real capability gaps are demonstrated. Reuse existing OS typography, token and runtime; no new global CSS owner.

## 4. First-layer destination map

| Destination | Deliverable / editor export | Publishing mode |
|---|---|---|
| Homepage identity / key Scripture | paired Scripture Seal with reversible impression motion and static final frame | separately approved editorial release |
| P2 01–07 realm introductions | each realm's own verified theme verse as a signature impression that marks the chapter transition; one shared DNA, scene-specific short handoff | draft-scoped composition; no repeated identical 7 intros |
| 02 西望 / Journal cover and columns | selected frontispiece/cover seal, and Folio for in-text highlights | issue/edition release |
| 03 Emmaus / ONE entry | source-bound seal/folio while preserving true Bible reader and green cover | versioned section release |
| 04 Olive Mountain | theme Romans 10:17 intro signature; actual speaker adjacent quotations use Folio | protect original 12 speaker posters, V82 and scroll timeline |
| 05 Dawn Library, 06 Cinema, 07 Daylight Café | first-layer theme seals on transitions, Folio for local quotations | section-scoped release |
| **伯利恆一日 / Bethlehem — A Day** | **daily featured artwork from selected verse/phrase/keywords + complete selected Scripture + reflection** | **daily scheduled publishing and archived date permalink** |
| Other selected callouts | Scripture Folio without enforced mixed interweaving | normal editorial publish |

**Scope exclusion:** running Bible text in ONE stays the native reader; non-scripture generic headings do not automatically become Scripture Seal components.

## 5. Daily publishing lifecycle

### Canonical state machine

`PLANNED → SOURCED → DRAFT → IN_REVIEW → APPROVED → SCHEDULED → PUBLISHED`

With `NEEDS_REVISION`, `FAILED`, `CANCELLED`, `SUPERSEDED` paths and explicit rollback. Only **APPROVED** immutable version can be scheduled/published. A content or verse edit after approval invalidates approval and creates a new candidate version.

1. Assign Toronto-local calendar date and the season/observance metadata; record why the passage was selected.
2. Select and verify Bible book/chapter/verse range and translations; store provenance/revision.
3. Highlight one verse, exact phrase or keyword set for artwork without falsifying the quote.
4. Choose Seal-derived daily art layout, preview complete artwork and 320px readable view; store static fallback.
5. Enter the full day's chosen scripture and pastoral reflection; validate context/theology and attribution.
6. Human reviewer approves content + artwork + rights, with a traceable approved source digest.
7. Publish now or `schedule_at` with unambiguous America/Toronto timezone and UTC stored instant.
8. Scheduler identifies due approved records, idempotently publishes one date+edition key, checks deployed URL and version, writes an audit receipt.
9. Date permalink and archive become visible; corrections/retractions are versioned (never silent rewrite).

### Scheduler / operational safety

- Use existing site publishing and GitHub/Cloudflare mechanisms as appropriate; audit before selecting server-side job, Actions cron or other trigger. Do **not** claim scheduler exists without a test.
- Scheduler must not autonomously choose passages or generate unapproved reflections. Only publish previously approved entries.
- Idempotency key such as `bethlehem:{YYYY-MM-DD}:{approved_revision}`; repeated job runs cannot double-publish or overwrite.
- Failure leaves an approved item unpublished with actionable alert; no fabricated content or silently backdated release. Recovery job must be safe to rerun.
- Preview, live release and rollback need deployment provenance and a post-release check; timezone DST boundaries and delayed deploys require tests.
- Dates without approved content: explicit empty/fallback behavior to be decided, **never fabricate a verse**.

## 6. Minimum structured data contract

```json
{
  "entry_id": "bethlehem-YYYY-MM-DD",
  "column_id": "bethlehem",
  "edition_local_date": "YYYY-MM-DD",
  "timezone": "America/Toronto",
  "calendar_context": {"church_season": null, "observance": null, "source": null},
  "passage": {"reference": "", "zh_translation_id": "", "en_translation_id": "KJV", "verified_verses": [], "source_provenance": []},
  "featured_artwork": {"excerpt_text_zh": "", "excerpt_text_en": "", "excerpt_verse_refs": [], "exact_quote": true, "design_recipe_id": "", "layout_polarity": "", "static_fallback_uri": ""},
  "reflection": {"title": "", "body": "", "editor_id": "", "reviewer_id": ""},
  "publication": {"state": "DRAFT", "approved_revision": null, "scheduled_at_utc": null, "published_revision": null, "permalink": null}
}
```

This is a **draft contract**, not a live schema or claim that current apps accept it. Publication identities and exact canonical path are to be reconciled with existing Journal, Search and ONE routing before implementation.

## 7. Milestones with quality gates

**M0 — Project establishment / current:** charter, ownership, dependencies, site application inventory, entry model and publish acceptance. Historical daily devotional project remains `READY` unless updated in its existing master work register by a separate authorized priority process.

**M1 — Master artwork:** two compelling pure static yin/yang mixed-bilingual letterpress seals, same true optical grid, without added frames, labels and fake textures. Independent art approval, monochrome success.

**M2 — Editor vertical slice:** open a sourced passage, select 1 excerpt from a 3-verse selection, edit an artwork recipe, view 1648/768/390/320, preserve exact quote and save draft. The canvas is the output surface.

**M3 — One approved Bethlehem edition:** complete scripture selection, proofed artwork, full passage, reflection, approval, preview permalink and publication proof, plus ONE/Search connections if supported.

**M4 — Scheduled daily release:** approved entries can be scheduled against Toronto local days, publish exactly once, survive retries/DST/failed deploy, archive correctly and issue verifiable release receipt. Do not schedule public daily cadence before completing M3.

**M5 — Shared-section adoption:** each P2 first-layer realm theme mark, Journal cover and special Folio usages adapted independently with approved static artwork and reversible scroll. No destructive changes to existing releases.

**M6 — Production hardening:** permissions, authorship, versioning, accessibility, security, content licensing, audit logs, monitoring/backup and documented rollback tested.

## 8. Acceptance tests

- **Design:** audience recognizes Seal/Folio family without labels, even at black-and-white test; yin/yang states are not unrelated posters; small Folio remains clean and legible.
- **Scripture:** exactly sourced Chinese+KJV, accurate passage/verse and excerpt boundaries; main 3 verses stay 3 verses; no AI-text substitution.
- **Editor:** WYSIWYG matches actual HTML output; edit/save/reopen/export and change history are consistent; cannot change protected verse by dragging a layout control.
- **Calendar:** right Toronto day, meaningful content selection, dates/archives, consecutive days, leap-day/DST tests, missing-day behavior.
- **Publish:** approved-only, scheduled timestamp correct, exactly-once idempotent release, preview/live separation, audit/provenance, post-deploy verification, explicit rollback.
- **P2:** render 1648/768/390/320 and confirm scroll-pose forward/reverse equality, no occlusion of posters/covers, no independent clocks, motion reduction.
- **Governance:** Design OS remains sole token authority; live main, published 01–03 and V82 protected until specific editorial approval.

## 9. Cross-links and responsibility

- Canonical column: `docs/MASTER_SITE_ARCHITECTURE.md` §2 and §3.
- Design OS editorial manual: `docs/design/WESTSIDE-EDITORIAL-MANUAL.md`.
- Scripture identity prototype/brief: `docs/projects/scripture-signature/SEAL-AND-FOLIO-MASTER-ENGINEERING-BRIEF-2026-11-08.md`.
- Seven realm entrance decision: `docs/projects/scripture-signature/SEVEN-REALM-SCRIPTURE-SEAL-TRANSITION-DECISION-2026-11-08.md`.
- Existing visual editor architecture: `dore-design/publishing/EDITORIAL-STUDIO-ARCHITECTURE.md`.
- Previous Daily Devotional plan: `dore-core/projects/DORÉ-DAILY-DEVOTIONAL-ROADMAP-RECONCILIATION-2026-09-01.md` — historical READY/provenance, not evidence of existing daily scheduling.
- Existing publishing program and workflows require technical compatibility assessment before reuse.

## 10. Non-goals and reporting

No claims of completed editor, installed daily job, live Bethlehem calendar, new route or CI acceptance from this planning file alone. This charter records authorized project direction, not a command to change site architecture, launch a separate service, pay for SaaS, auto-write theology, or merge PR #1385. Changes to scope, scheduler host, access control, canonical routes and actual release remain subject to separate engineering decisions.
