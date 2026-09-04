# Doré Search 2.0 — Open Bible capability intake

Status: ACTIVE ENGINEERING INPUT
Date: 2026-09-04
Issue: #281

Principle: resources are food for Doré to digest. Open-source projects do not replace Doré's learned Bible-search judgment; they supply mature parsers, corpora, graphs, morphology, semantic retrieval, study workflows, and local inference so Doré can spend its learning budget on relevance, connection, judgment, and timing.

## First intake wave

### Retrieval / intelligence layers
- crizin/bible-db — MIT code; source-dependent data licensing; multilingual SQLite/JSONL; Strong's; Hebrew/Greek morphology; semantic-domain tags; committed semantic vectors. ADOPT FOR TRIAL: schema, morphology/domain retrieval, local SQLite patterns. Do not import translation text without explicit license review.
- neuu-org/bible-crossrefs-dataset — 1.1M+ OpenBible + TSK edges; CC BY 4.0 consolidated dataset; weighted graph. ADOPT FOR TRIAL: cross-reference graph/ranking benchmark.
- CrossReferences-org/bible-cross-references — phrase-level TSK-derived anchors, CC BY 4.0. ADOPT FOR TRIAL: phrase-to-cross-reference alignment.
- echology-io/open-scripture-intelligence — normalized Scripture/chunks/graph/topics/entities/embeddings architecture. STUDY/COMPARE: intelligence-layer architecture; verify dataset maturity before adoption.
- kbennett2000/concord — offline semantic Scripture API; multilingual embedding model; places/topics/original-language layers; private translation pattern. STUDY/REUSE PATTERNS: offline retrieval and licensed-translation separation.
- loveJesus/rhema-chirho — Rust scholarship/search engine: Boolean, phrase, proximity, Strong's, lemma, morphology, semantic domains, crossrefs, syntax, discourse, concept expansion, hybrid ranking, WASM/API. HIGH-PRIORITY CODE STUDY: query model and hybrid ranker; verify license/dependency compatibility before code adoption.
- placek/deepbible — browser study workspace with translations, Markdown notes, lexical help, crossrefs, commentaries, semantic search. STUDY UX/DATA PIPELINE.
- dgreenheck/tolle-lege — word-level original-language alignment, Strong's, morphology, weighted crossrefs. STUDY DATA PIPELINE and ranking.

### Chinese / reference parsing
- linkongren/obsidian-bible-study — Chinese CUV-oriented reference shorthand/parser, Bible reader, mobile workflow. HIGH PRIORITY: inspect parser and aliases; license review before reuse.
- tim-hub/obsidian-bible-reference — Scripture reference insertion/suggestion. STUDY parser/editor integration.
- der-bingle/obsidian-scripture — local Scripture sidebars and reference navigation. STUDY local/sidebar patterns.

### Notes / study-preparation
- harvouscom/harvous — open Bible-study notes app emphasizing organizing, remembering, and findability. STUDY inner-search and note model.
- FishArmy100/bible_study_app_v2 (Ascribe) — offline/open note-taking/search app. STUDY offline/editor/search integration; GPL boundary must be respected.
- strongs-de/strongs (Akribos) — parallel translations, Strong's, morphology, crossrefs, PostgreSQL FTS/trigram. STUDY query/index strategy.

### Semantic search examples
- ashrielbrian/bible_semsearch — vector Bible search using OpenAI + SentenceTransformers. REFERENCE ONLY: architecture is simple; copyrighted translation/embedding provenance must not be imported blindly.

## Doré target architecture

1. Chinese/English reference parser and canonical verse coordinates.
2. Traditional/Simplified aliases, book/person/place normalization.
3. Exact/full-text/phrase/proximity retrieval.
4. Entity/topic/original-language expansion.
5. Strong's + morphology + semantic-domain retrieval.
6. Weighted cross-reference graph and multi-hop traversal.
7. Local/offline semantic retrieval where feasible.
8. Hybrid ranker: lexical + graph + semantic + ONE + Dawn Library.
9. Biblical relevance gate for Living Search.
10. Personal Inner Search over user's own writing.
11. Optional paid/general LLM only above the core retrieval layer.
12. Voice query is another input modality, not a separate search engine.

## Mandatory benchmark before any PASS

Natural Chinese prose, not keyword-only:
- 基列 → 基列雅比 → 掃羅死後: recover Judges/Samuel/Chronicles connections with defensible ranking.
- 曠野 → 耶穌受試探: recover Matthew/Mark/Luke and Deuteronomy 6–8, not merely verses containing 曠野.
- 為什麼舊約沒有聖靈？: challenge the false premise by surfacing OT רוח / 神的靈 / 耶和華的靈 evidence before synthesis.
- ambiguous people/place names and same-name disambiguation.
- Traditional/Simplified Chinese and common Chinese Bible abbreviations.
- spoken natural-language query variants.
- irrelevant ordinary writing: suppress Bible suggestions rather than forcing accidental matches.

Measure: relevance, recall/breadth, surprising-but-defensible connections, traceability/citation, false-positive noise, latency, and local/runtime cost.

## Engineering rule

No source counts as learned because it appears in this registry. For each serious source: inspect provenance/license -> extract reusable method/data/code -> sandbox trial -> benchmark delta -> adopt/reject -> record durable learning -> integrate only if objective evidence improves Doré Search.

No generic test or command exit code may mark Search 2.0 complete. Completion requires actual before/after benchmark evidence and integrated capability.