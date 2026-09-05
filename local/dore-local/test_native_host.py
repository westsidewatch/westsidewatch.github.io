#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import io
import json
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("dore_native_host_tested", HERE / "native_host.py")
HOST = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(HOST)


def encode(payload):
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return struct.pack("<I", len(body)) + body


def decode(raw):
    size = struct.unpack("<I", raw[:4])[0]
    return json.loads(raw[4 : 4 + size])


def test_framing_round_trip():
    payload = {"protocol": "dore.a2a/1", "action": "discover"}
    assert HOST.read_message(io.BytesIO(encode(payload))) == payload
    out = io.BytesIO()
    HOST.write_message(out, {"ok": True})
    assert decode(out.getvalue()) == {"ok": True}


def test_health_does_not_touch_control_plane():
    result = HOST.route_payload({"type": "dore.native.health"})
    assert result == {
        "ok": True,
        "service": "dore-native-host",
        "protocol": "dore.a2a/1",
        "transport": "native-messaging",
    }


def test_typed_payload_uses_existing_adapter():
    seen = []
    original = HOST.ADAPTER.handle_companion_payload
    try:
        HOST.ADAPTER.handle_companion_payload = lambda payload: seen.append(payload) or {"status": "succeeded"}
        payload = {"protocol": "dore.a2a/1", "action": "discover"}
        assert HOST.route_payload(payload) == {"status": "succeeded"}
        assert seen == [payload]
    finally:
        HOST.ADAPTER.handle_companion_payload = original


def test_legacy_payload_is_not_reinvented():
    original = HOST.ADAPTER.handle_companion_payload
    try:
        HOST.ADAPTER.handle_companion_payload = lambda payload: None
        result = HOST.route_payload({"capability": "design2.stage2.acceptance"})
        assert result["ok"] is False
        assert result["error"] == "unsupported Companion payload"
    finally:
        HOST.ADAPTER.handle_companion_payload = original


def test_rejects_oversized_frame_before_reading_body():
    raw = struct.pack("<I", HOST.MAX_MESSAGE_BYTES + 1)
    try:
        HOST.read_message(io.BytesIO(raw))
    except ValueError as exc:
        assert "invalid Native Messaging body length" in str(exc)
    else:
        raise AssertionError("oversized frame was accepted")
