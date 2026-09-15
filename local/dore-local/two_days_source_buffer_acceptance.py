#!/usr/bin/env python3
"""Phase 1 acceptance: lossless, idempotent, restart-safe Two Days capture."""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import tempfile
from pathlib import Path


def canonical(payload):
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def main():
    with tempfile.TemporaryDirectory() as td:
        os.environ["DORE_TWO_DAYS_HOME"] = td
        import two_days_source_buffer as buffer
        buffer = importlib.reload(buffer)

        payload = {
            "protocol": "dore.a2a/1",
            "conversation_id": "two-days-real-regression",
            "turn_id": "turn-0001",
            "sequence_no": 1,
            "role": "user",
            "content": "繼續\n\n```text\n一天的難處一天當就夠了。\n```",
            "args": {"nested": ["中文", "KJV", {"exact": True}]},
        }
        expected = hashlib.sha256(canonical(payload)).hexdigest()

        first = buffer.capture(payload)
        assert first["ok"] and not first["replayed"], first
        assert first["sha256"] == expected, first

        replay = buffer.capture(payload)
        assert replay["ok"] and replay["replayed"], replay
        assert replay["event_id"] == first["event_id"], (first, replay)

        # Simulate process restart by discarding module state and reopening SQLite.
        buffer = importlib.reload(buffer)
        restored = buffer.read("two-days-real-regression", "turn-0001")
        assert restored, restored
        assert restored["sha256"] == expected, restored
        assert restored["content_raw"] == canonical(payload), restored
        assert restored["sequence_no"] == 1 and restored["role"] == "user", restored

        conflict = dict(payload)
        conflict["content"] = "被偷偷改過的內容"
        try:
            buffer.capture(conflict)
        except ValueError as exc:
            assert str(exc) == "two_days_source_identity_conflict", exc
        else:
            raise AssertionError("identity conflict was not blocked")

        db = Path(td) / "source-buffer" / "events.db"
        assert db.exists() and db.stat().st_size > 0, db
        print(json.dumps({
            "ok": True,
            "code": "TWO_DAYS_SOURCE_BUFFER_PHASE1_PASS",
            "sha256": expected,
            "restart_replay": "PASS",
            "idempotency": "PASS",
            "identity_conflict": "BLOCKED",
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
