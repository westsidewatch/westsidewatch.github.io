#!/usr/bin/env bash
set -euo pipefail
ROOT="${DORE_REPO_ROOT:-$HOME/westsidewatch.github.io}"
HOME_DORE="${DORE_LOCAL_HOME:-$HOME/.dore}"
LABEL="io.westsidewatch.dore.coordination"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
mkdir -p "$HOME/Library/LaunchAgents" "$HOME_DORE/logs" "$HOME_DORE/coordination"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>$LABEL</string>
<key>ProgramArguments</key><array><string>/usr/bin/python3</string><string>$ROOT/local/dore-local/dore_coordination_daemon.py</string></array>
<key>WorkingDirectory</key><string>$ROOT</string>
<key>EnvironmentVariables</key><dict><key>DORE_REPO_ROOT</key><string>$ROOT</string><key>DORE_LOCAL_HOME</key><string>$HOME_DORE</string><key>DORE_COORDINATION_INTERVAL_SECONDS</key><string>15</string></dict>
<key>RunAtLoad</key><true/><key>KeepAlive</key><true/>
<key>StandardOutPath</key><string>$HOME_DORE/logs/coordination-daemon.out.log</string>
<key>StandardErrorPath</key><string>$HOME_DORE/logs/coordination-daemon.err.log</string>
</dict></plist>
EOF
plutil -lint "$PLIST"
launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl kickstart -k "gui/$(id -u)/$LABEL"
sleep 2
launchctl print "gui/$(id -u)/$LABEL" >/dev/null
python3 - <<PY
import json,time
from pathlib import Path
p=Path('$HOME_DORE/coordination/daemon-state.json')
for _ in range(10):
 if p.exists():
  x=json.loads(p.read_text());print(json.dumps(x,ensure_ascii=False));raise SystemExit(0)
 time.sleep(1)
raise SystemExit('daemon_state_not_created')
PY
echo DORE_COORDINATION_DAEMON_PASS
