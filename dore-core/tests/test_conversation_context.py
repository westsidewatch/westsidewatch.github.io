import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "runtime" / "build_conversation_context.py"
spec = importlib.util.spec_from_file_location("build_conversation_context", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class ConversationContextPacketTests(unittest.TestCase):
    def test_active_p01_packet_is_bounded_private_and_replays_prior_meeting(self):
        packet = module.build_packet()
        self.assertEqual(packet["schema_version"], 2)
        self.assertEqual(packet["mode"], "INTERNAL_ALPHA_NOT_PUBLIC")
        self.assertFalse(packet["authority"]["public_conversation_authorized"])
        self.assertTrue(packet["authority"]["human_church_authority_final"])
        self.assertEqual(packet["project"]["id"], "P01-PREFLIGHT-SUBTITLE")
        roles = {source["role"] for source in packet["sources"]}
        self.assertTrue({
            "canonical_work_map",
            "persistent_runtime_state",
            "authority_and_identity",
            "conversation_alpha_contract",
            "active_project_brief",
            "prior_meeting_record",
        }.issubset(roles))
        self.assertEqual(packet["missing_evidence"], [])
        self.assertTrue(packet["ready_for_internal_meeting"])

        memory = packet["meeting_memory"]
        self.assertIsNotNone(memory)
        self.assertEqual(memory["project_id"], "P01-PREFLIGHT-SUBTITLE")
        self.assertFalse(memory["authority"]["public_conversation_authorized"])
        self.assertFalse(memory["authority"]["consequential_action_authorized_by_record"])
        self.assertTrue(memory["durable_contributions"])
        self.assertIn("production-verified", memory["durable_contributions"][0]["content"])
        self.assertTrue(memory["verified_learning"])
        self.assertTrue(memory["next_actions"])

    def test_unknown_project_cannot_silently_replace_persisted_runtime_context(self):
        with self.assertRaises(SystemExit):
            module.build_packet("NOT-THE-ACTIVE-PROJECT")


if __name__ == "__main__":
    unittest.main()
