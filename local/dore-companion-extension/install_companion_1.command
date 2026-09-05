#!/bin/bash
set -euo pipefail
REPO="westsidewatch/westsidewatch.github.io";ARCHIVE_URL="https://github.com/${REPO}/archive/refs/heads/main.zip";APP_ROOT="$HOME/Library/Application Support/DoreA2A";EXT_ROOT="$APP_ROOT/companion-current";TMP="$(mktemp -d "${TMPDIR:-/tmp}/dore-companion-install.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
[[ "$(uname -s)" == "Darwin" ]] || { echo "macOS required" >&2;exit 2; }
command -v curl >/dev/null;command -v python3 >/dev/null
curl -fL --retry 3 --connect-timeout 15 "$ARCHIVE_URL" -o "$TMP/main.zip";mkdir -p "$TMP/unpack";ditto -x -k "$TMP/main.zip" "$TMP/unpack";SRC="$(find "$TMP/unpack" -mindepth 1 -maxdepth 1 -type d|head -n1)";EXT_SRC="$SRC/local/dore-companion-extension"
python3 - "$EXT_SRC/manifest.json" <<'PY'
import json,sys
m=json.load(open(sys.argv[1]));assert m['manifest_version']==2;assert 'nativeMessaging' in m['permissions'];assert m['browser_specific_settings']['gecko']['id']=='dore-companion@westsidewatch.ca';print('Companion',m['version'],'manifest: PASS')
PY
bash "$SRC/local/dore-local/install_native_messaging.sh"
rm -rf "$EXT_ROOT";mkdir -p "$EXT_ROOT";ditto "$EXT_SRC" "$EXT_ROOT"
VERSION="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["version"])' "$EXT_ROOT/manifest.json")"
printf 'DORÉ Companion %s\nNative host: ca.dore.companion\nRuntime: zero metered API/cloud dependency\n' "$VERSION" > "$EXT_ROOT/INSTALL-STATUS.txt"
open -a Firefox "about:debugging#/runtime/this-firefox" 2>/dev/null||true;open -R "$EXT_ROOT/manifest.json"||true
echo "DORÉ Companion $VERSION local install: READY"
