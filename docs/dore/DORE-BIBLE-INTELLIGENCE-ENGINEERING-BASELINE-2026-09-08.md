# DORÉ Bible Intelligence — Engineering Baseline

Date: 2026-09-08
Status: engineering start baseline

## Product goal

Build a local-first, personal-context-aware Bible research system whose task result can exceed a generic ChatGPT answer for the user's Bible-study workflow. This is not a claim that a local model is generally smarter than ChatGPT.

The system must combine:

1. ChatGPT-like query understanding and association.
2. Canonical structured Bible evidence and provenance.
3. DORÉ personal context and historical notes.
4. ONE as a Bible-world source and optional deep-study destination.
5. Multiwrite as the persistent preparation/writing environment.
6. Study Flow so evidence becomes an editable teaching/sermon rundown.
7. Present projection so the same source document can become a live presentation without PowerPoint being the source of truth.

## Frozen principle

> Models propose associations; evidence verifies them; DORÉ owns the relationship, ranking, context assembly, and action.

External systems are substrates/donors, never DORÉ authority.

## Query planner: minimum capability first

Order of escalation:

1. canonical Bible reference parser
2. exact/entity/reference lookup
3. lexical / substring / FTS / BM25
4. canonical relations: verse/person/place/lemma/cross-reference
5. personal/context retrieval
6. semantic Scripture/document retrieval
7. evidence alignment
8. reasoning specialist only when the question requires synthesis

Reference, exact text, Strong's, morphology, person/place and basic cross-reference queries should not require a large model.

## Evidence model

Canonical facts and interpretive relations must remain distinct.

Canonical examples:
- verse identity
- person/place identity
- lemma/morphology
- explicit occurrence
- source-backed geography

Interpretive examples:
- manna ↔ daily bread
- wilderness provision ↔ Matthew 6 anxiety
- literary/theological thematic relationships

Interpretive relations require provenance and must never silently become canonical truth.

## Mature-resource admission candidates

POC / source-donor priority:
- Concord: offline semantic Scripture + structured Bible retrieval patterns
- STEPBible Data: original-language, morphology, names/entities, structured scholarly data
- CrossWire/SWORD ecosystem: Bible/commentary/lexicon/general-book resource model; license admission remains per resource
- Bible Passage Reference Parser / OSIS patterns: canonical reference normalization
- QMD: document/evidence retrieval; already admitted substrate
- SQLite FTS5 / Orama POC: zero/low-model instant reflex
- LongMemory: current/history/personal knowledge substrate; non-authority

Multiwrite / UX donors:
- Harvous / Selah: Bible-note and Scripture-link patterns
- Semantic Backlinks / Various Complements: ambient recall interaction
- Pagefind Component UI: result rendering/accessibility primitives
- block-editor/Vizel patterns: reorderable Study Flow
- FreeShow: rundown/timeline/cue model donor
- Reveal.js / Marp: presentation and export substrate/donor

Do not add a resident daemon or model merely because a candidate is mature. Preserve the Free Gate and Intelligence-per-Resource Gate.

## DORÉ Context Result vNext

Provider-neutral result fields should converge on:

- type
- title
- snippet
- relation
- source_kind
- source_ref
- confidence
- provenance[]
- preview
- actions[]
- canonical_reference (when applicable)
- evidence_status: canonical | supported | possible | disputed | unsupported

Products must not learn substrate/provider names.

## Multiwrite Bible Study document

Do not create separate incompatible products for Bible-study preparation, live notes, and sermon preparation. Use one structured Study Document with projections/modes.

Core blocks:
- heading / outline
- BibleReference
- note
- evidence/result pin
- quotation/source
- question
- application
- cue
- media/presentation block

A result can be:
- Keep: retain in research material
- Flow: place into the teaching/sermon rundown
- Present: include in audience projection

## Modes

### Prepare
Ambient contextual recall enabled. Search may surface personal notes, Scripture, ONE preview, Journal/Archive, books/documents, canonical Bible resources and other admitted sources.

### Live
Ambient recommendations default off. Show current cue, next cue, references, pinned material and time. Explicit fast search remains available. Reordering must be low-friction and safe under pressure.

### Present
No search UI. Project selected structured blocks. The Study Document remains the source of truth; PDF/PPTX are exports, not authoring formats.

## ONE × Multiwrite context policy

Standalone Multiwrite:
- ONE may appear as one ranked source among many.
- ONE result first opens a useful in-Multiwrite preview.
- entering ONE is optional and explicit.

Multiwrite embedded in ONE:
- same underlying Multiwrite document/note system
- ONE self-recommendations are suppressed
- other fuzzy/contextual results remain available

The user should remain in the current product unless they explicitly choose deeper navigation.

## Ambient UI target

Use a three-state interaction rather than a permanent search popup:

1. Ghost — very faint context hint while writing
2. Rail — 3–5 high-quality ranked results after pause/focus
3. Preview — expand selected evidence inside the current product

The UI must disappear when irrelevant and must not interrupt fast typing.

## Bible challenge set — first acceptance corpus

Use real difficult question classes, including:
- Why does Matthew 6:34 follow 6:33?
- Does 'our debtors' include oneself?
- Why is 'the evil one' characteristic/significant in Matthew?
- What attitude lies behind 'Is Saul also among the prophets?'
- Why did Jabesh-gilead not join the action against Benjamin?
- Was Josephus a Christian?
- Why do Jesus' wilderness replies cluster in Deuteronomy 6–8?

Evaluate each answer for:
- recall
- textual accuracy
- original-language accuracy when relevant
- historical accuracy
- relationship quality
- provenance/evidence
- uncertainty discipline
- personal/current-task relevance
- usefulness for teaching
- latency
- resource cost

## Hard gates

1. Recall Gate — important relevant Scripture/evidence should not be systematically missed versus a strong general-model baseline.
2. Precision Gate — canonical references, names, places, original-language facts and quotations must resolve to admitted evidence.
3. Evidence Gate — important factual claims can answer 'why do you say this?' with provenance.
4. Context Gate — current ONE location, Multiwrite document, personal notes and Study Flow can affect ranking without contaminating canonical truth.
5. Action Gate — evidence can become Keep / Flow / Present without copy-paste into another authoring system.
6. Free Gate — core Bible research remains useful offline with commercial API keys removed.
7. Minimum Capability Gate — deterministic/structured retrieval wins before model escalation.
8. Product Interface Freeze — ONE and Multiwrite consume DORÉ contracts, never QMD/Concord/SWORD/etc. directly.

## First implementation slice

Do not attempt the entire Bible Intelligence system in one change.

Slice BI-1:
1. introduce shared BibleReference contract
2. introduce Study Document / Study Flow domain schema independent of UI
3. extend provider-neutral Context Result with Bible/evidence/action metadata without breaking existing callers
4. introduce search context policy (`host`, `mode`, self-source suppression)
5. preserve current `context.fuzzy-search` contract and passive lexical-first route
6. add tests for standalone Multiwrite vs embedded-in-ONE result policy

Slice BI-2:
- wire production search corpus to real Context Result hits
- add canonical Bible/reference substrate POC behind DORÉ boundary
- benchmark first challenge queries

Slice BI-3:
- Multiwrite Bible Study UI: Prepare + Ghost/Rail/Preview + Keep/Flow/Present
- ONE embedded Multiwrite surface

Slice BI-4:
- Live rundown and Present projection
- Reveal/Marp/FreeShow-derived implementation decisions after POC

## Non-goals for BI-1

- no new large resident model
- no PowerPoint clone
- no duplication of ONE's 66-book Bible corpus inside Multiwrite
- no provider-specific UI
- no claim that DORÉ is already the world's best Bible search
- no promotion of interpretive associations to canonical truth
