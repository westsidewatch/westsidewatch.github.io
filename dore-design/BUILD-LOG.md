# Doré Design — Construction / Teaching Log

Status: WORKING PRODUCT FOUNDATION — MAC + CI ACCEPTED

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

A stale Westside structural label was discovered in the previously persisted local workspace. The design engine removes the obsolete legacy structural node during migration instead of reintroducing old editorial structure from memory.

Teaching point: current product state is authoritative. Historical design memory can explain lineage but must not silently regenerate superseded structures.

## Build 008 — Complete workspace loop

Implemented durable `dore.design.workspace.v1` multi-page documents, shared design tokens, page CRUD, node CRUD, canvas dimensions, text/rule creation, Inspector editing, keyboard deletion, history/Undo, per-page deterministic SVG render/export, browser verification, Doré CLI, resident HTTP API and safe legacy-structure migration.

GitHub Actions run `33379449502` completed SUCCESS. Stronger same-artifact acceptance run `33379655465` also completed SUCCESS.

Physical Mac task `dd-product-019` then completed successfully: the resident 0.8 service installed, `DORE_DESIGN_LOCAL_ACCEPTANCE_PASS` returned, the same workspace was mutated and rerendered, machine verification passed, cleanup passed, and obsolete legacy structure was absent.

## Build 009 — Human direct manipulation + product closure

The product entry point is `app_product.py`; the macOS resident installer launches it at `127.0.0.1:4310`.

Added direct canvas pointer dragging. Moving a visible layer writes its new coordinates into the same structured workspace used by Doré. Human editing and Doré editing therefore operate on the same artifact rather than on separate representations.

The 0.9 acceptance gate includes legacy regressions, workspace lifecycle, page/layer CRUD, human deletion, Doré CLI read/write/export/verify, history/undo, resident HTTP execution, same-artifact mutation -> SVG rerender -> machine verification -> cleanup, and the direct-manipulation product entry point.

GitHub Actions run `33379900466`: SUCCESS.

Physical Mac task `dd-product-020`: SUCCESS.

Resident health returned:

`version=0.9`, `workspace=multi-page`, `direct_manipulation=true`.

Live resident acceptance returned:

`DORE_DESIGN_LOCAL_ACCEPTANCE_PASS`, `page_count=3`, `revision=15`, `same_artifact_mutation=true`, `resident_render=true`, `resident_verify=true`, `cleanup=true`.

Final workspace verification returned PASS for schema validity, multi-page structure, unique page IDs, node structure, rendering of all pages, history availability and obsolete-structure removal.

`Doré Design 0.9 working product foundation: PASS`

## Build 010 — Real ChatGPT → Doré → local execution chain

Real Westside Watch design work established the first end-to-end human/agent/local execution chain:

`Human -> ChatGPT -> GitHub coordination-inbox -> resident Doré coordination daemon -> Doré worker -> local repository / Doré Design / localhost -> execution + verification -> Doré outbox -> GitHub -> ChatGPT -> Human`.

This is no longer only an architectural plan. Both directions have executed in real work. ChatGPT has written bounded `local_exec` tasks into the repository coordination inbox; the Mac-resident Doré daemon has synchronized the repository, drained those tasks, executed them against the local Doré Design installation, and generated durable result messages back into `local/dore-local/coordination-outbox`.

The resident worker owns execution semantics. `coordination_worker.py` consumes unprocessed messages, preserves the active parent goal, executes allow-listed local commands, records attempts, and calls `reply()` with success or failure evidence. `coordination_mailbox.py` persists Doré-to-ChatGPT messages and publishes them to GitHub using an isolated git worktree with retry and remote-exact checks. `dore_coordination_daemon.py` continuously synchronizes `origin/main` and drains the worker.

The chain has also demonstrated failure evidence rather than only success evidence. Doré Design 1.7.1 deployment returned a real local result showing the resident service version, editable Journal workspace page, node count, runtime-mirror retirement, asset fallback status, acceptance checks, retries, and terminal failure state. This confirms that the transport can carry execution results back even when the product task itself fails.

Current maturity classification: **RUNNING, BIDIRECTIONAL, NOT YET HARDENED**.

Known hardening work remains: deterministic task/result correlation, one canonical receipt per task, clearer separation between transport success and product acceptance, stale-result suppression, improved failure classification, and a visible health/status surface for inbox → execution → outbox delivery.

Teaching point: GitHub is currently the durable bridge because ChatGPT cannot directly enter the Mac. Doré is the execution agent on the other side of that bridge. If Doré Design later becomes an online service, Doré's role should remain; only the transport changes from Git-backed local coordination toward a direct Doré API/message bus. GitHub should then return to its primary roles of source control, review, provenance and deployment evidence.

## Product boundary after acceptance

Doré Design is now the working local structured design environment. It is no longer a one-page demo or an upstream-provider experiment.

The next Westside Watch work is real design production performed inside Doré Design. New editing features may be added when real work exposes a concrete need, but they are product evolution rather than a prerequisite for declaring the working foundation complete.
