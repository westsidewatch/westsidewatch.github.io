#!/bin/bash
set -euo pipefail

# Install the DORÉ Native Messaging host for the current Firefox Companion.
# Firefox owns host process lifetime; this script installs no daemon/LaunchAgent.

HOST_NAME="io.westsidewatch.dore"
APP_ROOT="$HOME/Library/Application Support/DoreA2A"
HOST_ROOT="$APP_ROOT/native-host"
HOST_BIN="$HOST_ROOT/dore-native-host"
MANIFEST_DIR="$HOME/Library/Application Support/Mozilla/NativeMessagingHosts"
MANIFEST="$MANIFEST_DIR/$HOST_NAME.json"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON3="$(command -v python3 || true)"
EXTENSION_ID="${1:-${DORE_COMPANION_EXTENSION_ID:-}}"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "DORÉ Native Messaging installer requires macOS." >&2
  exit 2
fi
if [[ -z "$PYTHON3" ]]; then
  echo "Python 3 is required." >&2
  exit 3
fi
if [[ -z "$EXTENSION_ID" ]]; then
  echo "Companion extension ID is required: $0 <firefox-extension-id>" >&2
  exit 4
fi
if [[ ! -f "$SCRIPT_DIR/native_host.py" || ! -f "$SCRIPT_DIR/a2a_adapter.py" ]]; then
  echo "DORÉ native host files are incomplete." >&2
  exit 5
fi

mkdir -p "$HOST_ROOT" "$MANIFEST_DIR"

# Use a stable executable wrapper because Firefox manifests accept one absolute
# executable path, not an interpreter plus arguments.
cat > "$HOST_BIN" <<EOF
#!/bin/bash
set -euo pipefail
export DORE_REPO_ROOT="$REPO_ROOT"
exec "$PYTHON3" "$SCRIPT_DIR/native_host.py"
EOF
chmod 700 "$HOST_BIN"

HOST_BIN="$HOST_BIN" EXTENSION_ID="$EXTENSION_ID" "$PYTHON3" - <<'PY' > "$MANIFEST.tmp"
import json, os
print(json.dumps({
    "name": "io.westsidewatch.dore",
    "description": "DORÉ local A2A Native Messaging host",
    "path": os.environ["HOST_BIN"],
    "type": "stdio",
    "allowed_extensions": [os.environ["EXTENSION_ID"]],
}, ensure_ascii=False, indent=2))
PY
mv -f "$MANIFEST.tmp" "$MANIFEST"
chmod 600 "$MANIFEST"

# Host-only smoke: exercise Firefox's exact 4-byte LE framing without starting
# localhost:4312 and without creating any persistent process.
HOST_BIN="$HOST_BIN" "$PYTHON3" - <<'PY'
import json, os, struct, subprocess
p=subprocess.Popen([os.environ['HOST_BIN']], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
msg=json.dumps({'type':'dore.native.health'}, separators=(',',':')).encode()
p.stdin.write(struct.pack('<I',len(msg))+msg); p.stdin.flush()
header=p.stdout.read(4)
assert len(header)==4, p.stderr.read().decode('utf-8','replace')
size=struct.unpack('<I',header)[0]
body=json.loads(p.stdout.read(size))
assert body['ok'] is True
assert body['service']=='dore-native-host'
assert body['protocol']=='dore.a2a/1'
assert body['transport']=='native-messaging'
p.terminate(); p.wait(timeout=2)
print('DORÉ Native Messaging host: PASS')
PY

echo "manifest=$MANIFEST"
echo "host=$HOST_BIN"
echo "extension=$EXTENSION_ID"
