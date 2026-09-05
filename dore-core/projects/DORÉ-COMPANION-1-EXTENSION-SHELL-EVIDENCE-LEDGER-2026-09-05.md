# DORÉ COMPANION 1.0 EXTENSION SHELL EVIDENCE LEDGER — 2026-09-05

Status: BOUNDED_RECONCILIATION_COMPLETE
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register extension: `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-SPARSE-CAPABILITY-RUNTIME-2026-09-05.md`
P01 impact: NONE

## Bounded evidence reviewed

- commit `2e2db37df4b30ad6b2ae5be499c54c8da34e5885` — `DORÉ A2A: rebuild Firefox Companion 1.0`;
- `local/dore-companion-extension/manifest.json`;
- `local/dore-companion-extension/background.js`;
- `local/dore-companion-extension/content_script.js`;
- Companion Native transport contract tests extended by the same commit;
- GitHub combined-status and commit-associated workflow-run receipt surfaces for the introducing head;
- prior Companion Native Messaging and A2A/control-plane reconciliation ledgers.

## Current classification

### Companion 1.0 Firefox extension shell
`ACTIVE_PARALLEL / VERIFIED_COMPLETE_SUBMILESTONE`

A coherent browser-side product shell now exists in repository implementation. It is no longer only a transport primitive: the extension has an installable Firefox manifest, ChatGPT command capture for `/dore`, background routing into the existing native-first transport, health probing, and an in-page live status badge/result event surface.

### Live Companion 1.0 acceptance
`ACTIVE / UNKNOWN_NEEDS_EVIDENCE`

No persisted GitHub status object or workflow run is available for the introducing head, and this bounded sweep did not find live Firefox installation or Mac Native Messaging acceptance evidence. Repository implementation must therefore not be promoted into production/browser acceptance.

## Evidence boundary

1. The manifest pins Firefox identity/version, requests Native Messaging permission, loads the new background bridge and injects the ChatGPT content script on `chatgpt.com` / `chat.openai.com`.
2. The content script detects `/dore` commands on Enter and send/submit interactions, avoids blocking the normal ChatGPT event, de-duplicates near-identical commands, polls health, and surfaces `CHECKING/ONLINE/WORKING/PASS/OFFLINE` state through a fixed badge.
3. The background bridge converts the command into protocol `dore.a2a/1`, identifies the Companion 1.0 client and delegates dispatch to the already-established native transport module rather than introducing another orchestration path.
4. The extended contract suite checks installable-manifest identity, native-first transport ordering, background routing, `/dore` command capture, health signaling and result-event presence.
5. These are implementation/contract facts only. They do not prove ChatGPT DOM stability across UI variants, actual extension installation, native-host registration, end-to-end request/result identity, unauthorized mutation refusal, or sustained resident reliability.
6. No P01 subtitle/runtime/deployment/binding/audio-transcription state was changed.

## Current quality judgment

This closes a real usability gap between lower-level transport work and an actual browser Companion shell. The direction is consistent with one persistent Doré intelligence: ChatGPT remains the user interaction surface, while `/dore` commands are handed to the local typed control plane through the established Native Messaging path.

The main debt is acceptance evidence. The content script currently depends on generic ChatGPT textarea/contenteditable/send-button heuristics. That is an appropriate first shell, but it must earn a live-browser PASS before being treated as stable product integration. The fixed in-page status badge is also a first operational surface, not necessarily the final UX.

## Durable learned principles

- Transport completion is not product-shell completion; a usable browser surface must bind command capture, status, health and result delivery together.
- Browser DOM integration should remain narrow and non-blocking: Companion must not interfere with normal ChatGPT sending when it is not handling a `/dore` command.
- Companion should reuse the existing typed/native routing seam rather than create another local agent or server.
- An installable manifest and contract tests are not substitutes for live browser/native-host acceptance.
- Status UX is operational evidence support; it should expose real transport state rather than imply success from command capture alone.

## Revisit / supersession judgment

- Earlier transport-only Companion state is superseded as the current product-shell description by Companion 1.0, while its Native Messaging implementation remains a dependency and historical provenance.
- `localhost:4312` remains compatibility/debug fallback, not production-primary transport.
- The present fixed ChatGPT status badge is `COMPLETED_REVISIT_CANDIDATE` UX debt once end-to-end function is proven; do not redesign it before acceptance evidence exists.

## Smallest next proof

Persist one acceptance packet proving:

1. capability-runtime/Companion CI PASS at a head containing Companion 1.0;
2. Firefox installs the extension with the expected extension ID;
3. Companion health reaches the registered Native Messaging host on Mac;
4. one real ChatGPT `/dore` command passes content script → background → native transport → host → mature adapter/control plane and returns a result/status event;
5. the same extension leaves ordinary non-`/dore` ChatGPT sends untouched;
6. one unauthorized mutation request is refused at the authority boundary.

Do not infer whole-system A2A or Companion completion from this packet; it closes only the Companion 1.0 browser/native acceptance boundary.

## Receipt check — 2026-09-05

For head `2e2db37df4b30ad6b2ae5be499c54c8da34e5885`:

- combined commit statuses: no status objects returned;
- commit-associated workflow runs: no workflow runs returned.

This is missing persisted acceptance evidence, not a failing result. No blocker and no human action are created by this sweep finding.

## P01 isolation

P01 remains unchanged and must not be interrupted or replaced by Companion work.
