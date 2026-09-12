import json
import unittest
from pathlib import Path

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

    def test_real_discovery_corpus_routes_without_mutation(self):
        before = CANDIDATES.read_bytes()
        data = json.loads(before)
        items = data.get('items', [])
        self.assertGreaterEqual(len(items), 900)

        resolver = UrlSurfaceResolver()
        resolved = 0
        for item in items:
            route = resolver.resolve(item.get('sourceUrl', ''))
            if route.adapter is not None:
                resolved += 1

        coverage = resolved / len(items)
        self.assertGreaterEqual(coverage, 0.95)
        self.assertEqual(before, CANDIDATES.read_bytes(), 'surface routing must never mutate discovery candidates')


if __name__ == '__main__':
    unittest.main()
