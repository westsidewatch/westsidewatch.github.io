"""SVG geometry similarity regression."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from check_olive_geometry_similarity import similarity, polygons, audit

class SimilarityTest(unittest.TestCase):
    def test_identical_shapes_are_rejected(self):
        p="M0 0 H40 V40 H0Z"
        self.assertEqual(similarity(p,p),1.0)
    def test_different_shapes(self):
        self.assertEqual(similarity("M0 0 H20 V20 H0Z","M80 80 H100 V100 H80Z"),0.0)
    def test_multisubpath(self):
        self.assertEqual(len(polygons("M0 0 H10 V10 H0Z M20 20 H30 V30 H20Z")),2)
    def test_unsupported_command_fails_closed(self):
        with self.assertRaises(ValueError):
            polygons("M0 0 C10 10 20 20 30 30Z")
    def test_series(self):
        self.assertEqual(len(audit()["pairs"]),66)

if __name__=="__main__":
    unittest.main()
