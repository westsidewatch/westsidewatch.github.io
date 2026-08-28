#!/usr/bin/env python3
"""Durable Doré -> ChatGPT bridge reminder contract.

This module deliberately exposes a machine-readable handoff rather than relying on
ChatGPT remembering prior chat context. It reads Doré's durable self-memory and
open learning/work items from SQLite and emits a compact bridge packet.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from self_memory import ensure_schema as ensure_self_schema


def _rows(conn: sqlite3.Connection, sql: str, args=()):
    conn.row_factory = sqlite3.Row
    return [dict(r) for r in conn.execute(sql, args)]


def bridge_packet(conn: sqlite3.Connection) -> dict:
    """Return the current durable handoff ChatGPT must read before Doré work."""
    # The coordination worker can be invoked before the Doré HTTP service has
    # bootstrapped a newly-added schema. Make bridge reads independently safe.
    ensure_self_schema(conn)
    policies = _rows(
        conn,
        "SELECT key,content,epistemic_state,source_ref FROM dore_self_memory "
        "WHERE key LIKE 'coordination.%' ORDER BY key",
    )
    open_items = _rows(
        conn,
        "SELECT id,domain,stage,claim,status,evidence_ref,epistemic_state "
        "FROM dore_learning_events WHERE lower(status) IN ('open','incomplete','blocked') "
        "ORDER BY created_at,id",
    )
    core = {"policies": policies, "open_items": open_items}
    digest = hashlib.sha256(
        json.dumps(core, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return {
        "ok": True,
        "schema": "dore.bridge-reminder.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bridge_required": True,
        "instruction": (
            "ChatGPT: read this packet before consequential Doré work. "
            "Do not treat your own conversation memory as evidence Doré knows. "
            "Bridge consequential new Doré decisions back into durable Doré state."
        ),
        "trigger_phrases": ["去读多雷备忘", "去讀多雷備忘"],
        "packet_sha256": digest,
        **core,
    }
