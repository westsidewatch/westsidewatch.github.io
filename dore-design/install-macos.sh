#!/bin/bash
set -euo pipefail
ROOT="${DORE_REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
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
if command -v lsof >/dev/null 2>&1; then
  PIDS="$(lsof -tiTCP:4310 -sTCP:LISTEN 2>/dev/null || true)"
  if [[ -n "$PIDS" ]]; then
    echo "$PIDS" | xargs kill >/dev/null 2>&1 || true
    sleep 0.25
  fi
fi
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl kickstart -k "gui/$(id -u)/io.westsidewatch.dore-design"
VALID=0
for i in {1..60}; do
  if /usr/bin/curl -fsS http://127.0.0.1:4310/api/health >/tmp/dore-design-health.json 2>/dev/null; then
    /usr/bin/curl -fsS http://127.0.0.1:4310/api/design-candidates/living-water-01 >/tmp/dore-design-candidate-01.json 2>/dev/null || true
    /usr/bin/curl -fsS http://127.0.0.1:4310/api/design-candidates/living-water-02 >/tmp/dore-design-candidate-02.json 2>/dev/null || true
    if python3 - <<'PY'
import json,sys

def load(path):
    try:return json.load(open(path))
    except Exception:return {}
h=load('/tmp/dore-design-health.json')
c1=load('/tmp/dore-design-candidate-01.json')
c2=load('/tmp/dore-design-candidate-02.json')
ok=(h.get('service')=='dore-design' and h.get('source_of_truth')=='structured-workspace' and c1.get('ok') is True and c1.get('page_id')=='living-water-candidate-01' and c2.get('ok') is True and c2.get('page_id')=='living-water-candidate-02')
print(json.dumps({'ok':ok,'health':h,'candidate01':c1,'candidate02':c2},ensure_ascii=False))
sys.exit(0 if ok else 1)
PY
    then VALID=1;break;fi
  fi
  sleep 0.25
done
if [[ "$VALID" == "1" ]]; then
  if [[ "${DORE_SKIP_CONTROL_PLANE_REFRESH:-0}" != "1" ]]; then
    [[ -f "$ROOT/local/dore-local/install-unix-a2a-macos.sh" ]] && bash "$ROOT/local/dore-local/install-unix-a2a-macos.sh"
    [[ -f "$ROOT/local/dore-local/install-github-relay-macos.sh" ]] && bash "$ROOT/local/dore-local/install-github-relay-macos.sh" || true
  fi
  exit 0
fi
{
  echo '{"ok":false,"error":"dore_design_candidate_health_timeout"}'
  echo "--- runtime root ---"; echo "$ROOT"
  echo "--- app ---"; echo "$APP"
  echo '--- health ---'; cat /tmp/dore-design-health.json 2>/dev/null || true
  echo; echo '--- candidate 01 ---'; cat /tmp/dore-design-candidate-01.json 2>/dev/null || true
  echo; echo '--- candidate 02 ---'; cat /tmp/dore-design-candidate-02.json 2>/dev/null || true
  echo; echo '--- port owner ---'; lsof -nP -iTCP:4310 -sTCP:LISTEN 2>/dev/null || true
  echo '--- dore-design.err.log ---'; tail -n 120 "$LOGDIR/dore-design.err.log" 2>/dev/null || true
  echo '--- dore-design.out.log ---'; tail -n 80 "$LOGDIR/dore-design.out.log" 2>/dev/null || true
  echo '--- launchctl ---'; launchctl print "gui/$(id -u)/io.westsidewatch.dore-design" 2>/dev/null | tail -n 80 || true
} >&2
exit 1
