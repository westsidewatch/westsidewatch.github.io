#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNTIME="$HOME/.dore/runtime/penpot-mcp"
VISION_MODEL="${DORE_LOCAL_VISION_MODEL:-qwen3-vl:8b}"

command -v brew >/dev/null || { echo "ERROR: Homebrew is required to provision isolated Node 22 for Penpot MCP." >&2; exit 2; }
command -v ollama >/dev/null || { echo "ERROR: Ollama is required." >&2; exit 2; }

# Penpot MCP is tested against Node 22.x. Keep its runtime isolated from the
# user's default Node so newer Node/Corepack changes cannot break Doré.
NODE22_PREFIX="$(brew --prefix node@22 2>/dev/null || true)"
if [[ -z "$NODE22_PREFIX" || ! -x "$NODE22_PREFIX/bin/node" ]]; then
  echo "Installing isolated Node 22 runtime for Penpot MCP..."
  brew install node@22
  NODE22_PREFIX="$(brew --prefix node@22)"
fi
NODE22="$NODE22_PREFIX/bin/node"
NPM22="$NODE22_PREFIX/bin/npm"
NPX22="$NODE22_PREFIX/bin/npx"
[[ -x "$NODE22" && -x "$NPM22" && -x "$NPX22" ]] || { echo "ERROR: Node 22 runtime incomplete at $NODE22_PREFIX" >&2; exit 3; }

echo "Penpot MCP Node: $($NODE22 --version) ($NODE22)"

mkdir -p "$RUNTIME"
cd "$RUNTIME"
# Remove artifacts created by a different Node generation before reinstalling.
rm -rf node_modules package-lock.json
if [[ ! -f package.json ]]; then "$NPM22" init -y >/dev/null 2>&1; fi
PATH="$NODE22_PREFIX/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin" "$NPM22" install --save-exact @penpot/mcp@2.15.4

PKG="$RUNTIME/node_modules/@penpot/mcp/package.json"
[[ -f "$PKG" ]] || { echo "ERROR: @penpot/mcp package not installed" >&2; exit 3; }
BIN_REL="$($NODE22 -e 'const p=require(process.argv[1]); const b=p.bin; console.log(typeof b==="string"?b:(b&&Object.values(b)[0])||"")' "$PKG")"
[[ -n "$BIN_REL" ]] || { echo "ERROR: @penpot/mcp package has no executable bin" >&2; exit 3; }
MCP_BIN="$RUNTIME/node_modules/@penpot/mcp/$BIN_REL"
[[ -f "$MCP_BIN" ]] || { echo "ERROR: resolved Penpot MCP executable missing: $MCP_BIN" >&2; exit 3; }

printf '%s\n' "$MCP_BIN" > "$RUNTIME/mcp-bin-path"
printf '%s\n' "$NODE22" > "$RUNTIME/node-path"
printf '%s\n' "$NODE22_PREFIX/bin" > "$RUNTIME/node-bin-dir"

echo "Penpot MCP runtime: $RUNTIME"
echo "Penpot MCP executable: $MCP_BIN"

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
