import unittest

from dore_core.intelligence.registry import Provider, provider_map, validate as validate_provider
from dore_core.intelligence.residency import ResidencyState
from dore_core.intelligence.router import choose_route
from dore_core.intelligence.substrates import LONGMEMORY, QMD, validate as validate_substrate


class IntelligenceFabricTests(unittest.TestCase):
    def test_deterministic_lane_wins_before_ai(self):
        decision = choose_route("research", deterministic_available=True, providers={"research": "large"})
        self.assertEqual(decision.lane, "deterministic")
        self.assertIsNone(decision.provider)

    def test_tiny_lane_prevents_large_model_load(self):
        decision = choose_route("language", tiny_sufficient=True, resident={"tiny-reflex": "tiny-local"}, providers={"language": "large-local"})
        self.assertEqual(decision.lane, "tiny-hot")
        self.assertEqual(decision.provider, "tiny-local")
        self.assertEqual(decision.load, "reuse")

    def test_resident_specialist_is_reused(self):
        decision = choose_route("coding", resident={"coding": "code-local"}, providers={"coding": "other"})
        self.assertEqual(decision.lane, "resident-specialist")
        self.assertEqual(decision.provider, "code-local")

    def test_single_large_residency_evicts_previous_specialist(self):
        state = ResidencyState(max_large_resident=1)
        self.assertEqual(state.admit("language", "lang-local", large=True), ())
        self.assertEqual(state.admit("coding", "code-local", large=True), ("language",))
        self.assertEqual(state.resident_map(), {"coding": "code-local"})

    def test_tiny_and_large_can_coexist_without_two_large_models(self):
        state = ResidencyState(max_large_resident=1)
        state.admit("tiny-reflex", "tiny-local", large=False)
        state.admit("reasoning", "reason-local", large=True)
        self.assertEqual(state.resident_map(), {"tiny-reflex": "tiny-local", "reasoning": "reason-local"})

    def test_free_local_provider_gate(self):
        self.assertEqual(provider_map([Provider("language", "local-language")]), {"language": "local-language"})
        with self.assertRaises(ValueError):
            validate_provider(Provider("language", "remote", local=False))
        with self.assertRaises(ValueError):
            validate_provider(Provider("language", "paid", paid=True))

    def test_longmemory_and_qmd_are_non_authoritative_substrates(self):
        self.assertEqual(validate_substrate(LONGMEMORY).role, "knowledge")
        self.assertEqual(validate_substrate(QMD).role, "retrieval")
        self.assertFalse(LONGMEMORY.authoritative)
        self.assertFalse(QMD.authoritative)


if __name__ == "__main__":
    unittest.main()
