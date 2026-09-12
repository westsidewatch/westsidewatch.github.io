import json
import unittest
from pathlib import Path

from dore_core.capabilities.surface_mounts import SurfaceMountRegistry
from dore_core.capabilities.url_surface import UrlSurfaceResolver

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / 'static/dawn-library/biblical-world/discovery-candidates.json'
ACCEPTANCE = ROOT / 'data/dawn-capability-acceptance-corpus.json'


class DawnUrlSurfaceTests(unittest.TestCase):
    def test_known_routes(self):
        resolver = UrlSurfaceResolver()
        cases = {
            'https://example.org/iiif/manifest.json': 'iiif-visual-surface',
            'https://example.org/book.pdf': 'pdfjs',
            'https://archive.org/details/completeworksofj19002jose': 'book-reader',
            'https://www.gutenberg.org/ebooks/20': 'bibliographic-page',
            'https://openlibrary.org/works/OL1W': 'zotero-translate',
        }
        for url, adapter in cases.items():
            self.assertEqual(resolver.resolve(url).adapter, adapter)
        self.assertEqual(resolver.resolve('https://example.org/article').fallback, 'readability')
        self.assertIsNone(resolver.resolve('not-a-url').adapter)

    def test_mount_registry_truth(self):
        registry = SurfaceMountRegistry()
        mounted = ('bibliographic-page', 'iiif-visual-surface', 'pdfjs', 'book-reader', 'video-surface')
        for adapter in mounted:
            self.assertEqual(registry.state(adapter), 'mounted')
            self.assertTrue(registry.executable(adapter))
            self.assertIsNotNone(registry.get(adapter).implementation)
            self.assertIsNotNone(registry.get(adapter).evidence)

        proven = ('cover-resolve', 'zotero-translate', 'readability')
        for adapter in proven:
            self.assertEqual(registry.state(adapter), 'integration-proven')
            self.assertFalse(registry.executable(adapter))
            self.assertIsNotNone(registry.get(adapter).implementation)
            self.assertIsNotNone(registry.get(adapter).evidence)

        self.assertEqual(registry.state('oembed-opengraph'), 'reserved')
        self.assertEqual(registry.state('unknown-adapter'), 'unavailable')

    def test_acceptance_corpus_policy(self):
        data = json.loads(ACCEPTANCE.read_text())
        fixtures = data['fixtures']
        self.assertEqual(data['schema'], 'dawn.capability.acceptance.corpus.v1')
        self.assertTrue(any(item['language'].startswith('zh') for item in fixtures))
        self.assertEqual(len(fixtures), len({item['id'] for item in fixtures}))
        required = {'bibliographic-page','iiif-visual-surface','pdfjs','book-reader','zotero-translate','readability','video-surface','cover-resolve'}
        self.assertTrue(required.issubset({item['capability'] for item in fixtures}))
        for item in fixtures:
            self.assertTrue(item['url'].startswith('https://'))
            self.assertNotIn('wikisource', item['url'].lower())
            self.assertIn(item['stage'], {'reserved','fixture-found','integration-proven','mounted'})

    def test_real_discovery_corpus_routes_without_mutation(self):
        before = CANDIDATES.read_bytes()
        items = json.loads(before).get('items', [])
        self.assertGreaterEqual(len(items), 900)
        resolver = UrlSurfaceResolver()
        resolved = executable = 0
        for item in items:
            source = item.get('sourceUrl', '').strip()
            payload = resolver.payload(source)
            plan = resolver.plan(source)
            self.assertTrue(payload.external)
            self.assertEqual(payload.ownership, 'external')
            self.assertEqual(payload.source_url, source)
            resolved += payload.adapter is not None
            executable += plan.executable
        self.assertGreaterEqual(resolved / len(items), 0.95)
        self.assertEqual(executable, len(items))
        self.assertEqual(before, CANDIDATES.read_bytes())


if __name__ == '__main__':
    unittest.main()
