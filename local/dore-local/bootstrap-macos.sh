#!/usr/bin/env bash
set -euo pipefail
ROOT="${DORE_LOCAL_HOME:-$HOME/.dore}"
MODEL="${DORE_LOCAL_MODEL:-qwen3:8b}"
EMBED_MODEL="${DORE_LOCAL_EMBED_MODEL:-qwen3-embedding:0.6b}"

echo "Doré Local bootstrap"
echo "Home: $ROOT"

if [[ "$(uname -s)" != "Darwin" ]]; then echo "ERROR: macOS required" >&2; exit 1; fi
ARCH="$(uname -m)"
if [[ "$ARCH" != "arm64" ]]; then echo "ERROR: Apple Silicon arm64 required; got $ARCH" >&2; exit 1; fi

command -v python3 >/dev/null || { echo "ERROR: python3 is required" >&2; exit 1; }
command -v sqlite3 >/dev/null || { echo "ERROR: sqlite3 is required" >&2; exit 1; }
if ! command -v ollama >/dev/null; then
  echo "ERROR: Ollama is not installed. Install the official macOS app first: https://ollama.com/download/mac" >&2
  exit 2
fi

mkdir -p "$ROOT"/{data,archive/raw-history,archive/conversations,logs,backups,imports}
DB="$ROOT/data/dore.sqlite3"
sqlite3 "$DB" <<'SQL'
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS dore_meta (key TEXT PRIMARY KEY,value TEXT NOT NULL,updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS dore_raw_history (
 id TEXT PRIMARY KEY, source TEXT NOT NULL, source_conversation_id TEXT NOT NULL,
 source_message_id TEXT, project_id TEXT NOT NULL DEFAULT 'dore-global', actor_id TEXT NOT NULL DEFAULT 'import',
 role TEXT NOT NULL, title TEXT, content TEXT NOT NULL, content_sha256 TEXT NOT NULL,
 source_created_at TEXT NOT NULL, source_updated_at TEXT, archive_key TEXT, imported_at TEXT NOT NULL,
 import_id TEXT, provenance_json TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_raw_source_message ON dore_raw_history(source,source_conversation_id,source_message_id);
CREATE INDEX IF NOT EXISTS idx_raw_time ON dore_raw_history(source_created_at);
CREATE INDEX IF NOT EXISTS idx_raw_conversation_time ON dore_raw_history(source_conversation_id,source_created_at);
CREATE INDEX IF NOT EXISTS idx_raw_project_time ON dore_raw_history(project_id,source_created_at);
CREATE TABLE IF NOT EXISTS dore_conversations (
 id TEXT PRIMARY KEY, project_id TEXT NOT NULL, actor_id TEXT NOT NULL DEFAULT 'local', mode TEXT NOT NULL DEFAULT 'LOCAL',
 title TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS dore_messages (
 id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL, project_id TEXT NOT NULL, actor_id TEXT NOT NULL DEFAULT 'local',
 role TEXT NOT NULL, content TEXT NOT NULL, content_sha256 TEXT NOT NULL, archive_key TEXT, created_at TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_msg_conversation_hash ON dore_messages(conversation_id,content_sha256,role);
CREATE INDEX IF NOT EXISTS idx_msg_conversation_created ON dore_messages(conversation_id,created_at DESC);
CREATE INDEX IF NOT EXISTS idx_msg_project_created ON dore_messages(project_id,created_at DESC);
INSERT INTO dore_meta(key,value) VALUES('node_kind','mac-local') ON CONFLICT(key) DO UPDATE SET value=excluded.value,updated_at=CURRENT_TIMESTAMP;
INSERT INTO dore_meta(key,value) VALUES('memory_core','sqlite+filesystem') ON CONFLICT(key) DO UPDATE SET value=excluded.value,updated_at=CURRENT_TIMESTAMP;
INSERT INTO dore_meta(key,value) VALUES('workers_ai_required','false') ON CONFLICT(key) DO UPDATE SET value=excluded.value,updated_at=CURRENT_TIMESTAMP;
SQL

if ! curl -fsS http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  echo "ERROR: Ollama is installed but not running. Open the Ollama app, then rerun this script." >&2
  exit 3
fi

echo "Pulling local conversation model: $MODEL"
ollama pull "$MODEL"
echo "Pulling local embedding model: $EMBED_MODEL"
ollama pull "$EMBED_MODEL"

cat > "$ROOT/node.env" <<EOF
DORE_LOCAL_HOME=$ROOT
DORE_LOCAL_HOST=127.0.0.1
DORE_LOCAL_PORT=8788
DORE_LOCAL_MODEL=$MODEL
DORE_LOCAL_EMBED_MODEL=$EMBED_MODEL
OLLAMA_BASE_URL=http://127.0.0.1:11434
EOF
chmod 600 "$ROOT/node.env"

echo "DORE_LOCAL_BOOTSTRAP_PASS"
echo "Database: $DB"
echo "Models: $MODEL ; $EMBED_MODEL"
