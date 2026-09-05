#!/bin/bash
set -euo pipefail
ROOT="${DORE_REPO_ROOT:-$HOME/westsidewatch.github.io}"
APP="$ROOT/dore-design/app_design2.py"
PLIST="$HOME/Library/LaunchAgents/io.westsidewatch.dore-design.plist"
LOGDIR="$HOME/.dore/logs"
mkdir -p "$LOGDIR" "$HOME/Library/LaunchAgents"
PY="$(command -v python3)"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>io.westsidewatch.dore-design</string>
<key>ProgramArguments</key><array><string>$PY</string><string>$APP</string></array>
<key>WorkingDirectory</key><string>$ROOT</string>
<key>RunAtLoad</key><true/><key>KeepAlive</key><true/>
<key>StandardOutPath</key><string>$LOGDIR/dore-design.out.log</string>
<key>StandardErrorPath</key><string>$LOGDIR/dore-design.err.log</string>
</dict></plist>
EOF
launchctl bootout "gui/$(id -u)/io.westsidewatch.dore-design" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl kickstart -k "gui/$(id -u)/io.westsidewatch.dore-design"
for i in {1..30}; do
  if /usr/bin/curl -fsS http://127.0.0.1:4310/api/health >/tmp/dore-design-health.json 2>/dev/null; then
    python3 - <<'PY'
import json
h=json.load(open('/tmp/dore-design-health.json'))
assert h.get('version')=='2.0-dev-phase4'
assert h.get('resident_entrypoint')=='app_design2.py'
assert h.get('immutable_publication') is True
print(json.dumps(h,ensure_ascii=False))
PY
    # A production action may itself be executing through the Unix control
    # plane. Never restart that plane mid-RPC or the caller loses the response.
    if [[ "${DORE_SKIP_CONTROL_PLANE_REFRESH:-0}" != "1" ]]; then
      if [[ -f "$ROOT/local/dore-local/install-unix-a2a-macos.sh" ]]; then
        bash "$ROOT/local/dore-local/install-unix-a2a-macos.sh"
      fi
      if [[ -f "$ROOT/local/dore-local/install-github-relay-macos.sh" ]]; then
        bash "$ROOT/local/dore-local/install-github-relay-macos.sh" || true
      fi
    fi
    exit 0
  fi
  sleep 0.25
done
echo '{"ok":false,"error":"dore_design_health_timeout"}' >&2
exit 1
