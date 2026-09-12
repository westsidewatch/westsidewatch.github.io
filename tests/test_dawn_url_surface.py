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
        self.assertEqual(resolver.resolve('https://example.org/iiif/manifest.json').adapter, 'iiif-visual-surface')
        self.assertEqual(resolver.resolve('https://example.org/book.pdf').adapter, 'pdfjs')
        self.assertEqual(resolver.resolve('https://archive.org/details/completeworksofj19002jose').adapter, 'book-reader')
        self.assertEqual(resolver.resolve('https://archive.org/embed/completeworksofj19002jose').adapter, 'book-reader')
        self.assertEqual(resolver.resolve('https://www.gutenberg.org/ebooks/20').adapter, 'bibliographic-page')
        self.assertEqual(resolver.resolve('https://openlibrary.org/works/OL1W').adapter, 'zotero-translate')
        self.assertEqual(resolver.resolve('https://example.org/article').fallback, 'readability')
        self.assertIsNone(resolver.resolve('not-a-url').adapter)

    def test_payload_never_claims_external_content_ownership(self):
        payload = UrlSurfaceResolver().payload('https://www.gutenberg.org/ebooks/20')
        self.assertTrue(payload.external)
        self.assertEqual(payload.ownership, 'external')
        self.assertEqual(payload.source_url, 'https://www.gutenberg.org/ebooks/20')

    def test_mount_registry_does_not_confuse_evidence_with_execution(self):
        registry = SurfaceMountRegistry()
        self.assertTrue(registry.executable('bibliographic-page'))
        self.assertEqual(registry.state('bibliographic-page'), 'mounted')

        for adapter in ('iiif-visual-surface', 'pdfjs', 'cover-resolve'):
            self.assertFalse(registry.executable(adapter))
            self.assertEqual(registry.state(adapter), 'integration-proven')
            self.assertIsNotNone(registry.get(adapter).implementation)
            self.assertIsNotNone(registry.get(adapter).evidence)

        for adapter in ('book-reader', 'zotero-translate', 'readability', 'video-surface'):
            self.assertFalse(registry.executable(adapter))
            self.assertEqual(registry.state(adapter), 'fixture-found')
            self.assertIsNotNone(registry.get(adapter).evidence)

        self.assertFalse(registry.executable('oembed-opengraph'))
        self.assertEqual(registry.state('oembed-opengraph'), 'reserved')
        self.assertEqual(registry.state('unknown-adapter'), 'unavailable')

    def test_real_acceptance_corpus_has_required_domains_and_no_wikisource(self):
        data = json.loads(ACCEPTANCE.read_text())
        self.assertEqual(data['schema'], 'dawn.capability.acceptance.corpus.v1')
        fixtures = data['fixtures']
        ids = [item['id'] for item in fixtures]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(any(item['language'].startswith('zh') for item in fixtures))
        required = {'bibliographic-page','iiif-visual-surface','pdfjs','book-reader','zotero-translate','readability','video-surface','cover-resolve'}
        self.assertTrue(required.issubset({item['capability'] for item in fixtures}))
        for item in fixtures:
            url = item['url'].lower()
            self.assertTrue(url.startswith('https://'))
            self.assertNotIn('wikisource', url)
            self.assertIn(item['stage'], {'reserved', 'fixture-found', 'integration-proven', 'mounted'})

    def test_surface_plan_exposes_execution_truth(self):
        resolver = UrlSurfaceResolver()
        gutenberg = resolver.plan('https://www.gutenberg.org/ebooks/20')
        self.assertTrue(gutenberg.executable)
        self.assertEqual(gutenberg.mount_state, 'mounted')
        self.assertEqual(gutenberg.ownership, 'external')

        iiif = resolver.plan('https://example.org/iiif/manifest.json')
        self.assertFalse(iiif.executable)
        self.assertEqual(iiif.mount_state, 'integration-proven')
        self.assertEqual(iiif.adapter, 'iiif-visual-surface')

        pdf = resolver.plan('https://example.org/book.pdf')
        self.assertFalse(pdf.executable)
        self.assertEqual(pdf.mount_state, 'integration-proven')
        self.assertEqual(pdf.adapter, 'pdfjs')

        scan = resolver.plan('https://archive.org/details/completeworksofj19002jose')
        self.assertFalse(scan.executable)
        self.assertEqual(scan.mount_state, 'fixture-found')
        self.assertEqual(scan.adapter, 'book-reader')

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
