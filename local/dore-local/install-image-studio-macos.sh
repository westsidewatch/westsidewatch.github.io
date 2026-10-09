#!/bin/bash
# Install Doré Image Studio as a per-user macOS LaunchAgent.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd -P)"
ROOT="$(cd "$HERE/../.." && pwd -P)"
PY="$(command -v python3)"
[ -f "$ROOT/local/dore-local/image_studio.py" ] || { echo "Image Studio missing" >&2; exit 2; }
LABEL="io.westsidewatch.dore-image-studio"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOGDIR="$HOME/.dore/logs"
mkdir -p "$HOME/Library/LaunchAgents" "$LOGDIR"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>$LABEL</string>
<key>ProgramArguments</key><array>
<string>$PY</string><string>$ROOT/local/dore-local/image_studio.py</string>
</array>
<key>WorkingDirectory</key><string>$ROOT</string>
<key>RunAtLoad</key><true/>
<key>KeepAlive</key><true/>
<key>ProcessType</key><string>Background</string>
<key>StandardOutPath</key><string>$LOGDIR/image-studio.log</string>
<key>StandardErrorPath</key><string>$LOGDIR/image-studio.err.log</string>
</dict></plist>
EOF
plutil -lint "$PLIST"
DOMAIN="gui/$(id -u)"
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$PLIST"
launchctl enable "$DOMAIN/$LABEL"
launchctl kickstart -k "$DOMAIN/$LABEL"
for i in 1 2 3 4 5 6 7 8 9 10; do
  if curl -fsS --max-time 2 http://127.0.0.1:4313/health | grep -q '"ok": true'; then
    echo "Image Studio autostart PASS: http://127.0.0.1:4313/"
    exit 0
  fi
  sleep 1
done
echo "Image Studio health check failed; see $LOGDIR/image-studio.err.log" >&2
exit 3
