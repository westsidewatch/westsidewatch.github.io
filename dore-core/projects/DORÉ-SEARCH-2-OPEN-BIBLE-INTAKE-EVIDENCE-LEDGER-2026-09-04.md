# DORÉ SEARCH 2 OPEN BIBLE INTAKE EVIDENCE LEDGER — 2026-09-04

Status: BOUNDED_RECONCILIATION_COMPLETE / FIRST_ADOPTION_CYCLE_VERIFIED
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md` + `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-SEARCH-2-2026-09-04.md`
P01 impact: NONE

## Bounded evidence reviewed

- commit `82fe854e3fd74b0c0c652937a89fa628fcc5158b` — `dore search: begin large-scale open Bible capability intake`;
- `dore-core/research/DORÉ-SEARCH-2-OPEN-BIBLE-INTAKE-2026-09-04.md`;
- current canonical `SEARCH` row in `DORÉ-MASTER-WORK-REGISTER.md`;
- earlier Sweep Search reconciliation recorded in Checkpoint 19, including `BIBLE-SEARCH-WORK-NODE.md`, `search-cognition-protocol.md`, `dore_core/search/service.py`, browser Search implementation and `RQ-003` / `ME-006` evidence boundaries;
- Search 2 implementation chain ending in commits `e9a804cafa2f1297f43f8078a970c525db8711fe` and `9016dab3b3e15690cb737c3fb779cd22b268cb68`;
- persisted `reports/DORÉ-BIBLE-SEARCH-WORK-NODE.json` schema `dore.work-node.bible-search.v4`.

## Current classification

### Search 2.0 open-Bible capability intake

**Classification:** `ACTIVE_PARALLEL / DISCOVERY + ENGINEERING INPUT` under canonical `SEARCH`, with one bounded source-to-product adoption cycle now `VERIFIED_COMPLETE`.

This remains an active Search improvement program, not a completed Search capability. The intake establishes a first-wave source registry across retrieval engines, cross-reference datasets, original-language/morphology layers, Chinese reference parsing, semantic search, note/study workflows and offline/local inference patterns. It also states a concrete target architecture and benchmark family.

The governing interpretation is deliberately stronger than a resource list: external projects are inputs to Doré's learning and engineering loop, not substitutes for Doré's own relevance judgment. A source counts as learned only after provenance/license inspection, method/data/code extraction, sandbox trial, measured benchmark delta, adopt/reject judgment, durable learning and justified integration.

## First verified adoption cycle — NEUU/OpenBible + TSK cross-reference graph

A bounded Search 2 source-to-product cycle has now crossed from intake into implemented capability.

Persisted acceptance evidence records:

- 66 books;
- 31,060 unique verses;
- 1,117,426 directed cross-reference edges;
- source counts: 606,368 supported by both source families, 487,484 OpenBible, 23,574 TSK;
- generated lazy-by-source-book shards rather than eager loading of the full graph;
- traceable open-cross-reference provenance under CC BY 4.0;
- no Bible translation text copied into the generated cross-reference index;
- Search browser consumption of the open graph;
- ONE consumption through the Doré-owned open-cross-reference bridge rather than a duplicate database;
- visible ONE UI exposing source/vote/weight and multi-hop relationship-path information;
- work-node acceptance schema `dore.work-node.bible-search.v4`, `status: AVAILABLE`, `verdict: PASS`, `failures: []`.

This is a legitimate bounded engineering milestone and should be retained as reusable Search/ONE capability evidence. It is not proof that the permanent Bible Intelligence Loop, Search cognition, issue #281, or the whole Search 2.0 architecture is complete.

## Evidence boundary

1. The intake file and establishing commit prove that Search 2.0 discovery/engineering intake began and that a concrete benchmark contract exists.
2. The later million-edge implementation chain now proves one listed source family was actually adopted and integrated; the older statement that no listed dataset had been integrated is superseded for this specific NEUU/OpenBible+TSK graph only.
3. Other registry labels such as `ADOPT FOR TRIAL`, `HIGH-PRIORITY CODE STUDY`, `STUDY/COMPARE`, `STUDY/REUSE PATTERNS` remain discovery dispositions, not capability PASS states.
4. License cautions remain material. Translation text, embeddings, GPL code, dataset provenance and dependency compatibility must be checked independently before reuse. Registry inclusion is not rights clearance.
5. The broader target architecture — Chinese/English parser, Traditional/Simplified aliases, lexical/phrase/proximity retrieval, entity/original-language expansion, morphology/semantic domains, local semantic retrieval, hybrid ranking, Living Search relevance gate, Inner Search and optional LLM-above-core — remains a design target except where separately evidenced.
6. The mandatory natural-Chinese benchmark family is materially stronger than the older narrow negative-relevance regression. The graph milestone does not by itself prove the complete natural-Chinese benchmark family passes across multi-book connection, false-premise challenge, ambiguity, Chinese variants, spoken phrasing, irrelevant prose suppression, traceability, latency and cost.
7. Repository evidence now contains a persisted work-node PASS for the graph and visible ONE integration. No GitHub combined-status entry was available for the latest UI commit in this bounded check, so this ledger does not inflate that absence into an Actions-level green-run claim.
8. The older Search cognition boundary remains unchanged: `TAUGHT` does not become `CONCEPT_PASS` or `PRODUCT_PASS` merely because Search 2.0 now has richer engineering capability.

## Relationship to earlier Search work

Search 2.0 does not supersede the original `BibleSearchIndex` work-node or the current browser Search by declaration. It is a convergence/improvement program that should absorb proven methods while resolving the already-recorded Core/browser duplication debt.

The new cross-reference graph is directionally correct because ONE is explicitly a consumer of Doré-owned cross-reference intelligence rather than a second graph database. That reduces duplication for this capability, but it does not yet prove the broader parser/relevance/ranking service-boundary convergence identified in `RQ-003`.

The canonical direction remains:

`one evidence-governed Search intelligence boundary -> reusable parser/retrieval/graph/ranking services -> browser/product consumers -> deterministic and semantic benchmark evidence`.

## Current quality judgment

The intake is strong as an engineering-learning contract because it prevents two common failures: copying open-source code without understanding/licensing it, and declaring capability from source accumulation. The first real adoption cycle materially improves its credibility: a large source family was normalized, sharded, provenance-governed, integrated into Search, bridged into ONE and exposed with evidence-bearing relationship metadata.

Its remaining weakness is breadth versus proof. One successful graph cycle does not establish the Chinese parser, hybrid ranking, semantic retrieval, cognition or service-boundary goals. The next work should therefore convert another high-value gap into measured product evidence rather than expand the registry for its own sake.

## Smallest useful next proof

Run a bounded natural-Chinese Search acceptance packet using the newly integrated graph plus the existing Search baseline:

1. freeze a representative slice covering multi-book connection, ambiguity, false premise, Traditional/Simplified aliases, spoken phrasing and irrelevant prose;
2. record current outputs, traceability, false positives, latency and runtime cost;
3. identify whether the next missing capability is Chinese reference parsing/alias normalization, graph ranking or another canonical service;
4. implement the smallest canonical-boundary change rather than a third independent engine;
5. rerun the same slice and persist explicit adopt/reject evidence;
6. add browser/Core/ONE parity where the capability is shared.

## Supersession / revisit / retirement judgment

- The claim that Search 2 intake had no integrated source is now `SUPERSEDED` for the NEUU/OpenBible+TSK graph family by the persisted v4 PASS.
- The million-edge graph + ONE visible bridge is a bounded `VERIFIED_COMPLETE` milestone to retain as regression capability evidence.
- No whole Search milestone is eligible for `VERIFIED_COMPLETE` from this cycle.
- No existing production Search path is retired.
- `RQ-003` remains active: service-boundary convergence should evaluate parser/retrieval/ranking duplication, while the cross-reference graph is now an example of the preferred shared-consumer architecture.
- The parent Search row remains `MAINTENANCE + DISCOVERY`, with active-parallel Search 2 engineering.

## P01 isolation

No P01 subtitle/runtime/deployment/binding/credential/audio-transcription state, ordering or blocker was modified by this reconciliation.
