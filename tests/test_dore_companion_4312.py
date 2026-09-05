from __future__ import annotations

import importlib.util
import json
import pathlib
import threading
import unittest
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
SERVICE_PATH = ROOT / "local" / "dore-local" / "companion_4312.py"


def load_service():
    spec = importlib.util.spec_from_file_location("dore_companion_4312_test", SERVICE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class Companion4312ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = load_service()

    def test_health_preserves_legacy_and_exposes_design(self):
        h = self.service.health_payload()
        self.assertTrue(h["ok"])
        self.assertEqual(h["service"], "dore-a2a-plus")
        self.assertEqual(h["protocol"], "dore.a2a/1")
        caps = {c["id"]: c for c in h["capabilities"]}
        self.assertTrue(caps["design2.stage2.acceptance"]["available"])
        self.assertTrue(caps["design.compose"]["available"])
        self.assertTrue(caps["design.verify"]["available"])

    def test_legacy_stage2_diagnostic_remains_pass(self):
        for payload in (
            {"capability": "design2.stage2.acceptance"},
            {"command": "/dore stage2"},
            {"text": "dore stage2"},
        ):
            code, body = self.service.route_payload(payload)
            self.assertEqual(code, 200)
            self.assertEqual(body["status"], "PASS")
            self.assertEqual(body["capability"], "design2.stage2.acceptance")

    def test_typed_discover_uses_mature_adapter(self):
        code, body = self.service.route_payload({"protocol": "dore.a2a/1", "action": "discover"})
        self.assertEqual(code, 200)
        self.assertEqual(body["protocol"], "dore.a2a/1")
        self.assertEqual(body["status"], "succeeded")
        consumers = {c["id"]: c for c in body["consumers"]}
        self.assertEqual(consumers["design"]["capability_ids"], ["design.compose", "design.verify"])

    def test_typed_design_compose_and_status_round_trip(self):
        request = {
            "protocol": "dore.a2a/1",
            "action": "dispatch",
            "request_id": "companion-4312-compose-1",
            "conversation_id": "conversation-1",
            "session_id": "session-1",
            "consumer_id": "design",
            "capability_id": "design.compose",
            "payload": {"asset_candidate": {"kind": "test", "content": {"title": "DORÉ"}}},
        }
        code, first = self.service.route_payload(request)
        self.assertEqual(code, 200)
        self.assertEqual(first["status"], "succeeded")
        self.assertIn("design_patch", first["result"])

        code, replay = self.service.route_payload(request)
        self.assertEqual(code, 200)
        self.assertTrue(replay["replayed"])

        code, status = self.service.route_payload({
            "protocol": "dore.a2a/1",
            "action": "status",
            "request_id": request["request_id"],
            "conversation_id": request["conversation_id"],
            "session_id": request["session_id"],
        })
        self.assertEqual(code, 200)
        self.assertEqual(status["status"], "succeeded")

    def test_http_health_and_post_use_same_contract(self):
        server = self.service.ThreadingHTTPServer(("127.0.0.1", 0), self.service.Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f"http://127.0.0.1:{server.server_address[1]}"
            with urllib.request.urlopen(base + "/health", timeout=2) as response:
                health = json.load(response)
            self.assertEqual(health["service"], "dore-a2a-plus")

            data = json.dumps({"capability": "design2.stage2.acceptance"}).encode()
            req = urllib.request.Request(base + "/command", data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=2) as response:
                legacy = json.load(response)
            self.assertEqual(legacy["status"], "PASS")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
