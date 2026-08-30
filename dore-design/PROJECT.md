# Doré Design

Status: ACTIVE PROJECT
Established: 2026-08-30

## Mission

Doré Design is a design environment built specifically for the existing Doré local stack and real Westside Watch / ONE production work. It is not intended to reproduce Figma, Penpot, or any general-purpose design product.

The fixed goal is reliable autonomous design production. Tools and providers are replaceable.

## Target environment

- macOS local workstation
- Doré Local
- local Ollama models
- GitHub coordination and durable evidence
- MCP / CLI / native local automation
- zero incremental paid dependency
- human-visible, editable design output

## Core acceptance contract

A design workflow is not considered working until all of the following are true:

1. Doré can start and complete the work without the user acting as a terminal operator.
2. The user can see the actual rendered design.
3. The result remains structurally editable, not merely a flattened AI image.
4. Doré can inspect and modify the same document in later iterations.
5. Doré can export/render and visually verify its own result.
6. Repeated operations are stable and do not depend on metered paid AI/API quotas.
7. Failures produce machine-readable evidence and trigger bounded self-diagnosis/retry where safe.

## Architecture principle

Doré Design is machine-operable first and human-editable simultaneously:

Doré -> native design API / MCP / CLI -> document model -> canvas/render -> visual verifier

The human opens the same design document and sees/edit the real structure Doré is operating on.

No single provider is the architecture. Penpot, OpenPencil, Framesmith, Doop, Tela, or future projects are candidate engines/components behind adapters.

## Phase 0 — Open-source bake-off

Use one identical real production brief: Westside Watch homepage.

Candidates initially include:

- Penpot
- OpenPencil
- Framesmith
- Doop
- Tela

Each candidate must be evaluated for:

- autonomous local installation/operation
- machine control surface (MCP/CLI/API/RPC)
- editable document/scene structure
- visible render/export
- iterative mutation of an existing design
- local/macOS fit
- stability under repeated operations
- zero incremental paid dependency
- license/provenance and safe reuse
- useful components even if the candidate is not selected as the base engine

Passing an API smoke test is insufficient. A candidate must produce an actual Westside Watch design that the user can see.

## Selection strategy

Find the simplest stable base engine first. Then selectively reuse or adapt the best compatible components from other open-source candidates rather than rebuilding mature capabilities unnecessarily.

For every upstream component record:

- repository/source
- exact upstream revision/version
- license
- architecture role
- test evidence
- adoption level
- whether used as dependency, adapter, isolated service, inspiration, or incorporated code

License compatibility is a design constraint from the beginning, not a cleanup task at the end.

## Engineering rules

- Goal fixed; tools replaceable.
- Repair a provider only while repair cost is lower than switching or bypassing it.
- Prefer proven open-source components over rebuilding.
- Keep provider adapters replaceable.
- Never treat visual-verifier judgment as proof that a mutation occurred; structural evidence is required.
- Prefer small validated mutations over one-shot page generation.
- A failed provider must not block exploration of another provider.
- Local evidence Doré can obtain itself must not be delegated to the user.
- Human intervention is reserved for genuine login/authorization, unavoidable GUI-only actions, or high-risk/irreversible decisions.

## First milestone — Doré Design 0.1

Doré autonomously produces a complete first-pass Westside Watch homepage through at least one open-source design engine, exposes a human-visible editable result, performs a second autonomous revision on the same document, exports a render, verifies it, and repeats a representative operation suite reliably without paid API dependency.

## Long-term direction

Doré Design may eventually own its agent control layer, provider adapters, design document abstractions, visual verification, import/export, version history, and environment-specific workflows while continuing to reuse suitable open-source canvas/rendering engines.

The project succeeds by delivering stable real design work in the Doré environment, not by maximizing feature count or matching incumbent design software.