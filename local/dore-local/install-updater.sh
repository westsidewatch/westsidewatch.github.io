#!/bin/zsh
set -euo pipefail
ROOT="${DORE_REPO_ROOT:-$HOME/westsidewatch.github.io}"
HOME_DORE="${DORE_LOCAL_HOME:-$HOME/.dore}"
PLIST="$HOME/Library/LaunchAgents/io.westsidewatch.dore-updater.plist"
PYTHON="$(command -v python3)"
mkdir -p "$HOME/Library/LaunchAgents" "$HOME_DORE/coordination"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>io.westsidewatch.dore-updater</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON</string>
    <string>$ROOT/local/dore-local/dore_updater.py</string>
  </array>
  <key>WorkingDirectory</key><string>$ROOT</string>
  <key>RunAtLoad</key><true/>
  <key>StartInterval</key><integer>30</integer>
  <key>StandardOutPath</key><string>$HOME_DORE/coordination/updater-launchd.out.log</string>
  <key>StandardErrorPath</key><string>$HOME_DORE/coordination/updater-launchd.err.log</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>DORE_REPO_ROOT</key><string>$ROOT</string>
    <key>DORE_LOCAL_HOME</key><string>$HOME_DORE</string>
    <key>PATH</key><string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
  </dict>
</dict>
</plist>
EOF
plutil -lint "$PLIST"
launchctl bootout "gui/$(id -u)/io.westsidewatch.dore-updater" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl kickstart -k "gui/$(id -u)/io.westsidewatch.dore-updater"
echo "Doré updater installed: 30-second autonomous sync + coordination worker"
