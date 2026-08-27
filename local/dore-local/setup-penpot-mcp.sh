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
[[ -x "$NODE22" && -x "$NPM22" ]] || { echo "ERROR: Node 22 runtime incomplete at $NODE22_PREFIX" >&2; exit 3; }

echo "Penpot MCP Node: $($NODE22 --version) ($NODE22)"

launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
if [[ -f "$PLIST" ]]; then launchctl unload "$PLIST" 2>/dev/null || true; fi
sleep 1
rm -rf "$RUNTIME"
mkdir -p "$RUNTIME"
cd "$RUNTIME"
"$NPM22" init -y >/dev/null 2>&1

export PATH="$NODE22_PREFIX/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export COREPACK_ENABLE_DOWNLOAD_PROMPT=0
"$NPM22" install --save-exact corepack
COREPACK="$RUNTIME/node_modules/.bin/corepack"
[[ -x "$COREPACK" ]] || { echo "ERROR: Corepack executable missing" >&2; exit 3; }
"$COREPACK" prepare pnpm@11.4.0 --activate

# Install the published package without invoking its bootstrap yet. The package
# owns an internal pnpm workspace, so build approval must be written into that
# workspace rather than the outer Doré runtime.
"$NPM22" install --ignore-scripts --save-exact @penpot/mcp@2.15.4
PKG_DIR="$RUNTIME/node_modules/@penpot/mcp"
PKG="$PKG_DIR/package.json"
[[ -f "$PKG" ]] || { echo "ERROR: @penpot/mcp package not installed" >&2; exit 3; }

"$NODE22" - "$PKG" <<'NODE'
const fs = require('fs');
const file = process.argv[2];
const p = JSON.parse(fs.readFileSync(file, 'utf8'));
p.pnpm = p.pnpm || {};
p.pnpm.onlyBuiltDependencies = ['esbuild', 'sharp'];
fs.writeFileSync(file, JSON.stringify(p, null, 2) + '\n');
NODE

# pnpm 11 reads build approval from pnpm-workspace.yaml when a workspace file
# is present. Penpot ships one, so patch that source of truth as well.
WORKSPACE="$PKG_DIR/pnpm-workspace.yaml"
if [[ -f "$WORKSPACE" ]]; then
  "$NODE22" - "$WORKSPACE" <<'NODE'
const fs = require('fs');
const file = process.argv[2];
let s = fs.readFileSync(file, 'utf8');
// Remove an existing onlyBuiltDependencies block if present, preserving the
// next top-level key. Then append a deterministic approval block.
s = s.replace(/\nonlyBuiltDependencies:\n(?:[ \t]+-.*\n)*/g, '\n');
s = s.replace(/\nneverBuiltDependencies:\n(?:[ \t]+-.*\n)*/g, '\n');
s = s.replace(/\s+$/, '') + '\n\nonlyBuiltDependencies:\n  - esbuild\n  - sharp\n';
fs.writeFileSync(file, s);
NODE
fi

PNPM="$RUNTIME/node_modules/.bin/pnpm"
if [[ ! -x "$PNPM" ]]; then
  "$NPM22" install --ignore-scripts --save-exact pnpm@11.4.0
  PNPM="$RUNTIME/node_modules/.bin/pnpm"
fi
[[ -x "$PNPM" ]] || { echo "ERROR: pnpm executable missing" >&2; exit 3; }

# Complete Penpot's workspace bootstrap with the approval policy already in
# place. CI is set so ignored required builds are treated as a hard failure.
(
  cd "$PKG_DIR"
  CI=true "$PNPM" install
)

BIN_REL="$($NODE22 -e 'const p=require(process.argv[1]); const b=p.bin; console.log(typeof b==="string"?b:(b&&Object.values(b)[0])||"")' "$PKG")"
[[ -n "$BIN_REL" ]] || { echo "ERROR: @penpot/mcp package has no executable bin" >&2; exit 3; }
MCP_BIN="$PKG_DIR/$BIN_REL"
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
