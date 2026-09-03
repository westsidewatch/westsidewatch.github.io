#!/usr/bin/env python3
"""End-to-end acceptance for Storybook → Doré Design Promotion Pipeline v1."""
from __future__ import annotations

import hashlib
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import promotion_pipeline as pipeline


def request(base, path, data=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(base + path, data=body, headers={"Content-Type": "application/json"} if body else {}, method="POST" if body else "GET")
    with urllib.request.urlopen(req, timeout=5) as response:
        return response.status, response.headers.get_content_type(), response.read()


baseline_before = hashlib.sha256(pipeline.BASELINE.read_bytes()).hexdigest()
specimen = HERE / "promotion" / "specimens" / "living-current.v1.json"
gate = pipeline.evaluate(json.loads(specimen.read_text(encoding="utf-8")))
assert gate["ok"] and all(gate["checks"].values()), gate
bad = json.loads(specimen.read_text(encoding="utf-8")); bad["gates"]["WESTSIDE_FIT"] = False
assert not pipeline.evaluate(bad)["ok"], "promotion gate accepted failed Westside fit"
storybook_evidence = HERE / "knowledge-lab" / "evidence" / "storybook-autonomy" / "latest.json"
promoted = pipeline.promote_storybook_evidence(specimen, storybook_evidence); assert promoted["ok"] and promoted["promoted"]

with tempfile.TemporaryDirectory() as directory:
    env = os.environ.copy(); env["DORE_DESIGN_DATA"] = directory
    initialize = subprocess.run([sys.executable, "-c", "import app_workspace; app_workspace.workspace()"], cwd=HERE, env=env, text=True, capture_output=True, timeout=30)
    assert initialize.returncode == 0, initialize.stderr
    rebuild = subprocess.run([sys.executable, str(HERE / "upgrade_living_fortress_v2.py")], cwd=HERE, env=env, text=True, capture_output=True, timeout=30)
    assert rebuild.returncode == 0, rebuild.stderr
    install = subprocess.run([sys.executable, str(HERE / "install_homepage_candidates.py")], cwd=HERE, env=env, text=True, capture_output=True, timeout=30)
    assert install.returncode == 0, install.stderr
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0)); port = sock.getsockname()[1]
    env["DORE_DESIGN_PORT"] = str(port)
    server = subprocess.Popen([sys.executable, str(HERE / "app_visual_v2.py")], cwd=HERE, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        base = f"http://127.0.0.1:{port}"
        for _ in range(50):
            try:
                request(base, "/api/health"); break
            except Exception: time.sleep(.1)
        else: raise AssertionError("Doré Design service did not start")
        status, _, raw = request(base, "/api/candidates"); candidates = json.loads(raw)
        assert status == 200 and candidates["candidates"][0]["id"] == "new-westside-living-current-v1"
        _, content_type, editor = request(base, "/editor?page=homepage-concept-dispatch")
        assert content_type == "text/html" and b"STORYBOOK" in editor and b"CANDIDATE JUDGMENT" in editor
        _, _, canvas = request(base, "/editor-canvas?page=homepage-concept-dispatch")
        assert b"LIVING CURRENT" in canvas and b'data-node-id="home-title"' in canvas
        _, _, raw = request(base, "/api/candidates/judgment", {"candidate_id": "new-westside-living-current-v1", "decision": "accepted", "reason": "Vertical current and restrained two-ink field fit New Westside.", "signals": ["editorial-gravity", "living-water"]})
        judgment = json.loads(raw); assert judgment["ok"] and not judgment["baseline_262_modified"]
        _, _, raw = request(base, "/api/candidates"); after = json.loads(raw)
        assert after["candidates"][0]["runtime_status"] == "accepted"
        feedback = Path(directory) / "candidate-feedback.jsonl"
        row = json.loads(feedback.read_text(encoding="utf-8").splitlines()[-1])
        assert row["returns_to"] == ["storybook", "knowledge-lab"]
    finally:
        server.terminate()
        try: server.wait(timeout=3)
        except subprocess.TimeoutExpired: server.kill()

baseline_after = hashlib.sha256(pipeline.BASELINE.read_bytes()).hexdigest()
assert baseline_after == baseline_before == "e1eb928a030fa9af1924513d34b73c93afa5afc69878fd93494cb6f9cc8fa034"
print(json.dumps({"ok": True, "code": "DORE_STORYBOOK_PROMOTION_V1_PASS", "candidate_id": "new-westside-living-current-v1", "promotion_gate": "PASS", "candidate_gallery": "PASS", "editable_canvas": "PASS", "feedback_roundtrip": "PASS", "baseline_262_immutable": True}, ensure_ascii=False))
