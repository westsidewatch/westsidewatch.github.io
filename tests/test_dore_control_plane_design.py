import unittest

from dore_core.capabilities.executor import CapabilityExecutor
from dore_core.capabilities.registry import default_registry
from dore_core.capabilities.runtime import LazyCapabilityRuntime
from dore_core.control_plane.model import ControlRequest
from dore_core.control_plane.runtime import build_design_control_plane


class DesignControlPlaneTests(unittest.TestCase):
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

    def test_design_is_first_discoverable_consumer(self):
        consumers = self.plane.discover()
        self.assertEqual([c.id for c in consumers], ["design"])
        self.assertEqual(consumers[0].capability_ids, ("design.compose", "design.verify"))

    def test_conversation_session_binding_and_typed_result(self):
        result = self.plane.dispatch(ControlRequest(
            request_id="req-1",
            conversation_id="conv-1",
            session_id="sess-1",
            consumer_id="design",
            capability_id="design.compose",
            payload={"asset_candidate": {"uri": "local://candidate/1"}},
        ))
        self.assertEqual(result.status, "succeeded")
        self.assertIn("design_patch", result.result)
        self.assertEqual(self.plane.status("req-1"), result)

    def test_request_id_is_idempotent(self):
        request = ControlRequest(
            request_id="req-repeat",
            conversation_id="conv-1",
            session_id="sess-1",
            consumer_id="design",
            capability_id="design.compose",
            payload={"asset_candidate": {"uri": "local://candidate/1"}},
        )
        first = self.plane.dispatch(request)
        second = self.plane.dispatch(request)
        self.assertFalse(first.replayed)
        self.assertTrue(second.replayed)
        self.assertEqual(first.result, second.result)

    def test_conversation_cannot_jump_sessions(self):
        first = ControlRequest(
            request_id="req-bind",
            conversation_id="conv-bind",
            session_id="sess-a",
            consumer_id="design",
            capability_id="design.compose",
            payload={"asset_candidate": {"uri": "local://candidate/1"}},
        )
        second = ControlRequest(
            request_id="req-jump",
            conversation_id="conv-bind",
            session_id="sess-b",
            consumer_id="design",
            capability_id="design.compose",
            payload={"asset_candidate": {"uri": "local://candidate/2"}},
        )
        self.assertEqual(self.plane.dispatch(first).status, "succeeded")
        rejected = self.plane.dispatch(second)
        self.assertEqual(rejected.status, "failed")
        self.assertIn("another session", rejected.error)

    def test_design_cannot_call_unexposed_capability(self):
        result = self.plane.dispatch(ControlRequest(
            request_id="req-deny",
            conversation_id="conv-1",
            session_id="sess-1",
            consumer_id="design",
            capability_id="image.generate",
        ))
        self.assertEqual(result.status, "failed")
        self.assertIn("not exposed", result.error)


if __name__ == "__main__":
    unittest.main()
