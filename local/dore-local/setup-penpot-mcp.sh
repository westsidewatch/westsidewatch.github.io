#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNTIME="$HOME/.dore/runtime/penpot-mcp"
VISION_MODEL="${DORE_LOCAL_VISION_MODEL:-qwen3-vl:8b}"
LABEL="io.westsidewatch.penpot-mcp"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"

command -v brew >/dev/null || { echo "ERROR: Homebrew is required to provision isolated Node 22 for Penpot MCP." >&2; exit 2; }
command -v ollama >/dev/null || { echo "ERROR: Ollama is required." >&2; exit 2; }

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

# A previously registered KeepAlive LaunchAgent can keep touching the old MCP
# tree while setup removes it, producing macOS 'Directory not empty' races.
# Stop/unload it before rebuilding the runtime from scratch.
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
if [[ -f "$PLIST" ]]; then launchctl unload "$PLIST" 2>/dev/null || true; fi
sleep 1

rm -rf "$RUNTIME"
mkdir -p "$RUNTIME"
cd "$RUNTIME"
"$NPM22" init -y >/dev/null 2>&1

# Penpot's published package bootstraps a pnpm workspace. pnpm 11 blocks native
# dependency build scripts unless explicitly approved. Penpot's own issue
# identifies esbuild and sharp as the required builds. Preconfigure pnpm before
# installing so the package bootstrap is non-interactive and reproducible.
"$NODE22" - <<'NODE'
const fs = require('fs');
const p = JSON.parse(fs.readFileSync('package.json','utf8'));
p.pnpm = p.pnpm || {};
p.pnpm.onlyBuiltDependencies = Array.from(new Set([...(p.pnpm.onlyBuiltDependencies || []), 'esbuild', 'sharp']));
fs.writeFileSync('package.json', JSON.stringify(p, null, 2) + '\n');
NODE

export PATH="$NODE22_PREFIX/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export COREPACK_ENABLE_DOWNLOAD_PROMPT=0
"$NPM22" install --save-exact corepack
COREPACK="$RUNTIME/node_modules/.bin/corepack"
[[ -x "$COREPACK" ]] || { echo "ERROR: Corepack executable missing" >&2; exit 3; }
"$COREPACK" enable --install-directory "$NODE22_PREFIX/bin" 2>/dev/null || true
"$COREPACK" prepare pnpm@11.4.0 --activate
"$NPM22" install --save-exact @penpot/mcp@2.15.4

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
