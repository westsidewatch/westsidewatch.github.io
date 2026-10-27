#!/usr/bin/env bash
# A2A-received, version-pinned P2 specification review through installed Codex EGM.
# This is a REVIEW ONLY: do not change the cover, page implementation or main.
set -euo pipefail

P2_BRANCH="p2-latest-magazine-motion-preview-20261023"
EXPECTED_SHA="${P2_A2A_SOURCE_SHA:-}"
if [[ ! "$EXPECTED_SHA" =~ ^[0-9a-f]{40}$ ]]; then
  echo "A2A EGM ERROR: exact P2_A2A_SOURCE_SHA lease required" >&2
  exit 12
fi
EGM_BRANCH="integrate-egm-into-westside-design-os-20261027"
TARGET="docs/design/P2-VOL00-EGM-SPREAD-SPEC.md"
REPORT="docs/design/P2-VOL00-EGM-GOLDFISH-REPORT.md"
ROOT="${DORE_REPO_ROOT:-${HOME}/westsidewatch.github.io}"
if [[ ! -d "$ROOT/.git" && ! -f "$ROOT/.git" ]]; then
  if [[ -d "$HOME/.dore/control-checkout/.git" ]]; then ROOT="$HOME/.dore/control-checkout"; fi
fi
if [[ ! -d "$ROOT/.git" && ! -f "$ROOT/.git" ]]; then
  printf 'A2A EGM ERROR: no trusted local repository checkout at %s\n' "$ROOT" >&2
  exit 2
fi
cd "$ROOT"
git fetch --no-tags origin "+refs/heads/$P2_BRANCH:refs/remotes/origin/$P2_BRANCH" "+refs/heads/$EGM_BRANCH:refs/remotes/origin/$EGM_BRANCH"
ACTUAL_SHA="$(git rev-parse "refs/remotes/origin/$P2_BRANCH")"
if [[ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
  printf 'A2A EGM ERROR: branch changed; expected %s actual %s. Do not review stale input.\n' "$EXPECTED_SHA" "$ACTUAL_SHA" >&2
  exit 3
fi
REVIEW_ROOT="$HOME/.dore/egm-p2-review-${EXPECTED_SHA:0:12}"
if [[ ! -d "$REVIEW_ROOT/.git" && ! -f "$REVIEW_ROOT/.git" ]]; then
  mkdir -p "$(dirname "$REVIEW_ROOT")"
  git worktree add --detach "$REVIEW_ROOT" "$EXPECTED_SHA"
fi
if [[ "$(git -C "$REVIEW_ROOT" rev-parse HEAD)" != "$EXPECTED_SHA" ]]; then
  echo "A2A EGM ERROR: worktree source mismatch" >&2
  exit 4
fi
if [[ ! -f "$REVIEW_ROOT/$TARGET" ]]; then
  echo "A2A EGM ERROR: P2 review target missing" >&2
  exit 5
fi

# The verified Codex native CLI is bundled under ChatGPT's plugin appserver,
# rather than a conventional Homebrew/npm-global PATH entry on this Mac.
export PATH="$HOME/.codex/plugins/.plugin-appserver/codex-cli/bin:/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin:$HOME/.local/bin:$HOME/.npm-global/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
if ! command -v codex >/dev/null 2>&1; then
  echo "A2A EGM ERROR: codex CLI unavailable in worker environment" >&2
  exit 6
fi
PROOF="$REVIEW_ROOT/.dev/egm/p2-4fa21ce51444"
mkdir -p "$PROOF"
codex plugin list > "$PROOF/plugin-list.txt" 2>&1
if ! grep -Eqi '(^|[[:space:]])egm([[:space:]@]|$)' "$PROOF/plugin-list.txt"; then
  echo "A2A EGM ERROR: installed egm@egm not found; no simulated Goldfish allowed" >&2
  exit 7
fi
git show "refs/remotes/origin/$EGM_BRANCH:docs/design/WESTSIDE-EGM-INTEGRATION.md" > "$PROOF/westside-egm-integration.md"
git show "refs/remotes/origin/$EGM_BRANCH:AGENTS.md" > "$PROOF/integration-agent-entrypoint.md"

# Design OS authority lives on the companion EGM integration branch. P2 is a
# separate draft feature branch; its worktree intentionally has no EGM gitlink.
PIN_LINE="$(git ls-tree "refs/remotes/origin/$EGM_BRANCH" -- .tools/elephant-goldfish-model)"
PIN_SHA="$(printf '%s\n' "$PIN_LINE" | awk '$1=="160000" && $2=="commit" {print $3}')"
if [[ ! "$PIN_SHA" =~ ^[0-9a-f]{40}$ ]]; then
  echo "EGM ERROR: companion Design OS branch has no pinned gitlink" >&2
  exit 13
fi
PIN_EXPECTED="b3a35956759bf7f024af2ff061b2e0b44b438e4c"
if [[ "$PIN_SHA" != "$PIN_EXPECTED" ]]; then
  echo "EGM ERROR: companion pin changed; manual source re-review required" >&2
  exit 14
fi
cat > "$PROOF/egm-source-authority.txt" <<EOF
EGM_source_branch=$EGM_BRANCH
EGM_submodule=.tools/elephant-goldfish-model
EGM_pinned_commit=$PIN_SHA
EGM_installed_plugin=egm@egm
EGM_installed_plugin_metadata=$(grep -E '^egm@egm' "$PROOF/plugin-list.txt" | head -1)
P2_art_branch=$P2_BRANCH
P2_source_commit=$EXPECTED_SHA
NOTE: EGM is on its own draft branch; P2 does not need a duplicate gitlink.
NOTE: Run the installed reviewer in native independent subagent contexts.
EOF


TASK_PROMPT="$(cat <<'TASK'
Use the **installed official egm@egm** plugin's real egm-review workflow.
TargetFile: docs/design/P2-VOL00-EGM-SPREAD-SPEC.md
Step: uninterrupted (consolidated, all applicable review stages; Stage 9 is N/A without an implementation plan).
GoldfishContext: docs/design/WESTSIDE-EDITORIAL-MANUAL.md,
docs/design/WESTSIDE-DESIGN-OS.md, ENGINEERING-GOVERNANCE.md,
static/experiments/p2-double-square-video-lab.html,
static/css/p2-vol00-editorial.css, tests/p2-vol00-preview.cjs,
and .dev/egm/p2-4fa21ce51444/westside-egm-integration.md,
.dev/egm/p2-4fa21ce51444/egm-source-authority.txt.
Important: EGM's source pin belongs to the separate Design OS integration
branch. The runner has verified that exact pinned gitlink by git ls-tree.
It is correct that the P2 art branch does not contain a duplicate EGM
submodule. Treat the companion branch as the source authority, not as a
missing P2 dependency. Read the verified local source authority record.
Before dispatch, READ the locally installed plugin's real skill and persona/standard files.
Goldfish reviewers MUST be fresh isolated native Codex subagents, each with
fork_context:false or fork_turns:"none", with native completion and successful
read evidence. Do not use yourself as a pretend second opinion.
Review the current REJECTED P2 left page against the immutable right-hand city
gate cover and the actual Portaly printed-spread reference. Validate reference
URL and disclose any unavailable screenshot rather than inventing evidence.
Focus on global hierarchy, real print texture, negative space, Chinese glyph
treatment, star/title visual connection, responsive states and anti-collision.
Do not silently select alternative architecture; identify editorial decisions.
Record findings as Blocker/Major/Nit, with exact spec sections and evidence.
No website-code edits, no new artwork, no image generation, no main merge.
Write a clear self-contained **Markdown consolidated report** at
docs/design/P2-VOL00-EGM-GOLDFISH-REPORT.md.
Explicitly distinguish NATIVE VERIFIED, PARTIAL, or NOT RUN and explain why.
This run is review only: do not edit the feature spec without human approval.
The output report must include real agent stage coverage 5–8, reviewer personas,
findings, non-completion if applicable, and suggested owner resolution decisions.
Deliver report file, then a short terminal result. Do not claim art approval.
TASK
)"
echo "A2A EGM: starting official native isolated P2 Goldfish review at $EXPECTED_SHA"
set +e
codex exec -C "$REVIEW_ROOT" --approve-for-me --skip-git-repo-check --json \
  --output-last-message "$PROOF/codex-final.md" "$TASK_PROMPT" \
  > "$PROOF/codex-events.jsonl" 2> "$PROOF/codex-stderr.log"
CODEX_RC=$?
set -e
printf '%s\n' "$CODEX_RC" > "$PROOF/codex-exitcode.txt"
if [[ "$CODEX_RC" -ne 0 ]]; then
  echo "A2A EGM: Codex review returned $CODEX_RC; native evidence saved locally, no PASS claimed." >&2
  tail -c 3000 "$PROOF/codex-stderr.log" >&2 || true
  exit "$CODEX_RC"
fi
if [[ ! -s "$REVIEW_ROOT/$REPORT" ]]; then
  echo "A2A EGM ERROR: review completed without a durable report; fail closed." >&2
  exit 8
fi
if ! grep -Eqi 'spawn_agent|fork_turns|fork_context|egm-(zoom-out|design|comprehension|implementation)' "$PROOF/codex-events.jsonl"; then
  echo "A2A EGM ERROR: native child dispatch not evident in Codex trace; do not claim independent review." >&2
  exit 9
fi
if ! grep -Eq 'Stage 5|Stage 6|Stage 7|Stage 8|階段.?5|階段.?6' "$REVIEW_ROOT/$REPORT"; then
  echo "A2A EGM ERROR: P2 report missing stage coverage, no verified completion." >&2
  exit 10
fi
git -C "$REVIEW_ROOT" diff --check
git -C "$REVIEW_ROOT" add -- "$REPORT"
if git -C "$REVIEW_ROOT" diff --cached --quiet; then
  echo "A2A EGM ERROR: no new report to publish" >&2
  exit 11
fi
git -C "$REVIEW_ROOT" -c user.name="Dore EGM A2A" -c user.email="westsidewatchca@gmail.com" \
  commit -m "docs(p2): record native EGM Goldfish review of Vol.00 spread"
git -C "$REVIEW_ROOT" push origin "HEAD:refs/heads/$P2_BRANCH"
NEW_SHA="$(git -C "$REVIEW_ROOT" rev-parse HEAD)"
printf '{"ok":true,"code":"P2_EGM_GOLDFISH_REPORT_PUBLISHED","branch":"%s","source_sha":"%s","report_sha":"%s","report":"%s"}\n' \
  "$P2_BRANCH" "$EXPECTED_SHA" "$NEW_SHA" "$REPORT"
