import json
import unittest
from pathlib import Path

from dore_core.capabilities.archive_bookreader import ArchiveBookReaderAdapter
from dore_core.capabilities.surface_mounts import SurfaceMountRegistry


ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE = ROOT / 'data/dawn-capability-acceptance-corpus.json'
SURFACE = ROOT / 'static/dawn-library/surfaces/bookreader.html'
VIEWER = ROOT / 'static/js/dawn-bookreader-surface.js'


class DawnBookReaderTests(unittest.TestCase):
    def test_real_josephus_scan_maps_to_official_archive_embed(self):
        data = json.loads(ACCEPTANCE.read_text())
        fixture = next(item for item in data['fixtures'] if item['id'] == 'internetarchive-josephus-1900-bookreader')
        item_id = fixture['edition']['internetArchiveId']
        target = ArchiveBookReaderAdapter().resolve(item_id)
        self.assertIsNotNone(target)
        self.assertEqual(target.item_id, 'completeworksofj19002jose')
        self.assertEqual(target.embed_url, fixture['url'])
        self.assertEqual(target.details_url, 'https://archive.org/details/completeworksofj19002jose')
        self.assertEqual(fixture['edition']['openLibraryEditionId'], 'OL24645724M')

    def test_adapter_rejects_arbitrary_urls_and_scriptable_ids(self):
        adapter = ArchiveBookReaderAdapter()
        self.assertIsNone(adapter.resolve('https://example.org/book'))
        self.assertIsNone(adapter.resolve('book?id=<script>'))
        self.assertIsNone(adapter.resolve(''))

    def test_surface_uses_official_archive_embed_and_keeps_escape_hatch(self):
        html = SURFACE.read_text()
        js = VIEWER.read_text()
        self.assertIn('data-dawn-bookreader-surface', html)
        self.assertIn('data-bookreader-frame', html)
        self.assertIn('/js/dawn-bookreader-surface.js', html)
        self.assertIn('https://archive.org/embed/${itemId}', js)
        self.assertIn('https://archive.org/details/${itemId}', js)
        self.assertIn("root.dataset.externalSource = 'true'", js)
        self.assertIn("root.dataset.viewerState = 'ready'", js)

    def test_registry_records_real_end_to_end_integration_without_claiming_mount(self):
        registry = SurfaceMountRegistry()
        mount = registry.get('book-reader')
        self.assertEqual(mount.state, 'integration-proven')
        self.assertEqual(mount.implementation, 'static/js/dawn-bookreader-surface.js')
        self.assertIn('internetarchive-josephus-1900-bookreader', mount.evidence)
        self.assertFalse(registry.executable('book-reader'))


if __name__ == '__main__':
    unittest.main()
