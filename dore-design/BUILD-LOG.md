# Doré Design — Construction / Teaching Log

Status: MULTI-PAGE PRODUCT ACCEPTED IN CI / MAC 0.8 ACTIVATION EVIDENCE PENDING

Doré observes this log while ChatGPT owns the mainline engineering.

## Build 001 — Own the minimum working spine

Decision: stop making provider success a prerequisite for Doré Design. Build a tiny self-owned spine first, then reuse upstream components behind it.

Implemented: `structured document JSON -> mutation API -> browser canvas`.

Teaching point: a design tool is not an image generator. The durable object is the structured document. Canvas is a view; mutation changes the object; render makes it visible.

## Build 002 — Make the document durable and operable

Added revision snapshots, stable node CRUD, token edits, explicit canvas dimensions and deterministic SVG export.

Teaching point: editing must preserve identity. A changed node remains the same node in the same document; revision advances and prior state remains recoverable.

## Build 005 — Working self-owned core

Implemented schema validation, atomic persistence, history/restore, node CRUD, tokens, deterministic SVG, machine verifier, browser workbench, HTTP API, CLI and macOS LaunchAgent service mode.

GitHub Actions run `33358200400` completed SUCCESS on the 0.5 core. This established the first complete single-document behavior contract.

## Build 006–007 — Replace the one-page limitation

The one-canvas document was not accepted as the product. Doré Design was moved to a workspace model with pages/artboards and a page-aware machine control surface.

Human controls added: page selection, page add/rename/duplicate/delete, layer selection, text creation, layer duplicate/delete, keyboard Delete/Backspace. Doré received matching CLI controls over the same workspace.

A stale Westside structural label was discovered in the previously persisted local workspace. The design engine now removes the obsolete legacy structural node during migration instead of reintroducing old editorial structure from memory.

Teaching point: current product state is authoritative. Historical design memory can explain lineage but must not silently regenerate superseded structures.

## Build 008 — Complete usable workspace loop

The production entry point is now `app_workspace.py` and the resident installer launches that engine.

Implemented product surface:

- durable `dore.design.workspace.v1` multi-page document;
- shared design tokens;
- page CRUD and canvas dimensions;
- node create/edit/duplicate/delete;
- text and rule creation;
- browser Inspector plus keyboard delete;
- history snapshots and Undo / Cmd-or-Ctrl-Z;
- per-page deterministic SVG render/export;
- machine verification of every page with per-page SHA-256;
- browser Verify surface;
- Doré CLI over the same workspace;
- resident HTTP API over the same workspace;
- safe legacy-structure migration;
- dedicated live acceptance probe that mutates the resident artifact, confirms SVG rerender, runs verifier, then removes its probe.

### Behavioral acceptance

GitHub Actions run `33379449502` completed SUCCESS after the workspace CI syntax was repaired.

A stronger same-artifact acceptance was then added. GitHub Actions run `33379655465` completed SUCCESS on commit `5d968a6769fab6fdceaf207a16d1fea8f640128a`.

That gate exercises:

- legacy regression tests;
- workspace schema and lifecycle;
- multi-page CRUD;
- human-equivalent layer deletion;
- Doré CLI read/write/verify/export;
- history and undo;
- resident HTTP service;
- live mutation of the same resident artifact;
- rerender into SVG after mutation;
- machine verification after mutation;
- cleanup of the temporary acceptance node;
- macOS installer contract pointing at the 0.8 workspace engine.

`Doré Design 0.8 behavior contract: PASS`

### Physical Mac activation

The source and behavior contract are accepted. A consolidated local task `dd-product-019` has been issued to the resident Doré execution path. It installs the accepted workspace engine, runs `local_acceptance.py` against `127.0.0.1:4310`, and then runs the workspace verifier.

Do not mark physical activation PASS until the Mac returns `DORE_DESIGN_LOCAL_ACCEPTANCE_PASS` (or equivalent direct runtime evidence). Cloud CI proves the program; local evidence proves the running Mac instance.

## Product boundary

Doré Design is now a usable structured multi-page design workspace rather than a one-page demo. Further visual production for Westside Watch is work performed *in* Doré Design; it is not a reason to restart provider discovery or rebuild the product foundation.
