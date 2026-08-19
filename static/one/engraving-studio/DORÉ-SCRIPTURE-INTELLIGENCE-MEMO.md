# Doré Scripture Intelligence Memo

Status: **FUTURE ARCHITECTURE MEMO — NOT CURRENT IMPLEMENTATION**

Purpose: preserve a possible long-term extension of Doré beyond illustration so this idea does not remain only in chat. This memo is descriptive, not a runtime contract, and must not be loaded by ONE reader/runtime.

## Core idea

Doré may eventually evolve from Westside Watch's dedicated Bible visual intelligence into a broader **Westside Watch Scripture Intelligence Layer**.

The common core would not be "image generation." The common core would be Doré's accumulated ability to:

- read Scripture in canonical context;
- recognize Bible books, chapters, people, places, events and quotations;
- distinguish explicit Scripture from paraphrase and ordinary church speech;
- use Westside Watch / church terminology consistently;
- apply accumulated editorial corrections and project-specific language memory;
- expose those capabilities to multiple Westside Watch products without allowing one product's rules to contaminate another.

The existing Engraving Studio remains the first mature specialization of that intelligence.

## Proposed capability separation

Do not collapse every Doré function into one undifferentiated prompt. A future shared core should expose separate profiles/capabilities:

### Doré / Visual

Current Engraving Studio specialization.

- Scripture-to-image reasoning;
- Doré original study and visual ancestry;
- ONE chapter plates and covers;
- Journal editorial illustration;
- Social / print / apparel / motion derivation.

Visual-generation rules must not automatically govern subtitle or text editing.

### Doré / Scripture

Possible text-focused Scripture specialist.

- detect Bible quotations and near-quotations in transcripts;
- identify likely book/chapter/verse references when evidence is sufficient;
- compare a spoken quotation against the project's approved Bible text/version;
- correct obvious Scripture transcription errors while preserving the speaker's intended meaning;
- flag uncertain matches instead of inventing a verse;
- provide structured evidence: detected quotation, proposed correction, reference, confidence, and review requirement.

### Doré / Editorial

Possible Westside Watch / church language specialist.

- maintain approved church, ministry, publication and brand terminology;
- normalize known proper names and official titles;
- normalize Bible-book names and recurring theological terms according to an explicit lexicon;
- preserve direct testimony and sermon wording unless a correction is clearly transcriptional or explicitly approved;
- distinguish house-style normalization from theological rewriting.

### Doré / Subtitle

Possible specialization for the future **Westside Story / 西區故事** video-caption product.

Suggested pipeline:

`Video/audio -> transcription + timestamps -> Doré Scripture/Editorial review -> human review where required -> SRT/VTT -> video burn-in/export`

Doré should operate on the transcript/subtitle text and metadata, not on the FFmpeg burn-in mechanics themselves.

## Westside Story use case

Doré could be especially useful after automatic speech transcription, where ordinary speech-recognition systems often misrecognize:

- Bible book names;
- biblical people and place names;
- verse quotations;
- church names and ministry names;
- pastor/member names in the approved local lexicon;
- theological vocabulary;
- traditional Chinese church wording.

A future subtitle editor should not simply ask Doré for "a better sentence." It should return structured edits so the application can distinguish safe corrections from editorial changes.

Recommended correction classes:

- `TRANSCRIPTION_ERROR` — clear speech-to-text error;
- `SCRIPTURE_CORRECTION` — identifiable Bible quotation/reference correction;
- `PROPER_NOUN_CORRECTION` — approved person/place/church/ministry name;
- `HOUSE_STYLE_NORMALIZATION` — punctuation, official project terminology or established style;
- `POSSIBLE_THEOLOGICAL_CHANGE` — wording could alter doctrinal or speaker meaning; human approval required;
- `UNCERTAIN` — insufficient evidence; preserve original and flag for review.

Hard rule: **Doré must not silently rewrite a testimony, sermon, prayer or theological statement merely because it prefers another formulation.**

## API / product-service direction

Doré's GitHub Markdown files are knowledge/rules/memory; they are not themselves an API.

If Doré becomes a reusable product service, build a server-side **Doré API/service layer** that loads only the capability required by the calling product.

Conceptual product calls:

- `ONE -> Doré / Visual + Scripture context`
- `Westside Watch Journal -> Doré / Visual + Editorial`
- `西區故事 -> Doré / Subtitle + Scripture + Editorial`
- `Daily devotional -> Doré / Scripture + Editorial + optional Visual`

The implementation may use a model API plus retrieval over curated Scripture, Doré memory, and Westside Watch editorial resources. The exact model/vendor/API is an implementation choice and should remain replaceable.

The service should favor structured machine-readable responses over unconstrained rewritten prose. Example conceptual fields:

- original text;
- proposed text;
- correction class;
- Scripture reference if any;
- evidence/source used;
- confidence;
- `requiresHumanReview`;
- explanation limited to what the application needs.

## Shared knowledge versus isolated behavior

A future common Doré core may share:

- canonical Scripture identity and text/reference knowledge;
- Bible people/place/event knowledge;
- Westside Watch approved vocabulary;
- church proper-name lexicon;
- accumulated verified corrections.

But behavior remains isolated by capability:

- visual composition rules do not alter subtitle prose;
- subtitle brevity/timing rules do not alter Bible interpretation;
- house style does not overwrite historical Scripture text;
- visual Doré references do not become theological evidence;
- product-specific prompts/memory must not silently become universal Doré doctrine.

## Possible church terminology layer

A separate future **Westside Watch Editorial Lexicon** may record approved forms for:

- official church name(s);
- pastor/member names where appropriate;
- ministries and meeting names;
- Westside Watch product names;
- Bible-book names and preferred abbreviations;
- recurring theological/church terms;
- Chinese/English capitalization and punctuation conventions;
- terms that must never be auto-rewritten.

This lexicon should be versioned, explicit and reviewable. Doré should consult it; Doré should not invent permanent terminology rules by itself.

## Maturity rule

This extension should happen only after the current Doré visual system and ONE production workflow remain stable. The memo records the direction; it does **not** expand the current Missing Plate list or interrupt `025-003` production.

Potential maturity sequence:

`Doré Visual (current) -> shared Scripture core -> Scripture Editor -> Editorial Lexicon -> Subtitle profile -> reusable Doré service/API`

Each stage requires its own tests and human-review boundaries.

## Relationship to current Doré documents

- `README.md` — what Doré ultimately is and where it is used.
- `ONE-DORE-LEARNING-CURVE.md` — how the visual intelligence learns.
- Living Studio / Visual Grammar — what the visual intelligence has learned and stabilized.
- `ONE-PRODUCTION-ROADMAP-TEMP.md` + progress JSON — current temporary ONE production state.
- **This memo** — possible future non-visual Scripture/editorial/service expansion. It should remain a memo until a separate implementation project is intentionally started.

## Do not do yet

- Do not make this memo a ONE runtime dependency.
- Do not add subtitle code to ONE.
- Do not mix FFmpeg/video processing into Engraving Studio runtime.
- Do not let future subtitle corrections train visual grammar automatically.
- Do not treat the memo as permission for automatic theological rewriting.
- Do not interrupt the current Missing Plate execution order.
