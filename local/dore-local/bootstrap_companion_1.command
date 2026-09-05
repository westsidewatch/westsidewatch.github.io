#!/bin/bash
set -euo pipefail

# DORÉ Companion 1.0 — one-shot macOS bootstrap.
# Deliberately does NOT read, pull, reset, merge, rebase, or modify the user's
# ~/westsidewatch.github.io checkout. A divergent working tree is irrelevant.
# Runtime cost: zero paid APIs/cloud services.

REPO="westsidewatch/westsidewatch.github.io"
ARCHIVE_URL="https://github.com/${REPO}/archive/refs/heads/main.zip"
APP_ROOT="$HOME/Library/Application Support/DoreA2A"
RELEASES="$APP_ROOT/native-releases"
CURRENT="$APP_ROOT/native-current"
EXT_DIR="$APP_ROOT/companion-1.0"
HOST_NAME="ca.dore.companion"
EXTENSION_ID="dore-companion@westsidewatch.ca"
MANIFEST_DIR="$HOME/Library/Application Support/Mozilla/NativeMessagingHosts"
HOST_MANIFEST="$MANIFEST_DIR/${HOST_NAME}.json"
LAUNCHER="$APP_ROOT/dore-native-host"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/dore-companion1.XXXXXX")"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RELEASE="$RELEASES/$STAMP"

cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

fail() {
  printf '\nDORÉ Companion 1.0 bootstrap: FAIL\n%s\n' "$1" >&2
  printf '\nPress Return to close...'
  read -r _ || true
  exit 1
}

[[ "$(uname -s)" == "Darwin" ]] || fail "This bootstrap requires macOS."
PYTHON3="$(command -v python3 || true)"
[[ -n "$PYTHON3" ]] || fail "Python 3 is required."
command -v curl >/dev/null 2>&1 || fail "curl is required."
command -v ditto >/dev/null 2>&1 || fail "ditto is required."

printf '\nDORÉ Companion 1.0 — zero-cost bootstrap\n'
printf 'Local Git checkout: untouched\n\n'

printf '[1/5] Downloading clean main snapshot...\n'
curl -fL --retry 3 --connect-timeout 15 "$ARCHIVE_URL" -o "$TMP/main.zip" || fail "Could not download DORÉ main snapshot."
mkdir -p "$TMP/unpack"
ditto -x -k "$TMP/main.zip" "$TMP/unpack"
SRC="$(find "$TMP/unpack" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
[[ -n "$SRC" ]] || fail "Downloaded snapshot could not be unpacked."
[[ -f "$SRC/local/dore-local/native_host.py" ]] || fail "Native host missing from downloaded main."
[[ -f "$SRC/local/dore-local/a2a_adapter.py" ]] || fail "A2A adapter missing from downloaded main."
[[ -f "$SRC/local/dore-local/test_native_host.py" ]] || fail "Native host test missing from downloaded main."
[[ -f "$SRC/local/dore-companion-extension/manifest.json" ]] || fail "Companion 1.0 manifest missing from downloaded main."
[[ -f "$SRC/local/dore-companion-extension/background.js" ]] || fail "Companion 1.0 background bridge missing."
[[ -f "$SRC/local/dore-companion-extension/content_script.js" ]] || fail "Companion 1.0 content script missing."
[[ -f "$SRC/local/dore-companion-extension/native_transport.js" ]] || fail "Companion 1.0 native transport missing."

printf '[2/5] Preflighting exact downloaded Native Host...\n'
PYTHONPATH="$SRC" DORE_REPO_ROOT="$SRC" "$PYTHON3" "$SRC/local/dore-local/test_native_host.py" || fail "Native Host preflight failed."

printf '[3/5] Installing Native Messaging host...\n'
mkdir -p "$RELEASES" "$MANIFEST_DIR" "$APP_ROOT"
mkdir -p "$RELEASE"
ditto "$SRC" "$RELEASE/repo"
ln -sfn "$RELEASE" "$APP_ROOT/native-current.new"
mv -f "$APP_ROOT/native-current.new" "$CURRENT"

cat > "$LAUNCHER" <<EOF
#!/bin/bash
set -euo pipefail
export DORE_REPO_ROOT="${CURRENT}/repo"
exec "${PYTHON3}" "${CURRENT}/repo/local/dore-local/native_host.py"
EOF
chmod 755 "$LAUNCHER"

cat > "$HOST_MANIFEST" <<EOF
{
  "name": "${HOST_NAME}",
  "description": "DORÉ local A2A Native Messaging host",
  "path": "${LAUNCHER}",
  "type": "stdio",
  "allowed_extensions": ["${EXTENSION_ID}"]
}
EOF
chmod 644 "$HOST_MANIFEST"

HOST_MANIFEST="$HOST_MANIFEST" "$PYTHON3" - <<'PY' || fail "Native Messaging manifest validation failed."
import json, os
p=os.environ['HOST_MANIFEST']
with open(p, encoding='utf-8') as f:
    m=json.load(f)
assert m['name']=='ca.dore.companion'
assert m['type']=='stdio'
assert os.path.isabs(m['path'])
assert m['allowed_extensions']==['dore-companion@westsidewatch.ca']
print('Native Messaging manifest: PASS')
PY

printf '[4/5] Staging Companion 1.0 extension...\n'
rm -rf "$EXT_DIR.new"
mkdir -p "$EXT_DIR.new"
ditto "$SRC/local/dore-companion-extension" "$EXT_DIR.new"
rm -rf "$EXT_DIR"
mv "$EXT_DIR.new" "$EXT_DIR"

EXT_DIR="$EXT_DIR" "$PYTHON3" - <<'PY' || fail "Companion 1.0 extension validation failed."
import json, os, pathlib
p=pathlib.Path(os.environ['EXT_DIR'])
m=json.loads((p/'manifest.json').read_text(encoding='utf-8'))
assert m['version']=='1.0.0'
assert 'nativeMessaging' in m['permissions']
assert m['browser_specific_settings']['gecko']['id']=='dore-companion@westsidewatch.ca'
for name in ('background.js','content_script.js','native_transport.js'):
    assert (p/name).is_file(), name
print('Companion 1.0 extension: PASS')
PY

# Keep newest three Native Host snapshots.
find "$RELEASES" -mindepth 1 -maxdepth 1 -type d -print0 | xargs -0 ls -dt 2>/dev/null | tail -n +4 | while IFS= read -r old; do rm -rf "$old"; done || true

printf '[5/5] Opening the only remaining Firefox security gate...\n'
open "$EXT_DIR" >/dev/null 2>&1 || true
open "about:debugging#/runtime/this-firefox" >/dev/null 2>&1 || true

printf '\nDORÉ Companion 1.0 bootstrap: PASS\n'
printf 'Native Host: installed\n'
printf 'Extension: %s\n' "$EXT_DIR"
printf 'Local Git checkout: untouched\n'
printf '\nFirefox now only needs its own security UI action: load manifest.json from the opened Companion 1.0 folder.\n'
printf 'If Companion 0.11 is still loaded temporarily, remove it in about:debugging first, then load 1.0.\n'
printf '\nPress Return after Firefox is ready...'
read -r _ || true
