#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd -P)"
DORE="$HOME/.dore"
IMAGE_HOME="$DORE/image"
PLIST="$HOME/Library/LaunchAgents/io.westsidewatch.dore-image-local.plist"
COMFY_PLIST="$HOME/Library/LaunchAgents/io.westsidewatch.dore-comfyui.plist"
LABEL="io.westsidewatch.dore-image-local"
COMFY_LABEL="io.westsidewatch.dore-comfyui"
UIDN="$(id -u)"
DOMAIN="gui/$UIDN"
PY="$(command -v python3)"
mkdir -p "$HOME/Library/LaunchAgents" "$DORE/logs" "$IMAGE_HOME"
touch "$DORE/logs/image-local.log" "$DORE/logs/image-local.err.log" "$DORE/logs/comfyui.log" "$DORE/logs/comfyui.err.log"

probe_comfy(){ curl -fsS --max-time 2 http://127.0.0.1:8188/system_stats >/dev/null 2>&1 || curl -fsS --max-time 2 http://127.0.0.1:8188/ >/dev/null 2>&1; }

if ! probe_comfy; then
  COMFY_MAIN=""
  for p in "$HOME/ComfyUI/main.py" "$HOME/Documents/ComfyUI/main.py" "$HOME/Applications/ComfyUI/main.py"; do
    if [ -f "$p" ]; then COMFY_MAIN="$p"; break; fi
  done
  if [ -n "$COMFY_MAIN" ]; then
    COMFY_DIR="$(dirname "$COMFY_MAIN")"
    COMFY_PY="$PY"
    for p in "$COMFY_DIR/.venv/bin/python" "$COMFY_DIR/venv/bin/python"; do
      if [ -x "$p" ]; then COMFY_PY="$p"; break; fi
    done
    cat > "$COMFY_PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>$COMFY_LABEL</string>
<key>ProgramArguments</key><array><string>$COMFY_PY</string><string>$COMFY_MAIN</string><string>--listen</string><string>127.0.0.1</string><string>--port</string><string>8188</string></array>
<key>RunAtLoad</key><true/><key>KeepAlive</key><true/><key>ProcessType</key><string>Background</string>
<key>WorkingDirectory</key><string>$COMFY_DIR</string>
<key>StandardOutPath</key><string>$DORE/logs/comfyui.log</string><key>StandardErrorPath</key><string>$DORE/logs/comfyui.err.log</string>
</dict></plist>
EOF
    plutil -lint "$COMFY_PLIST" >/dev/null
    launchctl bootout "$DOMAIN/$COMFY_LABEL" 2>/dev/null || true
    launchctl bootstrap "$DOMAIN" "$COMFY_PLIST" 2>/dev/null || launchctl load -w "$COMFY_PLIST"
    launchctl enable "$DOMAIN/$COMFY_LABEL" 2>/dev/null || true
    launchctl kickstart -k "$DOMAIN/$COMFY_LABEL" 2>/dev/null || true
    for _ in $(seq 1 30); do probe_comfy && break; sleep 2; done
  fi
fi

if ! probe_comfy; then
  echo "ERROR: ComfyUI renderer not reachable on 127.0.0.1:8188 and no supported local install was discovered" >&2
  exit 20
fi

MODEL="$($PY - <<'PY'
import json, urllib.request
u='http://127.0.0.1:8188/object_info/CheckpointLoaderSimple'
try:
    with urllib.request.urlopen(u,timeout=5) as r: d=json.load(r)
    node=d.get('CheckpointLoaderSimple') or d
    vals=((node.get('input') or {}).get('required') or {}).get('ckpt_name') or []
    choices=vals[0] if isinstance(vals,list) and vals else []
    print(choices[0] if isinstance(choices,list) and choices else '')
except Exception:
    print('')
PY
)"
if [ -z "$MODEL" ]; then
  echo "ERROR: ComfyUI is reachable but no checkpoint model is available" >&2
  exit 21
fi

CONFIG="$IMAGE_HOME/resident.json"
cat > "$CONFIG" <<EOF
{
  "schema": "dore.image.resident.v1",
  "endpoint": "http://127.0.0.1:8188",
  "model": $(printf '%s' "$MODEL" | "$PY" -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),
  "template": "dore-image/workflows/editorial-basic.json",
  "output_dir": "dore-image/generated"
}
EOF

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>$LABEL</string>
<key>ProgramArguments</key><array><string>$PY</string><string>$ROOT/scripts/dore_image_local_api.py</string></array>
<key>EnvironmentVariables</key><dict><key>DORE_IMAGE_CONFIG</key><string>$CONFIG</string></dict>
<key>RunAtLoad</key><true/><key>KeepAlive</key><true/><key>ProcessType</key><string>Background</string>
<key>WorkingDirectory</key><string>$ROOT</string>
<key>StandardOutPath</key><string>$DORE/logs/image-local.log</string><key>StandardErrorPath</key><string>$DORE/logs/image-local.err.log</string>
</dict></plist>
EOF
plutil -lint "$PLIST" >/dev/null
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl unload "$PLIST" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$PLIST" 2>/dev/null || launchctl load -w "$PLIST"
launchctl enable "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl kickstart -k "$DOMAIN/$LABEL" 2>/dev/null || true
for _ in $(seq 1 20); do
  if curl -fsS --max-time 2 http://127.0.0.1:8790/health | grep -q '"renderer": true'; then
    echo DORE_IMAGE_LOCAL_PASS
    exit 0
  fi
  sleep 1
done
echo "ERROR: Doré Image Local did not reach renderer-ready health" >&2
cat "$DORE/logs/image-local.err.log" >&2 2>/dev/null || true
exit 22
