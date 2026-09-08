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

if ! command -v node >/dev/null 2>&1 || ! command -v npm >/dev/null 2>&1; then
  echo '{"ok":false,"error":"node_and_npm_required"}'
  exit 2
fi

# Install into Doré-owned prefix only. No sudo, no global npm mutation.
npm install --no-audit --no-fund --prefix "$TOOLS" @tobilu/qmd longmemory

QMD="$TOOLS/node_modules/.bin/qmd"
LM="$TOOLS/node_modules/.bin/longmemory"
[ -x "$QMD" ] && [ -x "$LM" ]

cat > "$BIN/qmd" <<EOF
#!/usr/bin/env bash
exec "$QMD" "\$@"
EOF
cat > "$BIN/longmemory" <<EOF
#!/usr/bin/env bash
exec "$LM" "\$@"
EOF
chmod +x "$BIN/qmd" "$BIN/longmemory"

cat > "$BASE/env.sh" <<EOF
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
