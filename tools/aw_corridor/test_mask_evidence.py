#!/usr/bin/env python3

import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from mask_evidence import MaskError, build_problem


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

    data = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(data)


class MaskEvidenceTests(unittest.TestCase):
    def test_candidate_coverage_is_clipped_to_baseline_unseen(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_gray_png(root / "unseen.png", [[0, 255], [255, 0]])
            write_gray_png(root / "anchor.png", [[255, 255], [0, 0]])
            manifest = root / "mask-manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "max_residual_unseen_fraction": 0.0,
                        "poses": [
                            {"id": "P001", "unseen_mask": "unseen.png"}
                        ],
                        "candidates": [
                            {
                                "id": "A001",
                                "coverage_masks": {"P001": "anchor.png"},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            problem = build_problem(manifest)

            self.assertEqual(
                problem["poses"][0]["unseen"],
                ["P001:0:1", "P001:1:0"],
            )
            self.assertEqual(
                problem["candidates"][0]["covers"]["P001"],
                ["P001:0:1"],
            )

    def test_dimension_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_gray_png(root / "unseen.png", [[255, 0]])
            write_gray_png(root / "anchor.png", [[255], [0]])
            manifest = root / "mask-manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "poses": [
                            {"id": "P001", "unseen_mask": "unseen.png"}
                        ],
                        "candidates": [
                            {
                                "id": "A001",
                                "coverage_masks": {"P001": "anchor.png"},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(MaskError):
                build_problem(manifest)

    def test_soft_mask_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_gray_png(root / "unseen.png", [[128]])
            manifest = root / "mask-manifest.json"
            manifest.write_text(
                json.dumps(
                    {"poses": [{"id": "P001", "unseen_mask": "unseen.png"}]}
                ),
                encoding="utf-8",
            )

            with self.assertRaises(MaskError):
                build_problem(manifest)


if __name__ == "__main__":
    unittest.main()
