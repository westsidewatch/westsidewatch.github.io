#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("evidence_gate", HERE / "evidence_gate.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class EvidenceGateTests(unittest.TestCase):
    def test_generated_pixels_can_enter_only_unseen_positions(self):
        # Four RGB pixels. Pixels 1 and 3 are unseen.
        known = bytes([
            10, 11, 12,
            20, 21, 22,
            30, 31, 32,
            40, 41, 42,
        ])
        generated = bytes([
            110, 111, 112,
            120, 121, 122,
            130, 131, 132,
            140, 141, 142,
        ])
        mask = bytes([0, 1, 0, 1])

        output, report = MODULE.compose_unseen_only(
            known, generated, mask, channels=3
        )

        self.assertEqual(
            output,
            bytes([
                10, 11, 12,
                120, 121, 122,
                30, 31, 32,
                140, 141, 142,
            ]),
        )
        self.assertTrue(report.known_pixels_preserved)
        self.assertEqual(report.known_byte_delta_count, 0)
        self.assertEqual(report.known_pixel_count, 2)
        self.assertEqual(report.unseen_pixel_count, 2)

    def test_return_pose_is_exact_source_bytes(self):
        source = bytes([1, 2, 3, 4, 5, 6])
        generated_return = bytes([9, 9, 9, 9, 9, 9])

        frame = MODULE.hard_source_relock(
            generated_return,
            source,
            pose_id="P000",
            canonical_pose_id="P000",
        )

        self.assertIs(frame, source)
        self.assertTrue(MODULE.exact_relock_passes(frame, source))

    def test_noncanonical_pose_is_not_replaced(self):
        source = bytes([1, 2, 3])
        rendered = bytes([7, 8, 9])

        frame = MODULE.hard_source_relock(
            rendered,
            source,
            pose_id="P005",
            canonical_pose_id="P000",
        )

        self.assertEqual(frame, rendered)


if __name__ == "__main__":
    unittest.main()
