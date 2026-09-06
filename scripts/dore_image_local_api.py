#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import os
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
_IMAGE_SUFFIXES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".svg": "image/svg+xml"}


def _config_path() -> Path:
    return Path(os.environ.get("DORE_IMAGE_CONFIG", str(DEFAULT_CONFIG))).expanduser().resolve()


def _origin_allowed(origin: str) -> bool:
    if not origin:
        return False
    if origin in _ALLOWED_ORIGINS:
        return True
    return origin.startswith("https://") and origin.endswith(".westsidewatch-github-io.pages.dev")


def _comfy_health() -> tuple[bool, dict]:
    cfg_path = _config_path()
    if not cfg_path.exists():
        return False, {"config": False, "detail": "resident-config-missing"}
    try:
        config = load_resident_image_config(cfg_path)
        from dore_core.capabilities.image_renderer import ComfyUIRenderer
        from dore_core.capabilities.providers import ProviderDescriptor
        ok = ComfyUIRenderer(ProviderDescriptor("local-image-renderer", "http-json", config.endpoint, "local_free")).health().ok
        return ok, {"config": True, "detail": "ready" if ok else "renderer-unreachable", "endpoint": config.endpoint, "model": config.model}
    except Exception as exc:
        return False, {"config": True, "detail": type(exc).__name__}


def _safe_artifact(artifact: dict, asset_url: str) -> dict:
    safe = {k: artifact[k] for k in ("id", "sha256", "bytes", "mime_type") if k in artifact}
    safe["asset_url"] = asset_url
    return safe


def _native_svg(command) -> dict:
    out = ROOT / "dore-image" / "generated"
    out.mkdir(parents=True, exist_ok=True)
    seed = int(command.seed)
    title = html.escape(command.subject[:90])
    gold = "#CDB46A"
    ink = "#1E1E1B"
    paper = "#F5F0E5"
    lines = []
    for i in range(11):
        x1 = 90 + ((seed >> (i % 24)) % 280)
        y1 = 120 + i * 92
        x2 = 1110 - ((seed >> ((i + 7) % 24)) % 260)
        y2 = 130 + i * 94
        lines.append(f'<path d="M{x1} {y1} Q600 {y1-70+((seed+i)%140)} {x2} {y2}"/>')
    circles = []
    for i in range(5):
        cx = 250 + ((seed >> (i * 3)) % 700)
        cy = 300 + ((seed >> (i * 5 + 2)) % 850)
        r = 30 + ((seed >> (i * 4 + 1)) % 110)
        circles.append(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1500" viewBox="0 0 1200 1500">
<rect width="1200" height="1500" fill="{paper}"/>
<g fill="none" stroke="{gold}" stroke-width="3" opacity="0.84">{''.join(lines)}</g>
<g fill="none" stroke="{ink}" stroke-width="1.5" opacity="0.58">{''.join(circles)}</g>
<path d="M160 1180 L600 250 L1040 1180 Z" fill="none" stroke="{gold}" stroke-width="6" opacity="0.72"/>
<circle cx="600" cy="760" r="190" fill="none" stroke="{ink}" stroke-width="2"/>
<line x1="260" y1="1240" x2="940" y2="1240" stroke="{ink}" stroke-width="2"/>
<text x="600" y="1335" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="36" fill="{ink}" opacity="0.82">{title}</text>
</svg>'''
    raw = svg.encode("utf-8")
    sha = hashlib.sha256(raw).hexdigest()
    name = f"native-{sha[:20]}.svg"
    path = out / name
    path.write_bytes(raw)
    return {"id": f"sha256:{sha}", "sha256": sha, "bytes": len(raw), "mime_type": "image/svg+xml", "uri": str(path), "renderer": "dore-native-svg"}


class Handler(BaseHTTPRequestHandler):
    server_version = "DoreImageLocal/1.3"

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
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self) -> None:
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            comfy, meta = _comfy_health()
            self._json(200, {"ok": True, "node": "dore-image-local", "renderer": True, "renderer_mode": "comfyui" if comfy else "dore-native-svg", "native_svg": True, "comfyui": comfy, "detail": meta.get("detail"), "endpoint": meta.get("endpoint"), "model": meta.get("model"), "config": meta.get("config", False), "config_path": str(_config_path())})
            return
        if parsed.path == "/asset":
            raw_name = parse_qs(parsed.query).get("name", [""])[0]
            name = Path(raw_name).name
            if not name or name != raw_name or Path(name).suffix.lower() not in _IMAGE_SUFFIXES:
                self._json(400, {"ok": False, "error": "invalid asset name"}); return
            roots = [(ROOT / "dore-image" / "generated").resolve()]
            try:
                if _config_path().exists():
                    cfg = load_resident_image_config(_config_path())
                    roots.append((ROOT / cfg.output_dir).resolve())
            except Exception:
                pass
            target = None
            for root in roots:
                candidate = (root / name).resolve()
                if root in candidate.parents and candidate.is_file():
                    target = candidate; break
            if target is None:
                self._json(404, {"ok": False, "error": "asset not found"}); return
            data = target.read_bytes()
            self.send_response(200); self._cors(); self.send_header("Content-Type", _IMAGE_SUFFIXES[target.suffix.lower()]); self.send_header("Cache-Control", "no-store"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data); return
        self._json(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/generate": self._json(404, {"ok": False, "error": "not found"}); return
        if self.headers.get("X-Dore-Origin") != "dore-search": self._json(403, {"ok": False, "error": "invalid dore origin"}); return
        origin = self.headers.get("Origin", "")
        if origin and not _origin_allowed(origin): self._json(403, {"ok": False, "error": "origin not allowed"}); return
        try:
            declared = int(self.headers.get("Content-Length", "0"))
            if declared <= 0 or declared > 64 * 1024: self._json(413, {"ok": False, "error": "invalid request size"}); return
            payload = json.loads(self.rfile.read(declared))
            if not isinstance(payload, dict) or set(payload) - {"message"}: self._json(400, {"ok": False, "error": "unsupported request fields"}); return
            command = parse_image_command(str(payload.get("message", "")))
            with _LOCK:
                comfy, _ = _comfy_health()
                if comfy:
                    job_dir = ROOT / "dore-image" / "jobs"; job_dir.mkdir(parents=True, exist_ok=True)
                    job_path = job_dir / "search-ai-next.json"
                    job_path.write_text(json.dumps({"subject": command.subject, "brief": command.brief, "seed": command.seed, "source": "dore-search-ai", "design": False}, ensure_ascii=False, indent=2), encoding="utf-8")
                    result = autorun(_config_path(), job_path)
                    if result.get("status") != "PASS": self._json(503, {"ok": False, "status": result.get("status", "FAIL"), "error": "image generation failed", "reason": result.get("reason")}); return
                    artifact = dict(result.get("artifact") or {}); renderer = "comfyui"; recipe = result.get("recipe"); prompt_id = result.get("prompt_id")
                else:
                    artifact = _native_svg(command); renderer = "dore-native-svg"; recipe = {"family": "DORÉ/NATIVE-EDITORIAL", "seed": command.seed}; prompt_id = None
            name = Path(str(artifact.get("uri", ""))).name
            if not name: raise RuntimeError("renderer returned no asset")
            asset_url = f"http://{HOST}:{PORT}/asset?name={name}"
            safe = _safe_artifact(artifact, asset_url); safe["renderer"] = renderer
            self._json(200, {"ok": True, "capability": "image.generate", "message": command.message, "renderer": renderer, "artifact": safe, "recipe": recipe, "prompt_id": prompt_id, "asset_url": asset_url})
        except ValueError as exc: self._json(400, {"ok": False, "error": str(exc)})
        except Exception as exc: self._json(500, {"ok": False, "error": type(exc).__name__})

    def log_message(self, fmt: str, *args) -> None: return


def main() -> int:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(json.dumps({"status": "READY", "node": "dore-image-local", "host": HOST, "port": PORT, "config": str(_config_path())}))
    server.serve_forever(); return 0


if __name__ == "__main__": raise SystemExit(main())
