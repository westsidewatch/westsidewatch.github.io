# ADR-0001 — Two-index authority model

Status: accepted

Date: 2026-09-14

## Context

The repository accumulated product documents, branches, PRs, experiments, acceptance tests, A2A records and memory records faster than a stable cross-system index was established. An AI or engineer could find local implementation evidence but still fail to find the current main-site structure or determine which record was authoritative.

At the same time, the product architecture discovered a separate unifying principle: Scripture is the stable content/world coordinate system shared by ONE, Dawn Library, Paradise Cinema, Doré Folio, Search and later Doré Emergence.

These are related indexing problems, but they must not be collapsed into one graph.

The repository already has an active historical/operational reconciliation mechanism: `DORÉ-MASTER-WORK-REGISTER.md` and `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`. System Atlas must make that work discoverable and structurally grounded rather than creating a second competing memory sweep.

## Decision

The system uses two distinct canonical indexes.

1. **Bible Index** — content/world coordinates. Scripture is the stable line through which resources relate to passages, events, people, places, periods and themes. Product resources are projections over these coordinates.
2. **System Atlas** — engineering coordinates. Stable system entity IDs relate products, capabilities, code roots, canonical docs, schemas and dependencies. Branch names, PR numbers, providers and deployments are not system identity.

A separate operational register remains distinct:

3. **Doré Master Work Register** — workstream status, historical reconciliation frontier and durable project obligations. The existing Memory Consolidation Sweep feeds this register. It does not replace System Atlas identities or product canonical docs.

Authority boundaries are fixed:

- **GitHub canonical records** decide current engineering truth.
- **Doré Memory** persists and recalls history/context, but does not promote recalled material into canonical truth by itself.
- **Master Work Register** records operational status and reconciliation results; it is indexed from System Atlas instead of becoming a second architecture map.
- **A2A** executes against canonical identities/contracts, but does not own architectural memory.
- **ADRs** preserve why durable cross-system decisions were made; they do not replace current-state records.

## Consequences

A new cross-system product/capability must have a stable System Atlas identity and canonical path before it is considered architecturally established.

A durable architecture decision that changes authority, ownership, identity, or a cross-system boundary must be recorded as an ADR.

Historical branches, PRs, workflow logs, experiments and conversations remain provenance. The existing Memory Consolidation Sweep is the reconciliation process: its findings should attach to System Atlas entities, update the Master Work Register, promote current truth into canonical product/docs/schema records where appropriate, or mark old evidence superseded. It must not create another independent source of architectural identity.

The Bible Index and System Atlas can reference the same product, but neither substitutes for the other: one answers **where this belongs in the biblical world**, the other answers **where this belongs in the engineered system**. The Master Work Register answers **what is currently happening to it**.

## Return-to-mainline constraint

System Atlas foundation and the first System-Atlas-backed Memory Reconciliation pass are a temporary engineering detour. The product mainline remains Paradise Cinema: complete the Bible-media framework, make Moment/BiblicalAnchor first-class and deep-linkable, then return to Doré Emergence.
