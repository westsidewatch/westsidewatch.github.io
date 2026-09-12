import unittest

from camera_world_score import rank_candidates, score_candidate


class CameraWorldScoreTests(unittest.TestCase):
    def test_required_wide_is_not_punished_for_being_wide(self):
        wide = score_candidate({
            "id": "earned-wide",
            "narrative_value": 0.98,
            "reveal_value": 0.95,
            "rhythm_value": 0.85,
            "world_demand_fraction": 0.30,
            "avoidable_fraction": 0.15,
            "wide_scene_required": True,
        })
        cheap = score_candidate({
            "id": "cheap-but-weak",
            "narrative_value": 0.55,
            "reveal_value": 0.50,
            "rhythm_value": 0.65,
            "world_demand_fraction": 0.03,
            "avoidable_fraction": 0.80,
            "wide_scene_required": False,
        })
        self.assertGreater(wide["camera_world_score"], cheap["camera_world_score"])

    def test_cost_breaks_tie_between_equally_good_shots(self):
        payload = {
            "candidates": [
                {
                    "id": "expensive",
                    "narrative_value": 0.8,
                    "reveal_value": 0.8,
                    "rhythm_value": 0.8,
                    "world_demand_fraction": 0.18,
                    "avoidable_fraction": 1.0,
                },
                {
                    "id": "efficient",
                    "narrative_value": 0.8,
                    "reveal_value": 0.8,
                    "rhythm_value": 0.8,
                    "world_demand_fraction": 0.03,
                    "avoidable_fraction": 1.0,
                },
            ]
        }
        ranked = rank_candidates(payload)
        self.assertEqual(ranked[0]["id"], "efficient")

    def test_only_avoidable_demand_is_penalized(self):
        a = score_candidate({
            "world_demand_fraction": 0.4,
            "avoidable_fraction": 0.1,
        })
        b = score_candidate({
            "world_demand_fraction": 0.2,
            "avoidable_fraction": 0.9,
        })
        self.assertLess(a["avoidable_world_cost"], b["avoidable_world_cost"])


if __name__ == "__main__":
    unittest.main()
