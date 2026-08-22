# Doré Scripture Intelligence Memo — 2026-08-22 Addendum

Status: **ARCHITECTURE MEMO — FUTURE PRODUCT DIRECTION, NOT CURRENT RUNTIME**

This addendum belongs with `DORÉ-SCRIPTURE-INTELLIGENCE-MEMO.md` and records the 2026-08-22 product discussion. It does not replace the main memo. It makes explicit a direction already latent there: Doré is becoming Westside Watch's next product/project and a shared brand-level Scripture intelligence unit rather than remaining only an illustration subsystem inside ONE.

**Working-conversation status:** this is the first explicitly date-separated Doré product-definition conversation record. It is intentionally preserved as a record of developing thought, not treated as the final build specification. The cross-day workflow and chronological index are maintained in `DORÉ-WORKING-CONVERSATIONS.md`. Future substantial conversations (for example 2026-08-23) should receive separate dated records. Before implementation begins, the master memo and all dated records must be read together and synthesized into the current product definition.

## Product decision — Doré as the next Westside Watch project

Doré should be developed as a distinct Westside Watch product/project while preserving its root in ONE. Its accumulated knowledge must not be trapped inside one consumer. The purpose of separation is reuse and compounding memory, not fragmentation from Scripture or from the brand.

The key product principle is:

> **Products may change and models may change; Westside Watch's accumulated Scripture, church-language and editorial knowledge must persist.**

ONE remains a major canonical and study root for Doré. Westside Stories becomes an important real-world language consumer and feedback source. Future products may join the same bridge without rebuilding their own isolated Bible intelligence.

## Westside Stories — Doré as subtitle proofreader

Westside Stories already has its own local transcription pipeline and could implement additional subtitle correction directly. The architectural decision is deliberately **not** to bury all Bible/church correction logic inside Westside Stories, because doing so would duplicate and isolate knowledge Doré has already accumulated through ONE.

Preferred responsibility split:

`audio/video -> local ASR/Whisper -> raw timed segments -> Doré proofreading -> reviewed text -> SRT/VTT -> optional FFmpeg burn-in`

Westside Stories remains responsible for transcription, timing and media output. Doré acts as the **proofreader**, not the primary ear.

Hard rule: Doré must not silently rewrite subtitle timing. `start`, `end` and stable segment identity remain owned by Westside Stories. Doré receives text plus contextual metadata and returns text corrections, confidence/review information and provenance.

Doré proofreading should concentrate on errors where generic ASR is weak but brand knowledge is strong:

- Bible book names, people, places and events;
- Scripture quotations and chapter/verse references;
- theological and church vocabulary;
- Westside Watch and Living Water Assembly West terminology;
- speaker, ministry and recurring proper names when maintained in an approved church lexicon;
- Traditional Chinese normalization, punctuation and subtitle segmentation where meaning is not altered;
- Mandarin/Cantonese/English mixed speech and recurrent ASR homophones when context supports correction.

The system must distinguish safe lexical normalization from theological or substantive rewriting. Changes that may alter doctrine, quotation meaning, speaker intent or uncertain proper nouns require human review rather than automatic acceptance.

## The feedback loop — each product teaches the shared core

The important gain is bidirectional. Doré does not merely export knowledge to Westside Stories.

`ONE -> Doré -> Westside Stories -> human correction -> Doré -> ONE / main site / Journal / future products`

ONE contributes structured canonical knowledge, Scripture context, people, places, historical research and editorial decisions. Westside Stories contributes real speech: pronunciation variants, homophones, code-switching, church usage and the actual failure patterns of speech recognition. Human acceptance/rejection of Doré suggestions becomes new evidence.

A useful learning record is:

`ASR original -> Doré suggestion -> human final decision -> surrounding context -> source/product -> confidence -> reusable lesson`

This means subtitle proofreading expands the Bible/church lexicon. That expanded lexicon then improves other Westside Watch products. Work performed for one product becomes durable brand infrastructure rather than disposable local fixes.

## Shared architecture — Core, Knowledge, Adapters

Doré should be separated conceptually into three layers.

### 1. Doré Core

Shared reasoning/editorial rules that are not tied to a single UI or product:

- canonical-context reading;
- evidence and uncertainty handling;
- Traditional Chinese editorial standards;
- quotation/reference recognition;
- correction confidence and human-review thresholds;
- provenance and revision memory;
- guardrails against changing meaning merely to make language smoother.

### 2. Doré Knowledge

Durable shared knowledge accumulated across products:

- Bible books, people, places, events and canonical relationships;
- Scripture references and known quotation forms;
- historical-geographic and material-culture memory already developed by Doré / Visual;
- theological and church vocabulary;
- Westside Watch brand terminology;
- approved church names, ministries and proper nouns;
- known ASR confusion pairs and pronunciation variants;
- editorial decisions and accepted/rejected corrections;
- source provenance and confidence/evidence level.

This must become more than a flat `wrong -> right` dictionary. Contextual relationships matter. For example, a proposed correction for a place name should be strengthened when nearby text also identifies the related biblical person, chapter, event or geography. Doré should know why a term belongs in context, not only that two strings look or sound alike.

### 3. Product Adapters

Each product receives only the behavior appropriate to it.

- **Doré / Visual:** Scripture-to-image research, historical world-building, plate judgment and visual continuity.
- **ONE:** Scripture/content review, canonical entities, timeline/place relationships and future shared editorial assistance.
- **Westside Stories:** subtitle proofreading without taking ownership of timestamps or media encoding.
- **Main site / Journal / future products:** metadata normalization, naming consistency, Scripture/entity recognition, editorial checks or other narrowly defined services.

Product-specific rules must remain isolated at the adapter/profile layer so that subtitle habits do not contaminate ONE's reader behavior and visual-generation rules do not leak into ordinary editorial correction.

## 2026-08-22 continuation — what exists now versus what must be built

The conversation clarified that Doré is **not currently an independently executable intelligence product**. It is also not imaginary from zero. Its raw capability already exists in three forms:

1. a practiced Doré / Visual workflow developed through real ONE production;
2. accumulated research, corrections, visual judgment, Scripture/historical reasoning and evidence discipline in repository records;
3. architectural/product ideas that have now been made explicit but are not yet implemented as software services.

Therefore the correct distinction is:

> **The capability material already exists; the capability has not yet been engineered into an independent reusable system.**

The subtitle proofreader, shared cross-product API, central machine-readable Doré Knowledge Store and reusable service calls such as `Dore.refine_subtitles()` remain future implementation rather than present runtime ability.

## First software form — `dore-core`, not an app

The first true Doré software project should not begin as a website, chat UI, visual brand shell or subtitle-only feature. It should begin as an independent, UI-less **Doré Core — Westside Watch Scripture Intelligence Engine**.

Conceptual structure:

```text
DORÉ
├── Core
│   ├── scripture
│   ├── entities
│   ├── context
│   ├── correction
│   ├── evidence
│   └── provenance
├── Knowledge
│   ├── bible
│   ├── history
│   ├── church
│   ├── brand
│   ├── language
│   └── learned-corrections
├── Profiles / Adapters
│   ├── visual
│   ├── subtitles
│   ├── one
│   └── editorial
└── API
```

The separation is fundamental:

- **Core = how Doré reasons and judges.**
- **Knowledge = what Doré knows and remembers.**
- **Profile/Adapter = what Doré is allowed and expected to do for a particular product.**

Example: “do not improve fluency by changing a speaker's meaning” is a Core rule. “Gethsemane / 客西馬尼 and its canonical relationships” belongs to Knowledge. “For subtitles, never change `start`/`end` timing” belongs to the Westside Stories subtitle adapter.

## Doré must not equal one giant prompt

A major architectural guardrail was established: Doré must not be implemented as merely a long system prompt attached to one current AI model.

The intended composition is closer to:

`Knowledge + Rules + Memory + Retrieval + Model provider(s) + Product Profiles`

The model is replaceable infrastructure. Doré's durable identity resides in its accumulated structured knowledge, evidence, editorial memory, rules and interfaces.

This supports the permanent principle:

> **Models may change; Doré must not lose its memory.**

Doré 0.1 should therefore be capable of deterministic knowledge/rule work even before every function depends on an LLM. A model can later act as a reasoning provider where contextual interpretation is required, without becoming the sole location of Doré's knowledge.

## Minimal proof for Doré 0.1

The first implementation should prove a small number of real capabilities rather than attempt every discussed future function at once:

1. **Recognize Scripture context** — identify likely books, chapters, people, places, events and quotations/references from supplied content.
2. **Explain epistemic basis** — return source/evidence/confidence and preserve the existing Doré discipline of distinguishing textual certainty, editorial hypothesis and uncertainty.
3. **Serve one real external consumer** — use a genuine Westside Stories subtitle sample to prove that another product can call Doré and receive a contextual correction without surrendering timestamp ownership.

The third proof is strategically important: it is the point at which Doré stops being only an intelligence workflow living around ONE and becomes a reusable Westside Watch capability.

## 2026-08-22 continuation — persistent learning layer across the whole brand

The conversation then advanced the Core definition further. Because Westside Watch's products are church/ministry products and Scripture/church context is pervasive across them, Doré should not require a separate manual “feeding session” after normal work. The long-term goal is for Doré to become a **persistent learning layer that accompanies Westside Watch's ordinary product work by default**.

This does **not** mean every product must expose a Doré button or that Doré controls every product. It means that appropriate adapters can allow work to flow bidirectionally:

`product work <-> Doré shared intelligence`

Examples:

- ONE production uses Doré while its approved research and editorial decisions can become reusable Doré knowledge.
- Westside Stories uses Doré for contextual proofreading while human-confirmed corrections teach Doré real church speech, pronunciation and ASR failure patterns.
- Journal/editorial work can use Doré for Scripture/entity/editorial consistency while approved language decisions enrich shared memory.
- Main-site work can use Doré for Scripture/church/brand naming and information relationships while approved production content contributes current brand knowledge.
- Future Westside Watch products should be able to join the same shared layer through their own bounded adapters.

The principle is:

> **Feeding Doré should increasingly become a by-product of doing Westside Watch's real work, not a separate recurring clerical task.**

## Learning is not automatic truth — knowledge promotion gates

Persistent participation creates a major risk: if Doré permanently learns every draft, suggestion or temporary idea, its knowledge will become polluted and contradictory.

Therefore Doré should be able to observe broadly while promoting knowledge cautiously. A conceptual lifecycle is:

`Observed -> Candidate -> Approved -> Canonical`

- **Observed:** encountered in a conversation, draft, repository, transcript or product workflow; preserved with provenance but not treated as truth.
- **Candidate:** repeated, contextually supported or explicitly proposed for reuse, but still subject to review.
- **Approved:** human/editorially accepted for Westside Watch use.
- **Canonical:** reserved for knowledge whose authority warrants that status, especially stable Scripture/canonical facts; not merely a stronger synonym for “approved brand preference.”

The exact schema can change during implementation, but the distinction must survive. Doré should remember disagreement, revision and supersession rather than flatten successive ideas into simultaneous truth.

This mirrors the existing Doré evidence discipline: a hypothesis must never silently harden into fact.

## Existing Westside Watch work as Doré's bootstrap corpus

Doré should not begin learning from an empty database. Existing completed and in-progress Westside Watch work is the first major knowledge pool from which Doré can be bootstrapped.

Potential sources include ONE content and research, Doré / Visual records, main-site production content, Journal/editorial materials, Westside Stories material, brand specifications, approved church terminology, dated working conversations and relevant repository history.

However, repository ingestion must be provenance-aware. Existing content is not one homogeneous truth source. Doré must distinguish at minimum:

- current production data;
- superseded/legacy versions;
- approved brand specification;
- research/evidence records;
- architecture memo;
- dated working conversation;
- draft or proposal;
- human-confirmed correction;
- model-generated suggestion not yet approved.

Git history can therefore be useful not merely as content storage but as evidence of how a decision evolved, provided Doré does not treat every historical revision as simultaneously current.

## Brand-wide bidirectional model

The earlier one-way consumer model is superseded by a bidirectional relationship:

```text
                DORÉ
        ┌─────────────────┐
        │ Core            │
        │ Knowledge       │
        │ Memory          │
        │ Provenance      │
        └────────┬────────┘
                 │
          shared intelligence
                 │
      ┌──────────┼──────────┐
      ↕          ↕          ↕
     ONE      Stories    Journal
      ↕          ↕          ↕
      └──────────┼──────────┘
                 ↕
              Main Site
                 ↕
          Future Products
```

All arrows are intentionally bidirectional. Doré serves products and products, through reviewed outcomes, enrich Doré.

Different products teach different dimensions of the same shared intelligence:

- ONE deepens canonical, historical, geographic and study context;
- Westside Stories adds spoken language, pronunciation, code-switching and ASR correction experience;
- Journal adds theological/editorial expression and long-form language judgment;
- the main site adds current church/brand naming, information architecture and public-facing terminology;
- future products add new dimensions through bounded adapters.

Doré therefore should not have a meaningful state called “training complete.” Its architecture should permit it to grow alongside Westside Watch while retaining provenance, review gates and historical memory.

## Refined product definition from today's discussion

The working definition has advanced from simply “Westside Watch Scripture Intelligence Engine” to:

> **Doré Core is Westside Watch's persistent Scripture-and-church intelligence and learning layer: a shared, provenance-aware system that accompanies appropriate brand workflows, learns from reviewed real work, preserves durable knowledge independently of any single AI model, and returns that accumulated knowledge to ONE, Westside Stories, the main site, Journal and future ministry products through bounded product adapters.**

This is a working 2026-08-22 definition, not yet the final pre-build specification. It must remain available for comparison with later dated conversations.

## 2026-08-22 continuation — cognitive loop: observer before recorder

The discussion then moved below the product-feature layer into Doré Core's **cognitive architecture**. The central question is no longer whether Doré is a secretary, Bible database, image maker, visual director, subtitle proofreader or brand archivist. Those are possible faculties/roles. The deeper question is how Doré notices brand activity, understands context, decides whether it is relevant, selects an appropriate role, acts, observes the result and decides what—if anything—should become memory.

A key distinction was established:

> **Observe is not the same as Remember.**

Doré may observe a broad range of appropriate Westside Watch workflows without permanently promoting every sentence, draft, experiment or passing idea into durable knowledge. Observation is the intake layer; memory is a later judgment.

A conceptual cognitive loop is:

```text
Brand activity
    ↓
Observe
    ↓
Understand / contextualize / relate
    ↓
Is Doré relevant here?
    ├── no  → remain present, do not intervene
    └── yes → select an appropriate bounded role
                 ↓
              Assist
                 ↓
           Observe outcome
                 ↓
          Should this be remembered?
                 ↓
        classify / review / promote
```

This refines the earlier persistent-learning principle. **Presence does not imply intervention.** Doré can remain contextually present while acting only when relevance, confidence and product permission justify action.

## Doré's roles are faculties, not its identity

The conversation explicitly tested several possible identities:

- recorder of everything;
- recorder of important matters;
- observer of brand actions;
- secretary for production and AI conversations;
- Bible database;
- image maker;
- brand visual director/master;
- subtitle proofreader.

The working conclusion is that none of these alone should define Doré. They are bounded faculties exposed through roles/adapters. Doré Core instead decides:

- what is happening;
- which project/workstream/context it belongs to;
- what existing knowledge is relevant;
- whether Doré should participate;
- which faculty/role is appropriate;
- what level of certainty applies;
- whether the result deserves memory;
- what memory class/status it should receive;
- whether new work confirms, conflicts with or supersedes earlier understanding.

This implies a deeper Core shape than only `Core + Knowledge + Adapters`. The cognitive center now appears to require at least the concepts of **Observer, Context, Judgment, Memory and Role Routing**, with Evidence/Provenance available throughout.

Conceptually:

```text
                    DORÉ

               ┌── OBSERVER ──┐
               │              │
               ↓              │
             CONTEXT           │
               ↓              │
           REASONING           │
          ↙    ↓    ↘          │
    Knowledge Memory Evidence  │
          ↘    ↓    ↙          │
            JUDGMENT           │
               ↓              │
          ROLE ROUTER          │
        ↙      ↓       ↘       │
     Visual  Steward  Subtitle ...
        \       │       /
               ↓
             ACTION
               ↓
             RESULT
               │
               └────────→ OBSERVER
```

This diagram is exploratory, not yet an implementation contract, but the cognitive responsibilities it exposes must be considered before initial code structure is fixed.

## Working memory and durable knowledge must be distinct

Today's own conversation became the test case. At present the human must explicitly tell the current AI to write an important discussion into the 2026-08-22 Doré working record, identify whether it belongs to the dated record or master memo, and trigger the repository update.

A mature Doré should improve this workflow. If the active context is already known as:

`Westside Watch -> Doré -> Cognitive Architecture -> Working Conversation -> 2026-08-22`

then Doré should be capable of recognizing that a statement such as “Doré must not be one giant prompt” is potentially an `architecture_decision_candidate`, without requiring the human to restate the date, file hierarchy and project context every time.

However, Doré must **not** simply write every utterance into permanent knowledge. Two memory forms are therefore required conceptually:

### Working memory / work history

Preserves development and sequence: ideas proposed, questions raised, alternatives explored, later rejection, revision and supersession. This is where the dated 08-22 / 08-23 conversation records belong.

### Durable knowledge

Represents the current promoted understanding: approved/candidate principles, their provenance, what they supersede, and their current status.

A discarded idea may remain visible in work history while no longer being active durable knowledge. This distinction is necessary if Doré is to learn from the brand without confusing the history of thought with the current truth/state of the product.

## Doré / Steward — conversation and work-context faculty

The discussion identified a likely future faculty tentatively called **Doré / Steward**. This is not Doré Core itself. It is the role through which Doré can assist ongoing human–AI and production workflows.

Potential Steward behavior:

- at the start of a work session, recover the relevant project phase, prior decisions, open questions and authoritative sources;
- during work, observe without constant interruption;
- identify candidate decisions, possible supersessions, conflicts with existing approved knowledge and missing evidence;
- at the end or appropriate checkpoint, organize the work into new ideas, decisions, open questions, superseded ideas, conflicts, verification needs and possible Core/Knowledge changes;
- route those records to the correct dated working record and knowledge-promotion process.

This would reduce the human's current burden of repeatedly instructing an AI which memo to read, which date to use, which prior decision matters and which kind of record a new idea belongs to.

## Doré as context provider to other AI systems

A further consequence is that Doré's value is not only remembering for itself. It can become the layer that gives whichever AI/model is currently doing Westside Watch work the **right bounded context**.

Rather than loading an ever-growing giant prompt or every historical document, Doré could assemble a task-context package such as:

```text
Project: Doré
Current phase: Cognitive Architecture
Current workstream: Core memory model

Relevant approved principles:
- model-independent durable knowledge
- provenance required
- Observe != Remember
- product adapters remain bounded

Recent working decisions:
- relevant dated records only

Open questions:
- memory-promotion authority
- observation scope
- automatic participation boundary

Relevant sources:
- master memo
- dated working record(s)
- relevant ONE / Visual experience

Do not assume:
- candidate ideas are approved architecture
```

This means Doré may eventually function as a **context broker/steward** between Westside Watch's durable institutional memory and replaceable AI models. The AI provider can change while the project enters each session with coherent, provenance-aware context.

## Cognitive principle emerging from 2026-08-22

The discussion produced a concise working principle:

> **Doré observes broadly, assists selectively, records faithfully, promotes cautiously.**
>
> **多雷廣泛觀察，選擇參與，忠實記錄，謹慎沉澱。**

This should be treated as a strong candidate Core principle, not yet silently promoted to final architecture before later dated discussions and the pre-build synthesis.

The practical aspiration is equally important: if Doré is implemented correctly, the human should no longer need to repeatedly tell the active AI, “this belongs in Doré's 08-22 working record rather than the master memo.” Doré should understand the active work context well enough to assist with classification and recording, while final authority over important product decisions and promotion remains human.

## Future API/service contract

Doré should eventually expose stable service contracts rather than requiring every product to know its internal model or prompt implementation.

Conceptual examples:

`Dore.refine_subtitles(segments, context)`

`Dore.review_bible_content(content, context)`

`Dore.normalize_metadata(content, context)`

For subtitle work, the contract should preserve stable segment IDs and timing and return structured corrections rather than only a rewritten paragraph. A future response may include:

- corrected text;
- correction category;
- confidence;
- reason/context signal;
- provenance/source used;
- `requires_human_review`;
- optional candidate alternatives when evidence is insufficient.

The API boundary is important because the underlying model may change. Westside Stories, ONE and later products should depend on the Doré contract and knowledge layer, not on a particular vendor/model name.

## Provenance and conflict priority

Shared memory requires source identity. Every durable term or correction should be able to record where it came from, for example:

- canonical/Scripture source;
- ONE research/editorial decision;
- Doré Visual research;
- Westside Stories human-confirmed subtitle correction;
- official church/brand terminology;
- project-local suggestion not yet promoted to shared knowledge.

Conflicts must not be flattened into one undifferentiated dictionary. Canonical text, official naming and human-confirmed editorial decisions should be distinguishable from model inference and low-confidence speech corrections.

## Brand bridge principle

Doré's value as a standalone project is therefore not that every Westside Watch product must call an AI model. Its value is that the products can share a growing Scripture-and-church intelligence while keeping their own responsibilities and interfaces.

The desired compounding cycle is:

> **ONE gives Doré Scripture depth; Doré gives Westside Stories contextual proofreading; Westside Stories gives Doré real spoken-language corrections; Doré returns that learning to ONE, the main site and future products.**

This is the product bridge. Each new Westside Watch project should be able to add knowledge to the shared core and receive appropriate knowledge back without becoming coupled to the internal implementation of another product.

## Immediate architectural consequence

Do **not** begin by hard-coding a large Bible correction system into `Westside-Stories/app/main.py`.

Before production integration, define and version:

1. Doré Core responsibilities and human-review boundaries;
2. Doré Knowledge schema, including provenance and promotion from product-local learning to shared knowledge;
3. the first product adapter/API contract for Westside Stories subtitle proofreading;
4. failure behavior: if Doré is unavailable or uncertain, Westside Stories must retain the original Whisper result rather than blocking subtitle creation or inventing a correction;
5. a feedback path by which accepted/rejected subtitle corrections can become reviewed Doré knowledge.

Westside Stories should be the first external consumer that proves Doré can function as shared brand infrastructure beyond its original ONE/engraving role.