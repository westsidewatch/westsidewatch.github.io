# Doré Design — Construction / Teaching Log

Status: CORE ACCEPTED / MAC ACTIVATION PENDING

Doré observes this log while ChatGPT owns the mainline engineering.

## Build 001 — Own the minimum working spine

Decision: stop making provider success a prerequisite for Doré Design. Build a tiny self-owned spine first, then reuse upstream components behind it.

Implemented: `structured document JSON -> mutation API -> browser canvas`.

Teaching point: a design tool is not an image generator. The durable object is the structured document. Canvas is a view; mutation changes the object; render makes it visible.

## Build 002 — Make the document durable and operable

Added revision snapshots, stable node CRUD, token edits, explicit canvas dimensions and deterministic SVG export.

Teaching point: editing must preserve identity. A changed `hero` remains the same node in the same document; revision advances and prior state remains recoverable.

## Build 005 — Working self-owned Doré Design core

ChatGPT expanded the project from a demo spine into a usable local-first design workbench rather than continuing provider bake-offs.

Implemented product surface:

- schema validation and stable document/node identity;
- atomic persistence;
- revision history and restore/undo;
- node set/add/delete and bounded batch mutation;
- design-token editing;
- deterministic SVG renderer/export;
- machine verifier with render SHA-256;
- human browser workbench with Layers, live Canvas, Inspector, token editor, Undo, Verify and SVG Export;
- HTTP API and health endpoint;
- machine-native CLI for Doré;
- macOS LaunchAgent installer for resident service mode.

Human and Doré now have two control surfaces over the same durable document: browser workbench for the human, CLI/HTTP for Doré. Neither control surface owns the document; both mutate the same structured state.

### Behavioral acceptance

GitHub Actions run `33358200400` completed SUCCESS on commit `13cd877f318927dd290654f03ea50de146e4bf12`.

The acceptance run passed all of these independent gates:

- syntax + deterministic engine lifecycle;
- live HTTP service/workbench integration;
- same-document mutation and revision advance;
- batch mutation;
- SVG render/export;
- machine verification;
- machine CLI control surface;
- macOS installer shell contract;
- final acceptance gate.

A prior live-integration failure was traced to the test expecting ASCII `DORE` while the product correctly rendered the branded `DORÉ`; the test was corrected and the complete acceptance then passed. Teaching point: test failure is evidence about a contract, not automatically evidence that the product implementation is broken. Inspect the failed assertion before changing architecture.

### Current boundary

The product core is accepted. The remaining step is physical activation on the user's Mac: pull the accepted repository state, install/start the LaunchAgent, then verify the actual resident endpoint at `127.0.0.1:4310` on that machine.

This cannot currently be claimed complete because the existing repository coordination inbox is not being consumed by the Mac. The latest Mac-authored coordination-outbox commit remains from 03:03Z, while newer installation/acceptance envelopes remain without returned evidence. GitHub heartbeat workflows run on GitHub-hosted Linux runners and therefore cannot start a process on the Mac.

Teaching point for Doré: cloud CI proves the program contract; it does not prove deployment on a different physical machine. Never convert `CI PASS` into `installed locally` without local runtime evidence.

## Acceptance state

`Doré Design core: PASS`

`Doré Design resident on user's Mac: UNVERIFIED — local execution transport unavailable`

Do not reopen provider discovery because of this deployment boundary. The engineering product exists; repair the Mac execution/control-plane path, activate the resident service, obtain local health + document + mutation + render evidence, then merge the Westside visual sidecar into this workbench.
