import unittest
from pathlib import Path

from dore_core.capabilities.consolidation import ConsolidationLedger
from dore_core.capabilities.executor import CapabilityExecutor
from dore_core.capabilities.model import ArtifactRef, TaskState
from dore_core.capabilities.registry import default_registry
from dore_core.capabilities.runtime import LazyCapabilityRuntime
from dore_core.capabilities.synthetic_visual import synthetic_visual_handlers


class CapabilityConsolidationTests(unittest.TestCase):
    def setUp(self):
        self.registry = default_registry()
        self.root = Path(__file__).resolve().parents[1]

    def _successful_direct(self, suffix: int):
        runtime = LazyCapabilityRuntime(self.registry, root=self.root)
        executor = CapabilityExecutor(self.registry, runtime, synthetic_visual_handlers())
        state = TaskState(f"success-{suffix}")
        state.add_artifact(ArtifactRef("request", "request", {"need": f"hero {suffix}"}, ("test",)))
        return executor.execute("visual.direct", state), state

    def test_repeated_success_creates_candidate_not_promotion(self):
        ledger = ConsolidationLedger()
        manifest = self.registry.get("visual.direct")
        for i in range(3):
            result, state = self._successful_direct(i)
            self.assertTrue(result.ok)
            ledger.record(result, state, declared_inputs=manifest.inputs, declared_outputs=manifest.outputs)
        candidate = ledger.candidate("visual.direct", min_successes=3, target_level="L1")
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.status, "REGRESSION_REQUIRED")
        self.assertEqual(candidate.successful_runs, 3)
        self.assertEqual(candidate.failed_runs, 0)
        self.assertIn("not automatic", candidate.reason)

    def test_matching_failure_blocks_candidate(self):
        ledger = ConsolidationLedger()
        manifest = self.registry.get("visual.direct")
        for i in range(3):
            result, state = self._successful_direct(i)
            ledger.record(result, state, declared_inputs=manifest.inputs, declared_outputs=manifest.outputs)

        runtime = LazyCapabilityRuntime(self.registry, root=self.root)
        failing_executor = CapabilityExecutor(self.registry, runtime, handlers={})
        failed_state = TaskState("failed")
        failed = failing_executor.execute("visual.direct", failed_state)
        self.assertFalse(failed.ok)
        ledger.record(failed, failed_state, declared_inputs=manifest.inputs, declared_outputs=manifest.outputs)

        candidate = ledger.candidate("visual.direct", min_successes=3)
        self.assertEqual(candidate.status, "BLOCKED")
        self.assertEqual(candidate.successful_runs, 3)
        self.assertEqual(candidate.failed_runs, 1)

    def test_insufficient_evidence_stays_dormant(self):
        ledger = ConsolidationLedger()
        manifest = self.registry.get("visual.direct")
        result, state = self._successful_direct(1)
        ledger.record(result, state, declared_inputs=manifest.inputs, declared_outputs=manifest.outputs)
        candidate = ledger.candidate("visual.direct", min_successes=3)
        self.assertEqual(candidate.status, "INSUFFICIENT_EVIDENCE")
        self.assertIsNone(ledger.candidate("image.generate"))


if __name__ == "__main__":
    unittest.main()
