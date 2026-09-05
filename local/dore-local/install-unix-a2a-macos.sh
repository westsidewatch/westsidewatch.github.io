#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "ERROR: macOS required" >&2
  exit 1
fi

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PYTHON="$(command -v python3)"
UID_NOW="$(id -u)"
ROOT="${DORE_LOCAL_HOME:-$HOME/.dore}"
RUN_DIR="$ROOT/run"
LOG_DIR="$ROOT/logs"
AGENT_DIR="$HOME/Library/LaunchAgents"
PLIST="$AGENT_DIR/ca.dore.a2a.plist"
LABEL="ca.dore.a2a"
SOCKET="$RUN_DIR/dore.sock"

mkdir -p "$RUN_DIR" "$LOG_DIR" "$AGENT_DIR"
chmod 700 "$ROOT" "$RUN_DIR" 2>/dev/null || true

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON</string>
    <string>$REPO/local/dore-local/unix_rpc_server.py</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>DORE_REPO_ROOT</key><string>$REPO</string>
    <key>DORE_LOCAL_HOME</key><string>$ROOT</string>
    <key>PYTHONUNBUFFERED</key><string>1</string>
  </dict>
  <key>Sockets</key>
  <dict>
    <key>DoreA2A</key>
    <dict>
      <key>SockPathName</key><string>$SOCKET</string>
      <key>SockPathMode</key><integer>384</integer>
      <key>SockType</key><string>stream</string>
    </dict>
  </dict>
  <key>ProcessType</key><string>Background</string>
  <key>KeepAlive</key><false/>
  <key>RunAtLoad</key><false/>
  <key>ThrottleInterval</key><integer>5</integer>
  <key>Umask</key><integer>63</integer>
  <key>StandardOutPath</key><string>$LOG_DIR/a2a.stdout.log</string>
  <key>StandardErrorPath</key><string>$LOG_DIR/a2a.stderr.log</string>
</dict>
</plist>
EOF
chmod 600 "$PLIST"

plutil -lint "$PLIST" >/dev/null
launchctl bootout "gui/$UID_NOW/$LABEL" >/dev/null 2>&1 || true
rm -f "$SOCKET"
launchctl bootstrap "gui/$UID_NOW" "$PLIST"

# Connecting to the launchd-owned socket is the acceptance trigger; this must
# start Doré without Firefox, a localhost TCP daemon, or a resident bridge.
RESULT="$($PYTHON "$REPO/local/dore-local/unix_rpc_client.py" --method dore.health)"
printf '%s\n' "$RESULT"
printf '%s\n' "$RESULT" | grep -q '"transport": "unix-domain-socket"'
printf '%s\n' "$RESULT" | grep -q '"lifecycle": "launchd-socket-activation"'
printf '%s\n' "$RESULT" | grep -q '"browser_required": false'

echo "DORE_A2A_UNIX_INSTALL_PASS"
