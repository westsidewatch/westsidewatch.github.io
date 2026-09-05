#!/bin/bash
set -euo pipefail

# DORÉ A2A Companion clean installer/updater for macOS.
# Downloads a fresh main snapshot, installs it under Application Support, and
# registers one per-user LaunchAgent. No git checkout/cherry-pick is involved.

REPO="westsidewatch/westsidewatch.github.io"
ARCHIVE_URL="https://github.com/${REPO}/archive/refs/heads/main.zip"
APP_ROOT="$HOME/Library/Application Support/DoreA2A"
RELEASES="$APP_ROOT/releases"
CURRENT="$APP_ROOT/current"
LOG_DIR="$APP_ROOT/logs"
LABEL="io.westsidewatch.dore-a2a-companion"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
PORT="4312"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/dore-a2a-install.XXXXXX")"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RELEASE="$RELEASES/$STAMP"

cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "DORÉ installer requires macOS." >&2
  exit 2
fi

PYTHON3="$(command -v python3 || true)"
if [[ -z "$PYTHON3" ]]; then
  echo "Python 3 is required. Install Apple's Command Line Tools or Python 3, then rerun." >&2
  exit 3
fi

mkdir -p "$RELEASES" "$LOG_DIR" "$HOME/Library/LaunchAgents"

echo "[1/5] Downloading clean DORÉ main snapshot..."
curl -fL --retry 3 --connect-timeout 15 "$ARCHIVE_URL" -o "$TMP/main.zip"
mkdir -p "$TMP/unpack"
ditto -x -k "$TMP/main.zip" "$TMP/unpack"
SRC="$(find "$TMP/unpack" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
[[ -n "$SRC" && -f "$SRC/local/dore-local/companion_4312.py" ]] || { echo "Downloaded snapshot is incomplete." >&2; exit 4; }

# Preflight the exact downloaded runtime before touching the live service.
echo "[2/5] Preflighting downloaded runtime..."
PYTHONPATH="$SRC" DORE_REPO_ROOT="$SRC" "$PYTHON3" - <<'PY'
import importlib.util, json, os, pathlib
p=pathlib.Path(os.environ['DORE_REPO_ROOT'])/'local'/'dore-local'/'companion_4312.py'
s=importlib.util.spec_from_file_location('dore_companion_preflight', p)
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
h=m.health_payload()
assert h['ok'] and h['service']=='dore-a2a-plus' and h['protocol']=='dore.a2a/1'
code, legacy=m.route_payload({'capability':'design2.stage2.acceptance'})
assert code==200 and legacy['status']=='PASS'
code, typed=m.route_payload({'protocol':'dore.a2a/1','action':'discover'})
assert code==200 and typed['status']=='succeeded'
assert any(c['id']=='design' for c in typed['consumers'])
print(json.dumps({'preflight':'PASS','service':h['service'],'protocol':h['protocol']}))
PY

mkdir -p "$RELEASE"
ditto "$SRC" "$RELEASE/repo"
ln -sfn "$RELEASE" "$APP_ROOT/current.new"
mv -f "$APP_ROOT/current.new" "$CURRENT"

# Remove only old DORÉ user LaunchAgents that explicitly reference this service
# or port, then stop any stale listener on 4312. This avoids parallel daemons.
echo "[3/5] Replacing old DORÉ resident..."
DOMAIN="gui/$(id -u)"
launchctl bootout "$DOMAIN/$LABEL" >/dev/null 2>&1 || true
for old in "$HOME"/Library/LaunchAgents/*dore*.plist "$HOME"/Library/LaunchAgents/*Dore*.plist; do
  [[ -f "$old" && "$old" != "$PLIST" ]] || continue
  if grep -Eqi '4312|dore-a2a|dore_a2a|dore-local' "$old"; then
    launchctl bootout "$DOMAIN" "$old" >/dev/null 2>&1 || launchctl unload "$old" >/dev/null 2>&1 || true
  fi
done
STALE="$(lsof -tiTCP:${PORT} -sTCP:LISTEN 2>/dev/null || true)"
if [[ -n "$STALE" ]]; then
  kill $STALE >/dev/null 2>&1 || true
  for _ in 1 2 3 4 5; do
    sleep 0.2
    lsof -tiTCP:${PORT} -sTCP:LISTEN >/dev/null 2>&1 || break
  done
fi

cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${PYTHON3}</string>
    <string>${CURRENT}/repo/local/dore-local/companion_4312.py</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>DORE_REPO_ROOT</key><string>${CURRENT}/repo</string>
    <key>PYTHONUNBUFFERED</key><string>1</string>
  </dict>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>ProcessType</key><string>Interactive</string>
  <key>StandardOutPath</key><string>${LOG_DIR}/companion.out.log</string>
  <key>StandardErrorPath</key><string>${LOG_DIR}/companion.err.log</string>
</dict>
</plist>
PLIST
plutil -lint "$PLIST" >/dev/null

echo "[4/5] Installing LaunchAgent..."
launchctl bootstrap "$DOMAIN" "$PLIST"
launchctl kickstart -k "$DOMAIN/$LABEL"

# Health acceptance: wait up to ~10 seconds and validate the exact contract.
echo "[5/5] Verifying localhost:${PORT}..."
PASS=0
for _ in $(seq 1 40); do
  BODY="$(curl -fsS --max-time 1 "http://127.0.0.1:${PORT}/health" 2>/dev/null || true)"
  if [[ -n "$BODY" ]] && BODY="$BODY" "$PYTHON3" - <<'PY' >/dev/null 2>&1
import json, os
h=json.loads(os.environ['BODY'])
assert h.get('ok') is True
assert h.get('service')=='dore-a2a-plus'
assert h.get('protocol')=='dore.a2a/1'
assert any(x.get('id')=='design2.stage2.acceptance' and x.get('available') for x in h.get('capabilities',[]))
assert any(x.get('id')=='design.compose' and x.get('available') for x in h.get('capabilities',[]))
PY
  then PASS=1; break; fi
  sleep 0.25
done

if [[ "$PASS" != "1" ]]; then
  echo "DORÉ service failed health acceptance. Log: $LOG_DIR/companion.err.log" >&2
  tail -n 30 "$LOG_DIR/companion.err.log" >&2 2>/dev/null || true
  exit 5
fi

# Keep only the newest three clean releases.
find "$RELEASES" -mindepth 1 -maxdepth 1 -type d -print0 | xargs -0 ls -dt 2>/dev/null | tail -n +4 | while IFS= read -r old; do rm -rf "$old"; done || true

echo "DORÉ A2A Companion: PASS"
echo "service=dore-a2a-plus protocol=dore.a2a/1 port=4312"
