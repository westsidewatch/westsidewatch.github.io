# DORÉ COORDINATION TRANSPORT — EVIDENCE LEDGER

Date: 2026-08-30
Sweep: DORÉ Memory Consolidation Sweep 01
Current classification: `CORE/CONTINUOUS` shared execution/coordination infrastructure; bounded implementation milestone is real, full trust/authority hardening is not verified.

## Bounded evidence reviewed

- `.github/workflows/dore-coordination-transport.yml`
- `local/dore-local/coordination_mailbox.py`
- `local/dore-local/coordination_worker.py`
- `local/dore-local/test_coordination_transport.py`
- current `local/dore-local/coordination-inbox/` and `coordination-outbox/` repository surfaces
- recent `dore: publish coordination message ...` commits on `main`

## What is actually implemented

1. A durable JSONL mailbox exists under the local Doré home with separate inbox, outbox, receipt and delivery ledgers.
2. Doré→ChatGPT messages are rendered to one-message-per-file repository outbox artifacts and published with isolated path-only git commits, explicitly avoiding unrelated staged/unstaged autonomous work.
3. Delivery is idempotence-aware: already published message IDs are not retried, and an exact already-remote file is treated as successful prior delivery.
4. ChatGPT→Doré repository inbox messages are drained by a resident coordination worker with persisted processed IDs, attempts, active-message state and failure diagnostics.
5. The worker dispatches bounded task kinds including complete recall, read-only and mutating Penpot work, Penpot AI-kit adoption/reprovisioning, export probes and an allowlisted local-exec path.
6. The offline transport contract verifies duplicate inbound suppression, durable outbound retention on failed publish attempts, retry behavior and suppression of retries after a recorded successful delivery.
7. The GitHub workflow compiles the mailbox/worker/test modules and executes the offline transport contract on relevant changes.
8. Current repository history contains repeated `dore: publish coordination message ...` commits and a populated coordination outbox, which is direct production evidence that the outbound git-backed publication path is operating, not merely specified.

## Evidence boundary

The bounded evidence does **not** justify declaring the whole coordination system `VERIFIED_COMPLETE`:

- the offline test covers mailbox transport behavior, not every worker dispatch kind;
- this pass did not establish a persisted CI run result for the workflow itself;
- local worker state and every inbox→dispatch→reply cycle were not independently replayed in this sweep;
- there is no cryptographic/authenticated envelope proven at the repository inbox boundary.

## Authority / security finding

`coordination_worker.py` authorizes `local_exec` primarily by checking `msg.sender == "chatgpt"`, while repository inbox JSON is itself the transport surface. The executable is constrained by an allowlist and cwd roots, which is materially safer than arbitrary shell execution, but a sender string is not a strong origin proof. The current contract therefore has an authority-boundary debt: repository write access and message-origin trust are effectively coupled.

This does not block current Sweep 01 progress and does not justify disabling the transport, but it should be reconciled under `NERVOUS-SYSTEM` authority work. A future hardening milestone should define one authenticated envelope or equivalent origin-verification mechanism, preserve replay/idempotence protection, and add negative tests proving forged/unauthorized inbox messages cannot reach `local_exec` or mutating Penpot dispatches.

## Retrospective evaluation

- **Original objective:** create free, durable, asynchronous Doré↔ChatGPT coordination that survives ordinary session boundaries and does not let unrelated repository state block communication.
- **Completion evidence:** implementation files, offline contract test, workflow contract, live repository outbox population and repeated coordination publication commits.
- **Current quality:** useful and operationally proven for outbound transport; worker architecture is pragmatic and bounded, but authority verification is not yet strong enough to call the execution plane fully hardened.
- **What was learned:** durable coordination benefits from isolated transport commits, explicit receipts/delivery state, idempotent message IDs, persisted worker state and bounded dispatch contracts.
- **Weakness / debt:** sender-string trust at a repo-backed execution boundary; incomplete negative authorization testing; incomplete end-to-end evidence for every dispatch family.
- **Revisit trigger:** before broadening local execution privileges, adding new mutating dispatch kinds, exposing coordination beyond the current trusted repo context, or claiming Nervous-System authority enforcement.
- **Current disposition:** retain and maintain as `CORE/CONTINUOUS`; add authority hardening to the Nervous-System evidence queue rather than reopening the transport as a separate product.

## Sweep classification

- Coordination transport foundation: `CORE/CONTINUOUS`
- Bounded outbound durable-delivery milestone: `VERIFIED_COMPLETE` as a sub-milestone only
- Full bidirectional execution-plane hardening: `ACTIVE / UNKNOWN_NEEDS_EVIDENCE`
- Retirement/supersession: none
- P01 impact: none; no P01 state or action changed in this batch
