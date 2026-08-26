# PENPOT-BRIDGE-01 — Doré ↔ Penpot MCP

Status: ACTIVE_PARALLEL / IMPLEMENTING
Established: 2026-08-26
Owner: Westside Watch
Executor / learner: Doré
Priority: subordinate to CONV-MEM-V1 / Full Conversation Memory P0

## Purpose

Make Doré the operating bridge between the human editorial/design conversation and Penpot, so the design loop becomes:

`human intent → Doré judgment → Penpot MCP action → canvas evidence → Doré verification → VIS-LEARN / memory`

The user must not become a manual drawing executor for Doré.

## Governing constraints

1. **Full Conversation Memory remains P0.** This project may proceed in parallel but must not displace CONV-MEM-V1 completion work.
2. **Free-first.** Penpot is selected because the core design workflow can remain free/open. No paid dependency may become a prerequisite without an explicit later decision.
3. **Secret isolation.** Penpot MCP keys/tokens never enter Git, logs, screenshots, generated design docs, or user-visible responses.
4. **Remote MCP for Doré Runtime.** Doré's deployed/runtime bridge uses Penpot Remote MCP, because a cloud/runtime agent cannot reach a user's `localhost` Local MCP endpoint.
5. **Local MCP remains optional tooling.** Local MCP can be used for local development or debugging, but it is not the canonical Doré bridge.
6. **Read before write.** First prove authenticated MCP initialization and tool discovery; then inspect the focused file/page; only then enable bounded write operations.
7. **Evidence before autonomy claims.** Doré is not considered connected merely because a key exists. PASS requires real MCP tool readback from the intended Penpot file.
8. **VIS-LEARN.** Every human correction to Doré's design work must be captured as a transferable rule/hypothesis and tested again.

## Security model

Runtime secret name:

`PENPOT_MCP_KEY`

It must be configured only in the deployment/runtime secret store.

Remote endpoint template:

`https://design.penpot.app/mcp/stream?userToken=<secret>`

The bridge must never return or log the resolved URL because it contains the secret.

## Phase 1 — connection probe

Create a private/guarded Doré endpoint that:

1. verifies `PENPOT_MCP_KEY` is bound;
2. sends MCP `initialize` to Penpot Remote MCP;
3. sends `notifications/initialized` when required;
4. requests `tools/list`;
5. returns only sanitized capability metadata (tool names/descriptions/count), never tokens or raw auth URLs.

### PASS gate

- deployed runtime has the Penpot secret binding;
- MCP initialize succeeds against Penpot Remote MCP;
- `tools/list` returns Penpot capabilities;
- no key appears in response/log/source;
- failure states distinguish missing secret, auth failure, transport/protocol failure, and Penpot-side disabled/disconnected state.

## Phase 2 — focused-file read

With `Westside Watch — Design System 1.0` open and Penpot MCP connected, Doré must:

- list pages;
- identify the focused page;
- inspect existing layers/components/tokens;
- report what it actually sees with MCP evidence.

No design writes occur before this read gate passes.

## Phase 3 — first bounded write

First visual act:

> Create one Living Paper frame in the focused Penpot file, then read it back and verify its dimensions, naming and fill.

This is `PENPOT-BRIDGE-01`'s first write PASS. It is intentionally small: the goal is to prove the bridge and learning loop, not to design the homepage.

## Subsequent ladder

`BRIDGE-01 connection/read/write proof`
→ `BRIDGE-02 design tokens`
→ `BRIDGE-03 Visual DNA (光·線·紙·刻·築)`
→ `BRIDGE-04 Westside Doré Website Asset Pack v0.1`
→ `BRIDGE-05 Editorial Grammar (磚·垛·流)`
→ `BRIDGE-06 Living Editorial Wall`
→ `BRIDGE-07 complete Westside website system`

## Visual constitutional inheritance

Penpot does not redefine Westside. It executes the already established system:

- Living Paper carries.
- Ink Black prints/forms.
- Midnight Blue watches only when the scene is truly night.
- First Light Gold highlights/traces; it is not a large background field.
- Visual DNA: `Light / Line / Paper / Engraving / Architecture`.
- Website Editorial Grammar: `Brick / Battlement / Flow`.
- `5:8` is the highest editorial container.
- Inherit the grammar, not the material.
- Journal can change the weather, not the city.
- Free Foundation — The Gate Stays Open.

## Current human action already completed

- Penpot account MCP Server enabled.
- MCP key generated.
- Key stored locally in macOS Keychain as `dore-penpot-mcp` without exposing it in chat/Git.
- A Penpot file named `Westside Watch — Design System 1.0` exists.

## Next executable action

Implement and deploy the sanitized Remote MCP connection probe, then provision `PENPOT_MCP_KEY` into the Doré deployment secret store and run the real initialize/tools-list verification.
