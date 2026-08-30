#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNTIME="$HOME/.dore/runtime/penpot-mcp"
MODEL="${DORE_LOCAL_MODEL:-gemma4:e4b}"
VISION_MODEL="$MODEL"
LABEL="io.westsidewatch.penpot-mcp"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"

command -v brew >/dev/null || { echo "ERROR: Homebrew is required to provision isolated Node 22 for Penpot MCP." >&2; exit 2; }
command -v ollama >/dev/null || { echo "ERROR: Ollama is required." >&2; exit 2; }
NODE22_PREFIX="$(brew --prefix node@22 2>/dev/null || true)"
if [[ -z "$NODE22_PREFIX" || ! -x "$NODE22_PREFIX/bin/node" ]]; then brew install node@22; NODE22_PREFIX="$(brew --prefix node@22)"; fi
NODE22="$NODE22_PREFIX/bin/node"; NPM22="$NODE22_PREFIX/bin/npm"
[[ -x "$NODE22" && -x "$NPM22" ]] || { echo "ERROR: Node 22 runtime incomplete at $NODE22_PREFIX" >&2; exit 3; }
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
if [[ -f "$PLIST" ]]; then launchctl unload "$PLIST" 2>/dev/null || true; fi
sleep 1; rm -rf "$RUNTIME"; mkdir -p "$RUNTIME"; cd "$RUNTIME"; "$NPM22" init -y >/dev/null 2>&1
export PATH="$NODE22_PREFIX/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin" COREPACK_ENABLE_DOWNLOAD_PROMPT=0
"$NPM22" install --save-exact corepack
COREPACK="$RUNTIME/node_modules/.bin/corepack"; "$COREPACK" prepare pnpm@10.28.2 --activate
"$NPM22" install --ignore-scripts --save-exact @penpot/mcp@2.13.3 pnpm@10.28.2
PKG_DIR="$RUNTIME/node_modules/@penpot/mcp"; PKG="$PKG_DIR/package.json"; WORKSPACE="$PKG_DIR/pnpm-workspace.yaml"; PNPM="$RUNTIME/node_modules/.bin/pnpm"
[[ -f "$PKG" && -x "$PNPM" ]] || { echo "ERROR: Penpot MCP bootstrap prerequisites missing" >&2; exit 3; }
if [[ -f "$WORKSPACE" ]]; then
  "$NODE22" - "$WORKSPACE" <<'NODE'
const fs=require('fs'); const file=process.argv[2]; let s=fs.readFileSync(file,'utf8');
for (const key of ['onlyBuiltDependencies','ignoredBuiltDependencies','neverBuiltDependencies']) s=s.replace(new RegExp(`\\n${key}:\\n(?:[ \\t]+-.*\\n)*`,'g'),'\n');
s=s.replace(/\nallowBuilds:\n(?:[ \t]+[^\n]+\n)*/g,'\n'); s=s.replace(/\s+$/,'')+'\n\nallowBuilds:\n  esbuild: true\n  sharp: true\n'; fs.writeFileSync(file,s);
NODE
fi
"$NODE22" - "$PKG" <<'NODE'
const fs=require('fs'); const file=process.argv[2]; const p=JSON.parse(fs.readFileSync(file,'utf8'));
if(p.pnpm){for(const k of ['onlyBuiltDependencies','ignoredBuiltDependencies','neverBuiltDependencies','allowBuilds']) delete p.pnpm[k]; if(!Object.keys(p.pnpm).length) delete p.pnpm;} fs.writeFileSync(file,JSON.stringify(p,null,2)+'\n');
NODE
(cd "$PKG_DIR"; CI=true "$PNPM" install)
SERVER_TS="$PKG_DIR/packages/server/src/PenpotMcpServer.ts"
[[ -f "$SERVER_TS" ]] || { echo "ERROR: Penpot MCP server source missing: $SERVER_TS" >&2; exit 4; }
"$NODE22" - "$SERVER_TS" <<'NODE'
const fs=require('fs'); const file=process.argv[2]; let s=fs.readFileSync(file,'utf8');
function must(oldText,newText,label){if(!s.includes(oldText)) throw new Error('patch anchor missing: '+label); s=s.replace(oldText,newText);}
must('private registerTools(): void {','private registerTools(server: McpServer = this.server): void {','registerTools signature');
s=s.replace(/this\.server\.registerTool\(/g,'server.registerTool(');
const fresh8 = `                    const freshServer = new McpServer(
                        { name: "penpot-mcp-server", version: "1.0.0" },
                        { instructions: this.getInitialInstructions() }
                    );
                    this.registerTools(freshServer);
                    await freshServer.connect(transport);`;
const fresh4 = `                const freshServer = new McpServer(
                    { name: "penpot-mcp-server", version: "1.0.0" },
                    { instructions: this.getInitialInstructions() }
                );
                this.registerTools(freshServer);
                await freshServer.connect(transport);`;
must('                    await this.server.connect(transport);',fresh8,'streamable connect');
must('                await this.server.connect(transport);',fresh4,'sse connect');
fs.writeFileSync(file,s);
NODE
(cd "$PKG_DIR/packages/server"; "$PNPM" run build)
echo "DORE_PENPOT_TRANSPORT_PATCH_PASS"
BIN_REL="$($NODE22 -e 'const p=require(process.argv[1]); const b=p.bin; console.log(typeof b==="string"?b:(b&&Object.values(b)[0])||"")' "$PKG")"
[[ -n "$BIN_REL" ]] || { echo "ERROR: @penpot/mcp package has no executable bin" >&2; exit 3; }
MCP_BIN="$PKG_DIR/$BIN_REL"; [[ -f "$MCP_BIN" ]] || { echo "ERROR: resolved Penpot MCP executable missing: $MCP_BIN" >&2; exit 3; }
printf '%s\n' "$MCP_BIN" > "$RUNTIME/mcp-bin-path"; printf '%s\n' "$NODE22" > "$RUNTIME/node-path"; printf '%s\n' "$NODE22_PREFIX/bin" > "$RUNTIME/node-bin-dir"
ollama pull "$VISION_MODEL"; bash "$HERE/install-penpot-mcp-launchagent.sh"
cat <<EOF
DORE_PENPOT_MCP_PREP_PASS
Penpot MCP package: @penpot/mcp@2.13.3
Transport reuse patch: applied
Plugin manifest: http://localhost:4400/manifest.json
MCP endpoint: http://localhost:4401/mcp
Active Doré engine: $MODEL
Visual verification engine: $VISION_MODEL
EOF
