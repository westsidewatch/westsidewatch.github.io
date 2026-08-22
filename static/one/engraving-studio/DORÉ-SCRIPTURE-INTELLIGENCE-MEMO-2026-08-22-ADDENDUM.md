# Doré Scripture Intelligence Memo — 2026-08-22 Addendum

Status: **ARCHITECTURE MEMO — FUTURE PRODUCT DIRECTION, NOT CURRENT RUNTIME**

This addendum belongs with `DORÉ-SCRIPTURE-INTELLIGENCE-MEMO.md` and records the 2026-08-22 product discussion. It does not replace the main memo. It makes explicit a direction already latent there: Doré is becoming Westside Watch's next product/project and a shared brand-level Scripture intelligence unit rather than remaining only an illustration subsystem inside ONE.

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