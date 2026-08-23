# Doré Foundation — Biblical World

Status: ACTIVE EDUCATION — FULL COURSE RUN
Started: 2026-08-22
Full-course run started: 2026-08-22
Prerequisite milestone: `SCRIPTURE_READING_COMPLETE`
Reflex prerequisite: `REFLEX_CONSOLIDATION_1_0_GRADUATED`

## Why this stage exists

Doré can now read Scripture. The next task is to learn the world in which Scripture occurs without collapsing text, history, archaeology, geography, tradition, or scholarly reconstruction into one undifferentiated answer.

This is an educational stage, not yet a milestone. Small capability gates inside it must not be described as milestones.

## Learning model from this run onward

Every Biblical World lesson must grow two things together:

1. **Knowledge** — durable, provenance-aware knowledge of the biblical world.
2. **Reflex** — transferable routes that determine when and how that knowledge is activated, combined, checked and bounded.

A lesson is not complete merely because facts were ingested. It must produce transferable behavior on unseen stimuli. Real Doré Bible Search failures are learning signals, not answer-patch instructions.

### Question-intent reflex rule

Doré must never graduate a question capability merely because one wording works. A known query is a **stimulus**, not a feature specification.

Every question-learning change must target a transferable intent family and pass paraphrase + unseen-transfer tests. The intended route is:

`free-form question → intent family → scope → entities/concepts/relations → evidence route → answer shape`

Initial intent families include, but are not limited to:
- `ENTITY_LOOKUP` — who/what is X?
- `ENTITY_COUNT` — how many X are in Scripture?
- `ENTITY_RELATION` — who is X's father/son/wife/king/etc.?
- `PASSAGE_LOOKUP` — where does Scripture say X?
- `PLACE/ROUTE` — where is X / how far / what route?
- `TIME/SEQUENCE` — when / before-after / reign-period questions;
- `PRESENCE_BY_SCOPE` — does X occur/exist in OT/NT/book/period? e.g. `舊約有聖靈嗎？`;
- `CONCEPT/THEME` — semantic/theme questions whose wording need not occur literally, e.g. `十字架的影子`;
- `ORIGINAL_LANGUAGE` — source-form/lemma questions;
- `EVIDENCE/INTERPRETATION` — what is explicit, inferred, traditional, reconstructed, or disputed?

A rule that matches only `聖經有幾位馬利亞？` is a FAIL even if that query returns a correct answer. It must transfer to unseen names and paraphrases such as `新約有多少個約翰？`, `聖經裡叫猶大的有幾個？`, etc., without hard-coded names.

Likewise, `舊約有聖靈嗎？` must not be implemented as a phrase-specific shortcut. It belongs to a reusable `PRESENCE_BY_SCOPE` route that can transfer to questions such as `舊約有復活的觀念嗎？` or `新約有祭司制度嗎？`, while preserving the distinction between literal lexical occurrence and concept-level presence.

`十字架的影子` belongs to semantic/theme routing and must remain a transfer test rather than a memorized verse list.

## Product–education constraint

This stage must improve real external directions while preserving Core independence:

1. **Doré Bible Search** — grow from verse/word search toward reliable person, place, event, period, route, historical-context and eventually evidence-bounded semantic/theme search.
2. **ONE** — Doré Search is also ONE's internal biblical search/intelligence layer. ONE is simultaneously a learning laboratory: its chapter Scripture, story/background modules, maps, chronology, cross-references, Gospel harmony, resources and study-question entry points provide passage-bounded stimuli from which Doré can discover missing capabilities and exercise learned ones.
3. **Bounded subtitle proofreader** — gain robust recognition of biblical people, places, peoples, book names, aliases, abbreviations and transliteration variants, plus contextual disambiguation.
4. **Westside Watch brand content bridge** — ONE provides a controlled route from canonical Scripture and evidence-bearing Core knowledge into brand study/content surfaces. Doré may learn the structure, recurring questions and information needs of ONE, then propose or produce evidence-bounded improvements to ONE; brand/editorial interpretation must remain distinct from Scripture-explicit claims.

The stage must not be distorted merely to satisfy those products. Product needs identify useful educational priorities; evidence rules still govern Core.

## ONE learning loop

From BW-1 onward, ONE participates in Doré's education through a bidirectional loop:

`ONE passage/context → Doré stimulus → Core entity/world/search routes → evidence-bearing answer/candidate → ONE surface → failure/ambiguity signal → Doré learning queue`

Rules:
- ONE is a **work node and learning laboratory**, not Doré's source of biblical truth.
- Scripture and provenance-bearing source corpora remain evidence sources; ONE's authored questions, layouts and editorial modules are stimuli/context unless independently sourced.
- Doré must learn ONE's information architecture and recurring user intents so that future Core capability can improve ONE without coupling Core to ONE's UI implementation.
- Chapter context should constrain entity disambiguation and ranking. A user searching inside Matthew 1 should not receive the same unbounded ranking as a global search when passage context is relevant.
- ONE's prepared/exegetical questions may become **diagnostic prompts**. Their prepared answers must not become hidden gold answers unless separately evidence-labelled and admitted into an evaluation set.
- Search failures, unresolved entities, missing geography/chronology/context and repeated question classes become learning signals by capability class, not one-off answer patches.
- Improvements flow outward from Core to ONE; ONE-specific presentation logic does not become Core doctrine.

### ONE learning surfaces by Biblical World section

- **BW-1 Entity**: chapter people/place/people-group mentions, aliases, pronouns, same-name disambiguation, entity aggregation questions such as `聖經有幾位馬利亞？`.
- **BW-2 Geography**: maps, routes, rivers, mountains, ancient/modern place candidates and chapter-bounded place queries.
- **BW-3 Chronology**: ONE timeline nodes, reigns, sequence questions and passage-to-period context.
- **BW-4 Peoples/polities**: nations, empires, rulers and changing political context around each chapter.
- **BW-5 Institutions/social world**: temple, priesthood, household, money, measures, agriculture and other explanatory entry points already natural to chapter study.
- **BW-6 Evidence**: every surfaced explanation must preserve the distinction among Scripture-explicit, inferred, historical/archaeological reconstruction, tradition and editorial interpretation.

### Future ONE optimization capability

Doré may optimize ONE only after the relevant capability has evidence and tests. Optimization can include detecting missing chapter entities/context, proposing better search/context entry points, finding duplicated or inconsistent background information, identifying unanswered recurring study questions, and supplying provenance-aware structured data. Visual/editorial changes remain product decisions and are not autonomously learned as biblical facts.

## Curriculum

### BW-1 Entity identity and aliases
Doré learns stable identities for persons, places, people groups, polities, offices, institutions, events and material objects.

Required abilities:
- distinguish identical names belonging to different entities;
- connect Chinese, English, Hebrew, Aramaic, Greek and conventional transliterations as aliases without declaring them identical when evidence is uncertain;
- connect an entity to canonical attestations;
- preserve historical names and later names separately;
- expose ambiguity rather than silently choosing;
- use ONE chapter context as a ranking/disambiguation constraint without treating ONE editorial text as identity evidence;
- aggregate same-name candidates canon-wide for questions such as `聖經有幾位馬利亞？`, preserving disputed identity merges rather than forcing a single count;
- treat `ENTITY_COUNT` as a transferable question family, not a Mary-specific pattern.

Reflex growth: mention/question → intent family → scope (ONE chapter or global canon) → candidate entities → context constraints → disambiguation/aggregation → attestations → uncertainty.

Direct product benefit: entity search, ONE contextual search and subtitle name correction.

### BW-2 Geography
Doré learns physical and historical geography: settlements, regions, rivers, mountains, roads, routes and changing political boundaries.

Required abilities:
- coordinates with source and precision;
- ancient name / modern-site candidate separation;
- route and distance calculations labelled as reconstruction rather than Scripture fact;
- multiple proposed identifications with confidence and evidence;
- time-aware geography where names/boundaries change.

Reflex growth: place/question → intent family → identity → attestations → geographic evidence → reconstruction boundary.

Direct product benefit: Biblical Places search, ONE maps, subtitle place-name recognition.

### BW-3 Chronology
Doré learns relative and absolute chronology, reigns, synchronisms, periods and uncertainty ranges.

Required abilities:
- distinguish explicit biblical sequence from reconstructed absolute dating;
- represent BCE/CE ranges and competing chronologies;
- connect events to rulers, empires and textual attestations;
- never fabricate a precise year where sources permit only a range.

Reflex growth: temporal question → intent family → textual sequence → historical anchors → candidate ranges → competing chronologies → bounded conclusion.

Direct product benefit: timeline search, ONE chronology, context ranking.

### BW-4 Peoples, kingdoms and empires
Doré learns Israel/Judah and surrounding peoples/polities across changing historical periods, including Assyrian, Babylonian, Persian, Hellenistic and Roman contexts.

Required abilities:
- time-bound political identity;
- ruler/reign relationships;
- territorial change;
- distinguish biblical designation from modern historical terminology.

Reflex growth: people/polity question → intent family → period → ruler/territory/context → textual and external evidence → historical naming boundary.

### BW-5 Institutions and social world
Doré learns temple, priesthood, synagogue, household, kinship, kingship, courts, military structures, trade, agriculture, money, weights/measures and everyday social conventions.

Required abilities:
- place each institution in its historical period;
- distinguish textual description from comparative historical reconstruction;
- preserve uncertainty and regional variation.

Reflex growth: social/institutional question → intent family → period/context → textual evidence → comparative evidence → bounded reconstruction.

### BW-6 Evidence discipline
Every world claim must carry one of these evidence classes:
- `SCRIPTURE_EXPLICIT`
- `SCRIPTURE_INFERRED`
- `PRIMARY_EXTRA_BIBLICAL`
- `ARCHAEOLOGICAL`
- `GEOSPATIAL_OBSERVATION`
- `SCHOLARLY_RECONSTRUCTION`
- `TRADITIONAL_IDENTIFICATION`
- `EDITORIAL_NORMALIZATION`

Every claim must carry provenance, temporal scope, and where appropriate confidence/controversy status.

Reflex growth: question/claim → intent family → evidence class → provenance → temporal scope → confidence/controversy → permitted wording.

## Full-course execution order

`BW-1 → BW-2 → BW-3 → BW-4 → BW-5 → BW-6 → cross-domain consolidation → canon-spanning blind exam → BIBLICAL_WORLD_COMPLETE`

Do not stop merely because an individual BW section passes. Failures are repaired and rerun until the end-to-end graduation gate is green or a genuine evidence/product decision requires human judgment.

## Semantic transfer test — 「十字架的影子」

Reserved user-facing transfer stimulus: **十字架的影子**.

Purpose: test whether Doré is growing beyond literal keyword retrieval toward evidence-bounded biblical semantic/theme search.

This phrase must **not** be hard-coded to a prepared answer or fixed verse list. It is a transfer test, not training data.

A mature response should be able to discover relevant relationships through learned entities, events, chronology, institutions, textual relations and evidence classes. Candidate relationships may include sacrificial, Passover, suffering, crucifixion, typological or intertextual material only when the evidence route supports them.

Required epistemic separation:
- what a biblical passage explicitly says;
- what is inferred through textual/intertextual relationship;
- what later Christian interpretation identifies typologically/theologically;
- what remains uncertain or disputed.

The test FAILS if Doré merely searches the literal characters `十字架` or returns a memorized list. It also FAILS if later theological interpretation is presented as though the source passage explicitly stated it.

This semantic transfer test is diagnostic during training. Final success is evaluated only after the six Biblical World sections have been consolidated; it does not replace the canon-spanning blind exam.

## Graduation definition

This stage is complete only when a canon-spanning blind exam can give Doré arbitrary passages/questions and require it to reconstruct the relevant world through:

`question → intent family → passage/entities/concepts → place → time → polity → social/institutional context → evidence classes → competing reconstructions → uncertainty`

with no unsupported precision and no confusion between Scripture statements and later reconstruction.

The future major milestone name is reserved as `BIBLICAL_WORLD_COMPLETE`; it must not be issued until the whole stage and end-to-end benchmark pass.

## First work-oriented checkpoint

The first checkpoint is **Biblical Entity Recognition**, because it simultaneously strengthens Bible Search, ONE contextual intelligence, and is a prerequisite for a bounded subtitle proofreader. Passing that checkpoint is not a milestone.
