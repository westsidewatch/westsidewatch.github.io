import json
import unittest
from pathlib import Path

from dore_core.capabilities.cover_resolver import CoverResolver
from dore_core.capabilities.surface_mounts import SurfaceMountRegistry


ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE = ROOT / 'data/dawn-capability-acceptance-corpus.json'
SURFACE = ROOT / 'static/dawn-library/surfaces/cover.html'
VIEWER = ROOT / 'static/js/dawn-cover-surface.js'


class DawnCoverResolverTests(unittest.TestCase):
    def test_edition_olid_resolves_exact_real_fixture_url(self):
        data = json.loads(ACCEPTANCE.read_text())
        fixture = next(item for item in data['fixtures'] if item['id'] == 'openlibrary-josephus-1900-cover')
        candidate = CoverResolver().resolve({'olid': fixture['edition']['openLibraryEditionId']})
        self.assertIsNotNone(candidate)
        self.assertEqual(fixture['stage'], 'integration-proven')
        self.assertEqual(candidate.identifier_type, 'olid')
        self.assertEqual(candidate.identifier, 'OL24645724M')
        self.assertEqual(candidate.url, fixture['url'])
        self.assertEqual(fixture['edition']['publishDate'], '1900')
        self.assertEqual(fixture['edition']['internetArchiveId'], 'completeworksofj19002jose')

    def test_resolver_never_uses_title_search_and_prefers_stable_edition_ids(self):
        resolver = CoverResolver()
        self.assertIsNone(resolver.resolve({'title': 'Complete works of Josephus'}))
        candidate = resolver.resolve({'isbn': '123', 'olid': 'OL24645724M', 'cover_id': '456'})
        self.assertEqual(candidate.identifier_type, 'cover_id')
        self.assertIn('/id/456-M.jpg?default=false', candidate.url)

    def test_cover_surface_is_external_pointer_not_local_copy(self):
        html = SURFACE.read_text()
        js = VIEWER.read_text()
        self.assertIn('data-dawn-cover-surface', html)
        self.assertIn('data-cover-image', html)
        self.assertNotIn('data:image/', html)
        self.assertIn("sourceUrl.protocol !== 'https:'", js)
        self.assertIn("root.dataset.externalSource = 'true'", js)
        self.assertIn('image.src = sourceUrl.href', js)
        self.assertIn("root.dataset.viewerState = 'ready'", js)

    def test_registry_records_integration_without_claiming_mount(self):
        mount = SurfaceMountRegistry().get('cover-resolve')
        self.assertEqual(mount.state, 'integration-proven')
        self.assertEqual(mount.implementation, 'dore_core/capabilities/cover_resolver.py')
        self.assertIn('openlibrary-josephus-1900-cover', mount.evidence)
        self.assertFalse(SurfaceMountRegistry().executable('cover-resolve'))


if __name__ == '__main__':
    unittest.main()
