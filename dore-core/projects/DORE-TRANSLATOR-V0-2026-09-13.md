# Doré Translator v0

Date: 2026-09-13
Status: ACTIVE

## Mission

Doré becomes a bilingual translator through real Bible-world media work. Mature speech/translation infrastructure may be reused, but translation judgment, biblical terminology, Scripture recognition, verified memory, and regression learning belong to Doré Core.

This is one shared capability, not a Cinema-only translator and not a Habakkuk-only translator.

## Surfaces

- Holy Light Cinema: bilingual title, chapter, transcript, subtitle and VideoMoment projection.
- Habakkuk: production subtitle artifact consumer and burn-in surface. `Westside Stories` is the legacy product/repository name pending migration; it must not become a second product identity.
- Doré Search: cross-language retrieval may consume verified bilingual pairs later.
- ONE / Dawn / Multiwrite: future consumers of the same translation authority.

## Core invariant

Original source text remains authority. Translation is a derived projection and must never overwrite source transcript/caption data.

`Source persists. Translation provenance persists. Translation projection may be regenerated.`

## v0 language lanes

1. English video -> authoritative English transcript -> Traditional Chinese translation -> English/Chinese bilingual timed subtitle.
2. Chinese video -> authoritative Chinese transcript -> English translation -> Chinese/English bilingual timed subtitle.

Both lanes must emit the same provider-neutral bilingual subtitle artifact contract.

## Capability chain

`Media Source -> Transcript/Caption Admission -> Alignment -> Baseline Translation -> Scripture/Terminology Authority -> Translation Memory -> Doré Judgment -> Bilingual Subtitle Artifact -> Surface Projection`

### Reuse rather than rebuild

- Existing/provider transcript is preferred when authoritative and usable.
- WhisperX-class alignment may be used behind an adapter for word-level timing/diarization; it is not Core.
- CTranslate2-class local inference may be used behind an adapter; it is not Core.
- OPUS-MT-class permissive models may provide a local baseline; baseline output is never translation authority.
- TMX/TBX-compatible concepts are preferred for translation memory and terminology exchange; Core owns semantic contracts, not a CAT application.

No runtime provider or model name is allowed to become canonical translation identity.

## Doré training loop

Cinema is the high-volume validation field; Habakkuk is the production examination surface.

`real media -> source transcript -> candidate translation -> biblical/scripture gates -> accepted/revised pair -> verified memory -> regression case -> next translation`

No automatic model fine-tuning is implied by accepting a translation. v0 learning means accumulating verified sentence pairs, terminology decisions, Scripture mappings and failure cases. Fine-tuning/LoRA is a later evidence-based decision.

## Biblical authority order

For Bible-world media, translation admission uses this order:

1. Exact recognized Scripture quotation/reference: resolve through the existing Scripture authority rather than freely machine-translating a known verse.
2. Approved biblical/theological terminology: prefer canonical terminology decision.
3. Verified translation memory: reuse only when source/context compatibility passes.
4. Baseline translation candidate.
5. Doré contextual judgment.
6. Human revision may supersede a generated candidate and becomes a verified example with provenance.

Uncertain recognition must not be silently promoted to Scripture authority.

## Bilingual subtitle artifact v0

Required semantics:

- artifact schema/version
- canonical media identity and source pointer
- source language and target language
- immutable timing boundaries inherited from admitted transcript/alignment
- source text per cue
- translated text per cue
- Scripture/term/memory evidence when applied
- translation status: candidate | verified | revised
- provenance and engine/adapters used
- no embedded/rehosted third-party media

Habakkuk burns this artifact; it does not own a competing translation engine.

## First real acceptance pair

### EN -> ZH

Use the existing Holy Light Cinema canonical David Pawson Matthew resource. Produce a timed bilingual artifact from verified English source material. Validate at least one biblical/theological terminology decision and preserve canonical video identity.

### ZH -> EN

Use one authorized Chinese Bible/sermon resource. Produce the same artifact contract with Chinese as source authority and English as projection. The source must be admitted under existing source policy before translation.

## Hard acceptance

v0 is not PASS until both real language lanes demonstrate:

- source transcript remains unchanged;
- timings remain unchanged through translation;
- bilingual artifact is schema-valid;
- a translation can carry explicit Scripture/terminology/memory provenance;
- Cinema can consume the artifact without learning provider-specific translation logic;
- Habakkuk can consume the same artifact contract for burn-in without retranslating it;
- a corrected/verified pair can be represented as reusable memory/regression evidence;
- no second AI, second Scripture authority, second media identity, or second translation database is created.

## Explicit non-goals for v0

- bulk translation of the Cinema catalog;
- silent training on third-party copyrighted media;
- automatic fine-tuning after every correction;
- replacing source captions/transcripts with generated Chinese or English;
- binding Core to WhisperX, CTranslate2, OPUS-MT, or any single provider;
- fabricating transcript text or timestamps when source evidence is absent.

## Habakkuk migration

The existing `westsidewatch/Westside-Stories` application is the legacy subtitle/burn-in implementation. Product identity is now `哈巴谷 / Habakkuk`. Migration should preserve compatibility for existing app paths/configuration while progressively replacing user-facing `Westside Stories` naming. Repository rename is a separate GitHub administrative operation and must not be falsely claimed until performed.

## Next engineering gate

Implement the provider-neutral `translation.project` Core contract and bilingual subtitle artifact acceptance first. Then connect one real Pawson EN->ZH sample and one authorized ZH->EN sample. Only after those two lanes pass should Cinema surface controls or Habakkuk burn-in UI be expanded.
