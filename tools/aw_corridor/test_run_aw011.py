import json
import tempfile
import unittest
from pathlib import Path

from run_aw011 import InputError, build, validate_camera_spine


class RunAw011Tests(unittest.TestCase):
    def test_camera_spine_requires_exact_return(self):
        with self.assertRaises(InputError):
            validate_camera_spine(
                {"poses": [{"id": "P000"}, {"id": "P001"}, {"id": "P002"}]},
                "P000",
            )

    def test_preflight_binds_source_spine_and_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dore-011.bin").write_bytes(b"canonical-dore-011")
            (root / "camera.json").write_text(
                json.dumps(
                    {
                        "poses": [
                            {"id": "P000"},
                            {"id": "P001"},
                            {"id": "P002"},
                            {"id": "P000"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (root / "evidence.json").write_text(
                json.dumps(
                    {
                        "max_residual_unseen_fraction": 0.0,
                        "poses": [
                            {"id": "P001", "unseen": ["a"]},
                            {"id": "P002", "unseen": ["b"]},
                        ],
                        "candidates": [
                            {
                                "id": "A001",
                                "covers": {"P001": ["a"], "P002": ["b"]},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            manifest = root / "production.json"
            manifest.write_text(
                json.dumps(
                    {
                        "aw_id": "AW-011",
                        "source": {"asset": "dore-011.bin", "canonical_pose_id": "P000"},
                        "camera": {"spine_file": "camera.json"},
                        "scaffold": {"provider": "fixture-provider"},
                        "anchors": {"candidate_coverage_file": "evidence.json"},
                    }
                ),
                encoding="utf-8",
            )

            report = build(manifest, root / "out")

            self.assertEqual(report["status"], "READY_FOR_SCAFFOLD")
            self.assertEqual(report["camera"]["ordered_pose_ids"], ["P000", "P001", "P002", "P000"])
            self.assertEqual(report["evidence"]["selected_anchor_ids"], ["A001"])
            self.assertTrue((root / "out" / "anchor-plan.json").is_file())
            self.assertTrue((root / "out" / "build-manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
