CREATE TABLE IF NOT EXISTS dore_conversations (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  actor_id TEXT NOT NULL DEFAULT 'internal',
  mode TEXT NOT NULL DEFAULT 'INTERNAL_ALPHA',
  title TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_dore_conversations_project_updated
  ON dore_conversations(project_id, updated_at DESC);

CREATE TABLE IF NOT EXISTS dore_messages (
  id TEXT PRIMARY KEY,
  conversation_id TEXT NOT NULL,
  project_id TEXT NOT NULL,
  actor_id TEXT NOT NULL DEFAULT 'internal',
  role TEXT NOT NULL CHECK (role IN ('system','user','assistant','dore','tool')),
  content TEXT NOT NULL,
  content_sha256 TEXT NOT NULL,
  archive_key TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(conversation_id) REFERENCES dore_conversations(id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_dore_messages_conversation_hash
  ON dore_messages(conversation_id, content_sha256, role);
CREATE INDEX IF NOT EXISTS idx_dore_messages_conversation_created
  ON dore_messages(conversation_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_dore_messages_project_created
  ON dore_messages(project_id, created_at DESC);

CREATE TABLE IF NOT EXISTS dore_memory_chunks (
  id TEXT PRIMARY KEY,
  message_id TEXT NOT NULL,
  conversation_id TEXT NOT NULL,
  project_id TEXT NOT NULL,
  ordinal INTEGER NOT NULL DEFAULT 0,
  content TEXT NOT NULL,
  vector_id TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(message_id) REFERENCES dore_messages(id)
);

CREATE INDEX IF NOT EXISTS idx_dore_chunks_conversation_created
  ON dore_memory_chunks(conversation_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_dore_chunks_project_created
  ON dore_memory_chunks(project_id, created_at DESC);
CREATE UNIQUE INDEX IF NOT EXISTS idx_dore_chunks_vector_id
  ON dore_memory_chunks(vector_id) WHERE vector_id IS NOT NULL;
