#!/usr/bin/env python3

import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("plan_anchors", HERE / "plan_anchors.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class AnchorPlannerTests(unittest.TestCase):
    def test_prefers_true_marginal_coverage_and_stops_without_redundant_anchor(self):
        fixture = Path(__file__).resolve().parents[2] / "experiments" / "aw-011" / "evidence.fixture.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        poses, candidates, threshold = MODULE.parse_problem(data)
        report = MODULE.plan(poses, candidates, threshold)

        self.assertTrue(report["corridor_passes"])
        self.assertEqual(report["selected_anchor_ids"], ["A-wide", "A-finish"])
        self.assertNotIn("A-redundant", report["selected_anchor_ids"])
        self.assertEqual(report["unresolved_pose_ids"], [])

    def test_zero_or_negative_gain_anchor_is_never_purchased(self):
        data = {
            "max_residual_unseen_fraction": 0.0,
            "poses": [{"id": "P001", "unseen": ["x"]}],
            "candidates": [
                {
                    "id": "A-useless",
                    "covers": {"P001": []},
                    "redundancy_penalty": 1.0,
                }
            ],
        }
        poses, candidates, threshold = MODULE.parse_problem(data)
        report = MODULE.plan(poses, candidates, threshold)

        self.assertFalse(report["corridor_passes"])
        self.assertEqual(report["selected_anchor_ids"], [])
        self.assertEqual(report["unresolved_pose_ids"], ["P001"])

    def test_overlap_is_charged_only_once(self):
        data = {
            "max_residual_unseen_fraction": 0.0,
            "poses": [{"id": "P001", "unseen": ["x", "y"]}],
            "candidates": [
                {"id": "A1", "covers": {"P001": ["x"]}},
                {"id": "A2", "covers": {"P001": ["x", "y"]}},
            ],
        }
        poses, candidates, threshold = MODULE.parse_problem(data)
        report = MODULE.plan(poses, candidates, threshold)

        self.assertEqual(report["selected_anchor_ids"], ["A2"])
        self.assertTrue(report["corridor_passes"])


if __name__ == "__main__":
    unittest.main()
