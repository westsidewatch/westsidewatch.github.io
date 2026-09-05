#!/bin/bash
set -euo pipefail
ROOT="${DORE_REPO_ROOT:-$HOME/westsidewatch.github.io}"
APP="$ROOT/local/dore-local/a2a_http_bridge.py"
PLIST="$HOME/Library/LaunchAgents/io.westsidewatch.dore-a2a.plist"
LOGDIR="$HOME/.dore/logs"
mkdir -p "$LOGDIR" "$HOME/Library/LaunchAgents"
PY="$(command -v python3)"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>io.westsidewatch.dore-a2a</string>
<key>ProgramArguments</key><array><string>$PY</string><string>$APP</string></array>
<key>WorkingDirectory</key><string>$ROOT/local/dore-local</string>
<key>EnvironmentVariables</key><dict><key>DORE_REPO_ROOT</key><string>$ROOT</string><key>DORE_A2A_PORT</key><string>4312</string></dict>
<key>RunAtLoad</key><true/><key>KeepAlive</key><true/>
<key>StandardOutPath</key><string>$LOGDIR/dore-a2a.out.log</string>
<key>StandardErrorPath</key><string>$LOGDIR/dore-a2a.err.log</string>
</dict></plist>
EOF
launchctl bootout "gui/$(id -u)/io.westsidewatch.dore-a2a" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl kickstart -k "gui/$(id -u)/io.westsidewatch.dore-a2a"
for i in {1..30};do
 if /usr/bin/curl -fsS http://127.0.0.1:4312/health >/tmp/dore-a2a-health.json 2>/dev/null;then cat /tmp/dore-a2a-health.json;echo;exit 0;fi
 sleep .25
done
echo '{"ok":false,"error":"dore_a2a_health_timeout"}' >&2;exit 1
