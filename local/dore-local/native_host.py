#!/usr/bin/env python3
"""DORÉ Firefox Native Messaging host.

Firefox owns this process lifecycle through ``runtime.connectNative()``. The host
only translates the Native Messaging stdio framing to the established
``a2a_adapter.handle_companion_payload()`` seam; it does not create another HTTP
server or another control plane.

Stdlib only. No OpenAI API, no paid runtime, no GitHub mailbox transport.
"""
from __future__ import annotations

import importlib.util
import json
import os
import struct
import sys
from pathlib import Path
from typing import Any, BinaryIO

PROTOCOL = "dore.a2a/1"
SERVICE = "dore-native-host"
MAX_MESSAGE_BYTES = 1024 * 1024
ROOT = Path(os.environ.get("DORE_REPO_ROOT") or Path(__file__).resolve().parents[2]).expanduser().resolve()

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_adapter():
    path = Path(__file__).with_name("a2a_adapter.py")
    spec = importlib.util.spec_from_file_location("dore_local_a2a_adapter", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load adapter: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ADAPTER = _load_adapter()


def read_message(stream: BinaryIO) -> Any | None:
    header = stream.read(4)
    if not header:
        return None
    if len(header) != 4:
        raise EOFError("truncated Native Messaging header")
    (length,) = struct.unpack("<I", header)
    if length <= 0 or length > MAX_MESSAGE_BYTES:
        raise ValueError(f"invalid Native Messaging body length: {length}")
    data = stream.read(length)
    if len(data) != length:
        raise EOFError("truncated Native Messaging body")
    return json.loads(data.decode("utf-8"))


def write_message(stream: BinaryIO, payload: Any) -> None:
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(data) > MAX_MESSAGE_BYTES:
        raise ValueError("Native Messaging response exceeds size limit")
    stream.write(struct.pack("<I", len(data)))
    stream.write(data)
    stream.flush()


def route_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"ok": False, "service": SERVICE, "error": "Native Messaging payload must be an object"}

    if payload.get("type") == "dore.native.health":
        return {"ok": True, "service": SERVICE, "protocol": PROTOCOL, "transport": "native-messaging"}

    try:
        response = ADAPTER.handle_companion_payload(payload)
    except Exception as exc:
        return {"ok": False, "service": SERVICE, "protocol": PROTOCOL, "error": str(exc)}

    if response is None:
        return {"ok": False, "service": SERVICE, "protocol": PROTOCOL, "error": "unsupported Companion payload"}
    return response


def serve(stdin: BinaryIO | None = None, stdout: BinaryIO | None = None) -> None:
    source = stdin or sys.stdin.buffer
    sink = stdout or sys.stdout.buffer
    while True:
        try:
            payload = read_message(source)
            if payload is None:
                return
            write_message(sink, route_payload(payload))
        except (EOFError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            try:
                write_message(sink, {"ok": False, "service": SERVICE, "error": str(exc)})
            except Exception:
                return


if __name__ == "__main__":
    serve()
