#!/bin/bash
set -euo pipefail

REPO="westsidewatch/westsidewatch.github.io"
ARCHIVE_URL="https://github.com/${REPO}/archive/refs/heads/main.zip"
APP_ROOT="$HOME/Library/Application Support/DoreA2A"
EXT_ROOT="$APP_ROOT/companion-1.0"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/dore-companion-install.XXXXXX")"

cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "DORÉ Companion 1.0 installer requires macOS." >&2
  exit 2
fi

command -v curl >/dev/null || { echo "curl is required." >&2; exit 3; }
command -v python3 >/dev/null || { echo "Python 3 is required." >&2; exit 4; }

echo "[1/5] Downloading current DORÉ main..."
curl -fL --retry 3 --connect-timeout 15 "$ARCHIVE_URL" -o "$TMP/main.zip"
mkdir -p "$TMP/unpack"
ditto -x -k "$TMP/main.zip" "$TMP/unpack"
SRC="$(find "$TMP/unpack" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
[[ -n "$SRC" ]] || { echo "Could not locate downloaded DORÉ source." >&2; exit 5; }

EXT_SRC="$SRC/local/dore-companion-extension"
for required in manifest.json background.js content_script.js native_transport.js; do
  [[ -f "$EXT_SRC/$required" ]] || { echo "Missing Companion file: $required" >&2; exit 6; }
done

python3 - "$EXT_SRC/manifest.json" <<'PY'
import json, sys
p=sys.argv[1]
with open(p, encoding='utf-8') as f: m=json.load(f)
assert m['manifest_version']==2
assert m['version']=='1.0.0'
assert 'nativeMessaging' in m['permissions']
assert m['browser_specific_settings']['gecko']['id']=='dore-companion@westsidewatch.ca'
print('Companion manifest: PASS')
PY

echo "[2/5] Installing Native Messaging host..."
bash "$SRC/local/dore-local/install_native_messaging.sh"

echo "[3/5] Installing Companion 1.0 source bundle..."
rm -rf "$EXT_ROOT"
mkdir -p "$EXT_ROOT"
ditto "$EXT_SRC" "$EXT_ROOT"

cat > "$EXT_ROOT/INSTALL-STATUS.txt" <<EOF
DORÉ Companion 1.0 source installed locally.
Extension ID: dore-companion@westsidewatch.ca
Native host: ca.dore.companion
Path: $EXT_ROOT
Runtime cost: zero metered API/cloud dependency
EOF

echo "[4/5] Opening Firefox extension loader..."
if [[ -d "/Applications/Firefox.app" ]]; then
  open -a Firefox "about:debugging#/runtime/this-firefox" || true
else
  open "about:debugging#/runtime/this-firefox" || true
fi

# Reveal the exact manifest so the user only needs one UI action:
# Load Temporary Add-on -> choose manifest.json.
open -R "$EXT_ROOT/manifest.json" || true

echo "[5/5] Local install prepared."
echo
echo "ONE FIREFOX ACTION REMAINS:"
echo "  Load Temporary Add-on -> select:"
echo "  $EXT_ROOT/manifest.json"
echo
echo "Then refresh ChatGPT. DORÉ A2A should change from OFFLINE to ONLINE."
echo "DORÉ Companion 1.0 local install: READY"
