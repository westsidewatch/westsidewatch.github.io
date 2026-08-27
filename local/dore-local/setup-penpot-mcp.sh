#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VISION_MODEL="${DORE_LOCAL_VISION_MODEL:-qwen3-vl:8b}"

command -v node >/dev/null || { echo "ERROR: Node.js is required for Penpot MCP." >&2; exit 2; }
command -v npm >/dev/null || { echo "ERROR: npm is required for Penpot MCP." >&2; exit 2; }
command -v npx >/dev/null || { echo "ERROR: npx is required for Penpot MCP." >&2; exit 2; }
command -v ollama >/dev/null || { echo "ERROR: Ollama is required." >&2; exit 2; }

NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
echo "Node.js major: $NODE_MAJOR"

# Penpot MCP 2.15.x still invokes `corepack`. Node 25+ no longer bundles it.
# Install the official Corepack package into the user's current npm prefix when
# it is absent. Homebrew npm prefixes are normally user-writable; fail with a
# precise error rather than silently using a broken MCP runtime.
if ! command -v corepack >/dev/null 2>&1; then
  echo "Corepack is not bundled with this Node.js; installing official corepack package."
  npm install -g corepack@latest
fi
COREPACK="$(command -v corepack || true)"
[[ -n "$COREPACK" && -x "$COREPACK" ]] || { echo "ERROR: corepack installation did not produce an executable" >&2; exit 3; }
echo "Corepack: $COREPACK"
corepack --version

cd "$HERE/penpot-mcp"
npm install --omit=dev

# Keep a project-local fallback too, but the persistent MCP service now prefers
# the verified global executable above.
npm install --no-save --omit=dev corepack@latest

if [[ ! -x "$HERE/penpot-mcp/node_modules/.bin/corepack" ]]; then
  echo "ERROR: local corepack fallback was not installed" >&2
  exit 3
fi

echo "Pulling Doré visual verification model: $VISION_MODEL"
ollama pull "$VISION_MODEL"

COREPACK_BIN="$COREPACK" bash "$HERE/install-penpot-mcp-launchagent.sh"

cat <<EOF
DORE_PENPOT_MCP_PREP_PASS

Penpot MCP is registered as a persistent per-user LaunchAgent.
Verified corepack: $COREPACK
Local fallback: $HERE/penpot-mcp/node_modules/.bin/corepack
Plugin manifest: http://localhost:4400/manifest.json
MCP endpoint: http://localhost:4401/mcp
Verification command:
  node local/dore-local/penpot-mcp/client.mjs status
EOF
