"""Contract tests for Olive Mountain series geometry."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from olive_gold_geometry import assign, enrich, GOLD, OLIVE, PAPER

class OliveGeometryTest(unittest.TestCase):
    def test_twelve_unique_shapes(self):
        rows = assign([f"speaker-{n}" for n in range(12)])
        self.assertEqual(len(rows), 12)
        self.assertEqual(len({r["goldPath"] for r in rows}), 12)
        self.assertEqual(len({r["identity"] for r in rows}), 12)

    def test_palette_and_secondary_accent(self):
        for row in assign(["kou-shao-en", "rick-warren"]):
            self.assertEqual(row["palette"], {"paper": PAPER, "portrait": OLIVE, "geometry": GOLD})
            self.assertIn("olive", row["oliveAccent"])

    def test_enrichment_preserves_candidate(self):
        doc = {"records": [{"speaker": "kou-shao-en", "candidateId": "test"}]}
        result = enrich(doc)
        self.assertEqual(result["records"][0]["candidateId"], "test")
        self.assertIn("goldGeometry", result["records"][0])

    def test_duplicates_rejected(self):
        with self.assertRaises(ValueError):
            assign(["same", "same"])

if __name__ == "__main__":
    unittest.main()
