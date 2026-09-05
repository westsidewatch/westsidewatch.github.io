from __future__ import annotations

import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "local" / "dore-local" / "a2a_adapter.py"


def load_adapter():
    spec = importlib.util.spec_from_file_location("dore_local_a2a_adapter", ADAPTER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class MatureLocalA2AControlBridgeTests(unittest.TestCase):
    def setUp(self):
        self.adapter = load_adapter()

    def test_legacy_helpers_remain_available(self):
        task = self.adapter.dore_to_a2a_task(
            source_message_id="legacy-1",
            parent_goal="legacy acceptance",
            state="PASS",
            body="ok",
        )
        self.assertTrue(self.adapter.validate_task(task)["ok"])
        self.assertEqual(task["status"]["state"], "completed")

    def test_discover_design_over_mature_adapter(self):
        result = self.adapter.handle_companion_payload({
            "protocol": "dore.a2a/1",
            "action": "discover",
        })
        self.assertEqual(result["status"], "succeeded")
        self.assertEqual(result["consumers"][0]["id"], "design")
        self.assertEqual(
            result["consumers"][0]["capability_ids"],
            ("design.compose", "design.verify"),
        )

    def test_design_dispatch_replay_and_status(self):
        envelope = {
            "protocol": "dore.a2a/1",
            "action": "dispatch",
            "request_id": "mature-bridge-1",
            "conversation_id": "conversation-1",
            "session_id": "session-1",
            "consumer_id": "design",
            "capability_id": "design.compose",
            "payload": {
                "asset_candidate": {
                    "asset_id": "synthetic:mature-path",
                    "kind": "test-double",
                }
            },
        }
        first = self.adapter.handle_companion_payload(envelope)
        second = self.adapter.handle_companion_payload(envelope)
        self.assertEqual(first["status"], "succeeded")
        self.assertFalse(first["replayed"])
        self.assertTrue(second["replayed"])
        self.assertEqual(first["conversation_id"], "conversation-1")
        self.assertEqual(first["session_id"], "session-1")
        self.assertIn("design_patch", first["result"])

        status = self.adapter.handle_companion_payload({
            "protocol": "dore.a2a/1",
            "action": "status",
            "request_id": "mature-bridge-1",
            "conversation_id": "conversation-1",
            "session_id": "session-1",
        })
        self.assertEqual(status["status"], "succeeded")

    def test_non_typed_payload_is_left_for_existing_legacy_route(self):
        self.assertIsNone(self.adapter.handle_companion_payload({"capability": "design2.stage2.acceptance"}))


if __name__ == "__main__":
    unittest.main()
