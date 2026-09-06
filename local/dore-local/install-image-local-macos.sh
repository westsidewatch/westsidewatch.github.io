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
CONFIG="$IMAGE_HOME/resident.json"
SDCPP_REF="${DORE_SDCPP_REF:-master-802-e92e86f}"
SDCPP_HOME="${DORE_SDCPP_HOME:-$IMAGE_HOME/renderer/stable-diffusion.cpp}"
SDCPP_BIN="$SDCPP_HOME/build/bin/sd-cli"
MODEL_DIR="$IMAGE_HOME/models"
MODEL_NAME="stable-diffusion-v1-4-Q4_0.gguf"
MODEL_PATH="$MODEL_DIR/$MODEL_NAME"
MODEL_URL="${DORE_IMAGE_MODEL_URL:-https://huggingface.co/second-state/stable-diffusion-v-1-4-GGUF/resolve/main/stable-diffusion-v1-4-Q4_0.gguf}"

mkdir -p "$HOME/Library/LaunchAgents" "$DORE/logs" "$IMAGE_HOME" "$MODEL_DIR" "$(dirname "$SDCPP_HOME")"
touch "$DORE/logs/image-local.log" "$DORE/logs/image-local.err.log" "$DORE/logs/comfyui.log" "$DORE/logs/comfyui.err.log"

probe_comfy(){ curl -fsS --max-time 2 http://127.0.0.1:8188/system_stats >/dev/null 2>&1 || curl -fsS --max-time 2 http://127.0.0.1:8188/ >/dev/null 2>&1; }
comfy_model(){ "$PY" - <<'PY'
import json, urllib.request
try:
  with urllib.request.urlopen('http://127.0.0.1:8188/object_info/CheckpointLoaderSimple',timeout=5) as r:d=json.load(r)
  node=d.get('CheckpointLoaderSimple') or d; vals=((node.get('input') or {}).get('required') or {}).get('ckpt_name') or []; choices=vals[0] if isinstance(vals,list) and vals else []
  print(choices[0] if isinstance(choices,list) and choices else '')
except Exception: print('')
PY
}

# Reuse an already healthy ComfyUI installation when it truly has a checkpoint.
if ! probe_comfy; then
  COMFY_MAIN=""
  for p in "$HOME/ComfyUI/main.py" "$HOME/Documents/ComfyUI/main.py" "$HOME/Applications/ComfyUI/main.py"; do [ -f "$p" ] && COMFY_MAIN="$p" && break; done
  if [ -n "$COMFY_MAIN" ]; then
    COMFY_DIR="$(dirname "$COMFY_MAIN")"; COMFY_PY="$PY"
    for p in "$COMFY_DIR/.venv/bin/python" "$COMFY_DIR/venv/bin/python"; do [ -x "$p" ] && COMFY_PY="$p" && break; done
    cat > "$COMFY_PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><dict>
<key>Label</key><string>$COMFY_LABEL</string><key>ProgramArguments</key><array><string>$COMFY_PY</string><string>$COMFY_MAIN</string><string>--listen</string><string>127.0.0.1</string><string>--port</string><string>8188</string></array>
<key>RunAtLoad</key><true/><key>KeepAlive</key><true/><key>ProcessType</key><string>Background</string><key>WorkingDirectory</key><string>$COMFY_DIR</string>
<key>StandardOutPath</key><string>$DORE/logs/comfyui.log</string><key>StandardErrorPath</key><string>$DORE/logs/comfyui.err.log</string></dict></plist>
EOF
    plutil -lint "$COMFY_PLIST" >/dev/null
    launchctl bootout "$DOMAIN/$COMFY_LABEL" 2>/dev/null || true
    launchctl bootstrap "$DOMAIN" "$COMFY_PLIST" 2>/dev/null || launchctl load -w "$COMFY_PLIST"
    launchctl enable "$DOMAIN/$COMFY_LABEL" 2>/dev/null || true; launchctl kickstart -k "$DOMAIN/$COMFY_LABEL" 2>/dev/null || true
    for _ in $(seq 1 20); do probe_comfy && break; sleep 2; done
  fi
fi

MODEL=""
if probe_comfy; then MODEL="$(comfy_model)"; fi
if [ -n "$MODEL" ]; then
  cat > "$CONFIG" <<EOF
{"schema":"dore.image.resident.v2","renderer":"comfyui","endpoint":"http://127.0.0.1:8188","model":$(printf '%s' "$MODEL" | "$PY" -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),"template":"dore-image/workflows/editorial-basic.json","output_dir":"dore-image/generated"}
EOF
else
  # No model-backed renderer exists: self-equip stable-diffusion.cpp instead of
  # silently falling through to the decorative SVG emergency renderer.
  for cmd in git cmake curl; do command -v "$cmd" >/dev/null 2>&1 || { echo "ERROR: required build tool missing: $cmd" >&2; exit 30; }; done
  if [ ! -d "$SDCPP_HOME/.git" ]; then
    rm -rf "$SDCPP_HOME"
    git clone --recursive --depth 1 --branch "$SDCPP_REF" https://github.com/leejet/stable-diffusion.cpp.git "$SDCPP_HOME"
  else
    git -C "$SDCPP_HOME" fetch --depth 1 origin "refs/tags/$SDCPP_REF:refs/tags/$SDCPP_REF" || true
    git -C "$SDCPP_HOME" checkout -f "$SDCPP_REF"
    git -C "$SDCPP_HOME" submodule update --init --recursive --depth 1
  fi
  if [ ! -x "$SDCPP_BIN" ]; then
    cmake -S "$SDCPP_HOME" -B "$SDCPP_HOME/build" -DCMAKE_BUILD_TYPE=Release -DSD_WEBP=OFF -DSD_WEBM=OFF -DGGML_METAL=OFF
    cmake --build "$SDCPP_HOME/build" --config Release --target sd-cli -j 2
  fi
  [ -x "$SDCPP_BIN" ] || { echo "ERROR: stable-diffusion.cpp build did not produce sd-cli" >&2; exit 31; }
  if [ ! -f "$MODEL_PATH" ] || [ "$(wc -c < "$MODEL_PATH" | tr -d ' ')" -lt 1000000000 ]; then
    rm -f "$MODEL_PATH.part"
    curl --fail --location --retry 4 --retry-delay 3 --continue-at - "$MODEL_URL" -o "$MODEL_PATH.part"
    mv "$MODEL_PATH.part" "$MODEL_PATH"
  fi
  BYTES="$(wc -c < "$MODEL_PATH" | tr -d ' ')"
  [ "$BYTES" -ge 1000000000 ] || { echo "ERROR: image model download incomplete: $BYTES bytes" >&2; exit 32; }
  cat > "$CONFIG" <<EOF
{"schema":"dore.image.resident.v2","renderer":"stable-diffusion.cpp","binary":$(printf '%s' "$SDCPP_BIN" | "$PY" -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),"model":$(printf '%s' "$MODEL_PATH" | "$PY" -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),"model_source":$(printf '%s' "$MODEL_URL" | "$PY" -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),"renderer_ref":"$SDCPP_REF","width":512,"height":512,"steps":8,"timeout_seconds":1200,"negative_prompt":"text, watermark, logo, low quality, distorted","output_dir":"dore-image/generated"}
EOF
fi

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><dict>
<key>Label</key><string>$LABEL</string><key>ProgramArguments</key><array><string>$PY</string><string>$ROOT/scripts/dore_image_local_api.py</string></array>
<key>EnvironmentVariables</key><dict><key>DORE_IMAGE_CONFIG</key><string>$CONFIG</string></dict><key>RunAtLoad</key><true/><key>KeepAlive</key><true/><key>ProcessType</key><string>Background</string>
<key>WorkingDirectory</key><string>$ROOT</string><key>StandardOutPath</key><string>$DORE/logs/image-local.log</string><key>StandardErrorPath</key><string>$DORE/logs/image-local.err.log</string></dict></plist>
EOF
plutil -lint "$PLIST" >/dev/null
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true; launchctl unload "$PLIST" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$PLIST" 2>/dev/null || launchctl load -w "$PLIST"; launchctl enable "$DOMAIN/$LABEL" 2>/dev/null || true; launchctl kickstart -k "$DOMAIN/$LABEL" 2>/dev/null || true
for _ in $(seq 1 30); do
  H="$(curl -fsS --max-time 3 http://127.0.0.1:8790/health 2>/dev/null || true)"
  if printf '%s' "$H" | grep -Eq '"renderer_mode": "(comfyui|stable-diffusion.cpp)"' && printf '%s' "$H" | grep -q '"model_backed": true'; then echo "$H"; echo DORE_IMAGE_LOCAL_MODEL_BACKED_PASS; exit 0; fi
  sleep 1
done
echo "ERROR: Doré Image Local model-backed health failed" >&2; cat "$DORE/logs/image-local.err.log" >&2 2>/dev/null || true; exit 33
