import json
import unittest
from pathlib import Path

from dore_core.capabilities.surface_mounts import SurfaceMountRegistry
from dore_core.capabilities.video_surface import VideoSurfaceAdapter

ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE = ROOT / 'data/dawn-capability-acceptance-corpus.json'
SURFACE = ROOT / 'static/dawn-library/surfaces/video.html'
VIEWER = ROOT / 'static/js/dawn-video-surface.js'


class DawnVideoSurfaceTests(unittest.TestCase):
    def test_real_official_jesus_film_resolves_to_privacy_enhanced_embed(self):
        data = json.loads(ACCEPTANCE.read_text())
        fixture = next(item for item in data['fixtures'] if item['id'] == 'jesus-film-official-youtube')
        target = VideoSurfaceAdapter().resolve(fixture['url'])
        self.assertIsNotNone(target)
        self.assertEqual(target.provider, 'youtube')
        self.assertEqual(target.video_id, 'or22I3KOerA')
        self.assertEqual(target.embed_url, 'https://www.youtube-nocookie.com/embed/or22I3KOerA')
        self.assertEqual(target.source_url, fixture['url'])

    def test_adapter_rejects_unapproved_hosts_and_invalid_ids(self):
        adapter = VideoSurfaceAdapter()
        self.assertIsNone(adapter.resolve('https://example.org/watch?v=or22I3KOerA'))
        self.assertIsNone(adapter.resolve('https://www.youtube.com/watch?v=<script>'))
        self.assertIsNone(adapter.resolve(''))

    def test_surface_contract_keeps_external_ownership_and_escape_hatch(self):
        html = SURFACE.read_text()
        js = VIEWER.read_text()
        self.assertIn('data-dawn-video-surface', html)
        self.assertIn('data-external-source="true"', html)
        self.assertIn('data-video-frame', html)
        self.assertIn('/js/dawn-video-surface.js', html)
        self.assertIn('https://www.youtube-nocookie.com/embed/${id}', js)
        self.assertIn("root.dataset.viewerState = 'ready'", js)

    def test_registry_records_video_surface_as_mounted(self):
        registry = SurfaceMountRegistry()
        mount = registry.get('video-surface')
        self.assertEqual(mount.state, 'mounted')
        self.assertEqual(mount.implementation, 'static/js/dawn-video-surface.js')
        self.assertIn('jesus-film-official-youtube', mount.evidence)
        self.assertTrue(registry.executable('video-surface'))


if __name__ == '__main__':
    unittest.main()
