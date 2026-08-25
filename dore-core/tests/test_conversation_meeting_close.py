import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

RUNTIME_DIR = Path(__file__).resolve().parents[1] / "runtime"


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, RUNTIME_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


context_module = load_module("build_conversation_context_close", "build_conversation_context.py")
contribution_module = load_module("conversation_contribution_close", "conversation_contribution.py")
close_module = load_module("conversation_meeting_close", "conversation_meeting_close.py")


class ConversationMeetingCloseTests(unittest.TestCase):
    def setUp(self):
        self.packet = context_module.build_packet()
        self.grounded = contribution_module.build_contribution(
            context_packet=self.packet,
            contribution_type="evidence",
            content="P01 remains RUNNABLE in persistent runtime state.",
            evidence_refs=["persistent_runtime_state"],
            uncertainty="none",
            persistence_requested=True,
        )
        self.speculative = contribution_module.build_contribution(
            context_packet=self.packet,
            contribution_type="decision_candidate",
            content="Speculative proposal that should remain transient.",
            evidence_refs=["persistent_runtime_state"],
            uncertainty="speculative",
            persistence_requested=True,
        )

    def test_close_keeps_only_persistence_allowed_contributions(self):
        record = close_module.build_meeting_record(
            context_packet=self.packet,
            contributions=[self.grounded, self.speculative],
            next_actions=["Continue bounded Conversation Alpha implementation."],
        )
        self.assertEqual(len(record["durable_contributions"]), 1)
        self.assertEqual(record["durable_contributions"][0]["type"], "evidence")
        self.assertEqual(len(record["rejected_transient_or_unsafe"]), 1)
        self.assertFalse(record["authority"]["public_conversation_authorized"])
        self.assertFalse(record["authority"]["consequential_action_authorized_by_record"])

    def test_project_mismatch_is_rejected(self):
        altered = dict(self.grounded)
        altered["project_id"] = "OTHER-PROJECT"
        record = close_module.build_meeting_record(
            context_packet=self.packet,
            contributions=[altered],
        )
        self.assertEqual(record["durable_contributions"], [])
        self.assertEqual(record["rejected_transient_or_unsafe"][0]["reason"], "project_mismatch")

    def test_record_survives_round_trip_persistence(self):
        record = close_module.build_meeting_record(
            context_packet=self.packet,
            contributions=[self.grounded],
            verified_learning=["Grounded meeting-close records can be bounded and replayed."],
            unresolved_blockers=[],
        )
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "meeting.json"
            close_module.persist_meeting_record(record, path)
            restored = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(restored["project_id"], "P01-PREFLIGHT-SUBTITLE")
        self.assertEqual(len(restored["durable_contributions"]), 1)
        self.assertTrue(restored["authority"]["human_church_authority_final"])


if __name__ == "__main__":
    unittest.main()
