# Westside Design OS — EGM integration protocol

**Status:** integrated engineering method under the existing Westside Design OS.
**Not:** a second Design OS, a new source of visual tokens, a replacement art
director, or a new CI pipeline.

## 1. Origin, source pin and licensing

- Upstream: [google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model).
- License: Apache-2.0, preserved in the **complete upstream submodule**.
- Source: repository Git link `.tools/elephant-goldfish-model`, pinned to a reviewed commit by
  the **parent repository's tree** (never fetch `main` opportunistically).
- Initial imported revision: `b3a35956759bf7f024af2ff061b2e0b44b438e4c` (2026-10-27). Subsequent changes
  require one reviewed submodule-pointer update with upstream changelog inspection.
- The original `skills/`, `agents/`, `resources/document_standards/`,
  plugin manifests and license stay together. Skills alone are **not EGM**.
- Google's upstream release is not an officially supported Google product.
- No new external service is connected by this repository change; the installed
  host runs under its existing access/model permissions.

## 2. Installation versus activation

The Git submodule makes the *complete, version-pinned open source* available in
the repository. It is **not** an automatic system-wide Codex or ChatGPT plugin
installation. Use the idempotent local helper from the project root:

```sh
bash scripts/egm-setup.sh --prepare
bash scripts/egm-setup.sh --check
# If Codex is installed and plugin installation is desired:
bash scripts/egm-setup.sh --install-codex
```

The last command uses the **documented upstream Codex marketplace commands**:
`codex plugin marketplace add google/elephant-goldfish-model` and
`codex plugin add egm@egm`. The marketplace release may differ from the pinned
reference source: verify its version/contents before making a reproducibility
claim. Restart the coding session after plugin installation.

The **installed complete package** supplies the skills, personas and standards
actually executed. The repository gitlink supplies the required reference
revision. Before a live review, record both identities: `git ls-tree HEAD --
.tools/elephant-goldfish-model`, the initialized source's `git rev-parse HEAD`,
the installed path/version reported by `codex plugin list`, and a content
comparison of installed skills, agents, resources, docs and manifests against
the pinned checkout. Exclude Git metadata and generated test/cache files.
If contents differ, stop the reproducible Westside review until the installed
package matches the pin, or the repository owner explicitly accepts and records
the identified difference. Never silently change the gitlink or call a
mismatched run reproducible. Missing required runtime files make the review
incomplete, even if other reviewers finish.

For ChatGPT Work, use the upstream `docs/harnesses.md` setup instructions.
ChatGPT standard chats without native isolated subagents cannot perform an
authentic Goldfish review. **Fail closed; never use a single shared context to
pretend to be multiple reviewers.**

### Installation alternatives considered

The selected pinned submodule plus optional full host installation keeps a
reviewable source baseline in Git and provides native skill discovery. It
requires checking for drift between two copies. Marketplace-only installation
avoids the extra checkout but does not preserve the project's reviewed source
revision. Pinned source without host installation preserves that revision and
can be read manually, but does not establish native plugin discovery or workflow
activation. The selected arrangement retains both capabilities; the provenance
check above addresses its maintenance cost. None removes the need for isolated
reviewers or editorial acceptance.

## 3. Ownership and reading order

| Concern | Single authority |
| --- | --- |
| Brand, color, typography, spacing and motion tokens | `design-system/tokens/westside.tokens.json` and `docs/design/WESTSIDE-DESIGN-OS.md` |
| Allowed site/tool scopes | `design-system/scopes.json` |
| Shipped CSS/runtime | `static/css/westside-design-os.css`, plus owning surface CSS |
| Publication composition and visual evidence | `docs/design/WESTSIDE-EDITORIAL-MANUAL.md`, original references and approved assets |
| Project architecture and protected scope | `docs/MASTER_SITE_ARCHITECTURE.md`, `ENGINEERING-GOVERNANCE.md` |
| Spec drafting and *independent* document review | Complete upstream EGM skill/persona set |

EGM reads the above authorities and reports conflicts. It **cannot override**
approved visual assets, change the tokens, silently introduce new pages or
change an editor's art decision. EGM specs should cite exact files/commits
and links to genuine reference images and visual acceptance evidence.

## 4. Westside workflow (for consequential new designs)

Use this workflow for changes to architecture, publication composition,
typography, layout or motion behavior. A clear fix may omit **only** the
optional brainstorming step; it does not waive the applicable specification,
independent review, existing tests or art-direction gates.

1. **Elephant / define.** Read architectural records, current branch, protected
   assets, existing art direction and representative desktop/mobile screenshots.
   Use upstream `egm-brainstorm` where useful; a clear fix may skip brainstorming.
2. **Elephant / specify.** Use `egm-draft` to create a complete, independently
   understandable specification under `docs/design/`, scoped to the owning
   surface. Include reference, invariants, non-goals, expected geometry,
   typography, animation states, accessibility, tests and measurable success.
3. **Goldfish / falsify.** Execute upstream `egm-review` with **fresh isolated
   subagents**: zoom-out, naive comprehension, design critic, implementation
   readiness (as upstream prescribes). Give them only the spec and cited source.
   Preserve findings as artifacts under `.dev/egm/`. Record each finding as
   fixed, contested or explicitly accepted by its responsible owner. No self-review substitution.
4. **Implement.** Modify only permitted files, in a single cohesive change.
   Compare real screens at 1648, 768, 390 and 320 px (or the accepted viewport
   contract) and inspect actual animation time states, scroll reversal and
   reduced motion where applicable. Use existing Design OS/CI gates, not a new
   EGM-specific CI pipeline.
5. **Art-direction gate.** The editor must compare *actual screenshots* against
   the approved reference and formally accept the composition. Green CI,
   `egm-review` and spec approval never independently mean award-level visual
   acceptance or authorize merging.
6. **Trace drift.** Use upstream `egm-drift-report` when edited code diverges
   from an accepted living spec; update the spec and re-review meaningful
   changes, not the visual authority.

### Review record for each substantial design PR

The PR should link (a) versioned design spec, (b) reference and protected
assets, (c) *actual* Goldfish execution/report or **NOT RUN** with reason,
(d) before/after real screenshots at relevant viewports/states,
(e) existing CI results and known unrelated baseline failures, and
(f) explicit editor signoff if present. Never call a document draft
`approved` on the strength of a machine-only test.

Record execution separately from the verdict: **NOT RUN** means no authentic
review ran; **PARTIAL** means some required stages or reads did not finish;
**COMPLETE WITH FINDINGS** means all applicable stages finished with open
findings; **COMPLETE** means they finished without open findings. Record N/A
stages with a reason, never as passed. For each executed stage, retain actual
native launch/completion evidence, fresh-context parameters, persona/standard
paths, target identity, findings and report location. Retain successful read
evidence where the host exposes it; self-written receipts alone are not native
trace proof. Preserve completed reports after quota/tool failures and resume
the missing work against the same document identity, or re-review changed ranges.
For PARTIAL runs, explicitly list every completed and missing required stage
and read so the next session can identify the remaining work.

NOT RUN and PARTIAL leave this workflow's independent-review requirement
unsatisfied and cannot be represented as approval for implementation or release.
Before progressing under an exception, the repository owner must explicitly
accept its scope, reason and missing evidence in the review record; an agent
cannot grant that exception. For completed reviews, use the upstream finding
resolution/checkpoint process and record each finding as fixed, contested or
explicitly accepted by the responsible owner. This does not require zero
findings, and acceptance of residual specification findings is separate from
the editor's required acceptance of genuine screenshots. Existing CI and
protected-asset requirements remain in force in every case.

### P2 / Vol.00 first-use target (no artwork changed by this integration)

Scope: left folio's relationship to the already approved right-hand
Jerusalem gate cover. Keep the original right cover, gate light, official
Westside masthead, Morning Star asset and canonical Contents unchanged.
The specification must include the editor's actual right-cover screenshot,
a single approved independent-publication spread reference, visual hierarchy,
negative-space plan, left/right alignment and a no-overlap check for rules
versus major Chinese type. Review should explicitly reject decorative
pseudo-depth and unrelated repeat-type wallpaper. Do not proceed straight
from a green Playwright suite to a visual signoff.

## 5. Operational guarantees

- **One management system:** The Westside Design OS; EGM is a reviewer/workflow.
- **One established CI suite:** The existing `scripts/check_westside_design_os.py`
  checks this source registration without invoking models, downloading plugins
  or simulating an independent review. Browser/art review is unchanged.
- **No extra production payload:** The source lives outside Hugo static/assets;
  no font, site CSS, JS bundle, UI or image is added.
- **No automatic model execution:** No API, model runner or extra agent is automatically
  launched. Live EGM review may consume the user's existing model quota.
- **No forced reauthorization:** Any host security prompts remain host-owned;
  project code never attempts to bypass tool authorization.
- **No unapproved merge:** A draft PR stays draft until release requirements
  and editor permission are satisfied.
