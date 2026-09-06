#!/usr/bin/env python3
"""DORÉ durable wake runtime v0.1.

Stdlib-only sample for event/condition-triggered short-lived work:
SQLite durable queue -> bounded verifier -> atomic promotion -> durable outcome.

No resident daemon is required. A scheduler such as macOS launchd may invoke
`run-once`; the worker exits after processing a bounded number of due tasks.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS wake_tasks (
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    payload TEXT NOT NULL,
    state TEXT NOT NULL CHECK(state IN ('pending','running','passed','failed','retired')),
    next_wake_at INTEGER NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 3,
    lease_until INTEGER,
    last_error TEXT,
    result TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    idempotency_key TEXT UNIQUE
);
CREATE INDEX IF NOT EXISTS idx_wake_due ON wake_tasks(state, next_wake_at);
CREATE TABLE IF NOT EXISTS promotion_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    target_path TEXT NOT NULL,
    backup_path TEXT,
    candidate_path TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at INTEGER NOT NULL
);
"""


def now() -> int:
    return int(time.time())


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=5)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def enqueue(conn: sqlite3.Connection, kind: str, payload: dict[str, Any], *, wake_at: int | None = None,
            max_attempts: int = 3, idempotency_key: str | None = None) -> str:
    task_id = str(uuid.uuid4())
    ts = now()
    try:
        conn.execute(
            "INSERT INTO wake_tasks(id,kind,payload,state,next_wake_at,attempts,max_attempts,created_at,updated_at,idempotency_key) "
            "VALUES(?,?,?,?,?,?,?,?,?,?)",
            (task_id, kind, json.dumps(payload), 'pending', wake_at or ts, 0, max_attempts, ts, ts, idempotency_key),
        )
        conn.commit()
        return task_id
    except sqlite3.IntegrityError:
        if not idempotency_key:
            raise
        row = conn.execute("SELECT id FROM wake_tasks WHERE idempotency_key=?", (idempotency_key,)).fetchone()
        if row is None:
            raise
        return str(row['id'])


def claim_one(conn: sqlite3.Connection, lease_seconds: int = 120) -> sqlite3.Row | None:
    ts = now()
    conn.execute("BEGIN IMMEDIATE")
    row = conn.execute(
        "SELECT * FROM wake_tasks WHERE state='pending' AND next_wake_at<=? ORDER BY next_wake_at, created_at LIMIT 1",
        (ts,),
    ).fetchone()
    if row is None:
        conn.commit()
        return None
    changed = conn.execute(
        "UPDATE wake_tasks SET state='running', attempts=attempts+1, lease_until=?, updated_at=? "
        "WHERE id=? AND state='pending'",
        (ts + lease_seconds, ts, row['id']),
    ).rowcount
    conn.commit()
    if changed != 1:
        return None
    return conn.execute("SELECT * FROM wake_tasks WHERE id=?", (row['id'],)).fetchone()


def recover_expired_leases(conn: sqlite3.Connection) -> int:
    ts = now()
    changed = conn.execute(
        "UPDATE wake_tasks SET state='pending', lease_until=NULL, next_wake_at=?, updated_at=?, "
        "last_error=COALESCE(last_error,'expired lease recovered') "
        "WHERE state='running' AND lease_until IS NOT NULL AND lease_until<? AND attempts<max_attempts",
        (ts, ts, ts),
    ).rowcount
    conn.execute(
        "UPDATE wake_tasks SET state='failed', lease_until=NULL, updated_at=?, "
        "last_error=COALESCE(last_error,'max attempts reached after expired lease') "
        "WHERE state='running' AND lease_until IS NOT NULL AND lease_until<? AND attempts>=max_attempts",
        (ts, ts),
    )
    conn.commit()
    return changed


def run_argv(argv: list[str], timeout: int, cwd: str | None = None) -> tuple[bool, dict[str, Any]]:
    if not argv or not all(isinstance(x, str) and x for x in argv):
        return False, {'error': 'verifier argv must be a non-empty string list'}
    try:
        proc = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout, shell=False)
        detail = {'argv': argv, 'returncode': proc.returncode, 'stdout': proc.stdout[-4000:], 'stderr': proc.stderr[-4000:]}
        return proc.returncode == 0, detail
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, {'argv': argv, 'error': str(exc)}


def promote_file(conn: sqlite3.Connection, task_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    candidate = Path(payload['candidate_path']).expanduser().resolve()
    target = Path(payload['target_path']).expanduser().resolve()
    verifier = payload.get('verifier_argv')
    timeout = int(payload.get('verifier_timeout_seconds', 60))
    verify_cwd = payload.get('verifier_cwd')

    if not candidate.is_file():
        raise FileNotFoundError(f'candidate missing: {candidate}')
    if not isinstance(verifier, list):
        raise ValueError('verifier_argv is required; promotion without verification is forbidden')

    passed, evidence = run_argv(verifier, timeout, verify_cwd)
    if not passed:
        return {'accepted': False, 'stage': 'verify', 'evidence': evidence}

    target.parent.mkdir(parents=True, exist_ok=True)
    backup: Path | None = None
    if target.exists():
        backup_dir = target.parent / '.dore-backups'
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup = backup_dir / f'{target.name}.{task_id}.bak'
        shutil.copy2(target, backup)

    temp_target = target.with_name(f'.{target.name}.{task_id}.candidate')
    try:
        shutil.copy2(candidate, temp_target)
        os.replace(temp_target, target)
        conn.execute(
            "INSERT INTO promotion_log(task_id,target_path,backup_path,candidate_path,status,created_at) VALUES(?,?,?,?,?,?)",
            (task_id, str(target), str(backup) if backup else None, str(candidate), 'promoted', now()),
        )
        conn.commit()
        return {'accepted': True, 'stage': 'promote', 'evidence': evidence, 'target': str(target), 'backup': str(backup) if backup else None}
    except Exception:
        if temp_target.exists():
            temp_target.unlink(missing_ok=True)
        if backup and backup.exists():
            shutil.copy2(backup, target)
        raise


def execute_task(conn: sqlite3.Connection, row: sqlite3.Row) -> dict[str, Any]:
    payload = json.loads(row['payload'])
    if row['kind'] == 'promote_file':
        return promote_file(conn, str(row['id']), payload)
    if row['kind'] == 'probe':
        argv = payload.get('argv', [sys.executable, '-c', 'raise SystemExit(0)'])
        passed, evidence = run_argv(argv, int(payload.get('timeout_seconds', 30)), payload.get('cwd'))
        return {'accepted': passed, 'stage': 'probe', 'evidence': evidence}
    raise ValueError(f"unsupported task kind: {row['kind']}")


def finish(conn: sqlite3.Connection, row: sqlite3.Row, result: dict[str, Any] | None = None, error: Exception | None = None) -> None:
    ts = now()
    if error is None and result and result.get('accepted'):
        conn.execute("UPDATE wake_tasks SET state='passed', lease_until=NULL, result=?, last_error=NULL, updated_at=? WHERE id=?",
                     (json.dumps(result), ts, row['id']))
    else:
        reason = str(error) if error else json.dumps(result or {'accepted': False})
        if int(row['attempts']) >= int(row['max_attempts']):
            conn.execute("UPDATE wake_tasks SET state='failed', lease_until=NULL, last_error=?, result=?, updated_at=? WHERE id=?",
                         (reason, json.dumps(result) if result else None, ts, row['id']))
        else:
            backoff = min(3600, 30 * (2 ** max(0, int(row['attempts']) - 1)))
            conn.execute("UPDATE wake_tasks SET state='pending', lease_until=NULL, next_wake_at=?, last_error=?, result=?, updated_at=? WHERE id=?",
                         (ts + backoff, reason, json.dumps(result) if result else None, ts, row['id']))
    conn.commit()


def run_once(db_path: Path, limit: int = 3) -> dict[str, int]:
    conn = connect(db_path)
    recovered = recover_expired_leases(conn)
    processed = passed = failed_or_retry = 0
    for _ in range(max(1, limit)):
        row = claim_one(conn)
        if row is None:
            break
        processed += 1
        try:
            result = execute_task(conn, row)
            finish(conn, row, result=result)
            if result.get('accepted'):
                passed += 1
            else:
                failed_or_retry += 1
        except Exception as exc:
            finish(conn, row, error=exc)
            failed_or_retry += 1
    conn.close()
    return {'recovered': recovered, 'processed': processed, 'passed': passed, 'failed_or_retry': failed_or_retry}


def status(db_path: Path) -> list[dict[str, Any]]:
    conn = connect(db_path)
    rows = conn.execute("SELECT id,kind,state,next_wake_at,attempts,max_attempts,last_error,result FROM wake_tasks ORDER BY created_at DESC").fetchall()
    out = [dict(r) for r in rows]
    conn.close()
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default=os.environ.get('DORE_WAKE_DB', str(Path.home() / 'Library/Application Support/Dore/wake-state.sqlite3')))
    sub = parser.add_subparsers(dest='cmd', required=True)
    sub.add_parser('init')
    runp = sub.add_parser('run-once'); runp.add_argument('--limit', type=int, default=3)
    sub.add_parser('status')
    enq = sub.add_parser('enqueue')
    enq.add_argument('--kind', required=True, choices=['probe','promote_file'])
    enq.add_argument('--payload-json', required=True)
    enq.add_argument('--idempotency-key')
    enq.add_argument('--max-attempts', type=int, default=3)
    args = parser.parse_args()
    db = Path(args.db)
    if args.cmd == 'init':
        connect(db).close(); print(json.dumps({'ok': True, 'db': str(db)})); return 0
    if args.cmd == 'run-once':
        print(json.dumps(run_once(db, args.limit))); return 0
    if args.cmd == 'status':
        print(json.dumps(status(db), indent=2)); return 0
    if args.cmd == 'enqueue':
        conn = connect(db)
        task_id = enqueue(conn, args.kind, json.loads(args.payload_json), max_attempts=args.max_attempts, idempotency_key=args.idempotency_key)
        conn.close(); print(json.dumps({'task_id': task_id})); return 0
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
