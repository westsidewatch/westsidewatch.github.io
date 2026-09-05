#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dore_core.capabilities.image_command import parse_image_command
from dore_core.capabilities.image_runtime_config import load_resident_image_config
from scripts.dore_image_autorun import DEFAULT_CONFIG, run as autorun

HOST = "127.0.0.1"
PORT = 8790
_LOCK = threading.Lock()
_ALLOWED_ORIGINS = {
    "https://westsidewatch.github.io",
    "https://westsidewatch-github-io.pages.dev",
    "http://127.0.0.1",
    "http://localhost",
}
_IMAGE_SUFFIXES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def _origin_allowed(origin: str) -> bool:
    if not origin:
        return False
    if origin in _ALLOWED_ORIGINS:
        return True
    return origin.startswith("https://") and origin.endswith(".westsidewatch-github-io.pages.dev")


def _safe_artifact(artifact: dict, asset_url: str) -> dict:
    """Return browser-safe artifact metadata; never expose workstation paths."""
    safe = {k: artifact[k] for k in ("id", "sha256", "bytes", "mime_type") if k in artifact}
    safe["asset_url"] = asset_url
    return safe


class Handler(BaseHTTPRequestHandler):
    server_version = "DoreImageLocal/1.1"

    def _cors(self) -> None:
        origin = self.headers.get("Origin", "")
        if _origin_allowed(origin):
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Headers", "content-type,x-dore-origin")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        if self.headers.get("Access-Control-Request-Private-Network", "").lower() == "true":
            self.send_header("Access-Control-Allow-Private-Network", "true")

    def _json(self, status: int, payload: dict) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            cfg = DEFAULT_CONFIG.exists()
            renderer = False
            detail = "resident-config-missing"
            if cfg:
                try:
                    config = load_resident_image_config(DEFAULT_CONFIG)
                    from dore_core.capabilities.image_renderer import ComfyUIRenderer
                    from dore_core.capabilities.providers import ProviderDescriptor
                    renderer = ComfyUIRenderer(ProviderDescriptor("local-image-renderer", "http-json", config.endpoint, "local_free")).health().ok
                    detail = "ready" if renderer else "renderer-unreachable"
                except Exception as exc:
                    detail = type(exc).__name__
            self._json(200, {"ok": True, "node": "dore-image-local", "config": cfg, "renderer": renderer, "detail": detail})
            return
        if parsed.path == "/asset":
            raw_name = parse_qs(parsed.query).get("name", [""])[0]
            name = Path(raw_name).name
            if not name or name != raw_name or Path(name).suffix.lower() not in _IMAGE_SUFFIXES:
                self._json(400, {"ok": False, "error": "invalid asset name"})
                return
            try:
                config = load_resident_image_config(DEFAULT_CONFIG)
                root = (ROOT / config.output_dir).resolve()
                target = (root / name).resolve()
                if root not in target.parents or not target.is_file():
                    raise FileNotFoundError(name)
                data = target.read_bytes()
                self.send_response(200)
                self._cors()
                self.send_header("Content-Type", _IMAGE_SUFFIXES[target.suffix.lower()])
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            except Exception:
                self._json(404, {"ok": False, "error": "asset not found"})
            return
        self._json(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/generate":
            self._json(404, {"ok": False, "error": "not found"})
            return
        if self.headers.get("X-Dore-Origin") != "dore-search":
            self._json(403, {"ok": False, "error": "invalid dore origin"})
            return
        origin = self.headers.get("Origin", "")
        if origin and not _origin_allowed(origin):
            self._json(403, {"ok": False, "error": "origin not allowed"})
            return
        try:
            declared = int(self.headers.get("Content-Length", "0"))
            if declared <= 0 or declared > 64 * 1024:
                self._json(413, {"ok": False, "error": "invalid request size"})
                return
            payload = json.loads(self.rfile.read(declared))
            if not isinstance(payload, dict) or set(payload) - {"message"}:
                self._json(400, {"ok": False, "error": "unsupported request fields"})
                return
            command = parse_image_command(str(payload.get("message", "")))
            job_dir = ROOT / "dore-image" / "jobs"
            job_dir.mkdir(parents=True, exist_ok=True)
            with _LOCK:
                job_path = job_dir / "search-ai-next.json"
                job = {"subject": command.subject, "brief": command.brief, "seed": command.seed, "source": "dore-search-ai"}
                job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
                result = autorun(DEFAULT_CONFIG, job_path)
            if result.get("status") != "PASS":
                self._json(503, {"ok": False, "status": result.get("status", "FAIL"), "error": "image generation failed"})
                return
            artifact = dict(result.get("artifact") or {})
            name = Path(str(artifact.get("uri", ""))).name
            if not name:
                raise RuntimeError("renderer returned no asset")
            asset_url = f"http://{HOST}:{PORT}/asset?name={name}"
            self._json(200, {"ok": True, "capability": "image.generate", "message": command.message, "artifact": _safe_artifact(artifact, asset_url), "recipe": result.get("recipe"), "prompt_id": result.get("prompt_id"), "asset_url": asset_url})
        except ValueError as exc:
            self._json(400, {"ok": False, "error": str(exc)})
        except Exception as exc:
            self._json(500, {"ok": False, "error": type(exc).__name__})

    def log_message(self, fmt: str, *args) -> None:
        return


def main() -> int:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(json.dumps({"status": "READY", "node": "dore-image-local", "host": HOST, "port": PORT}))
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
