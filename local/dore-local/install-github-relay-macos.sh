#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "DORE_A2A_GITHUB_INSTALL_BLOCKED reason=macos_required" >&2
  exit 20
fi

REPO_SLUG="${DORE_GITHUB_REPO:-westsidewatch/westsidewatch.github.io}"
ROOT="${DORE_LOCAL_HOME:-$HOME/.dore}"
RUNNER_DIR="$ROOT/github-runner"
LOG_DIR="$ROOT/logs"
PLIST="$HOME/Library/LaunchAgents/ca.dore.github-runner.plist"
LABEL="ca.dore.github-runner"
GH="$(command -v gh || true)"

mkdir -p "$RUNNER_DIR" "$LOG_DIR" "$HOME/Library/LaunchAgents"
chmod 700 "$ROOT" "$RUNNER_DIR" 2>/dev/null || true

if [[ -z "$GH" ]]; then
  echo "DORE_A2A_GITHUB_INSTALL_BLOCKED reason=gh_missing"
  exit 20
fi
if ! "$GH" auth status >/dev/null 2>&1; then
  echo "DORE_A2A_GITHUB_INSTALL_BLOCKED reason=gh_not_authenticated"
  exit 21
fi

if [[ ! -f "$RUNNER_DIR/.runner" ]]; then
  TOKEN="$($GH api --method POST "repos/$REPO_SLUG/actions/runners/registration-token" --jq .token 2>/dev/null || true)"
  if [[ -z "$TOKEN" ]]; then
    echo "DORE_A2A_GITHUB_INSTALL_BLOCKED reason=runner_token_unavailable"
    exit 22
  fi

  TAG="$($GH api repos/actions/runner/releases/latest --jq .tag_name)"
  VERSION="${TAG#v}"
  case "$(uname -m)" in
    arm64) ARCH="arm64" ;;
    x86_64) ARCH="x64" ;;
    *) echo "DORE_A2A_GITHUB_INSTALL_BLOCKED reason=unsupported_arch"; exit 23 ;;
  esac
  ARCHIVE="$RUNNER_DIR/actions-runner.tar.gz"
  URL="https://github.com/actions/runner/releases/download/$TAG/actions-runner-osx-$ARCH-$VERSION.tar.gz"
  curl -fsSL "$URL" -o "$ARCHIVE"
  tar -xzf "$ARCHIVE" -C "$RUNNER_DIR"
  rm -f "$ARCHIVE"

  NAME="dore-$(scutil --get LocalHostName 2>/dev/null || hostname -s)"
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

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$RUNNER_DIR/runsvc.sh</string>
  </array>
  <key>WorkingDirectory</key><string>$RUNNER_DIR</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>ProcessType</key><string>Background</string>
  <key>ThrottleInterval</key><integer>10</integer>
  <key>StandardOutPath</key><string>$LOG_DIR/github-runner.stdout.log</string>
  <key>StandardErrorPath</key><string>$LOG_DIR/github-runner.stderr.log</string>
</dict>
</plist>
EOF
chmod 600 "$PLIST"
plutil -lint "$PLIST" >/dev/null
UID_NOW="$(id -u)"
launchctl bootout "gui/$UID_NOW/$LABEL" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$UID_NOW" "$PLIST"
launchctl kickstart -k "gui/$UID_NOW/$LABEL"
sleep 2
if launchctl print "gui/$UID_NOW/$LABEL" >/dev/null 2>&1; then
  echo "DORE_A2A_GITHUB_RUNNER_INSTALL_PASS"
else
  echo "DORE_A2A_GITHUB_INSTALL_BLOCKED reason=launchd_not_running"
  exit 24
fi
