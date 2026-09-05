import unittest
from pathlib import Path

from dore_core.capabilities.executor import CapabilityExecutor
from dore_core.capabilities.model import ArtifactRef, TaskState
from dore_core.capabilities.registry import default_registry
from dore_core.capabilities.runtime import LazyCapabilityRuntime
from dore_core.capabilities.synthetic_visual import synthetic_visual_handlers


class CapabilityExecutorTests(unittest.TestCase):
    def _executor(self):
        registry = default_registry()
        provider_calls = []

        def load_provider(ref: str):
            provider_calls.append(ref)
            return {"provider": ref, "mode": "test-double"}

        root = Path(__file__).resolve().parents[1]
        runtime = LazyCapabilityRuntime(registry, root=root, provider_loader=load_provider)
        return CapabilityExecutor(registry, runtime, synthetic_visual_handlers()), provider_calls

    def test_full_visual_sequence_uses_one_shared_state(self):
        executor, provider_calls = self._executor()
        state = TaskState("visual-e2e")
        state.add_artifact(ArtifactRef("request", "request", {"need": "Matthew 3 hero"}, ("user",)))
        sequence = (
            "visual.direct",
            "visual.grammar",
            "image.generate",
            "image.critic",
            "design.compose",
            "design.verify",
        )
        results = executor.execute_sequence(sequence, state)
        self.assertEqual(len(results), 6)
        self.assertTrue(all(result.ok for result in results))
        schemas = [artifact.schema for artifact in state.artifacts.values()]
        for schema in (
            "visual_brief",
            "style_recipe",
            "asset_candidate",
            "critique_result",
            "design_patch",
            "verification_result",
        ):
            self.assertIn(schema, schemas)
        self.assertEqual(provider_calls, ["local-image-renderer"])
        self.assertEqual(state.telemetry["provider_activations"], 1)
        self.assertEqual(state.telemetry["capability_executions"], 6)
        verification = next(a for a in state.artifacts.values() if a.schema == "verification_result")
        self.assertTrue(verification.payload["contract_valid"])
        self.assertFalse(verification.payload["real_render_verified"])

    def test_failure_stops_sequence_and_records_evidence(self):
        executor, _ = self._executor()
        state = TaskState("missing-upstream")
        results = executor.execute_sequence(("image.generate", "image.critic"), state)
        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].ok)
        self.assertIn("missing typed task artifacts", results[0].error)
        self.assertEqual(state.telemetry["capability_failures"], 1)
        self.assertEqual(state.telemetry["last_failure"]["capability_id"], "image.generate")
        self.assertEqual(state.telemetry["provider_activations"], 0)

    def test_handler_cannot_emit_undeclared_schema(self):
        registry = default_registry()
        runtime = LazyCapabilityRuntime(registry, root=Path(__file__).resolve().parents[1])

        def bad_handler(loaded, inputs, state):
            return {"wrong_schema": {"bad": True}}

        executor = CapabilityExecutor(registry, runtime, {"visual.direct": bad_handler})
        state = TaskState("bad-handler")
        result = executor.execute("visual.direct", state)
        self.assertFalse(result.ok)
        self.assertIn("output schema mismatch", result.error)
        self.assertNotIn("wrong_schema", [a.schema for a in state.artifacts.values()])


if __name__ == "__main__":
    unittest.main()
