#!/bin/bash
set -euo pipefail
ROOT="$HOME/westsidewatch.github.io"
DORE="$HOME/.dore"
PLIST="$HOME/Library/LaunchAgents/io.westsidewatch.dore-local.plist"
UPDATER_PLIST="$HOME/Library/LaunchAgents/io.westsidewatch.dore-updater.plist"
LABEL="io.westsidewatch.dore-local"
UPDATER_LABEL="io.westsidewatch.dore-updater"
UIDN="$(id -u)"
DOMAIN="gui/$UIDN"
mkdir -p "$HOME/Library/LaunchAgents" "$DORE/logs"
touch "$DORE/logs/local-api.log" "$DORE/logs/local-api.err.log" "$DORE/logs/updater.log" "$DORE/logs/updater.err.log"
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
 <key>DORE_LOCAL_MODEL</key><string>gemma4:e4b</string>
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
cat > "$UPDATER_PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>$UPDATER_LABEL</string>
<key>ProgramArguments</key><array><string>$PY</string><string>$ROOT/local/dore-local/local_updater.py</string></array>
<key>EnvironmentVariables</key><dict>
 <key>DORE_REPO_ROOT</key><string>$ROOT</string>
 <key>DORE_LOCAL_HOME</key><string>$DORE</string>
</dict>
<key>RunAtLoad</key><true/>
<key>StartInterval</key><integer>60</integer>
<key>ProcessType</key><string>Background</string>
<key>LimitLoadToSessionType</key><string>Aqua</string>
<key>StandardOutPath</key><string>$DORE/logs/updater.log</string>
<key>StandardErrorPath</key><string>$DORE/logs/updater.err.log</string>
<key>WorkingDirectory</key><string>$ROOT</string>
</dict></plist>
EOF
plutil -lint "$PLIST"
plutil -lint "$UPDATER_PLIST"
for item in "$LABEL:$PLIST" "$UPDATER_LABEL:$UPDATER_PLIST"; do
  lab="${item%%:*}"; file="${item#*:}"
  launchctl bootout "$DOMAIN/$lab" 2>/dev/null || true
  launchctl unload "$file" 2>/dev/null || true
  if ! launchctl bootstrap "$DOMAIN" "$file" 2>"$DORE/logs/${lab}.bootstrap.err"; then launchctl load -w "$file"; fi
  launchctl enable "$DOMAIN/$lab" 2>/dev/null || true
  launchctl kickstart -k "$DOMAIN/$lab" 2>/dev/null || true
done
sleep 2
launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1 || { echo "ERROR: Doré Local LaunchAgent not registered" >&2; exit 4; }
launchctl print "$DOMAIN/$UPDATER_LABEL" >/dev/null 2>&1 || { echo "ERROR: Doré updater LaunchAgent not registered" >&2; exit 6; }
if curl -fsS http://127.0.0.1:8788/health >/dev/null 2>&1; then echo DORE_LOCAL_AUTOSTART_PASS; else echo "ERROR: Doré Local health check failed" >&2; exit 5; fi
echo DORE_LOCAL_UPDATER_REGISTERED
