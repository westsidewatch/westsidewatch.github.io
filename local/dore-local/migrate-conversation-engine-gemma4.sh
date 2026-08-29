#!/usr/bin/env bash
set -euo pipefail
ROOT="${DORE_LOCAL_HOME:-$HOME/.dore}"
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
ENV="$ROOT/node.env"
MODEL="gemma4:e4b"

command -v ollama >/dev/null || { echo 'MIGRATION_BLOCKED: ollama missing' >&2; exit 2; }
curl -fsS http://127.0.0.1:11434/api/tags >/dev/null || { echo 'MIGRATION_BLOCKED: ollama not running' >&2; exit 3; }

echo "[1/5] Pull $MODEL"
ollama pull "$MODEL"

echo "[2/5] Smoke-test engine directly"
OUT="$(curl -fsS http://127.0.0.1:11434/api/chat -H 'Content-Type: application/json' -d '{"model":"gemma4:e4b","messages":[{"role":"system","content":"You are the replaceable inference engine for Doré. Reply only ENGINE_PASS."},{"role":"user","content":"health check"}],"stream":false}')"
printf '%s' "$OUT" | grep -q 'ENGINE_PASS' || { echo 'MIGRATION_BLOCKED: Gemma smoke test failed' >&2; exit 4; }

echo "[3/5] Switch Doré node.env without touching memory"
mkdir -p "$ROOT"
if [[ -f "$ENV" ]]; then cp "$ENV" "$ENV.pre-gemma4-$(date -u +%Y%m%dT%H%M%SZ).bak"; fi
python3 - "$ENV" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); lines=p.read_text().splitlines() if p.exists() else []
out=[]; seen=False
for line in lines:
    if line.startswith('DORE_LOCAL_MODEL='):
        out.append('DORE_LOCAL_MODEL=gemma4:e4b'); seen=True
    else: out.append(line)
if not seen: out.append('DORE_LOCAL_MODEL=gemma4:e4b')
p.write_text('\n'.join(out)+'\n')
PY
chmod 600 "$ENV"

echo "[4/5] Restart Doré Local"
launchctl kickstart -k "gui/$(id -u)/io.westsidewatch.dore-local"
for _ in $(seq 1 30); do
  if HEALTH="$(curl -fsS http://127.0.0.1:8788/health 2>/dev/null)"; then
    if printf '%s' "$HEALTH" | grep -q 'gemma4:e4b'; then break; fi
  fi
  sleep 1
done
HEALTH="$(curl -fsS http://127.0.0.1:8788/health)"
printf '%s' "$HEALTH" | grep -q 'gemma4:e4b' || { echo "MIGRATION_BLOCKED: Doré did not restart on $MODEL" >&2; exit 5; }

echo "[5/5] Doré identity/conversation smoke test"
CID="engine-migration-$(date -u +%Y%m%dT%H%M%SZ)"
CHAT="$(curl -fsS http://127.0.0.1:8788/chat -H 'Content-Type: application/json' -d "{\"conversation_id\":\"$CID\",\"project_id\":\"dore-global\",\"message\":\"你是誰？你目前使用什麼本地推理引擎？請簡短回答。\"}")"
printf '%s\n' "$HEALTH" > "$ROOT/logs/gemma4-migration-health.json"
printf '%s\n' "$CHAT" > "$ROOT/logs/gemma4-migration-chat.json"
echo "DORE_GEMMA4_E4B_MIGRATION_PASS"
