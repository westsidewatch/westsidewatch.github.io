#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "DORE_GITHUB_RUNNER_RECONCILE_BLOCKED reason=macos_required" >&2
  exit 20
fi

REPO_SLUG="${DORE_GITHUB_REPO:-westsidewatch/westsidewatch.github.io}"
ROOT="${DORE_LOCAL_HOME:-$HOME/.dore}"
RUNNER_DIR="$ROOT/github-runner"
LOG_DIR="$ROOT/logs"
LABEL="ca.dore.github-runner"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
GH="$(command -v gh || true)"
UID_NOW="$(id -u)"

mkdir -p "$LOG_DIR" "$HOME/Library/LaunchAgents"

if [[ -z "$GH" ]] || ! "$GH" auth status >/dev/null 2>&1; then
  echo "DORE_GITHUB_RUNNER_RECONCILE_BLOCKED reason=gh_unavailable"
  exit 21
fi

if [[ ! -x "$RUNNER_DIR/runsvc.sh" ]] || [[ ! -f "$RUNNER_DIR/.runner" ]]; then
  echo "DORE_GITHUB_RUNNER_RECONCILE_BLOCKED reason=runner_not_configured"
  exit 22
fi

NAME="$(python3 - <<'PY'
import json
from pathlib import Path
p=Path.home()/'.dore/github-runner/.runner'
try:
    print(json.loads(p.read_text()).get('agentName',''))
except Exception:
    print('')
PY
)"
if [[ -z "$NAME" ]]; then
  NAME="dore-$(scutil --get LocalHostName 2>/dev/null || hostname -s)"
fi

REMOTE_JSON="$($GH api "repos/$REPO_SLUG/actions/runners?per_page=100" 2>/dev/null || true)"
REMOTE_PRESENT="$(python3 - "$NAME" <<'PY' <<<"$REMOTE_JSON"
import json,sys
name=sys.argv[1]
try:
    data=json.load(sys.stdin)
except Exception:
    print('unknown'); raise SystemExit
for runner in data.get('runners',[]):
    if runner.get('name') == name:
        print('yes'); raise SystemExit
print('no')
PY
)"

# If GitHub forgot the runner but local credentials remain, repair registration.
if [[ "$REMOTE_PRESENT" == "no" ]]; then
  REMOVE_TOKEN="$($GH api --method POST "repos/$REPO_SLUG/actions/runners/remove-token" --jq .token 2>/dev/null || true)"
  if [[ -n "$REMOVE_TOKEN" ]]; then
    (cd "$RUNNER_DIR" && ./config.sh remove --unattended --token "$REMOVE_TOKEN") >/dev/null 2>&1 || true
  fi
  rm -f "$RUNNER_DIR/.runner" "$RUNNER_DIR/.credentials" "$RUNNER_DIR/.credentials_rsaparams"
  TOKEN="$($GH api --method POST "repos/$REPO_SLUG/actions/runners/registration-token" --jq .token 2>/dev/null || true)"
  if [[ -z "$TOKEN" ]]; then
    echo "DORE_GITHUB_RUNNER_RECONCILE_BLOCKED reason=registration_token_unavailable"
    exit 23
  fi
  (
    cd "$RUNNER_DIR"
    ./config.sh --unattended --replace \
      --url "https://github.com/$REPO_SLUG" \
      --token "$TOKEN" \
      --name "$NAME" \
      --labels dore \
      --work _work
  )
fi

# launchd owns process lifetime; always reconcile the service itself.
if [[ ! -f "$PLIST" ]]; then
  echo "DORE_GITHUB_RUNNER_RECONCILE_BLOCKED reason=launchd_plist_missing"
  exit 24
fi

if ! launchctl print "gui/$UID_NOW/$LABEL" >/dev/null 2>&1; then
  launchctl bootstrap "gui/$UID_NOW" "$PLIST" >/dev/null 2>&1 || true
fi
launchctl kickstart -k "gui/$UID_NOW/$LABEL" >/dev/null 2>&1 || true

sleep 2
if launchctl print "gui/$UID_NOW/$LABEL" >/dev/null 2>&1; then
  echo "DORE_GITHUB_RUNNER_RECONCILE_PASS name=$NAME remote=$REMOTE_PRESENT"
else
  echo "DORE_GITHUB_RUNNER_RECONCILE_BLOCKED reason=launchd_not_running"
  exit 25
fi
