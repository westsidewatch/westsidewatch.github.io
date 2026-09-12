import json
import unittest
from pathlib import Path

from dore_core.capabilities.surface_mounts import SurfaceMountRegistry
from dore_core.capabilities.url_surface import UrlSurfaceResolver


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / 'static/dawn-library/biblical-world/discovery-candidates.json'


class DawnUrlSurfaceTests(unittest.TestCase):
    def test_known_routes(self):
        resolver = UrlSurfaceResolver()
        self.assertEqual(resolver.resolve('https://example.org/iiif/manifest.json').adapter, 'iiif-visual-surface')
        self.assertEqual(resolver.resolve('https://example.org/book.pdf').adapter, 'pdfjs')
        self.assertEqual(resolver.resolve('https://www.gutenberg.org/ebooks/20').adapter, 'bibliographic-page')
        self.assertEqual(resolver.resolve('https://openlibrary.org/works/OL1W').adapter, 'zotero-translate')
        self.assertEqual(resolver.resolve('https://example.org/article').fallback, 'readability')
        self.assertIsNone(resolver.resolve('not-a-url').adapter)

    def test_payload_never_claims_external_content_ownership(self):
        payload = UrlSurfaceResolver().payload('https://www.gutenberg.org/ebooks/20')
        self.assertTrue(payload.external)
        self.assertEqual(payload.ownership, 'external')
        self.assertEqual(payload.source_url, 'https://www.gutenberg.org/ebooks/20')

    def test_mount_registry_does_not_confuse_routes_with_installed_equipment(self):
        registry = SurfaceMountRegistry()
        self.assertTrue(registry.executable('bibliographic-page'))
        self.assertEqual(registry.state('bibliographic-page'), 'mounted')
        for adapter in ('iiif-visual-surface', 'pdfjs', 'book-reader', 'zotero-translate', 'oembed-opengraph', 'readability'):
            self.assertFalse(registry.executable(adapter))
            self.assertEqual(registry.state(adapter), 'dormant')
        self.assertEqual(registry.state('unknown-adapter'), 'unavailable')

    def test_surface_plan_exposes_execution_truth(self):
        resolver = UrlSurfaceResolver()
        gutenberg = resolver.plan('https://www.gutenberg.org/ebooks/20')
        self.assertTrue(gutenberg.executable)
        self.assertEqual(gutenberg.mount_state, 'mounted')
        self.assertEqual(gutenberg.ownership, 'external')

        pdf = resolver.plan('https://example.org/book.pdf')
        self.assertFalse(pdf.executable)
        self.assertEqual(pdf.mount_state, 'dormant')
        self.assertEqual(pdf.adapter, 'pdfjs')

    def test_real_discovery_corpus_routes_without_mutation(self):
        before = CANDIDATES.read_bytes()
        data = json.loads(before)
        items = data.get('items', [])
        self.assertGreaterEqual(len(items), 900)

        resolver = UrlSurfaceResolver()
        resolved = 0
        executable = 0
        for item in items:
            payload = resolver.payload(item.get('sourceUrl', ''))
            plan = resolver.plan(item.get('sourceUrl', ''))
            self.assertTrue(payload.external)
            self.assertEqual(payload.ownership, 'external')
            self.assertEqual(payload.source_url, item.get('sourceUrl', '').strip())
            if payload.adapter is not None:
                resolved += 1
            if plan.executable:
                executable += 1

        coverage = resolved / len(items)
        self.assertGreaterEqual(coverage, 0.95)
        self.assertEqual(executable, len(items), 'current 939-candidate corpus is entirely covered by the mounted Gutenberg surface')
        self.assertEqual(before, CANDIDATES.read_bytes(), 'surface routing must never mutate discovery candidates')


if __name__ == '__main__':
    unittest.main()
