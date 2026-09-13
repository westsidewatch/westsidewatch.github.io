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

1. English video -> authoritative English transcript -> Traditional Chinese translation -> English/Chinese bilingual timed subtitle.
2. Chinese video -> authoritative Chinese transcript -> English translation -> Chinese/English bilingual timed subtitle.

Both lanes emit the same provider-neutral bilingual subtitle artifact contract.

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

### Source admission result

PASS at the source-admission layer:

- canonical JESUS identity and source pointer are preserved;
- official English transcript page is recorded as source authority evidence;
- an official-page verified transcript sentinel is recorded without copying the full provider transcript into the repository;
- the provider Traditional Chinese subtitle surface is recorded only as an evaluation/reference projection and cannot overwrite source authority;
- no film/audio/subtitle media is rehosted;
- GitHub CI live-probes the official Jesus Film Project Arclight playback endpoint to verify provider liveness.

The provider transcript webpage returns HTTP 403 to GitHub Actions direct fetches. This is treated as a provider access boundary, not as missing source evidence. CI therefore separates two facts: transcript evidence is an official-page verified snapshot; runtime liveness is verified independently against the official Arclight embed endpoint.

### Timing gate

`timingStatus: not-admitted`
`subtitleReady: false`

No cue timestamp has been invented. The next EN -> ZH gate is to admit a real provider caption timing track or run an authorized alignment adapter over accessible source audio/captions. Only then can the first real timed bilingual subtitle artifact be declared PASS.

## First real ZH -> EN acceptance

Use one authorized Chinese Bible/sermon resource under the same artifact contract. Chinese source remains authority and English remains projection.

## Doré training loop

`real media -> source transcript -> candidate translation -> biblical/scripture gates -> accepted/revised pair -> verified memory -> regression case -> next translation`

Cinema is the real-world validation surface; Habakkuk is the production subtitle/burn-in consumer. No automatic model fine-tuning is implied by accepting a translation.

## Hard acceptance

v0 is not complete until both real language lanes demonstrate source text preservation, real timing preservation, schema-valid bilingual artifact, explicit Scripture/terminology/memory provenance, Cinema consumption, Habakkuk consumption, and reusable verified correction evidence without creating a second AI, Scripture authority, media identity or translation database.

## Explicit non-goals

No bulk catalog translation, silent training on third-party media, per-correction auto-fine-tuning, generated replacement of source captions, provider lock-in, media rehosting, or fabricated transcript/timestamps.

## Habakkuk migration

The existing `westsidewatch/Westside-Stories` application is the legacy subtitle/burn-in implementation. Product identity is `哈巴谷 / Habakkuk`; compatibility should be preserved during migration. Repository rename remains a separate GitHub administrative operation until actually performed.

## Next engineering gate

1. Make `translation.project` callable through the canonical Capability Bus, not registry-only.
2. Resolve/admit real JESUS caption timings or an authorized alignment path.
3. Generate the first real JESUS EN -> ZH timed bilingual artifact.
4. Then execute the authorized ZH -> EN lane.
