import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE = ROOT / 'data/dawn-capability-acceptance-corpus.json'
SURFACE = ROOT / 'static/dawn-library/surfaces/pdf.html'
VIEWER = ROOT / 'static/js/dawn-pdf-surface.js'


class DawnPdfSurfaceTests(unittest.TestCase):
    def test_real_ccel_pdf_fixture_is_bound_to_pdfjs_surface(self):
        data = json.loads(ACCEPTANCE.read_text())
        fixture = next(item for item in data['fixtures'] if item['id'] == 'ccel-augustine-confessions-pdf')
        self.assertEqual(fixture['capability'], 'pdfjs')
        self.assertEqual(fixture['kind'], 'book-pdf')
        self.assertEqual(fixture['expectContentType'], 'application/pdf')
        self.assertTrue(fixture['url'].startswith('https://www.ccel.org/'))

    def test_surface_uses_real_pdfjs_not_browser_native_pdf_embed(self):
        html = SURFACE.read_text()
        js = VIEWER.read_text()
        self.assertIn('data-dawn-pdf-surface', html)
        self.assertIn('/js/dawn-pdf-surface.js', html)
        self.assertNotIn('<embed', html.lower())
        self.assertNotIn('<iframe', html.lower())
        self.assertIn('pdfjs-dist@', js)
        self.assertIn('pdf.min.mjs', js)
        self.assertIn('pdf.worker.min.mjs', js)
        self.assertIn('pdfjsLib.getDocument', js)
        self.assertIn('page.render', js)
        self.assertIn("sourceUrl.protocol !== 'https:'", js)
        self.assertIn("root.dataset.viewerState = 'ready'", js)

    def test_pdf_surface_keeps_external_ownership_and_escape_hatch(self):
        html = SURFACE.read_text()
        js = VIEWER.read_text()
        self.assertIn('data-pdf-source', html)
        self.assertIn("root.dataset.externalSource = 'true'", js)
        self.assertIn('sourceLink.href = sourceUrl.href', js)


if __name__ == '__main__':
    unittest.main()
