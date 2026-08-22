# Doré Core Architecture v0.1

Status: **FIRST ARCHITECTURE SYNTHESIS — PRE-IMPLEMENTATION**  
Date: **2026-08-22**

This document is the first synthesis of the Doré master memo and the dated 2026-08-22 working-conversation records. It is not a transcript and does not replace those records. Its purpose is to convert the accumulated discussion into a coherent architecture that can guide the first implementation of `dore-core`.

Later dated conversations may revise this document. Any revision must preserve provenance and state clearly what it supersedes.

---

## 1. Product identity

Doré is not a single model, prompt, app, chatbot, database, image generator or automation agent.

> **Doré Core is Westside Watch's persistent Scripture-and-church intelligence and learning layer: a shared, provenance-aware system that accompanies appropriate ministry and brand workflows, learns from reviewed real work, preserves durable knowledge independently of any single AI model, and returns that accumulated knowledge to ONE, Westside Stories, Liming Library, the main site, Journal and future ministry products through bounded capabilities and adapters.**

Doré begins with two inherited foundations before first deployment:

1. **deep Scripture / Christian-history / theological research competence**;
2. **deep initial familiarity with Westside Watch itself** — vision, ministry purpose, design language, editorial language, theological emphases, product history, existing work, approved terminology and important decisions.

Doré therefore does not enter Westside Watch as an intelligent stranger.

---

## 2. Doré Constitution — candidate permanent principles

The following principles should be treated as the initial constitutional layer. They are intentionally more stable than product features or provider choices.

1. **Model ≠ Doré.** Models are replaceable reasoning providers.
2. **Scripture fact ≠ interpretation.** Text, history, tradition, scholarly hypothesis and brand viewpoint remain distinguishable.
3. **Observation ≠ memory.** Doré may observe work without permanently storing it as knowledge.
4. **Memory ≠ truth.** Remembering that something was said does not make it authoritative.
5. **Working history ≠ current decision.** Superseded ideas remain traceable without remaining active.
6. **Presence ≠ intervention.** Doré may be contextually present and remain silent.
7. **Knowledge ≠ authority.** Knowing more does not grant Doré pastoral, spiritual or operational authority.
8. **Tool access ≠ permission.** A connected capability may only be used within explicit scopes.
9. **Suggestion ≠ action.** Preparing or recommending an action is different from executing it.
10. **Action ≠ success.** Every external action must be verified before Doré records it as completed.
11. **Product knowledge ≠ canonical knowledge.** Brand preferences and church terminology never become Scripture facts.
12. **Uncertainty must remain visible.** Doré must not harden a hypothesis into fact merely for fluency or confidence.
13. **Human responsibility remains.** High-impact decisions, theological conclusions, sensitive pastoral matters and irreversible actions remain under human authority.
14. **Models may change; Doré must not lose its memory.** Durable knowledge, provenance, rules and history live outside any one model.
15. **Doré observes broadly, assists selectively, records faithfully, promotes cautiously.**

These principles should eventually be machine-readable policy as well as documentation.

---

## 3. Core cognitive loop

Doré's fundamental unit is not a chat response. It is a governed cognitive cycle.

```text
Activity / Input
      ↓
OBSERVER
      ↓
CONTEXT
      ↓
RETRIEVE / RELATE
      ↓
EVIDENCE + KNOWLEDGE + MEMORY
      ↓
JUDGMENT
      ↓
RELEVANCE GATE
      ├── not relevant → remain present / no intervention
      └── relevant
             ↓
        ROLE ROUTER
             ↓
       SURFACE ROUTER
             ↓
        TOOL ROUTER
             ↓
      PERMISSION GATE
             ↓
           ACTION
             ↓
          VERIFY
             ↓
      OBSERVE OUTCOME
             ↓
       MEMORY DECISION
             ↓
 classify / preserve / promote / supersede
```

This loop must remain understandable and testable. Doré 0.1 should not hide its behavior behind a monolithic autonomous-agent abstraction.

---

## 4. Core components

### 4.1 Observer

Receives approved work events, content or queries and identifies what is happening without assuming that every event deserves action or memory.

Responsibilities:

- identify project, task, date/session and workstream;
- detect potentially meaningful entities/events/decisions;
- preserve raw provenance where appropriate;
- avoid converting observation directly into durable truth.

### 4.2 Context Engine

Context is a first-class object, not an informal prompt appendix.

A context package may include:

- brand / church;
- product;
- current phase and task;
- Scripture/book/chapter/passage;
- speaker/author where authorized;
- relevant approved decisions;
- recent working decisions;
- open questions;
- relevant knowledge sources;
- permissions and surface constraints;
- explicit exclusions / things not to assume.

Doré should build bounded task-context packages rather than loading all historical memory into every model call.

### 4.3 Retrieval / Relationship Engine

Finds relevant knowledge and relationships across Scripture, history, church, brand and operational memory.

It should prefer deterministic lookup, structured relationships and retrieval before expensive generative reasoning where possible.

### 4.4 Evidence / Epistemic Engine

Every important claim should be classifiable by authority/source type.

Initial distinctions should include at least:

- canonical / textual fact;
- historical/source-supported claim;
- scholarly interpretation;
- theological/confessional tradition;
- editorial hypothesis;
- Westside Watch approved viewpoint or convention;
- working-conversation proposal;
- model inference;
- unknown / unresolved.

Confidence must never erase category differences.

### 4.5 Judgment Engine

Determines:

- whether Doré should intervene;
- which faculty is appropriate;
- whether evidence is sufficient;
- whether human review is required;
- whether a correction/action is safe;
- whether new information confirms, conflicts with or supersedes existing knowledge.

### 4.6 Role Router

Roles are faculties of one Doré, not independent personalities or a required multi-agent swarm.

Early/near-term faculties:

- Scholar / biblical-historical research;
- Librarian;
- Steward / work-context companion;
- Scribe;
- Archivist;
- Editor;
- Proofreader;
- Researcher;
- Connector;
- Curator;
- Teacher where appropriate;
- Doré / Visual Director.

A strongly adversarial **Challenger / Sentinel corrective mode is explicitly deferred** until Doré has learned, accompanied, become useful and become trustworthy.

Sequence:

`learn -> accompany -> understand -> become useful -> become trustworthy -> then earn the right to challenge`

### 4.7 Surface Router

Doré is one intelligence with many possible surfaces. It should appear where the activity already happens instead of forcing every task into a dedicated Doré app.

Candidate surfaces:

- invisible/background service;
- ONE;
- Westside Stories;
- Liming Library;
- main site / Journal;
- desktop worker console;
- mobile web;
- sanctuary/projector live-caption surface;
- QR/context-specific page;
- notification/email/calendar surface where authorized;
- future voice interface.

Surface selection is independent from role selection.

### 4.8 Tool Router / Capability Gateway

Doré is the managed capability gateway for Westside Watch.

Products should prefer stable Doré capability contracts instead of independently rebuilding tool orchestration when Doré already owns the capability.

```text
Westside product
      ↓
Doré capability contract
      ↓
Context + Role + Tool Router + Permission
      ↓
MCP / API / local adapter
      ↓
external or local capability
```

Potential tools/providers include:

- Bible resources and study tools;
- maps/geography;
- Liming Library;
- search/research;
- ASR/translation/TTS;
- GitHub;
- Cloudflare;
- Google Calendar / Drive / Docs / Sheets;
- approved mail systems;
- Zoom / meeting systems;
- YouTube/media/storage/CDN;
- future approved services.

MCP or another protocol is an interface layer, not Doré's intelligence. Doré owns context, routing, permission, verification and provenance.

### 4.9 Permission Layer

Doré must never hold one unrestricted master key.

Initial action ladder:

`Know -> Suggest -> Prepare -> Act -> Verify -> Remember`

Each tool declares explicit scopes and action classes. Reading, proposing, creating, modifying and deleting are distinct permissions. Higher-impact actions may require human approval immediately before execution.

### 4.10 Verification Layer

After external action, Doré confirms the actual state rather than trusting the attempted call.

Examples:

- calendar event exists with expected details;
- deployment completed;
- file was written at expected location;
- subtitle output preserves timing;
- DNS change matches intended record;
- media publication has expected metadata.

Verification results become provenance-bearing operational records.

---

## 5. Knowledge architecture

Doré Knowledge must be separate from Core behavior.

Initial domains:

```text
knowledge/
├── scripture/
├── biblical-world/
├── christian-history/
├── theology/
├── church/
├── westside-brand/
├── language/
├── visual/
├── library/
├── operational/
└── learned-corrections/
```

The knowledge layer should become a structured relationship graph rather than a flat glossary.

Example relationship cluster:

```text
Genesis 32
  ├── Jacob
  ├── Jabbok / 雅博河
  ├── Penuel
  ├── Esau
  ├── wrestling
  └── blessing
```

A subtitle correction can then use canonical/contextual relationships instead of string similarity alone.

Every durable record should be able to carry:

- stable ID;
- type/domain;
- names/aliases/languages;
- relationships;
- source/provenance;
- authority/evidence class;
- confidence where appropriate;
- status;
- created/updated metadata;
- supersedes / superseded-by links;
- product-local versus shared scope;
- review history.

---

## 6. Memory architecture

Doré requires at least two logically distinct memory systems.

### 6.1 Working Memory / Work History

Preserves the history of thought and work:

- dated conversations;
- drafts;
- experiments;
- rejected ideas;
- revisions;
- decision sequences;
- task/session context.

It must be possible to reconstruct how an idea developed without treating every historical state as current truth.

### 6.2 Durable Knowledge

Contains promoted understanding used across future work.

Initial promotion lifecycle:

`Observed -> Candidate -> Approved -> Canonical`

- **Observed:** encountered and provenance-preserved, not treated as truth.
- **Candidate:** plausible/reusable but awaiting stronger review or confirmation.
- **Approved:** accepted for Westside Watch/product use.
- **Canonical:** reserved for knowledge whose authority genuinely warrants canonical status; it is not merely a stronger brand approval level.

The precise workflow may evolve, but automatic memory must never equal automatic truth promotion.

---

## 7. Foundation / pre-birth corpus

Doré should not enter Companion Mode empty.

### 7.1 Scripture and biblical world

Target: expert/research-grade foundation.

Includes:

- canonical structure and text relationships;
- Chinese/English Scripture references and relevant original-language support;
- people, places, events, genealogies, chronology and cross-references;
- ancient Near Eastern, Second Temple, Jewish, Greco-Roman and early-Christian context;
- biblical geography, archaeology and material culture;
- interpretive history and major traditions with provenance.

### 7.2 Christian history and theology

Includes:

- church history;
- councils, major doctrinal developments and controversies;
- major Christian traditions;
- theological vocabulary;
- Chinese Christian terminology;
- explicit distinction between Scripture, tradition, scholarship and local editorial viewpoint.

### 7.3 Westside Watch identity corpus

Includes existing approved work and its decision history:

- vision and ministry purpose;
- design/visual grammar;
- editorial voice and naming;
- theological emphases as represented in approved work;
- ONE;
- Doré / Visual records;
- main site;
- Journal work;
- Westside Stories;
- Liming Library;
- brand specifications;
- approved church terminology;
- relevant Git history and architecture records.

Doré should be born familiar enough with Westside Watch to offer contextually useful ideas from the beginning.

### 7.4 Operational memory

Includes:

- architecture memos;
- dated working conversations;
- approved and superseded decisions;
- known mistakes/corrections;
- unresolved questions;
- provenance/status metadata.

Foundation ingestion must classify authority rather than indiscriminately indexing everything as fact.

---

## 8. Companion Mode

Companion Mode is the default long-term participation model.

Principle:

> **Feeding Doré should increasingly become a by-product of doing Westside Watch's real work, not a separate recurring clerical task.**

Doré accompanies approved workflows through observation, retrieval, assistance and reviewed learning.

It does not need to speak continuously. A good companion experience means Doré often understands the active work without drawing attention to itself.

The full brand loop is bidirectional:

```text
ONE ↕
Stories ↕
Journal ↕       DORÉ
Main Site ↕
Liming Library ↕
Future Products ↕
```

Each product contributes different experience; reviewed experience becomes reusable shared intelligence.

---

## 9. Product and church-life adapters

### 9.1 ONE

ONE remains the human-facing Scripture reader/study portal.

Doré should provide ONE with shared intelligence and managed capabilities rather than forcing ONE to maintain every external integration itself.

**ONE = human Scripture portal.**  
**Doré = persistent intelligence / memory / capability layer.**

### 9.2 Westside Stories

First bounded capability:

`audio/video -> local ASR -> raw timed segments -> Doré proofreading -> SRT/VTT -> media output`

Hard rule: Doré does not silently modify timestamp ownership.

Returned corrections should eventually support:

- corrected text;
- category;
- confidence;
- evidence/context signal;
- provenance;
- human-review requirement;
- candidate alternatives.

### 9.3 Liming Library / 黎明書局

Strong candidate for first major post-foundation Doré assignment.

Goals:

- inventory;
- classification;
- metadata normalization;
- source/provenance;
- duplicate/edition handling;
- Scripture/topic/person/place linking;
- retrieval/recommendation;
- links to ONE, Stories, Journal and church teaching.

Doré should help transform Liming Library from a collection into a church knowledge hub.

### 9.4 Doré / Visual

Existing mature specialization to be formalized as an adapter/faculty rather than remain isolated production memory.

It contributes Scripture reading, historical-geographic/material-culture research, evidence discipline, visual judgment and continuity memory.

### 9.5 Church frontstage

Early frontstage candidate: live sermon captioning/interpretation.

Example:

`church audio -> ASR -> Doré Bible/church context -> translation/terminology -> projector/mobile display`

Possible forms:

- Cantonese sermon -> Mandarin subtitles;
- Chinese sermon -> Chinese + English bilingual subtitles.

The frontstage principle is access and service, not making Doré the center of church life.

---

## 10. Provider architecture

Doré should support replaceable providers.

Provider categories may include:

- LLM reasoning;
- embeddings/retrieval;
- ASR;
- translation;
- TTS;
- image generation/editing;
- search;
- external tools.

Provider selection belongs behind stable Doré interfaces. A product should not need redesign because an underlying AI vendor/model changes.

Preferred order where possible:

`deterministic rules / structured lookup -> retrieval -> model reasoning`

Large-model reasoning is used where semantic judgment is genuinely needed, not as a substitute for databases, policy or provenance.

---

## 11. Storage architecture

GitHub is the initial development and approved-source-of-truth home for:

- Core code;
- schemas;
- policies;
- architecture;
- approved corpus files;
- adapters;
- tests;
- migrations;
- versioned knowledge seeds;
- decision history.

GitHub is **not** sufficient as the sole runtime store for mature Doré.

Runtime will eventually require separable stores for:

- structured operational data;
- retrieval/indexing/vector search where useful;
- session/working state;
- high-frequency corrections/events;
- credentials/tokens (never committed to Git);
- live subtitle/session data.

The specific database technology should not be fixed prematurely. Doré 0.1 should remain light enough to run locally where practical.

---

## 12. Traceability and governance

Every significant Doré action should eventually be traceable across:

`input/context -> retrieved sources -> judgment -> role -> tool/provider -> permission -> action -> verification -> memory outcome`

Traceability is required for debugging, theological/editorial accountability, operational safety and learning.

Sensitive/private church material must not become default training or shared knowledge merely because Doré can access it. Observation scope and retention policy must be explicit per surface/product.

---

## 13. Explicit non-goals for initial Doré

Doré 0.1 is **not**:

- a self-trained foundation model;
- a giant system prompt;
- a universal chatbot UI;
- a swarm of autonomous specialist agents;
- an autonomous preacher or pastor;
- a blanket surveillance layer over church life;
- an unrestricted administrator of connected tools;
- an autonomous self-modifying brand system;
- a Challenger/Sentinel that constantly corrects people;
- a replacement for ONE, Stories, Journal or other product surfaces.

---

## 14. Doré 0.1 implementation target

The first implementation should prove architecture, not feature quantity.

Minimum success criteria:

1. **Core can start independently of any UI.**
2. **Context is a structured object.**
3. **A small provenance-aware Knowledge Store exists.**
4. **Core can recognize Scripture entities/context from a real input.**
5. **Core can return evidence/status rather than only prose.**
6. **Working memory is distinguishable from durable knowledge.**
7. **At least one product adapter can call a stable Doré contract.**
8. **Westside Stories subtitle proofreading is the first bounded external proof.**
9. **A basic Tool/Capability interface exists even before many tools are connected.**
10. **Permission classes exist before any high-impact external write is enabled.**
11. **Actions/results can be logged with provenance.**
12. **Doré can operate with a replaceable model provider rather than embedding model identity into Core.**

A likely first public/internal callable contract may resemble:

```text
Dore.analyze_context(input, context)
Dore.refine_subtitles(segments, context)
Dore.retrieve(query, context)
Dore.invoke_capability(name, request, context, permission)
```

Exact API syntax is not fixed by v0.1.

---

## 15. Suggested repository skeleton

When implementation begins, a dedicated `dore-core` repository or clearly isolated package should approximately separate concerns as follows:

```text
dore-core/
├── core/
│   ├── observer/
│   ├── context/
│   ├── retrieval/
│   ├── evidence/
│   ├── judgment/
│   ├── roles/
│   ├── surfaces/
│   ├── tools/
│   ├── permissions/
│   ├── verification/
│   └── memory/
├── knowledge/
│   ├── scripture/
│   ├── history/
│   ├── theology/
│   ├── church/
│   ├── westside/
│   ├── language/
│   └── visual/
├── adapters/
│   ├── one/
│   ├── westside-stories/
│   ├── liming-library/
│   ├── visual/
│   └── site/
├── providers/
│   ├── llm/
│   ├── asr/
│   ├── translation/
│   └── search/
├── capabilities/
│   ├── mcp/
│   ├── local/
│   └── external/
├── schemas/
├── policies/
├── tests/
├── migrations/
└── docs/
```

This is a conceptual boundary map, not a requirement to create every directory on day one.

---

## 16. First post-foundation work sequence

Current strongest candidates:

1. **Westside Stories subtitle proofreader** — simplest bounded proof of external Doré consumption;
2. **Liming Library reorganization** — first broad Librarian/knowledge-graph exercise;
3. **Doré / Visual formalization** — migrate existing ONE-derived visual intelligence into the shared architecture;
4. **ONE capability gateway integration** — ONE begins delegating selected external capability/tool routing to Doré rather than duplicating orchestration;
5. **live sermon caption/translation prototype** — first meaningful frontstage church surface after backstage reliability is established.

The order may change after implementation review, but the architecture should support all five without redesigning Core.

---

## 17. Architecture checkpoint

The 2026-08-22 architecture-discovery phase is sufficient to begin implementation planning.

The next engineering step should **not** be to build every discussed faculty. It should be to create the smallest coherent `dore-core` skeleton that preserves these boundaries and proves one real cross-product flow end to end.

The implementation should be judged less by how impressive the first AI response looks and more by whether:

- memory survives provider changes;
- evidence remains traceable;
- product-specific rules remain isolated;
- permissions remain explicit;
- knowledge can grow without becoming polluted;
- ONE and other products can call Doré without knowing every underlying tool;
- Doré can learn from real Westside work without requiring a separate manual feeding ritual.

That is the architectural test of Doré v0.1.