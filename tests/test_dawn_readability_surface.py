import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SURFACE = ROOT / 'static/dawn-library/surfaces/readability.html'
VIEWER = ROOT / 'static/js/dawn-readability-surface.js'
PROBE = ROOT / 'scripts/run_dawn_readability_probe.mjs'


class DawnReadabilitySurfaceTests(unittest.TestCase):
    def test_surface_contract_uses_local_payload_and_external_escape_hatch(self):
        html = SURFACE.read_text()
        js = VIEWER.read_text()
        self.assertIn('data-dawn-readability-surface', html)
        self.assertIn('data-external-source="true"', html)
        self.assertIn('/js/dawn-readability-surface.js', html)
        self.assertIn('/dawn-library/readability/', js)
        self.assertIn("payload.ownership !== 'external'", js)
        self.assertIn("root.dataset.viewerState = 'ready'", js)

    def test_probe_uses_mozilla_readability_and_real_bibleproject_source(self):
        script = PROBE.read_text()
        self.assertIn("from '@mozilla/readability'", script)
        self.assertIn('bibleproject.com/articles/', script)
        self.assertIn('dawn.readability.acceptance.v1', script)
        self.assertIn('ownership', script)
        self.assertIn('textLength', script)


if __name__ == '__main__':
    unittest.main()
