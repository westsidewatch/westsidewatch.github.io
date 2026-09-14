# Architecture Decision Records

This directory records durable architecture decisions that affect more than one product, capability, or execution surface.

## Authority

- Current system identity and relationships live in `data/system-atlas.v0.json`.
- Current product/site structure lives in its canonical product documentation, including `docs/MASTER_SITE_ARCHITECTURE.md`.
- ADRs explain why durable decisions were made. They do not replace current-state records.
- Pull requests, branches, chat transcripts, workflow logs and experiments are evidence/provenance, not canonical architecture by themselves.

## Lifecycle

`proposed -> accepted -> superseded`

A superseded ADR remains in Git history and points to its successor. It is not silently rewritten into a new decision.

## Index

- `ADR-0001-two-index-authority-model.md` — accepted — Bible Index for content/world coordinates; System Atlas for engineering coordinates; GitHub canonical record is current-truth authority; Doré Memory recalls; A2A executes.
- `ADR-0002-sharded-system-record-registry.md` — accepted — System Record Registry composes bounded shards behind one effective index, with incremental migration from the v0 monolith.

## Rule

Create an ADR only for a durable decision with cross-system consequences. Routine implementation details belong with the product or capability that owns them.
