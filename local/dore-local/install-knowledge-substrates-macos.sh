#!/usr/bin/env bash
set -euo pipefail

ROOT="${DORE_REPO_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
BASE="${DORE_LOCAL_AI_HOME:-$HOME/Library/Application Support/Dore/local-ai}"
TOOLS="$BASE/tools"
BIN="$BASE/bin"
DATA="$BASE/data"
QMD_HOME="$DATA/qmd"
LM_HOME="$DATA/longmemory"

mkdir -p "$TOOLS" "$BIN" "$QMD_HOME" "$LM_HOME"

# launchd/self-hosted runners intentionally have a minimal PATH. Recover only
# standard user-local package-manager locations; do not require a login shell.
for candidate in /opt/homebrew/bin /usr/local/bin "$HOME/.local/bin"; do
  if [[ -d "$candidate" ]]; then PATH="$candidate:$PATH"; fi
done
export PATH

NODE_BIN="$(command -v node || true)"
NPM_BIN="$(command -v npm || true)"
if [[ -z "$NODE_BIN" || -z "$NPM_BIN" ]]; then
  echo '{"ok":false,"error":"node_and_npm_required"}'
  exit 2
fi
NODE_MAJOR="$($NODE_BIN -p 'Number(process.versions.node.split(".")[0])')"
if [[ "$NODE_MAJOR" -lt 20 ]]; then
  echo "{\"ok\":false,\"error\":\"node_20_required\",\"node\":\"$($NODE_BIN --version)\"}"
  exit 2
fi

# Install into Doré-owned prefix only. No sudo, no global npm mutation.
"$NPM_BIN" install --no-audit --no-fund --prefix "$TOOLS" @tobilu/qmd longmemory

QMD="$TOOLS/node_modules/.bin/qmd"
LM="$TOOLS/node_modules/.bin/longmemory"
[ -x "$QMD" ] && [ -x "$LM" ]

cat > "$BIN/qmd" <<EOF
#!/usr/bin/env bash
export PATH="$(dirname "$NODE_BIN"):\$PATH"
exec "$QMD" "\$@"
EOF
cat > "$BIN/longmemory" <<EOF
#!/usr/bin/env bash
export PATH="$(dirname "$NODE_BIN"):\$PATH"
exec "$LM" "\$@"
EOF
chmod +x "$BIN/qmd" "$BIN/longmemory"

cat > "$BASE/env.sh" <<EOF
export PATH="$(dirname "$NODE_BIN"):\$PATH"
export DORE_QMD_BIN="$BIN/qmd"
export DORE_LONGMEMORY_BIN="$BIN/longmemory"
export DORE_QMD_HOME="$QMD_HOME"
export DORE_LONGMEMORY_DB="$LM_HOME/dore.db"
export DORE_LONGMEMORY_PROJECT="dore"
EOF

python3 "$ROOT/local/dore-local/knowledge-substrate-poc.py" \
  --repo "$ROOT" \
  --qmd "$BIN/qmd" \
  --longmemory "$BIN/longmemory" \
  --data "$DATA"
