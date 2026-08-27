#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VISION_MODEL="${DORE_LOCAL_VISION_MODEL:-qwen3-vl:8b}"

command -v node >/dev/null || { echo "ERROR: Node.js is required for Penpot MCP." >&2; exit 2; }
command -v npm >/dev/null || { echo "ERROR: npm is required for Penpot MCP." >&2; exit 2; }
command -v npx >/dev/null || { echo "ERROR: npx is required for Penpot MCP." >&2; exit 2; }
command -v ollama >/dev/null || { echo "ERROR: Ollama is required." >&2; exit 2; }

cd "$HERE/penpot-mcp"
npm install --omit=dev

echo "Pulling Doré visual verification model: $VISION_MODEL"
ollama pull "$VISION_MODEL"

bash "$HERE/install-penpot-mcp-launchagent.sh"

cat <<EOF
DORE_PENPOT_MCP_PREP_PASS

Penpot MCP is now registered as a persistent per-user LaunchAgent.
You no longer need to keep a separate Terminal running npx manually.
Plugin manifest: http://localhost:4400/manifest.json
MCP endpoint: http://localhost:4401/mcp
Verification command:
  node local/dore-local/penpot-mcp/client.mjs status
EOF
