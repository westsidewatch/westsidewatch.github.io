CREATE TABLE IF NOT EXISTS sensory_signals (
  id TEXT PRIMARY KEY,
  fingerprint TEXT NOT NULL UNIQUE,
  query TEXT NOT NULL,
  state TEXT NOT NULL CHECK (state IN ('QUEUED','RESEARCHING','WORKING','CANDIDATE_FOR_EXAM','CONSOLIDATED','DISPUTED','REOPENED','REJECTED')),
  heard_count INTEGER NOT NULL DEFAULT 1,
  first_heard_at TEXT NOT NULL,
  last_heard_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  research_task TEXT,
  brain_node TEXT,
  error TEXT
);
CREATE INDEX IF NOT EXISTS idx_sensory_state_updated ON sensory_signals(state,updated_at);
