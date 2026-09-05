import json
import threading
import time
import unittest
from urllib.request import Request, urlopen

from http.server import ThreadingHTTPServer

from dore_core.control_plane.resident_4312 import Resident4312, make_handler


class Resident4312Tests(unittest.TestCase):
    def setUp(self):
        self.resident = Resident4312(".")
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.resident))
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        time.sleep(0.02)

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=1)

    def _get(self, path):
        with urlopen(f"http://127.0.0.1:{self.port}{path}", timeout=2) as response:
            return response.status, json.loads(response.read().decode("utf-8"))

    def _post(self, payload):
        req = Request(
            f"http://127.0.0.1:{self.port}/a2a",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(req, timeout=2) as response:
            return response.status, json.loads(response.read().decode("utf-8"))

    def test_health(self):
        status, body = self._get("/health")
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertEqual(body["protocol"], "dore.a2a/1")

    def test_discover_design(self):
        status, body = self._post({"protocol": "dore.a2a/1", "action": "discover"})
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "succeeded")
        self.assertEqual([c["id"] for c in body["consumers"]], ["design"])

    def test_dispatch_design_compose_and_replay(self):
        envelope = {
            "protocol": "dore.a2a/1",
            "action": "dispatch",
            "request_id": "acceptance-design-1",
            "conversation_id": "conversation-live",
            "session_id": "session-live",
            "consumer_id": "design",
            "capability_id": "design.compose",
            "payload": {
                "asset_candidate": {
                    "asset_id": "acceptance:asset:1",
                    "kind": "test-double",
                }
            },
        }
        status, first = self._post(envelope)
        self.assertEqual(status, 200)
        self.assertEqual(first["status"], "succeeded")
        self.assertEqual(first["conversation_id"], "conversation-live")
        self.assertEqual(first["session_id"], "session-live")
        self.assertIn("design_patch", first["result"])
        self.assertFalse(first["replayed"])

        _, second = self._post(envelope)
        self.assertEqual(second["status"], "succeeded")
        self.assertTrue(second["replayed"])

    def test_status_is_bound_to_session(self):
        envelope = {
            "protocol": "dore.a2a/1",
            "action": "dispatch",
            "request_id": "acceptance-status-1",
            "conversation_id": "conversation-status",
            "session_id": "session-a",
            "consumer_id": "design",
            "capability_id": "design.compose",
            "payload": {"asset_candidate": {"asset_id": "acceptance:asset:2"}},
        }
        self._post(envelope)
        _, body = self._post({
            "protocol": "dore.a2a/1",
            "action": "status",
            "request_id": "acceptance-status-1",
            "conversation_id": "conversation-status",
            "session_id": "session-b",
        })
        self.assertEqual(body["status"], "failed")
        self.assertIn("not bound", body["error"])


if __name__ == "__main__":
    unittest.main()
