import unittest

from dore_core.capabilities.executor import CapabilityExecutor
from dore_core.capabilities.registry import default_registry
from dore_core.capabilities.runtime import LazyCapabilityRuntime
from dore_core.control_plane.runtime import build_design_control_plane
from dore_core.control_plane.transport import PROTOCOL, TransportError, handle_envelope


class ControlPlaneTransportTests(unittest.TestCase):
    def setUp(self):
        registry = default_registry()
        runtime = LazyCapabilityRuntime(registry, root=".")
        executor = CapabilityExecutor(registry, runtime)

        def compose(_loaded, inputs, _state):
            asset = inputs["asset_candidate"]
            return {"design_patch": {"source_hash": asset.content_hash, "ops": ["place"]}}

        def verify(_loaded, inputs, _state):
            patch = inputs["design_patch"]
            return {"verification_result": {"source_hash": patch.content_hash, "ok": True}}

        executor.register_handler("design.compose", compose)
        executor.register_handler("design.verify", verify)
        self.plane = build_design_control_plane(registry, executor)

    def envelope(self, **changes):
        base = {
            "protocol": PROTOCOL,
            "action": "dispatch",
            "request_id": "req-transport-1",
            "conversation_id": "conv-transport-1",
            "session_id": "sess-transport-1",
            "consumer_id": "design",
            "capability_id": "design.compose",
            "payload": {"asset_candidate": {"uri": "local://candidate/transport-1"}},
        }
        base.update(changes)
        return base

    def test_discovery_exposes_design_without_design_logic_in_transport(self):
        result = handle_envelope(self.plane, {"protocol": PROTOCOL, "action": "discover"})
        self.assertEqual(result["status"], "succeeded")
        self.assertEqual([item["id"] for item in result["consumers"]], ["design"])
        self.assertEqual(result["consumers"][0]["capability_ids"], ("design.compose", "design.verify"))

    def test_dispatch_returns_typed_design_result(self):
        result = handle_envelope(self.plane, self.envelope())
        self.assertEqual(result["protocol"], PROTOCOL)
        self.assertEqual(result["status"], "succeeded")
        self.assertIn("design_patch", result["result"])

    def test_replay_is_idempotent_but_request_id_identity_is_immutable(self):
        first = handle_envelope(self.plane, self.envelope())
        replay = handle_envelope(self.plane, self.envelope())
        hijack = handle_envelope(self.plane, self.envelope(session_id="sess-other"))
        self.assertFalse(first["replayed"])
        self.assertTrue(replay["replayed"])
        self.assertEqual(hijack["status"], "failed")
        self.assertIn("request_id already bound", hijack["error"])

    def test_status_is_bound_to_same_conversation_and_session(self):
        handle_envelope(self.plane, self.envelope())
        status = handle_envelope(self.plane, {
            "protocol": PROTOCOL,
            "action": "status",
            "request_id": "req-transport-1",
            "conversation_id": "conv-transport-1",
            "session_id": "sess-transport-1",
        })
        denied = handle_envelope(self.plane, {
            "protocol": PROTOCOL,
            "action": "status",
            "request_id": "req-transport-1",
            "conversation_id": "conv-transport-1",
            "session_id": "sess-other",
        })
        self.assertEqual(status["status"], "succeeded")
        self.assertEqual(denied["status"], "failed")
        self.assertIn("not bound", denied["error"])

    def test_unknown_consumer_and_capability_fail_closed(self):
        unknown = handle_envelope(self.plane, self.envelope(request_id="req-unknown", consumer_id="other"))
        denied = handle_envelope(self.plane, self.envelope(request_id="req-denied", capability_id="image.generate"))
        self.assertEqual(unknown["status"], "failed")
        self.assertEqual(denied["status"], "failed")

    def test_malformed_protocol_and_payload_fail_closed(self):
        with self.assertRaises(TransportError):
            handle_envelope(self.plane, self.envelope(protocol="wrong"))
        with self.assertRaises(TransportError):
            handle_envelope(self.plane, self.envelope(payload=[]))
        with self.assertRaises(TransportError):
            handle_envelope(self.plane, {"protocol": PROTOCOL, "action": "bogus"})


if __name__ == "__main__":
    unittest.main()
