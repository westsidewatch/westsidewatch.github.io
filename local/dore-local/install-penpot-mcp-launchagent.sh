#!/bin/bash
set -euo pipefail
RUNTIME="$HOME/.dore/runtime/penpot-mcp"
DORE="$HOME/.dore"
PLIST="$HOME/Library/LaunchAgents/io.westsidewatch.penpot-mcp.plist"
LABEL="io.westsidewatch.penpot-mcp"
UIDN="$(id -u)"
DOMAIN="gui/$UIDN"
mkdir -p "$HOME/Library/LaunchAgents" "$DORE/logs"
: > "$DORE/logs/penpot-mcp.log"
: > "$DORE/logs/penpot-mcp.err.log"

NODE="$(command -v node || true)"
if [[ -z "$NODE" ]]; then
  for p in /opt/homebrew/bin/node /usr/local/bin/node; do [[ -x "$p" ]] && NODE="$p" && break; done
fi
[[ -n "$NODE" && -x "$NODE" ]] || { echo "ERROR: node not found" >&2; exit 2; }
[[ -f "$RUNTIME/mcp-bin-path" ]] || { echo "ERROR: persistent Penpot MCP runtime not prepared" >&2; exit 2; }
MCP_BIN="$(cat "$RUNTIME/mcp-bin-path")"
COREPACK="$(cat "$RUNTIME/corepack-path")"
[[ -f "$MCP_BIN" ]] || { echo "ERROR: Penpot MCP executable missing: $MCP_BIN" >&2; exit 2; }
[[ -x "$COREPACK" ]] || { echo "ERROR: corepack missing: $COREPACK" >&2; exit 2; }
LOCALBIN="$RUNTIME/node_modules/.bin"
NODEDIR="$(dirname "$NODE")"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>$LABEL</string>
<key>ProgramArguments</key><array><string>$NODE</string><string>$MCP_BIN</string></array>
<key>EnvironmentVariables</key><dict>
 <key>PATH</key><string>$LOCALBIN:$NODEDIR:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
</dict>
<key>RunAtLoad</key><true/>
<key>KeepAlive</key><true/>
<key>ProcessType</key><string>Background</string>
<key>LimitLoadToSessionType</key><string>Aqua</string>
<key>StandardOutPath</key><string>$DORE/logs/penpot-mcp.log</string>
<key>StandardErrorPath</key><string>$DORE/logs/penpot-mcp.err.log</string>
<key>WorkingDirectory</key><string>$RUNTIME</string>
</dict></plist>
EOF

plutil -lint "$PLIST"
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl unload "$PLIST" 2>/dev/null || true
if ! launchctl bootstrap "$DOMAIN" "$PLIST" 2>"$DORE/logs/penpot-mcp-bootstrap.err"; then launchctl load -w "$PLIST"; fi
launchctl enable "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl kickstart -k "$DOMAIN/$LABEL" 2>/dev/null || true

ok=0
for _ in 1 2 3 4 5 6 7 8 9 10; do
  if curl -fsS http://127.0.0.1:4400/manifest.json >/dev/null 2>&1; then ok=1; break; fi
  sleep 2
done

if launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1; then echo DORE_PENPOT_MCP_AUTOSTART_REGISTERED; else echo "ERROR: Penpot MCP LaunchAgent not registered" >&2; exit 3; fi
if [[ "$ok" == 1 ]]; then
  echo DORE_PENPOT_MCP_HTTP_PASS
else
  echo "ERROR: Penpot MCP runtime failed to expose plugin manifest" >&2
  echo "--- LaunchAgent state ---" >&2
  launchctl print "$DOMAIN/$LABEL" 2>&1 | tail -n 45 >&2 || true
  echo "--- stderr ---" >&2
  tail -n 45 "$DORE/logs/penpot-mcp.err.log" >&2 || true
  echo "--- stdout ---" >&2
  tail -n 45 "$DORE/logs/penpot-mcp.log" >&2 || true
  exit 4
fi
