#!/usr/bin/env python3

import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from run_aw011 import InputError, build, validate_camera_spine


def write_gray_png(path: Path, rows: list[list[int]]) -> None:
    height = len(rows)
    width = len(rows[0])
    raw = b"".join(b"\x00" + bytes(row) for row in rows)

    def chunk(kind: bytes, payload: bytes) -> bytes:
        crc = zlib.crc32(kind + payload) & 0xFFFFFFFF
        return (
            struct.pack(">I", len(payload))
            + kind
            + payload
            + struct.pack(">I", crc)
        )

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


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
                        "source": {
                            "asset": "dore-011.bin",
                            "canonical_pose_id": "P000",
                        },
                        "camera": {"spine_file": "camera.json"},
                        "scaffold": {"provider": "fixture-provider"},
                        "anchors": {"candidate_coverage_file": "evidence.json"},
                    }
                ),
                encoding="utf-8",
            )

            report = build(manifest, root / "out")

            self.assertEqual(report["status"], "READY_FOR_SCAFFOLD")
            self.assertEqual(
                report["camera"]["ordered_pose_ids"],
                ["P000", "P001", "P002", "P000"],
            )
            self.assertEqual(report["evidence"]["source"], "planner_json")
            self.assertEqual(report["evidence"]["selected_anchor_ids"], ["A001"])
            self.assertTrue((root / "out" / "anchor-plan.json").is_file())
            self.assertTrue((root / "out" / "build-manifest.json").is_file())

    def test_preflight_builds_evidence_directly_from_warp_masks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dore-011.bin").write_bytes(b"canonical-dore-011")
            (root / "camera.json").write_text(
                json.dumps(
                    {
                        "poses": [
                            {"id": "P000"},
                            {"id": "P001"},
                            {"id": "P000"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            write_gray_png(root / "p001-unseen.png", [[255, 0]])
            write_gray_png(root / "a001-p001.png", [[255, 255]])
            (root / "masks.json").write_text(
                json.dumps(
                    {
                        "max_residual_unseen_fraction": 0.0,
                        "poses": [
                            {
                                "id": "P001",
                                "unseen_mask": "p001-unseen.png",
                            }
                        ],
                        "candidates": [
                            {
                                "id": "A001",
                                "coverage_masks": {
                                    "P001": "a001-p001.png"
                                },
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
                        "source": {
                            "asset": "dore-011.bin",
                            "canonical_pose_id": "P000",
                        },
                        "camera": {"spine_file": "camera.json"},
                        "scaffold": {"provider": "fixture-provider"},
                        "anchors": {"mask_manifest_file": "masks.json"},
                    }
                ),
                encoding="utf-8",
            )

            report = build(manifest, root / "out")

            self.assertEqual(report["status"], "READY_FOR_SCAFFOLD")
            self.assertEqual(report["evidence"]["source"], "warp_masks")
            self.assertEqual(report["evidence"]["selected_anchor_ids"], ["A001"])
            self.assertTrue((root / "out" / "evidence.from-masks.json").is_file())

    def test_evidence_outside_camera_spine_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dore-011.bin").write_bytes(b"canonical-dore-011")
            (root / "camera.json").write_text(
                json.dumps(
                    {"poses": [{"id": "P000"}, {"id": "P001"}, {"id": "P000"}]}
                ),
                encoding="utf-8",
            )
            (root / "evidence.json").write_text(
                json.dumps(
                    {
                        "poses": [
                            {"id": "P001", "unseen": []},
                            {"id": "P999", "unseen": []},
                        ],
                        "candidates": [],
                    }
                ),
                encoding="utf-8",
            )
            manifest = root / "production.json"
            manifest.write_text(
                json.dumps(
                    {
                        "aw_id": "AW-011",
                        "source": {"asset": "dore-011.bin"},
                        "camera": {"spine_file": "camera.json"},
                        "anchors": {"candidate_coverage_file": "evidence.json"},
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(InputError):
                build(manifest, root / "out")


if __name__ == "__main__":
    unittest.main()
