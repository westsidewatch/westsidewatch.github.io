#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PORT=43127
OUT="${1:-$HOME/Desktop/dore-video-smoke}"
BRIDGE="$ROOT/local/dore-local/video_bridge.py"
SMOKE="$ROOT/local/dore-local/video_smoke_test.py"

cleanup() {
  if [[ -n "${BRIDGE_PID:-}" ]]; then kill "$BRIDGE_PID" 2>/dev/null || true; fi
}
trap cleanup EXIT INT TERM

if ! curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
  python3 "$BRIDGE" --port "$PORT" >"/tmp/dore-video-bridge.log" 2>&1 &
  BRIDGE_PID=$!
  for _ in {1..20}; do
    curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break
    sleep .25
  done
fi

curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null
python3 "$SMOKE" --output "$OUT"
