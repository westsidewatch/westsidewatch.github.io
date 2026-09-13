# Doré Translator v0

Date: 2026-09-13
Status: ACTIVE

## Mission

Doré becomes a bilingual translator through real Bible-world media work. Mature speech/translation infrastructure may be reused, but translation judgment, biblical terminology, Scripture recognition, verified memory, and regression learning belong to Doré Core.

This is one shared capability, not a Cinema-only translator and not a Habakkuk-only translator.

## Core invariant

Original source text remains authority. Translation is a derived projection and must never overwrite source transcript/caption data.

`Source persists. Translation provenance persists. Translation projection may be regenerated.`

## v0 language lanes

1. English video -> authoritative English transcript/caption -> Traditional Chinese translation -> English/Chinese bilingual timed subtitle.
2. Chinese video -> authoritative Chinese transcript/caption -> English translation -> Chinese/English bilingual timed subtitle.

Both lanes emit the same provider-neutral `dore.bilingual-subtitle.v0` artifact contract.

## Capability chain

`Media Source -> Transcript/Caption Admission -> Alignment -> Baseline Translation -> Scripture/Terminology Authority -> Translation Memory -> Doré Judgment -> Bilingual Subtitle Artifact -> Surface Projection`

Mature alignment, local inference and CAT/TM tooling stay behind replaceable adapters. Provider/model identity never becomes canonical translation identity.

## Biblical authority order

1. Recognized Scripture quotation/reference resolves through Scripture authority when confidence is sufficient.
2. Approved biblical/theological terminology takes precedence over free-form machine wording.
3. Verified translation memory may be reused when source/context compatibility passes.
4. Baseline translation remains a candidate, never authority.
5. Doré contextual judgment may revise the candidate.
6. Accepted human revision becomes verified evidence with provenance, not an automatic model fine-tune.

## Bilingual subtitle artifact v0

`dore.bilingual-subtitle.v0` preserves canonical media identity, source pointer, source/target languages, source-authoritative immutable timing boundaries, source text, translated text, status and evidence/provenance. Habakkuk consumes this artifact for burn-in without owning a second translator.

## First real EN -> ZH acceptance: JESUS

Canonical resource: `cinema:video:jesus-film:jesus`.

Source: Jesus Film Project official JESUS resource. Chapter 12, `Sermon on the Mount`, is the first bounded translation training field.

### Source admission

PASS:

- canonical JESUS identity and source pointer are preserved;
- official English transcript remains source authority;
- official Traditional Chinese captions are evaluation/reference only and cannot overwrite source authority;
- no film/audio/caption media is persisted or rehosted;
- CI live-probes the official Arclight playback source.

### Real timing admission

PASS.

The official Arclight player exposes provider WebVTT caption tracks. CI resolves the live player and fetches the English and Traditional Chinese tracks using provider-compatible request context. English WebVTT is the timing/source authority; Traditional Chinese WebVTT remains evaluation-only.

First verified source timing windows from Luke 6:27:

- `34:21.110 -> 34:22.860`
- `34:24.210 -> 34:27.010`

No timestamp is fabricated. The bilingual artifact is generated transiently during acceptance, not stored as a copied third-party caption file.

### Core routing

PASS.

`translation.project` is now a callable Doré Capability Bus route, not registry-only. CI dispatches it through the shared Core bus with `caller_product=cinema`, verifies `dore-core` ownership, provider-neutral routing, source authority, translation non-authority, and immutable timing.

CI evidence now includes:

- `DORE_TRANSLATOR_JESUS_REAL_TIMED_ARTIFACT=PASS`
- `DORE_TRANSLATOR_JESUS_REAL_CUES=2`
- `DORE_TRANSLATION_CAPABILITY_BUS_E2E=PASS`
- `DORE_TRANSLATOR_JESUS_SOURCE_ADMISSION=PASS`
- `DORE_TRANSLATOR_JESUS_TIMING_GATE=REAL_PROVIDER_WEBVTT_PASS`

## First real ZH -> EN acceptance

Use one authorized Chinese Bible/sermon resource under the same artifact contract. Chinese source remains authority and English remains projection.

## Doré training loop

`real media -> source transcript -> candidate translation -> biblical/scripture gates -> accepted/revised pair -> verified memory -> regression case -> next translation`

Cinema is the real-world validation surface; Habakkuk is the production subtitle/burn-in consumer. No automatic model fine-tuning is implied by accepting a translation.

## Hard acceptance

v0 is not complete until both real language lanes demonstrate source text preservation, real timing preservation, schema-valid bilingual artifact, explicit Scripture/terminology/memory provenance, Cinema consumption, Habakkuk consumption, and reusable verified correction evidence without creating a second AI, Scripture authority, media identity or translation database.

The JESUS EN -> ZH source/timing/Core-routing slice is now PASS. The real ZH -> EN lane and Habakkuk artifact-consumer acceptance remain subsequent gates.

## Explicit non-goals

No bulk catalog translation, silent training on third-party media, per-correction auto-fine-tuning, generated replacement of source captions, provider lock-in, media rehosting, or fabricated transcript/timestamps.

## Habakkuk migration

The existing `westsidewatch/Westside-Stories` application is the legacy subtitle/burn-in implementation. Product identity is `哈巴谷 / Habakkuk`; compatibility should be preserved during migration. Repository rename remains a separate GitHub administrative operation until actually performed.

## Next engineering gate

1. Execute the first real authorized ZH -> EN source lane under the same artifact contract.
2. Connect accepted bilingual artifacts to Habakkuk as a consumer without retranslation.
3. Begin verified terminology/memory acceptance from real subtitle corrections.
