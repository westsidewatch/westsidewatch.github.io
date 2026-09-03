import tempfile
import unittest
from pathlib import Path

from multi_loop_control_plane import register, route, wake
from newsroom_control_plane import editorial_gravity, run_episode, validate_signal


def signal():
    return {"signal_id": "world-001", "title": "Toronto community emergency", "summary": "A verified local emergency affects neighbours and churches in Toronto", "occurred_at": "2026-09-03T12:00:00Z", "provenance": [{"publisher": "City of Toronto", "url": "https://www.toronto.ca/example"}], "topics": ["toronto", "emergency", "churches"], "urgency": 5, "local_relevance": 5, "mission_relevance": 4, "verification_confidence": 5, "human_impact": 5, "unknowns": ["full scope"]}


class NewsroomControlPlaneTest(unittest.TestCase):
    def test_signal_requires_provenance(self):
        bad = signal(); bad["provenance"] = []
        self.assertFalse(validate_signal(bad)["ok"])

    def test_popularity_cannot_preempt(self):
        weak = signal(); weak.update(urgency=1, local_relevance=0, mission_relevance=0, verification_confidence=1, human_impact=0, popularity=1000000)
        self.assertFalse(editorial_gravity(weak)["preempt"])

    def test_signal_yields_enriches_drafts_and_resumes(self):
        with tempfile.TemporaryDirectory() as d:
            state = Path(d) / "state.json"; assets = Path(d) / "assets.jsonl"
            register("storybook", "Continue design engineering", kind="storybook", priority=50, state_path=state)
            wake("storybook", "active-work", state_path=state); route(state_path=state)
            enrichment = {"knowledge_id": "dawn-local-response-1", "provenance_preserved": True, "sources": [{"id": "toronto", "url": "https://www.toronto.ca/example", "publisher": "City of Toronto", "title": "Toronto emergency churches"}], "source_count": 1}
            result = run_episode(signal(), state_path=state, asset_path=assets, enrichment_asset=enrichment)
            self.assertTrue(result["ok"])
            self.assertEqual(result["initial_route"], "newsroom-world-response")
            self.assertTrue(result["enriched"])
            self.assertEqual(result["knowledge_gaps"], [])
            self.assertEqual(result["resumed_loop"], "storybook")
            self.assertFalse(result["published"])
            self.assertEqual(result["draft"]["status"], "EDITORIAL_REVIEW")
            self.assertIn("YIELD", result["events"])


if __name__ == "__main__":
    unittest.main()
