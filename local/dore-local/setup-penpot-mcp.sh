#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNTIME="$HOME/.dore/runtime/penpot-mcp"
MODEL="${DORE_LOCAL_MODEL:-gemma4:e4b}"
VISION_MODEL="$MODEL"
LABEL="io.westsidewatch.penpot-mcp"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"
TAG="2.13.3"

command -v brew >/dev/null || { echo "ERROR: Homebrew is required." >&2; exit 2; }
command -v git >/dev/null || { echo "ERROR: git is required." >&2; exit 2; }
command -v ollama >/dev/null || { echo "ERROR: Ollama is required." >&2; exit 2; }
NODE22_PREFIX="$(brew --prefix node@22 2>/dev/null || true)"
if [[ -z "$NODE22_PREFIX" || ! -x "$NODE22_PREFIX/bin/node" ]]; then brew install node@22; NODE22_PREFIX="$(brew --prefix node@22)"; fi
NODE22="$NODE22_PREFIX/bin/node"; NPM22="$NODE22_PREFIX/bin/npm"
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
[[ -f "$PLIST" ]] && launchctl unload "$PLIST" 2>/dev/null || true
sleep 1; rm -rf "$RUNTIME"; mkdir -p "$RUNTIME"; cd "$RUNTIME"; "$NPM22" init -y >/dev/null 2>&1
export PATH="$NODE22_PREFIX/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin" COREPACK_ENABLE_DOWNLOAD_PROMPT=0
"$NPM22" install --save-exact corepack
COREPACK="$RUNTIME/node_modules/.bin/corepack"; "$COREPACK" prepare pnpm@10.28.2 --activate
"$NPM22" install --ignore-scripts --save-exact @penpot/mcp@2.13.3 pnpm@10.28.2
PKG_DIR="$RUNTIME/node_modules/@penpot/mcp"; PKG="$PKG_DIR/package.json"; PNPM="$RUNTIME/node_modules/.bin/pnpm"
(cd "$PKG_DIR"; CI=true "$PNPM" install)

# Replace the npm package's mismatched plugin source with the canonical Penpot 2.13.3 tag.
CANON="$RUNTIME/canonical-penpot"
git clone --depth 1 --branch "$TAG" https://github.com/penpot/penpot.git "$CANON"
rm -rf "$PKG_DIR/packages/plugin"
cp -R "$CANON/mcp/packages/plugin" "$PKG_DIR/packages/plugin"
# Assert the canonical 2.13.3 source does not contain the later penpot.flags compatibility gate.
if grep -R -n -F 'penpot.flags' "$PKG_DIR/packages/plugin/src" >/dev/null 2>&1; then
  echo "ERROR: canonical $TAG plugin unexpectedly contains penpot.flags gate" >&2; exit 5
fi
(cd "$PKG_DIR/packages/plugin"; "$PNPM" run build)
if grep -F 'incompatible with the connected Penpot version' "$PKG_DIR/packages/plugin/dist/plugin.js" >/dev/null 2>&1; then
  echo "ERROR: rebuilt canonical plugin still contains incompatible-version gate" >&2; exit 5
fi
echo "DORE_PENPOT_CANONICAL_PLUGIN_2133_PASS"

# Keep the proven per-transport MCP server fix.
SERVER_TS="$PKG_DIR/packages/server/src/PenpotMcpServer.ts"
"$NODE22" - "$SERVER_TS" <<'NODE'
const fs=require('fs'); const file=process.argv[2]; let s=fs.readFileSync(file,'utf8');
function must(a,b,l){if(!s.includes(a)) throw new Error('patch anchor missing: '+l); s=s.replace(a,b);}
must('private registerTools(): void {','private registerTools(server: McpServer = this.server): void {','registerTools');
s=s.replace(/this\.server\.registerTool\(/g,'server.registerTool(');
const a=`                    const freshServer = new McpServer(\n                        { name: "penpot-mcp-server", version: "1.0.0" },\n                        { instructions: this.getInitialInstructions() }\n                    );\n                    this.registerTools(freshServer);\n                    await freshServer.connect(transport);`;
const b=`                const freshServer = new McpServer(\n                    { name: "penpot-mcp-server", version: "1.0.0" },\n                    { instructions: this.getInitialInstructions() }\n                );\n                this.registerTools(freshServer);\n                await freshServer.connect(transport);`;
must('                    await this.server.connect(transport);',a,'streamable'); must('                await this.server.connect(transport);',b,'sse'); fs.writeFileSync(file,s);
NODE
(cd "$PKG_DIR/packages/server"; "$PNPM" run build)
echo "DORE_PENPOT_TRANSPORT_PATCH_PASS"
BIN_REL="$($NODE22 -e 'const p=require(process.argv[1]); const b=p.bin; console.log(typeof b==="string"?b:(b&&Object.values(b)[0])||"")' "$PKG")"
MCP_BIN="$PKG_DIR/$BIN_REL"; printf '%s\n' "$MCP_BIN" > "$RUNTIME/mcp-bin-path"; printf '%s\n' "$NODE22" > "$RUNTIME/node-path"; printf '%s\n' "$NODE22_PREFIX/bin" > "$RUNTIME/node-bin-dir"
ollama pull "$VISION_MODEL"; bash "$HERE/install-penpot-mcp-launchagent.sh"
cat <<EOF
DORE_PENPOT_MCP_PREP_PASS
Canonical plugin source: penpot/penpot tag $TAG
Compatibility gate absent: verified
Transport reuse patch: applied
Plugin manifest: http://localhost:4400/manifest.json
MCP endpoint: http://localhost:4401/mcp
EOF
