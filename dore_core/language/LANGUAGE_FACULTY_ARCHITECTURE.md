# Doré Language Faculty — site-wide substrate

Status: architecture locked; implementation/adapters proceed incrementally.

## Principle

Translation is not a Dawn Library feature and not an AI call. It is a native Doré language faculty available to the whole site. Product areas only expose local surfaces over it.

The faculty must run without requiring an LLM/remote AI request for ordinary translation. Models and engines are lazy-loaded and may execute locally/server-side/browser-side according to device and language route.

## Absorbed engine/model capabilities

- CTranslate2: common optimized inference substrate for compatible translation models.
- MADLAD-400: broad multilingual candidate route.
- OPUS-MT / Marian models: smaller language-pair routes where quality/size is preferable.
- Bergamot: browser/WASM, viewport-local translation route and alignment patterns.
- Argos Translate: offline package/model-management and fallback patterns.
- NLLB: benchmark/reference only unless licensing/deployment policy changes; not a production dependency.

These are providers behind Doré. No product surface talks directly to an engine.

## Core contract

Input:
- source language (detected or declared)
- target language
- stable segment(s)
- local context packet
- terminology/entity hints
- product profile
- rights/transformation state

Output:
- translated stable segment(s)
- source/target language
- provider/model provenance
- confidence/quality signals when available
- alignment data when available
- cache policy

## Routing

Doré selects the smallest sufficient route by language pair, device/runtime, model residency, text type and quality profile. Model loading is sparse and lazy. Repeated segments may reuse legal caches.

## Site projections

- Dawn Library: original / Traditional Chinese / bilingual reading; segment-aligned long-form translation.
- Doré Folio: selection/document translation during writing and research.
- Magazine: optional translation reading layer for eligible non-Chinese material.
- Cinema: subtitle/transcript translation when source/rights permit.
- Church: multilingual article/sermon/ministry text surfaces when useful.
- Search/discovery: translated snippets only when needed for comprehension; canonical identity remains language-neutral.
- ONE: may use general-language translation for non-Scripture surrounding scholarship, but Scripture text and Bible translations remain outside this automatic translation product.

## Hard boundaries

1. Translation does not create a new canonical Work or fake published edition.
2. Source text remains authority.
3. Bible Scripture text / Bible translations are excluded from automatic Dawn translation.
4. Existing copyrighted translations may provide only lawful metadata/terminology signals; never reconstruct them.
5. Provider/model licensing and source transformation rights are checked independently.
6. UI never exposes engine complexity unless diagnostic mode explicitly requests it.

## Architectural consequence

Language capability grows inward: one Doré faculty, many product surfaces. Adding an engine or model increases the site's language ability without adding a second translation product or requiring every section to call AI.
