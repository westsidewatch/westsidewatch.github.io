# 聖光影院 / Holy Light Cinema — Phase I

Status: ACTIVE
Parent surface: 橄欖山資源版塊
Core: shared Doré Core

## Product boundary

聖光影院是橄欖山資源版塊的獨立內容，不隸屬黎明書局。它與黎明書局共享所有可共用技術與同一個多雷核心；不建立第二套 AI、搜索、人物、經文、資源身份或來源政策。

聖光影院只增加時間影音媒介所需的能力：canonical video identity、provider probing、Video Reflex、timeline、VideoMoment、Cinema Projection 與 provider-aware playback/handoff。

## Phase I invariant

Source remains authoritative. Canonical identity remains stable. Reflex remains ephemeral. Provider-specific details stay behind adapters. Cinema stores knowledge about external video resources; it does not silently copy or re-host third-party media.

## First real-source acceptance set

1. Jesus Film Project
2. David Pawson on YouTube
3. GOOD TV on YouTube
4. GOOD TV first-party web video

These four sources must exercise embeddable playback, YouTube playback, teaching-series identity, first-party web resources, and graceful official-source handoff when embedding is unavailable or not permitted.

## Phase I execution chain

URL
→ Source Admission
→ Provider Probe
→ Canonical Video Resource
→ Video Reflex
→ transcript / scene / timeline
→ VideoMoment
→ Doré Search
→ Cinema Projection
→ precise playback or official-source handoff

## Canonical Video Resource v0

A canonical video resource must be provider-neutral and preserve at minimum:

- canonicalId
- title
- creator / speaker
- series / work relationship when known
- canonical source pointer
- provider sources
- language
- duration when available
- rights / access state
- embed capability
- provenance

Multiple provider URLs for the same teaching, sermon, film, or episode must not automatically become separate canonical works.

## VideoMoment v0

A VideoMoment is a time-bound projection over a canonical video resource, not a second video identity. It preserves:

- canonical video identity
- source pointer
- start time
- optional end time
- transcript span or semantic label
- provenance
- confidence where inference is involved

Persisted editorial annotations may exist later; transient Video Reflex events must not become a shadow database.

## First hard acceptance

A real query must resolve to a meaningful moment inside a real accepted video resource. Selecting that result must open Holy Light Cinema and either:

1. begin playback at the correct time through an allowed provider integration; or
2. degrade to an official-source handoff when inline playback is unavailable or not permitted.

Canonical identity must remain unchanged across both paths.

## Non-goals for Phase I

- no bulk ingestion
- no copied third-party video archive
- no independent Cinema AI
- no second search engine
- no Cinema-only scripture/person graph
- no premature poster-wall UI
- no claim of universal provider support before real-source acceptance
