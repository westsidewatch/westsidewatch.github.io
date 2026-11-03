# Westside Watch — coding agent entrypoint

Read in this order before modifying the main site or a tool:

1. `ENGINEERING-GOVERNANCE.md` — non-negotiable repository engineering cadence, protected assets, release authorization.
2. `docs/MASTER_SITE_ARCHITECTURE.md` — canonical project and route architecture.
3. `docs/design/WESTSIDE-DESIGN-OS.md` — the ONE visual authority.
4. `docs/design/WESTSIDE-EDITORIAL-MANUAL.md` — the Design OS editorial/art-direction chapter.
5. `docs/design/WESTSIDE-EGM-INTEGRATION.md` — how to use Google's upstream Elephant–Goldfish method **under** Design OS.

EGM artifact directory: .dev/egm

The complete pinned upstream source is linked at `.tools/elephant-goldfish-model/`
(Git submodule; initialize with `bash scripts/egm-setup.sh --prepare`).
Codex users can activate the upstream plugin with `bash scripts/egm-setup.sh --install-codex`.
**Do not mistake presence of the source for an installed/active plugin.**
Read and invoke the upstream skills and reviewer personas from the complete plugin;
do not copy a partial skill, invent a local EGM replacement or fake an independent Goldfish.

For nontrivial architecture, visuals or motion: Elephant writes the scoped spec from
real code/assets and existing decisions. Goldfish must review in a **fresh, isolated
subagent context** with only the spec and references; if the harness cannot spawn
fresh subagents, report `EGM REVIEW NOT RUN` and do not claim approval.
Review feedback goes into artifacts, not long chat dumps. The editor approves
actual browser screenshots; automated tests and agent reviews do not grant art signoff.

Maintain exactly one Design OS. Local styling stays scoped; no global palette,
font authority, new CSS runtime, new EGM CI workflow or independently managed
visual policy. Do not touch the protected right-side magazine cover when editing
its left folio, nor any Olive speaker/Church approved asset without authorization.

Keep related changes in one coherent commit and PR, run the existing checks,
fix relevant failures, and never merge an unapproved art trial or bypass CI.
