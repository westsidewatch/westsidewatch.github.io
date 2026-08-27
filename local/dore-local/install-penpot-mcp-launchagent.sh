#!/bin/bash
set -euo pipefail
ROOT="$HOME/westsidewatch.github.io"
DORE="$HOME/.dore"
PLIST="$HOME/Library/LaunchAgents/io.westsidewatch.penpot-mcp.plist"
LABEL="io.westsidewatch.penpot-mcp"
UIDN="$(id -u)"
DOMAIN="gui/$UIDN"
LOCALBIN="$ROOT/local/dore-local/penpot-mcp/node_modules/.bin"
mkdir -p "$HOME/Library/LaunchAgents" "$DORE/logs"
touch "$DORE/logs/penpot-mcp.log" "$DORE/logs/penpot-mcp.err.log"
NPX="$(command -v npx || true)"
if [[ -z "$NPX" ]]; then
  for p in /opt/homebrew/bin/npx /usr/local/bin/npx "$HOME/.nvm/versions/node"/*/bin/npx; do
    [[ -x "$p" ]] && NPX="$p" && break
  done
fi
[[ -n "$NPX" && -x "$NPX" ]] || { echo "ERROR: npx not found" >&2; exit 2; }
[[ -x "$LOCALBIN/corepack" ]] || { echo "ERROR: local corepack shim missing; run setup-penpot-mcp.sh" >&2; exit 2; }
NODEDIR="$(dirname "$NPX")"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>$LABEL</string>
<key>ProgramArguments</key><array><string>$NPX</string><string>-y</string><string>@penpot/mcp@stable</string></array>
<key>EnvironmentVariables</key><dict>
 <key>PATH</key><string>$LOCALBIN:$NODEDIR:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
</dict>
<key>RunAtLoad</key><true/>
<key>KeepAlive</key><true/>
<key>ProcessType</key><string>Background</string>
<key>LimitLoadToSessionType</key><string>Aqua</string>
<key>StandardOutPath</key><string>$DORE/logs/penpot-mcp.log</string>
<key>StandardErrorPath</key><string>$DORE/logs/penpot-mcp.err.log</string>
<key>WorkingDirectory</key><string>$ROOT</string>
</dict></plist>
EOF
plutil -lint "$PLIST"
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl unload "$PLIST" 2>/dev/null || true
if ! launchctl bootstrap "$DOMAIN" "$PLIST" 2>"$DORE/logs/penpot-mcp-bootstrap.err"; then
  launchctl load -w "$PLIST"
fi
launchctl enable "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl kickstart -k "$DOMAIN/$LABEL" 2>/dev/null || true
sleep 4
if launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1; then
  echo DORE_PENPOT_MCP_AUTOSTART_REGISTERED
else
  echo "ERROR: Penpot MCP LaunchAgent not registered" >&2
  exit 3
fi
if curl -fsS http://127.0.0.1:4400/manifest.json >/dev/null 2>&1; then
  echo DORE_PENPOT_MCP_HTTP_PASS
else
  echo "WARN: Penpot MCP process registered but manifest not reachable yet" >&2
  tail -n 20 "$DORE/logs/penpot-mcp.err.log" >&2 2>/dev/null || true
fi
