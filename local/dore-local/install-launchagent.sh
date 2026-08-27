#!/bin/bash
set -euo pipefail
ROOT="$HOME/westsidewatch.github.io"
DORE="$HOME/.dore"
PLIST="$HOME/Library/LaunchAgents/io.westsidewatch.dore-local.plist"
LABEL="io.westsidewatch.dore-local"
UIDN="$(id -u)"
DOMAIN="gui/$UIDN"
mkdir -p "$HOME/Library/LaunchAgents" "$DORE/logs"
touch "$DORE/logs/local-api.log" "$DORE/logs/local-api.err.log"
PY="$(command -v python3)"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>$LABEL</string>
<key>ProgramArguments</key><array><string>$PY</string><string>$ROOT/local/dore-local/dore_local.py</string></array>
<key>EnvironmentVariables</key><dict>
 <key>DORE_LOCAL_HOME</key><string>$DORE</string>
 <key>DORE_LOCAL_HOST</key><string>127.0.0.1</string>
 <key>DORE_LOCAL_PORT</key><string>8788</string>
 <key>DORE_LOCAL_MODEL</key><string>qwen3:8b</string>
 <key>OLLAMA_BASE_URL</key><string>http://127.0.0.1:11434</string>
</dict>
<key>RunAtLoad</key><true/>
<key>KeepAlive</key><true/>
<key>ProcessType</key><string>Background</string>
<key>LimitLoadToSessionType</key><string>Aqua</string>
<key>StandardOutPath</key><string>$DORE/logs/local-api.log</string>
<key>StandardErrorPath</key><string>$DORE/logs/local-api.err.log</string>
<key>WorkingDirectory</key><string>$ROOT</string>
</dict></plist>
EOF
plutil -lint "$PLIST"
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl unload "$PLIST" 2>/dev/null || true
if ! launchctl bootstrap "$DOMAIN" "$PLIST" 2>"$DORE/logs/bootstrap.err"; then
  echo "bootstrap failed; trying compatibility loader" >&2
  launchctl load -w "$PLIST"
fi
launchctl enable "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl kickstart -k "$DOMAIN/$LABEL" 2>/dev/null || true
sleep 2
if launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1; then
  echo DORE_LOCAL_AUTOSTART_REGISTERED
else
  echo "ERROR: LaunchAgent not registered" >&2
  cat "$DORE/logs/bootstrap.err" >&2 2>/dev/null || true
  exit 4
fi
if curl -fsS http://127.0.0.1:8788/health >/dev/null 2>&1; then
  echo DORE_LOCAL_AUTOSTART_PASS
else
  echo "ERROR: LaunchAgent registered but health check failed" >&2
  cat "$DORE/logs/local-api.err.log" >&2 2>/dev/null || true
  exit 5
fi
