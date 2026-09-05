#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import io
import json
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("dore_native_host_test", HERE / "native_host.py")
assert SPEC and SPEC.loader
HOST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOST)


def frame(payload: dict) -> bytes:
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return struct.pack("<I", len(raw)) + raw


def unframe(data: bytes) -> dict:
    assert len(data) >= 4
    (size,) = struct.unpack("<I", data[:4])
    raw = data[4:]
    assert len(raw) == size
    return json.loads(raw.decode("utf-8"))


def test_framing_round_trip() -> None:
    payload = {"action": "native.health", "unicode": "多雷"}
    stream = io.BytesIO(frame(payload))
    assert HOST.read_message(stream) == payload

    out = io.BytesIO()
    HOST.write_message(out, payload)
    assert unframe(out.getvalue()) == payload


def test_native_health() -> None:
    result = HOST.route_payload({"action": "native.health"})
    assert result["ok"] is True
    assert result["protocol"] == "dore.a2a/1"
    assert result["transport"] == "firefox-native-messaging"
    assert result["resident"] is False
    assert result["paid_runtime"] is False


def test_adapter_discover_passthrough() -> None:
    result = HOST.route_payload({"protocol": "dore.a2a/1", "action": "discover"})
    assert result["protocol"] == "dore.a2a/1"
    assert result["status"] == "succeeded"
    assert any(c["id"] == "design" for c in result["consumers"])


def test_legacy_stage2_compatibility() -> None:
    result = HOST.route_payload({"command": "/dore stage2"})
    assert result["status"] == "PASS"
    assert result["capability"] == "design2.stage2.acceptance"
    assert result["transport"] == "firefox-native-messaging"


def test_process_loop_one_message() -> None:
    source = io.BytesIO(frame({"action": "native.health"}))
    sink = io.BytesIO()
    assert HOST.serve(source, sink) == 0
    result = unframe(sink.getvalue())
    assert result["service"] == "dore-a2a-native"


def main() -> None:
    test_framing_round_trip()
    test_native_health()
    test_adapter_discover_passthrough()
    test_legacy_stage2_compatibility()
    test_process_loop_one_message()
    print("DORÉ Native Messaging host: PASS")


if __name__ == "__main__":
    main()
