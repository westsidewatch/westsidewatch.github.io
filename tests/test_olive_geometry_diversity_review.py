"""Review-page integration contracts."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import render_olive_geometry_diversity as renderer

class GeometryReviewTest(unittest.TestCase):
    def test_review_is_not_published_cover(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / "geometry.html"
            with patch.object(renderer, "OUTPUT", out):
                renderer.build()
            page = out.read_text(encoding="utf-8")
            self.assertEqual(page.count("<figure>"), 12)
            self.assertEqual(page.count('class="placeholder"'), 12)
            self.assertIn("No speaker likeness", page)
            self.assertIn("#CEBD74", page)
            self.assertIn("#738A5A", page)
            self.assertIn("#FAF9F5", page)
            self.assertIn("kou-shao-en", page)
            self.assertIn("rick-warren", page)

if __name__ == "__main__":
    unittest.main()
