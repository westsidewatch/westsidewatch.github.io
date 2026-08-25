# DORÉ MASTER WORK REGISTER

Status: ACTIVE / CANONICAL / CONTINUOUSLY UPDATED
Established: 2026-08-24
Owner: Westside Watch
Executor / steward: Doré

## Why this exists

This is the single operational index for Doré's work. It consolidates durable work that has accumulated across Doré memory, foundational principles, architecture notes, project briefs, product roadmaps, experiments, maintenance work, learning requirements, and new ideas.

The source files remain authoritative for detailed specifications and evidence. This register is the authoritative place for answering: **What are we doing? In what order? Why? How far has it reached? What is blocked? What comes next? Where is the detailed record?**

No durable idea, project, maintenance obligation, learning requirement, or product improvement should remain only in conversation. New work is captured here (or in a linked project file and then indexed here), classified, prioritized against existing work, and given a next milestone. This prevents new ideas from silently replacing older commitments.

## Governing mission

Doré's highest purpose is the Great Commission. Researcher, editor, administrator, librarian, engineer, visual-production center, search system, subtitle worker, and future roles are capabilities/identities serving that mission. Work priority should therefore consider mission value, reader value, dependency order, safety/rights, production health, and learning leverage—not novelty alone.

## Status vocabulary

- `CORE/CONTINUOUS` — never treated as a one-off project.
- `ACTIVE` — currently executable and in progress.
- `ACTIVE_PARALLEL` — intentionally progresses beside the primary critical path.
- `READY` — sufficiently defined; waits for dependency/capacity.
- `DISCOVERY` — research/definition before implementation.
- `BLOCKED` — cannot progress without a named dependency/decision.
- `MAINTENANCE` — live product stewardship.
- `VERIFIED_COMPLETE` — completed with evidence, not merely committed.
- `COMPLETED_REVISIT_CANDIDATE` — original milestone completed, but current Doré judgment says a future revision may be worthwhile.
- `SUPERSEDED` — replaced by a later governing decision/implementation; preserved for provenance.
- `RETIRED` — intentionally no longer active or maintained.
- `UNKNOWN_NEEDS_EVIDENCE` — historical claim/status exists but current evidence is insufficient.
- `PARKED` — intentionally deferred, not forgotten.

## Priority / dependency order

| Order | ID | Workstream | Status | Current verified position | Next milestone / completion test | Depends on |
|---:|---|---|---|---|---|---|
| 0 | CORE | Doré mission, memory, capability accumulation | CORE/CONTINUOUS | Great Commission established as highest purpose; learning-through-real-work, memory discipline, portfolio stewardship, engineering growth and peer-AI learning established | Every project inherits core; generalized lessons flow back into core | none |
| 1 | RUNTIME | Autonomous project continuity / Project Runtime | ACTIVE | Persistent execution state + heartbeat + resume policy exist; P01 has demonstrated at least one no-human-rebrief resumed engineering cycle | Repeated autonomous cycles reliably claim work, execute, checkpoint and reach a terminal state without human re-brief | CORE |
| 1A | MEM-SWEEP-01 | First whole-system Memory Consolidation Sweep + completed-work evaluation | ACTIVE_PARALLEL | Sweep brief established; all Doré memory/project/architecture/product-history families must be reconciled without interrupting P01 | Master Register reconciled; completed-work ledger, revisit queue, superseded/retired index, missing-evidence register and capability-retention map produced; major source families accounted for | CORE, RUNTIME |
| 2 | P01-PREFLIGHT | Video URL → usable subtitle end-to-end preflight | ACTIVE | Search recognition, biblical-domain gate, subtitle job infrastructure, proofreader infrastructure, Library binding, canonicalization/dedup/resumable lookup implemented; not yet end-to-end production verified | Real caption/audio/transcription acquisition executor advances a real accepted job through proofreading/translation as applicable to SRT/VTT and reader-facing result; production test succeeds | RUNTIME |
| 3 | LIBRARY-INGEST | Doré → Liming Library controlled write/ingestion | ACTIVE_PARALLEL | Ingestion contract/registry and subtitle-resource binding foundation exist | Real P01 resources safely deduplicate/enrich/write provenance, series/work relationships and subtitle assets; rights-aware public result verified | P01-PREFLIGHT |
| 4 | 3MS | Three Morning Star master-teacher curation / P01 content | ACTIVE_PARALLEL | Three Morning Star standard, seed/calibration teachers, project memory and initial discovery work exist | Doré expands beyond supplied examples into a defensible biblical-world master-teacher map and begins verified Teacher → Series → Work population | CORE, LIBRARY-INGEST |
| 5 | VIS-LEARN | Doré modern design / editorial / spatial design education | ACTIVE_PARALLEL | Round 01 case-study corpus started (`dore-core/knowledge/VISUAL-CASE-STUDY-ROUND-01.md`) with Emergence Magazine, Rijksmuseum Collection Online, Curationist, The Creative Independent and It's Nice That; structured human + Doré study method established | Complete Round 01 structured observations, desktop/mobile + typography/IA comparison, contradictions, and ≥10 transferable hypotheses; promote no brand rule without prototype evidence | CORE |
| 6 | VIS-GRAMMAR | Westside Watch visual grammar from Doré engraving + Dawn system | DISCOVERY | Project established: Doré engraving is source grammar, not page template; Search full-bleed treatment is a context-specific exception | Doré proposes/tests coherent marks, line/hatching, battlement, portrait, background, frame/divider, map/scripture markers, typography, motion and restraint rules across digital + print | VIS-LEARN |
| 7 | DORE-EXHIBITION | Doré Works Exhibition in Liming Library | READY | Concept established; Search opening should connect to a real curated Doré works exhibition | Complete Westside-language visual/textual curation of Doré works with Scripture/context/provenance/rights; Search cover becomes an exhibition doorway | VIS-GRAMMAR, LIBRARY-INGEST |
| 8 | LIBRARY-V1 | Liming Library first comprehensive visual/product upgrade | READY | Current presentation judged insufficient; desired model is visual order, curated discovery, progressive information density, not text wall | Real Three Morning Star content becomes prototype: entrance → teacher → series → work → watch/read/download; desktop/mobile verified | 3MS, VIS-LEARN, VIS-GRAMMAR |
| 9 | BRAND-V1 | First Westside Watch ecosystem-wide visual upgrade | READY | Shared direction established but should not be prematurely imposed | Extract proven Westside visual grammar from Library prototype, then propagate appropriately to Main / ONE / Search / Join / Westside Stories without making them identical | LIBRARY-V1 |
| 10 | SEARCH | Doré Bible Search / unified search entrance | MAINTENANCE | Public search product exists; fuzzy Scripture search and video URL route are part of ongoing work; search boxes intended across Main/ONE/Join | Ordinary Scripture search remains regression-safe while Search becomes common door for Scripture/resources/video/conversation; responsive production quality maintained | RUNTIME, P01-PREFLIGHT |
| 11 | ONE | ONE Scripture study product | MAINTENANCE | Existing study product with book/chapter, maps/timeline/resources and shared Search integration; historical mobile/navigation/visual defects have required repeated repair | Consume trustworthy Library/resource Scripture relationships; preserve book/chapter study role; later receive proven Brand V1 visual grammar | LIBRARY-INGEST, BRAND-V1 |
| 12 | WSS | Westside Stories App + Doré API | ACTIVE_PARALLEL | Integration line exists; subtitle flow is intended to route regular tool users toward the App; deployed App version/integration still requires verified release-state tracking | Verify current App build truly consumes Doré API and publish/update reader-facing App information/download pathway from subtitle results | P01-PREFLIGHT |
| 13 | MAIN | Westside Watch main site / Journal | MAINTENANCE | Main site remains public brand center; Search entrance added; Journal/editorial language exists | Maintain reliability/content; later adopt proven Brand V1 visual system and stronger visual navigation/editorial presentation | BRAND-V1 |
| 14 | JOIN | Join | MAINTENANCE | Shared Search entrance added; church/community access role remains | Maintain responsive/alignment quality and later adopt proven Brand V1 grammar without losing utility | BRAND-V1 |
| 15 | DEVOTIONAL | Daily devotional / ongoing reader-facing spiritual content | READY | Mission role recognized as one doorway into the same biblical ecosystem | Define sustainable content/source/editorial workflow and connect Scripture/Library/ONE pathways | CORE, LIBRARY-INGEST |
| 16 | BIBLE-AI | External Bible-AI observation and peer dialogue | CORE/CONTINUOUS | Foundational principle established: learn from Bible-focused/general AI peers but verify against Scripture/primary/reliable sources | Periodic useful comparisons/dialogues generate concrete evals, capability ideas or corrections tied to real projects | CORE |
| 17 | CONVERSATION | Doré direct Conversation Runtime | PARKED / READINESS-WATCH | Purpose and readiness principle established; must expose real Doré knowledge/provenance/tools rather than a generic branded chatbot | Readiness threshold: Doré repeatedly discovers, plans, learns, executes, verifies and maintains projects with low scaffolding; then build direct human↔Doré conversation surface | RUNTIME + demonstrated autonomy |
| 18 | STEWARDSHIP | Existing-product maintenance / regression / production health | CORE/CONTINUOUS | Explicitly part of Doré's role; new capabilities should trigger reevaluation of old products | Continuous observe → detect → repair/enrich/upgrade → verify loop across all live Westside products | CORE |

## Completed work is part of the live plan

The Master Register must increasingly show not only active/future work but also major completed work and Doré's current evaluation of it.

Historical completion and current quality are separate judgments. A milestone can remain truthfully `VERIFIED_COMPLETE` for its original objective while also being placed on a `COMPLETED_REVISIT_CANDIDATE` watchlist because Doré has grown, standards have improved, or the ecosystem has changed.

For substantial completed work, Doré should preserve:

- original objective;
- completion evidence;
- current quality judgment;
- durable capability/lesson gained;
- weaknesses or technical/editorial/visual debt now visible;
- revisit trigger;
- current disposition: keep, maintain, enrich, refactor, redesign, migrate, supersede, retire, or revisit later.

The detailed process is governed by `dore-core/projects/DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`.

## Product architecture relationship

These are not isolated sites. The intended connected environment is:

`Westside Watch / 西望 public brand`

`Search ↔ Scripture ↔ ONE ↔ Liming Library ↔ Journal/Main ↔ subtitles ↔ Westside Stories ↔ devotional ↔ future Doré conversation`

A reader may enter anywhere. Cross-product links should be meaningful and context-sensitive, not mechanically promotional.

## P01 critical path right now

The current primary execution path is:

`Runtime continuity → transcription/caption acquisition executor → real subtitle job → Doré proofread/translate/Scripture alignment as applicable → SRT/VTT/result → rights/collection decision → Library/non-Library reader surface → Westside Stories pathway → ONE relationship when justified → production verification → VERIFIED_COMPLETE`

P01 is **not complete** merely because Runtime resumed once or because job infrastructure exists.

## Visual program right now

Visual work proceeds in parallel but does not jump directly to a whole-site reskin:

`design foundations → large case/reference corpus → Doré engraving source analysis → Westside visual grammar → Three Morning Star / Liming Library real prototype → extract proven system → ecosystem-wide upgrade`

Core visual principles already decided:

- visual order before text overload;
- entrance layers use lower text density / higher visual recognition;
- information density increases as the reader moves deeper;
- cards are for discovery/choice, not every content layer;
- Doré engraving is source grammar, not a full-page wallpaper rule;
- Dawn light / gold / stone / typography / engraving / navigation must become a coherent system;
- desktop and mobile share architecture/brand language but may use different compositions;
- visual identity should remain recognizable even if the logo/product name is hidden;
- Doré must learn when **not** to use engraving elements;
- typography craft (including line breaks, widows/orphans, mixed Chinese/English setting, measure, spacing, captions and metadata) is part of quality, not cleanup.

## Three Morning Star / Library content model

Target hierarchy:

`Three Morning Star → Teacher → Series → Work → video/PDF/transcript/subtitle → Scripture relationships → ONE`

Supplied teachers/resources are calibration examples, not the boundary of the collection. Doré is expected to discover higher-quality and broader biblical-world resources independently while preserving the Three Morning Star standard.

## Intake rule for every new idea

When a new idea appears, Doré must do all of the following before it can silently become active work:

1. Capture the idea in this register or a linked project/idea file.
2. Classify it as `core`, `new project`, `existing-product maintenance`, `learning`, `research`, or `idea/backlog`.
3. State which Great Commission / reader / infrastructure need it serves.
4. Check for duplication with an existing workstream.
5. Identify dependencies and risks (including rights/provenance/security/production).
6. Assign a priority relative to existing work; do not let novelty automatically outrank the current critical path.
7. Define one next milestone and a verifiable completion condition.
8. Link the detailed source/brief/evidence.
9. Update status as evidence changes.

If the idea is valuable but not timely, mark it `PARKED` or `READY`; do not lose it and do not disrupt active work.

## Update rule

This register must be updated when any of these occur:

- a new durable idea/project/obligation is accepted;
- a project changes status or priority;
- a dependency/blocker appears or clears;
- a milestone is verified;
- a project reaches a terminal state;
- a completed project is re-evaluated under newer Doré capability/standards;
- a new capability changes what older products can do;
- a product is retired/replaced;
- a foundational principle materially changes work priority.

Updates should be evidence-based. A commit is implementation evidence, not automatically production verification.

## Query protocol

When the user asks things such as **「多雷現在什麼進度？」、「所有項目做到哪裡？」、「下一步是什麼？」、「這個 idea 排在哪裡？」、「以前完成的工作現在怎麼評價？」**:

1. Read this register first.
2. Read `dore-core/runtime/project-execution-state.json` for the currently executing project.
3. Check recent relevant commits/checkpoints for evidence newer than this register.
4. Read the linked detailed project/memory/completed-work evaluation file where needed.
5. Answer from current evidence, and update this register if the evidence has moved.

This register is a map, not a substitute for source records.

## Consolidation / legacy-memory policy

Do **not** delete older Doré memory, architecture, research, project, benchmark, constitution, or evidence files merely because this register exists. They preserve provenance and detailed decisions. Instead:

- this register indexes and prioritizes them;
- overlapping old roadmaps become historical/detail sources rather than competing current priority lists;
- contradictions should be resolved explicitly and recorded;
- obsolete items should be marked superseded/retired rather than silently erased;
- completed work should retain original completion evidence plus Doré's current evaluation;
- future consolidation may add an archive/index, but deletion requires separate evidence and care.

## Known source families to keep indexed

The Doré repository already contains durable material across at least these families, all of which remain part of the system and should be progressively reconciled/indexed rather than forgotten:

- `dore-core/constitution/` — constitutional/identity boundaries;
- `dore-core/memory/` — durable memory and historical decisions;
- `dore-core/knowledge/` — learned principles, curation, resource knowledge;
- `dore-core/projects/` — active project briefs and project memory;
- `dore-core/runtime/` — live execution state/checkpoints;
- `dore-core/benchmarks/` and `dore-core/tests/` — capability/evaluation evidence;
- `dore-core/readers/` — reader-facing/reader-model material;
- `dore-core/reflex/` — reflex/behavioral mechanisms;
- `dore-core/cloudflare/` and architecture documents — infrastructure;
- GitHub workflows — recurring execution/verification machinery;
- product code/content for Main, ONE, Search, Join, Liming Library and related surfaces.

## Immediate operational instruction

Do not pause the active P01 Runtime in order to perform documentation cleanup. `MEM-SWEEP-01` is a parallel stewardship task. The critical path remains P01 subtitle preflight while design learning, Three Morning Star curation, Library ingestion, memory consolidation, and master-register reconciliation proceed in parallel at appropriate cadence.
