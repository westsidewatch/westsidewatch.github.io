# ADR-0002 — Sharded System Record Registry

Status: accepted

## Context

System record reconciliation began in a single `data/system-record-families.v0.json`. As more products, evidence sets, historical records, and local indexes were reconciled, every change required editing the same growing file. That recreates the original problem at a higher level: one central record becomes a bottleneck and makes bounded ownership harder to maintain.

## Decision

The System Record Registry becomes composable.

- `data/system-record-families/manifest.v1.json` defines registry composition.
- The existing v0 file remains a readable migration base while families move into bounded shards.
- Small shards own bounded classifications.
- Higher-priority bounded shards may resolve paths previously covered by a broad legacy `unreviewed` family.
- Mirror shards verify migration parity before a family is removed from the base.
- CI resolves the effective registry and rejects orphaned nested records or same-priority state conflicts.

The user and AI still see one effective registry. Sharding is an implementation detail for maintainability, not a second authority.

## Consequences

System Atlas can grow without making every project edit one monolithic registry file. Products can return their records to bounded homes while global discoverability remains unified. Historical provenance remains preserved, and migration can proceed incrementally rather than by a risky all-at-once rewrite.

This decision does not change the authority model from ADR-0001: GitHub canonical records determine current truth; Memory recalls; A2A executes; Bible Index remains the content/world coordinate authority.
