#!/usr/bin/env python3
"""DORÉ A2A Companion localhost service v1.

Single replacement service for the established ChatGPT Companion -> 127.0.0.1:4312
path.  It preserves the legacy Stage 2 diagnostic contract and routes typed
``dore.a2a/1`` envelopes through the mature ``a2a_adapter`` seam.

Stdlib only.  No OpenAI API, no GitHub mailbox control plane, no paid runtime.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

HOST = "127.0.0.1"
PORT = int(os.environ.get("DORE_A2A_PORT", "4312"))
SERVICE = "dore-a2a-plus"
PROTOCOL = "dore.a2a/1"
LEGACY_CAPABILITY = "design2.stage2.acceptance"
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


def health_payload() -> dict[str, Any]:
    return {
        "ok": True,
        "service": SERVICE,
        "protocol": PROTOCOL,
        "version": "1.0",
        "bind": f"{HOST}:{PORT}",
        "capabilities": [
            {"id": LEGACY_CAPABILITY, "available": True, "surface": "diagnostic"},
            {"id": "design.compose", "available": True, "consumer": "design"},
            {"id": "design.verify", "available": True, "consumer": "design"},
        ],
    }


def _legacy_stage2_requested(payload: dict[str, Any]) -> bool:
    capability = str(payload.get("capability") or payload.get("capability_id") or "").strip()
    command = str(payload.get("command") or payload.get("text") or payload.get("message") or "").strip().lower()
    return capability == LEGACY_CAPABILITY or command in {"/dore stage2", "dore stage2"}


def route_payload(payload: Any) -> tuple[int, dict[str, Any]]:
    if not isinstance(payload, dict):
        return 400, {"ok": False, "error": "JSON body must be an object"}

    try:
        typed = ADAPTER.handle_companion_payload(payload)
    except Exception as exc:
        return 400, {"ok": False, "protocol": PROTOCOL, "error": str(exc)}
    if typed is not None:
        return 200, typed

    if _legacy_stage2_requested(payload):
        return 200, {
            "ok": True,
            "service": SERVICE,
            "protocol": PROTOCOL,
            "capability": LEGACY_CAPABILITY,
            "available": True,
            "status": "PASS",
            "diagnostic": True,
        }

    return 400, {"ok": False, "error": "unsupported Companion payload"}


class Handler(BaseHTTPRequestHandler):
    server_version = "DoreA2A/1.0"

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write("[dore-a2a] " + (fmt % args) + "\n")

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path.rstrip("/") == "/health":
            self._json(200, health_payload())
            return
        self._json(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:
        if self.path.rstrip("/") not in {"", "/a2a", "/command", "/dispatch"}:
            self._json(404, {"ok": False, "error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 1024 * 1024:
                raise ValueError("invalid body length")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            self._json(400, {"ok": False, "error": str(exc)})
            return
        status, response = route_payload(payload)
        self._json(status, response)


def serve() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(json.dumps(health_payload(), ensure_ascii=False), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    serve()
