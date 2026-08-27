#!/bin/bash
set -euo pipefail
ROOT="$HOME/westsidewatch.github.io"
DORE="$HOME/.dore"
PLIST="$HOME/Library/LaunchAgents/io.westsidewatch.dore-local.plist"
mkdir -p "$HOME/Library/LaunchAgents" "$DORE/logs"
PY="$(command -v python3)"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>io.westsidewatch.dore-local</string>
<key>ProgramArguments</key><array><string>$PY</string><string>$ROOT/local/dore-local/dore_local.py</string></array>
<key>EnvironmentVariables</key><dict><key>DORE_LOCAL_HOME</key><string>$DORE</string><key>DORE_LOCAL_MODEL</key><string>qwen3:8b</string></dict>
<key>RunAtLoad</key><true/><key>KeepAlive</key><true/>
<key>StandardOutPath</key><string>$DORE/logs/local-api.log</string>
<key>StandardErrorPath</key><string>$DORE/logs/local-api.err.log</string>
<key>WorkingDirectory</key><string>$ROOT</string>
</dict></plist>
EOF
launchctl bootout "gui/$(id -u)/io.westsidewatch.dore-local" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl enable "gui/$(id -u)/io.westsidewatch.dore-local"
echo DORE_LOCAL_AUTOSTART_INSTALLED
