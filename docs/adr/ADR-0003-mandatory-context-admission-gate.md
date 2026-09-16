# ADR-0003 — Mandatory Context Admission Gate

Status: accepted

## Problem

Persisting Memory, ADRs, System Atlas, Master Work Register and CURRENT_MAINLINE does not guarantee that a fresh AI session retrieves the correct authority before answering. A retrieval miss can therefore degrade into plausible semantic completion.

## Decision

All registered Doré engineering entities require context admission before engineering facts may be answered.

`User term -> Entity Resolution -> System Atlas -> Current Authority -> Relevant Decisions/Artifacts -> Context Pack -> LLM`

For an exact registered entity hit, authority loading is mandatory. If required authority cannot be retrieved, the gate fails closed with:

`UNKNOWN — authoritative record not retrieved`

The model must not semantically complete the missing engineering fact.

Authority precedence is strict:

`GitHub current canon > accepted recent decision > durable event/decision history > memory summary > model inference`

Lower levels may help discovery but cannot overturn a higher level.

`project.dore.emergence` is the first permanent regression identity. Its aliases include `浮現`, `Emergence`, and `Doré Emergence`; its current checkpoint is `docs/CURRENT_MAINLINE.md` and its canonical path is `Context -> Bible Coordinate -> Canonical Relation -> Resource -> Emergence`.

## Acceptance

A fresh-context regression asks only `浮現` / `Emergence` / `Doré Emergence` / `project.dore.emergence`. It must resolve the permanent identity, load current GitHub authority, report `formally-established`, and expose the current canonical path. Unknown or authority-missing registered entities must not be answered from memory or model inference.

This is not another memory sweep. It turns the existing System Atlas and canonical records into an admission boundary for working memory.
