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
# @penpot/mcp currently invokes `corepack` internally on some Node installs.
# Newer Homebrew Node distributions may omit the corepack executable, so keep
# a project-local copy and expose it only to the Penpot MCP LaunchAgent.
npm install --no-save --omit=dev corepack

if [[ ! -x "$HERE/penpot-mcp/node_modules/.bin/corepack" ]]; then
  echo "ERROR: local corepack shim was not installed" >&2
  exit 3
fi

echo "Pulling Doré visual verification model: $VISION_MODEL"
ollama pull "$VISION_MODEL"

bash "$HERE/install-penpot-mcp-launchagent.sh"

cat <<EOF
DORE_PENPOT_MCP_PREP_PASS

Penpot MCP is now registered as a persistent per-user LaunchAgent.
Local corepack shim: $HERE/penpot-mcp/node_modules/.bin/corepack
Plugin manifest: http://localhost:4400/manifest.json
MCP endpoint: http://localhost:4401/mcp
Verification command:
  node local/dore-local/penpot-mcp/client.mjs status
EOF
