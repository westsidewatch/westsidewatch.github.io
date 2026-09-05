#!/usr/bin/env python3
"""DORÉ Firefox Native Messaging host.

Local carrier only: Firefox Companion -> stdio framing -> a2a_adapter ->
DORÉ ControlPlane.  It deliberately does not create a daemon, listen on a
socket, call OpenAI APIs, or use GitHub as a runtime message bus.
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
SERVICE = "dore-a2a-native"
HOST_NAME = "ca.dore.companion"
LEGACY_CAPABILITY = "design2.stage2.acceptance"
MAX_MESSAGE_BYTES = 1024 * 1024
ROOT = Path(os.environ.get("DORE_REPO_ROOT") or Path(__file__).resolve().parents[2]).expanduser().resolve()

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_adapter():
    path = Path(__file__).with_name("a2a_adapter.py")
    spec = importlib.util.spec_from_file_location("dore_local_a2a_adapter_native", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load adapter: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ADAPTER = _load_adapter()


def _read_exact(stream: BinaryIO, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError("unexpected EOF in Native Messaging frame")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def read_message(stream: BinaryIO) -> dict[str, Any] | None:
    header = stream.read(4)
    if not header:
        return None
    if len(header) != 4:
        raise EOFError("truncated Native Messaging header")
    (length,) = struct.unpack("<I", header)
    if length <= 0 or length > MAX_MESSAGE_BYTES:
        raise ValueError(f"invalid Native Messaging message length: {length}")
    raw = _read_exact(stream, length)
    payload = json.loads(raw.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Native Messaging payload must be a JSON object")
    return payload


def write_message(stream: BinaryIO, payload: dict[str, Any]) -> None:
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(raw) > MAX_MESSAGE_BYTES:
        raise ValueError("Native Messaging response exceeds size limit")
    stream.write(struct.pack("<I", len(raw)))
    stream.write(raw)
    stream.flush()


def _legacy_stage2_requested(payload: dict[str, Any]) -> bool:
    capability = str(payload.get("capability") or payload.get("capability_id") or "").strip()
    command = str(payload.get("command") or payload.get("text") or payload.get("message") or "").strip().lower()
    return capability == LEGACY_CAPABILITY or command in {"/dore stage2", "dore stage2"}


def health_payload() -> dict[str, Any]:
    return {
        "ok": True,
        "service": SERVICE,
        "host": HOST_NAME,
        "protocol": PROTOCOL,
        "transport": "firefox-native-messaging",
        "resident": False,
        "paid_runtime": False,
    }


def route_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("action") in {"native.health", "health"}:
        return health_payload()

    try:
        typed = ADAPTER.handle_companion_payload(payload)
    except Exception as exc:
        return {
            "ok": False,
            "protocol": PROTOCOL,
            "status": "failed",
            "error": {"code": "adapter_error", "message": str(exc)},
        }

    if typed is not None:
        return typed

    # Keep the already-PASSing Stage 2 diagnostic contract while transport is
    # migrated.  This is compatibility only; production typed traffic goes
    # through a2a_adapter above.
    if _legacy_stage2_requested(payload):
        return {
            "ok": True,
            "service": SERVICE,
            "protocol": PROTOCOL,
            "capability": LEGACY_CAPABILITY,
            "available": True,
            "status": "PASS",
            "diagnostic": True,
            "transport": "firefox-native-messaging",
        }

    return {
        "ok": False,
        "protocol": PROTOCOL,
        "status": "failed",
        "error": {"code": "unsupported_payload", "message": "unsupported Companion payload"},
    }


def serve(stdin: BinaryIO | None = None, stdout: BinaryIO | None = None) -> int:
    # stdout is protocol-only.  Any diagnostic output must go to stderr.
    source = stdin or sys.stdin.buffer
    sink = stdout or sys.stdout.buffer
    while True:
        try:
            payload = read_message(source)
            if payload is None:
                return 0
            response = route_payload(payload)
        except (EOFError, ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            print(f"[dore-native] framing error: {exc}", file=sys.stderr, flush=True)
            return 2
        except Exception as exc:  # Last-resort boundary: preserve the port.
            print(f"[dore-native] fatal error: {exc}", file=sys.stderr, flush=True)
            response = {
                "ok": False,
                "protocol": PROTOCOL,
                "status": "failed",
                "error": {"code": "native_host_error", "message": str(exc)},
            }
        write_message(sink, response)


if __name__ == "__main__":
    raise SystemExit(serve())
