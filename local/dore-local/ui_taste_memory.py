#!/usr/bin/env python3
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Iterable


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS dore_ui_taste_comparisons(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      surface_id TEXT NOT NULL,
      surface_family TEXT,
      task_context TEXT NOT NULL,
      primary_axis TEXT NOT NULL,
      candidate_a TEXT NOT NULL,
      candidate_b TEXT NOT NULL,
      winner TEXT NOT NULL,
      winner_reason TEXT NOT NULL,
      loser_reason TEXT NOT NULL,
      brand_fit TEXT,
      usability_floor_passed INTEGER NOT NULL DEFAULT 0,
      viewport_context TEXT,
      content_context TEXT,
      evidence_refs_json TEXT NOT NULL,
      confidence REAL NOT NULL DEFAULT 0.5,
      scope TEXT NOT NULL DEFAULT 'local',
      supersedes_id INTEGER,
      created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_ui_taste_comparison_context
      ON dore_ui_taste_comparisons(surface_family, primary_axis, created_at DESC);

    CREATE TABLE IF NOT EXISTS dore_ui_taste_rejections(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      surface_id TEXT NOT NULL,
      surface_family TEXT,
      direction TEXT NOT NULL,
      reason TEXT NOT NULL,
      failure_domain TEXT NOT NULL,
      scope TEXT NOT NULL DEFAULT 'local',
      evidence_refs_json TEXT NOT NULL,
      confidence REAL NOT NULL DEFAULT 0.5,
      contradicted_by_id INTEGER,
      created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_ui_taste_rejection_context
      ON dore_ui_taste_rejections(surface_family, failure_domain, created_at DESC);

    CREATE TABLE IF NOT EXISTS dore_ui_motion_vocabulary(
      term TEXT PRIMARY KEY,
      semantic_purpose TEXT NOT NULL,
      trigger_contract TEXT,
      enter_contract TEXT,
      settle_contract TEXT,
      exit_contract TEXT,
      interruption_contract TEXT,
      reduced_motion_equivalent TEXT,
      examples_json TEXT NOT NULL,
      counterexamples_json TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
    ''')
    conn.commit()


def _j(values: Iterable[str] | None) -> str:
    return json.dumps(list(values or []), ensure_ascii=False)


def record_comparison(
    conn: sqlite3.Connection,
    *,
    surface_id: str,
    task_context: str,
    primary_axis: str,
    candidate_a: str,
    candidate_b: str,
    winner: str,
    winner_reason: str,
    loser_reason: str,
    evidence_refs: Iterable[str],
    surface_family: str | None = None,
    brand_fit: str | None = None,
    usability_floor_passed: bool = False,
    viewport_context: str | None = None,
    content_context: str | None = None,
    confidence: float = 0.5,
    scope: str = 'local',
    supersedes_id: int | None = None,
) -> int:
    ensure_schema(conn)
    if winner not in {candidate_a, candidate_b}:
        raise ValueError('winner must be candidate_a or candidate_b')
    if scope not in {'local', 'surface-family', 'brand-pattern'}:
        raise ValueError('invalid scope')
    cur = conn.execute('''
      INSERT INTO dore_ui_taste_comparisons(
        surface_id,surface_family,task_context,primary_axis,candidate_a,candidate_b,winner,
        winner_reason,loser_reason,brand_fit,usability_floor_passed,viewport_context,
        content_context,evidence_refs_json,confidence,scope,supersedes_id,created_at
      ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        surface_id, surface_family, task_context, primary_axis, candidate_a, candidate_b, winner,
        winner_reason, loser_reason, brand_fit, 1 if usability_floor_passed else 0,
        viewport_context, content_context, _j(evidence_refs), max(0.0, min(1.0, float(confidence))),
        scope, supersedes_id, now(),
    ))
    conn.commit()
    return int(cur.lastrowid)


def record_rejection(
    conn: sqlite3.Connection,
    *,
    surface_id: str,
    direction: str,
    reason: str,
    failure_domain: str,
    evidence_refs: Iterable[str],
    surface_family: str | None = None,
    scope: str = 'local',
    confidence: float = 0.5,
    contradicted_by_id: int | None = None,
) -> int:
    ensure_schema(conn)
    if scope not in {'local', 'surface-family', 'brand-pattern'}:
        raise ValueError('invalid scope')
    cur = conn.execute('''
      INSERT INTO dore_ui_taste_rejections(
        surface_id,surface_family,direction,reason,failure_domain,scope,
        evidence_refs_json,confidence,contradicted_by_id,created_at
      ) VALUES(?,?,?,?,?,?,?,?,?,?)
    ''', (
        surface_id, surface_family, direction, reason, failure_domain, scope,
        _j(evidence_refs), max(0.0, min(1.0, float(confidence))), contradicted_by_id, now(),
    ))
    conn.commit()
    return int(cur.lastrowid)


def upsert_motion_term(
    conn: sqlite3.Connection,
    *,
    term: str,
    semantic_purpose: str,
    examples: Iterable[str],
    counterexamples: Iterable[str] | None = None,
    trigger_contract: str | None = None,
    enter_contract: str | None = None,
    settle_contract: str | None = None,
    exit_contract: str | None = None,
    interruption_contract: str | None = None,
    reduced_motion_equivalent: str | None = None,
) -> None:
    ensure_schema(conn)
    conn.execute('''
      INSERT INTO dore_ui_motion_vocabulary(
        term,semantic_purpose,trigger_contract,enter_contract,settle_contract,exit_contract,
        interruption_contract,reduced_motion_equivalent,examples_json,counterexamples_json,updated_at
      ) VALUES(?,?,?,?,?,?,?,?,?,?,?)
      ON CONFLICT(term) DO UPDATE SET
        semantic_purpose=excluded.semantic_purpose,
        trigger_contract=excluded.trigger_contract,
        enter_contract=excluded.enter_contract,
        settle_contract=excluded.settle_contract,
        exit_contract=excluded.exit_contract,
        interruption_contract=excluded.interruption_contract,
        reduced_motion_equivalent=excluded.reduced_motion_equivalent,
        examples_json=excluded.examples_json,
        counterexamples_json=excluded.counterexamples_json,
        updated_at=excluded.updated_at
    ''', (
        term, semantic_purpose, trigger_contract, enter_contract, settle_contract, exit_contract,
        interruption_contract, reduced_motion_equivalent, _j(examples), _j(counterexamples), now(),
    ))
    conn.commit()


def retrieve_precedent(
    conn: sqlite3.Connection,
    *,
    surface_family: str | None = None,
    primary_axis: str | None = None,
    limit: int = 6,
) -> dict:
    """Return a bounded, context-near precedent pack. Never dump the full ledger."""
    ensure_schema(conn)
    limit = max(1, min(int(limit), 12))
    clauses, args = [], []
    if surface_family:
        clauses.append('(surface_family=? OR scope=\'brand-pattern\')')
        args.append(surface_family)
    if primary_axis:
        clauses.append('primary_axis=?')
        args.append(primary_axis)
    where = (' WHERE ' + ' AND '.join(clauses)) if clauses else ''
    comparisons = [dict(r) for r in conn.execute(
        'SELECT * FROM dore_ui_taste_comparisons' + where + ' ORDER BY confidence DESC, created_at DESC LIMIT ?',
        (*args, limit),
    )]
    rclauses, rargs = [], []
    if surface_family:
        rclauses.append('(surface_family=? OR scope=\'brand-pattern\')')
        rargs.append(surface_family)
    rwhere = (' WHERE ' + ' AND '.join(rclauses)) if rclauses else ''
    rejections = [dict(r) for r in conn.execute(
        'SELECT * FROM dore_ui_taste_rejections' + rwhere + ' ORDER BY confidence DESC, created_at DESC LIMIT ?',
        (*rargs, limit),
    )]
    for row in comparisons:
        row['evidence_refs'] = json.loads(row.pop('evidence_refs_json'))
    for row in rejections:
        row['evidence_refs'] = json.loads(row.pop('evidence_refs_json'))
    return {
        'policy': 'bounded-context-precedent-v1',
        'comparisons': comparisons,
        'rejections': rejections,
        'max_per_kind': limit,
    }
