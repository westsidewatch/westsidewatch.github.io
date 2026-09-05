from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .bootstrap import build_local_design_control_plane
from .transport import TransportError, handle_envelope

HOST = "127.0.0.1"
PORT = 4312


class Resident4312:
    def __init__(self, root: str | Path = ".") -> None:
        self.plane = build_local_design_control_plane(root)

    def handle(self, envelope: dict[str, Any]) -> dict[str, Any]:
        return handle_envelope(self.plane, envelope)


def make_handler(resident: Resident4312):
    class Handler(BaseHTTPRequestHandler):
        server_version = "DoreA2A/1"

        def _json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/health":
                self._json(200, {"ok": True, "protocol": "dore.a2a/1", "service": "resident-4312"})
                return
            self._json(404, {"ok": False, "error": "not_found"})

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/a2a":
                self._json(404, {"ok": False, "error": "not_found"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 1024 * 1024:
                    raise TransportError("invalid content length")
                raw = self.rfile.read(length)
                payload = json.loads(raw.decode("utf-8"))
                if not isinstance(payload, dict):
                    raise TransportError("envelope must be an object")
                self._json(200, resident.handle(payload))
            except (TransportError, json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
                self._json(400, {"protocol": "dore.a2a/1", "status": "failed", "error": str(exc)})
            except Exception as exc:  # fail closed without leaking internals
                self._json(500, {"protocol": "dore.a2a/1", "status": "failed", "error": type(exc).__name__})

        def log_message(self, format: str, *args: object) -> None:
            return

    return Handler


def serve(root: str | Path = ".", host: str = HOST, port: int = PORT) -> None:
    if host not in {"127.0.0.1", "localhost"}:
        raise ValueError("resident control plane must bind to loopback")
    resident = Resident4312(root)
    httpd = ThreadingHTTPServer((host, port), make_handler(resident))
    httpd.serve_forever()


if __name__ == "__main__":
    serve()
