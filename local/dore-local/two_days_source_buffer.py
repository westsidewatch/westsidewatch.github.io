#!/usr/bin/env python3
"""Two Days v0 lossless local source buffer.

This layer records factual inbound A2A payloads before interpretation. It does
not summarize, embed, infer acceptance, or mutate Doré routing semantics.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "two-days.source-event.v0"


def _home() -> Path:
    base = Path(os.environ.get("DORE_LOCAL_HOME") or "~/Library/Application Support/Dore").expanduser()
    return Path(os.environ.get("DORE_TWO_DAYS_HOME") or (base / "two-days")).expanduser()


def _db_path() -> Path:
    return _home() / "source-buffer" / "events.db"


def _canonical_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def _identity(payload: dict[str, Any], digest: str) -> tuple[str, str, int]:
    conversation_id = str(payload.get("conversation_id") or payload.get("session_id") or "transport")
    turn_id = str(
        payload.get("turn_id")
        or payload.get("message_id")
        or payload.get("request_id")
        or payload.get("__dore_transport_id")
        or digest
    )
    raw_sequence = payload.get("sequence_no")
    try:
        sequence_no = int(raw_sequence) if raw_sequence is not None else -1
    except (TypeError, ValueError):
        sequence_no = -1
    return conversation_id, turn_id, sequence_no


def _connect() -> sqlite3.Connection:
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA synchronous=FULL")
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS source_events (
            event_id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            turn_id TEXT NOT NULL,
            sequence_no INTEGER NOT NULL,
            role TEXT NOT NULL,
            content_raw BLOB NOT NULL,
            captured_at TEXT NOT NULL,
            content_sha256 TEXT NOT NULL,
            schema_id TEXT NOT NULL,
            UNIQUE(conversation_id, turn_id)
        )
        """
    )
    return db


def capture(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise TypeError("two_days_payload_must_be_object")
    raw = _canonical_bytes(payload)
    digest = hashlib.sha256(raw).hexdigest()
    conversation_id, turn_id, sequence_no = _identity(payload, digest)
    event_id = hashlib.sha256(f"{conversation_id}\0{turn_id}".encode("utf-8")).hexdigest()
    role = str(payload.get("role") or "transport")
    captured_at = datetime.now(timezone.utc).isoformat()
    with _connect() as db:
        existing = db.execute(
            "SELECT content_sha256 FROM source_events WHERE conversation_id=? AND turn_id=?",
            (conversation_id, turn_id),
        ).fetchone()
        if existing:
            if existing[0] != digest:
                raise ValueError("two_days_source_identity_conflict")
            return {"ok": True, "event_id": event_id, "sha256": digest, "replayed": True}
        db.execute(
            "INSERT INTO source_events VALUES (?,?,?,?,?,?,?,?,?)",
            (event_id, conversation_id, turn_id, sequence_no, role, raw, captured_at, digest, SCHEMA),
        )
    return {"ok": True, "event_id": event_id, "sha256": digest, "replayed": False}


def read(conversation_id: str, turn_id: str) -> dict[str, Any] | None:
    with _connect() as db:
        row = db.execute(
            "SELECT event_id,sequence_no,role,content_raw,captured_at,content_sha256 FROM source_events WHERE conversation_id=? AND turn_id=?",
            (str(conversation_id), str(turn_id)),
        ).fetchone()
    if not row:
        return None
    raw = bytes(row[3])
    digest = hashlib.sha256(raw).hexdigest()
    if digest != row[5]:
        raise ValueError("two_days_source_hash_mismatch")
    return {
        "event_id": row[0],
        "conversation_id": str(conversation_id),
        "turn_id": str(turn_id),
        "sequence_no": row[1],
        "role": row[2],
        "content_raw": raw,
        "captured_at": row[4],
        "sha256": row[5],
    }
