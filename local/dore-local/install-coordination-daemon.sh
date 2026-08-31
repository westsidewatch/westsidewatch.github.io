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
rm -f "$HOME_DORE/coordination/daemon-state.json"
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl kickstart -k "gui/$(id -u)/$LABEL"
launchctl print "gui/$(id -u)/$LABEL" >/dev/null
python3 - <<PY
import json,time
from pathlib import Path
p=Path('$HOME_DORE/coordination/daemon-state.json')
last=None
for _ in range(30):
 if p.exists():
  try:last=json.loads(p.read_text())
  except Exception: last=None
  if last and last.get('status') in {'healthy','worker_error','sync_error','daemon_error'}:
   print(json.dumps(last,ensure_ascii=False))
   if last.get('status')=='healthy': raise SystemExit(0)
   raise SystemExit('coordination_daemon_not_healthy:'+last.get('status','unknown'))
 time.sleep(1)
print(json.dumps(last or {},ensure_ascii=False))
raise SystemExit('daemon_live_state_not_created')
PY
echo DORE_COORDINATION_DAEMON_PASS
