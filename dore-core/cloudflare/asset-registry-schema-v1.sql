-- Doré Asset Registry — production schema v1
-- Date: 2026-08-24
-- Purpose: durable metadata for assets whose binary source may live in R2 or GitHub.

CREATE TABLE IF NOT EXISTS asset_registry (
  id TEXT PRIMARY KEY,
  asset_code TEXT UNIQUE,
  storage_backend TEXT NOT NULL CHECK (storage_backend IN ('r2','github')),
  storage_locator TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  media_type TEXT NOT NULL,
  byte_size INTEGER NOT NULL DEFAULT 0,

  title TEXT,
  description TEXT,
  alt_text TEXT,
  creator TEXT,
  source_name TEXT,
  source_url TEXT,
  provenance TEXT,
  copyright_status TEXT,
  license TEXT,
  generated_by TEXT,

  preservation_class TEXT NOT NULL DEFAULT 'working'
    CHECK (preservation_class IN ('permanent','working','regenerable','temporary')),
  lifecycle_state TEXT NOT NULL DEFAULT 'active'
    CHECK (lifecycle_state IN ('active','review','superseded','quarantined','deleted')),

  scripture_refs_json TEXT NOT NULL DEFAULT '[]',
  people_json TEXT NOT NULL DEFAULT '[]',
  places_json TEXT NOT NULL DEFAULT '[]',
  topics_json TEXT NOT NULL DEFAULT '[]',
  products_using_it_json TEXT NOT NULL DEFAULT '[]',
  journal_columns_json TEXT NOT NULL DEFAULT '[]',
  social_uses_json TEXT NOT NULL DEFAULT '[]',
  liming_resource_ids_json TEXT NOT NULL DEFAULT '[]',

  supersedes_asset_id TEXT,
  superseded_by_asset_id TEXT,
  first_used_at TEXT,
  last_used_at TEXT,
  use_count INTEGER NOT NULL DEFAULT 0,
  review_status TEXT NOT NULL DEFAULT 'pending',
  reviewed_at TEXT,

  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,

  UNIQUE(storage_backend, storage_locator)
);

CREATE INDEX IF NOT EXISTS idx_asset_registry_hash
  ON asset_registry(content_hash);
CREATE INDEX IF NOT EXISTS idx_asset_registry_backend
  ON asset_registry(storage_backend);
CREATE INDEX IF NOT EXISTS idx_asset_registry_preservation
  ON asset_registry(preservation_class);
CREATE INDEX IF NOT EXISTS idx_asset_registry_lifecycle
  ON asset_registry(lifecycle_state);
CREATE INDEX IF NOT EXISTS idx_asset_registry_review
  ON asset_registry(review_status);
CREATE INDEX IF NOT EXISTS idx_asset_registry_last_used
  ON asset_registry(last_used_at);

CREATE TABLE IF NOT EXISTS asset_usage (
  id TEXT PRIMARY KEY,
  asset_id TEXT NOT NULL,
  product TEXT NOT NULL,
  surface TEXT,
  content_ref TEXT,
  usage_role TEXT,
  used_at TEXT NOT NULL,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  FOREIGN KEY(asset_id) REFERENCES asset_registry(id)
);

CREATE INDEX IF NOT EXISTS idx_asset_usage_asset
  ON asset_usage(asset_id);
CREATE INDEX IF NOT EXISTS idx_asset_usage_product
  ON asset_usage(product);
CREATE INDEX IF NOT EXISTS idx_asset_usage_used_at
  ON asset_usage(used_at);

CREATE TABLE IF NOT EXISTS asset_maintenance_queue (
  id TEXT PRIMARY KEY,
  asset_id TEXT NOT NULL,
  action TEXT NOT NULL,
  reason TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'queued'
    CHECK (status IN ('queued','review','approved','rejected','completed','failed')),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(asset_id) REFERENCES asset_registry(id)
);

CREATE INDEX IF NOT EXISTS idx_asset_maintenance_status
  ON asset_maintenance_queue(status);

-- Storage policy thresholds are operating policy, not hard Cloudflare limits:
-- 70% of internal R2 budget: inventory + dedupe review
-- 80%: queue regenerable/temporary cleanup candidates
-- 90%: block non-essential large new assets until reviewed
-- Never auto-delete the only known permanent/master copy.
