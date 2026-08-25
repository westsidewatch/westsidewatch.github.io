import importlib.util
import unittest
from pathlib import Path

RUNTIME_DIR = Path(__file__).resolve().parents[1] / "runtime"


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, RUNTIME_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


context_module = load_module("build_conversation_context", "build_conversation_context.py")
contribution_module = load_module("conversation_contribution", "conversation_contribution.py")


class ConversationContributionTests(unittest.TestCase):
    def setUp(self):
        self.packet = context_module.build_packet()
        self.runtime_ref = "persistent_runtime_state"

    def test_grounded_judgment_carries_evidence_uncertainty_and_authority(self):
        item = contribution_module.build_contribution(
            context_packet=self.packet,
            contribution_type="judgment",
            content="P01 remains runnable but production verification is incomplete.",
            evidence_refs=[self.runtime_ref],
            uncertainty="low",
            authority_level="A1",
        )
        self.assertEqual(item["project_id"], "P01-PREFLIGHT-SUBTITLE")
        self.assertEqual(item["evidence_refs"], [self.runtime_ref])
        self.assertEqual(item["uncertainty"], "low")
        self.assertTrue(item["authority"]["human_church_authority_final"])
        self.assertFalse(item["authority"]["public_conversation_authorized"])

    def test_fact_like_contribution_without_evidence_is_rejected(self):
        with self.assertRaises(contribution_module.ContributionError):
            contribution_module.build_contribution(
                context_packet=self.packet,
                contribution_type="evidence",
                content="A project fact without evidence.",
            )

    def test_unknown_evidence_reference_is_rejected(self):
        with self.assertRaises(contribution_module.ContributionError):
            contribution_module.build_contribution(
                context_packet=self.packet,
                contribution_type="risk",
                content="Unknown evidence should not pass.",
                evidence_refs=["nonexistent-source"],
            )

    def test_speculative_decision_candidate_cannot_be_persisted(self):
        item = contribution_module.build_contribution(
            context_packet=self.packet,
            contribution_type="decision_candidate",
            content="A speculative change proposal.",
            evidence_refs=[self.runtime_ref],
            uncertainty="speculative",
            persistence_requested=True,
        )
        self.assertFalse(item["persistence"]["eligible"])
        self.assertFalse(item["persistence"]["allowed"])

    def test_grounded_evidence_can_be_marked_persistence_eligible(self):
        item = contribution_module.build_contribution(
            context_packet=self.packet,
            contribution_type="evidence",
            content="Persistent runtime states the project is RUNNABLE.",
            evidence_refs=[self.runtime_ref],
            uncertainty="none",
            persistence_requested=True,
        )
        self.assertTrue(item["persistence"]["eligible"])
        self.assertTrue(item["persistence"]["allowed"])


if __name__ == "__main__":
    unittest.main()
