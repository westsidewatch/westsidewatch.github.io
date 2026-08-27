#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNTIME="$HOME/.dore/runtime/penpot-mcp"
VISION_MODEL="${DORE_LOCAL_VISION_MODEL:-qwen3-vl:8b}"

command -v node >/dev/null || { echo "ERROR: Node.js is required for Penpot MCP." >&2; exit 2; }
command -v npm >/dev/null || { echo "ERROR: npm is required for Penpot MCP." >&2; exit 2; }
command -v ollama >/dev/null || { echo "ERROR: Ollama is required." >&2; exit 2; }

mkdir -p "$RUNTIME"
cd "$RUNTIME"
if [[ ! -f package.json ]]; then npm init -y >/dev/null 2>&1; fi

# Keep Penpot MCP outside npm's transient _npx cache. Repeated npx runs can prune
# Penpot's nested pnpm virtual store, so install the released package once into a
# persistent Doré runtime and launch its actual package binary directly.
npm install --save-exact @penpot/mcp@2.15.4 corepack

COREPACK="$RUNTIME/node_modules/.bin/corepack"
[[ -x "$COREPACK" ]] || { echo "ERROR: persistent corepack executable missing" >&2; exit 3; }

PKG="$RUNTIME/node_modules/@penpot/mcp/package.json"
[[ -f "$PKG" ]] || { echo "ERROR: @penpot/mcp package not installed" >&2; exit 3; }
BIN_REL="$(node -e 'const p=require(process.argv[1]); const b=p.bin; console.log(typeof b==="string"?b:(b&&Object.values(b)[0])||"")' "$PKG")"
[[ -n "$BIN_REL" ]] || { echo "ERROR: @penpot/mcp package has no executable bin" >&2; exit 3; }
MCP_BIN="$RUNTIME/node_modules/@penpot/mcp/$BIN_REL"
[[ -f "$MCP_BIN" ]] || { echo "ERROR: resolved Penpot MCP executable missing: $MCP_BIN" >&2; exit 3; }

printf '%s\n' "$MCP_BIN" > "$RUNTIME/mcp-bin-path"
printf '%s\n' "$COREPACK" > "$RUNTIME/corepack-path"

echo "Penpot MCP runtime: $RUNTIME"
echo "Penpot MCP executable: $MCP_BIN"
echo "Corepack: $COREPACK"

echo "Pulling Doré visual verification model: $VISION_MODEL"
ollama pull "$VISION_MODEL"

bash "$HERE/install-penpot-mcp-launchagent.sh"

cat <<EOF
DORE_PENPOT_MCP_PREP_PASS
Plugin manifest: http://localhost:4400/manifest.json
MCP endpoint: http://localhost:4401/mcp
Verification command:
  node local/dore-local/penpot-mcp/client.mjs status
EOF
