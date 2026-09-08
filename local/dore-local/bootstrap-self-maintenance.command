#!/bin/bash
set -euo pipefail

# One-time bridge from a manually maintained checkout to Doré-owned maintenance.
# It preserves the current HEAD behind a safety branch, rebases only a clean
# worktree onto origin/main, aborts on conflict, then refreshes Companion.

REPO="${DORE_WORKTREE:-$HOME/westsidewatch.github.io}"
cd "$REPO"

fail() { printf 'DORÉ self-maintenance bootstrap: FAIL — %s\n' "$1" >&2; exit "${2:-1}"; }
[[ -d .git ]] || fail "not a git worktree: $REPO" 2
[[ -z "$(git status --porcelain)" ]] || fail "working tree is not clean" 3

BRANCH="$(git symbolic-ref --quiet --short HEAD || true)"
[[ -n "$BRANCH" ]] || fail "detached HEAD is not accepted" 4
OLD_HEAD="$(git rev-parse HEAD)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
SAFE_BRANCH="dore-safety/${BRANCH//\//-}-$STAMP"

git branch "$SAFE_BRANCH" "$OLD_HEAD"
printf 'safety_branch=%s\n' "$SAFE_BRANCH"

git fetch origin main
NEW_MAIN="$(git rev-parse origin/main)"

if ! git rebase origin/main; then
  git rebase --abort || true
  [[ "$(git rev-parse HEAD)" == "$OLD_HEAD" ]] || git reset --hard "$OLD_HEAD"
  fail "rebase conflict; original HEAD restored and safety branch retained" 5
fi

NEW_HEAD="$(git rev-parse HEAD)"
[[ -z "$(git status --porcelain)" ]] || fail "post-rebase worktree is not clean" 6

# Refresh Native Messaging + Companion from the newly reconciled checkout.
bash local/dore-companion-extension/install_companion_1.command

python3 - "$BRANCH" "$OLD_HEAD" "$NEW_MAIN" "$NEW_HEAD" "$SAFE_BRANCH" <<'PY'
import json,sys
branch,old_head,main_head,new_head,safety=sys.argv[1:]
print(json.dumps({
  "ok": True,
  "status": "completed",
  "capability": "system.self-maintain.bootstrap",
  "branch": branch,
  "old_head": old_head,
  "origin_main": main_head,
  "new_head": new_head,
  "safety_branch": safety,
  "native_host_refreshed": True,
  "manual_bootstrap_complete": True
}, ensure_ascii=False))
PY
