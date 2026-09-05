#!/bin/bash
set -euo pipefail

# Install DORÉ as a Firefox Native Messaging host on macOS.
# No LaunchAgent, resident daemon, paid API, OpenAI API, or GitHub runtime bus.

REPO="westsidewatch/westsidewatch.github.io"
ARCHIVE_URL="https://github.com/${REPO}/archive/refs/heads/main.zip"
APP_ROOT="$HOME/Library/Application Support/DoreA2A"
RELEASES="$APP_ROOT/native-releases"
CURRENT="$APP_ROOT/native-current"
HOST_NAME="ca.dore.companion"
EXTENSION_ID="${DORE_COMPANION_EXTENSION_ID:-dore-companion@westsidewatch.ca}"
MANIFEST_DIR="$HOME/Library/Application Support/Mozilla/NativeMessagingHosts"
MANIFEST="$MANIFEST_DIR/${HOST_NAME}.json"
LAUNCHER="$APP_ROOT/dore-native-host"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/dore-native-install.XXXXXX")"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RELEASE="$RELEASES/$STAMP"

cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "DORÉ Native Messaging installer requires macOS." >&2
  exit 2
fi

PYTHON3="$(command -v python3 || true)"
if [[ -z "$PYTHON3" ]]; then
  echo "Python 3 is required." >&2
  exit 3
fi

mkdir -p "$RELEASES" "$MANIFEST_DIR" "$APP_ROOT"

echo "[1/4] Downloading DORÉ main snapshot..."
curl -fL --retry 3 --connect-timeout 15 "$ARCHIVE_URL" -o "$TMP/main.zip"
mkdir -p "$TMP/unpack"
ditto -x -k "$TMP/main.zip" "$TMP/unpack"
SRC="$(find "$TMP/unpack" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
[[ -n "$SRC" && -f "$SRC/local/dore-local/native_host.py" && -f "$SRC/local/dore-local/a2a_adapter.py" ]] || {
  echo "Downloaded snapshot does not contain the Native Messaging host yet." >&2
  exit 4
}

echo "[2/4] Preflighting exact downloaded host..."
PYTHONPATH="$SRC" DORE_REPO_ROOT="$SRC" "$PYTHON3" "$SRC/local/dore-local/test_native_host.py"

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

# Native Messaging host manifests require an absolute executable path.
cat > "$MANIFEST" <<EOF
{
  "name": "${HOST_NAME}",
  "description": "DORÉ local A2A Native Messaging host",
  "path": "${LAUNCHER}",
  "type": "stdio",
  "allowed_extensions": ["${EXTENSION_ID}"]
}
EOF
chmod 644 "$MANIFEST"

# JSON syntax and exact contract check.
MANIFEST="$MANIFEST" "$PYTHON3" - <<'PY'
import json, os
p=os.environ['MANIFEST']
with open(p, encoding='utf-8') as f:
    m=json.load(f)
assert m['name']=='ca.dore.companion'
assert m['type']=='stdio'
assert os.path.isabs(m['path'])
assert len(m['allowed_extensions'])==1
print('manifest: PASS')
PY

echo "[3/4] Installed Firefox Native Messaging host."
echo "host=${HOST_NAME} extension_id=${EXTENSION_ID}"
echo "manifest=${MANIFEST}"

# Do not stop the old 4312 service here. It remains a compatibility/debug
# fallback until browser->native->adapter->Design live acceptance passes.
echo "[4/4] 4312 compatibility path left unchanged."

# Keep newest three native snapshots.
find "$RELEASES" -mindepth 1 -maxdepth 1 -type d -print0 | xargs -0 ls -dt 2>/dev/null | tail -n +4 | while IFS= read -r old; do rm -rf "$old"; done || true

echo "DORÉ Native Messaging install: PASS"
