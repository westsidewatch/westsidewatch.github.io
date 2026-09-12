import json
import unittest
from pathlib import Path

from dore_core.capabilities.surface_mounts import SurfaceMountRegistry


ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / 'data/visual_graph.json'
ACCEPTANCE = ROOT / 'data/dawn-capability-acceptance-corpus.json'
VIEWER = ROOT / 'static/js/dawn-visual-viewer.js'
LAYOUT = ROOT / 'layouts/visual/single.html'


class DawnIiifIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.graph = json.loads(GRAPH.read_text())
        self.acceptance = json.loads(ACCEPTANCE.read_text())

    def test_princeton_fixture_is_the_same_resource_consumed_by_visual_surface(self):
        fixture = next(item for item in self.acceptance['fixtures'] if item['id'] == 'princeton-storm-sea-galilee-iiif')
        visual = next(item for item in self.graph['visual_works'] if item['id'] == 'visual-princeton-galilee-storm-1591')
        representation = visual['representations'][0]
        delivery = representation['delivery']

        self.assertEqual(fixture['stage'], 'integration-proven')
        self.assertEqual(fixture['url'], delivery['iiif_manifest'])
        self.assertEqual(delivery['mode'], 'iiif-image')
        self.assertTrue(delivery['deep_zoom'])
        self.assertEqual(delivery['deep_zoom_engine'], 'OpenSeadragon')
        self.assertTrue(delivery['iiif_image_service'].startswith('https://media.artmuseum.princeton.edu/iiif/3/'))
        self.assertEqual(representation['provider'], 'Princeton University Art Museum')
        self.assertEqual(representation['rights']['policy'], 'public-domain')

    def test_real_iiif_delivery_is_wired_to_the_actual_viewer_contract(self):
        viewer = VIEWER.read_text()
        layout = LAYOUT.read_text()

        self.assertIn("root.dataset.iiifService", viewer)
        self.assertIn("+ '/info.json'", viewer)
        self.assertIn('window.OpenSeadragon', viewer)
        self.assertIn("root.dataset.viewerState = 'ready'", viewer)
        self.assertIn('data-iiif-service=', layout)
        self.assertIn('data-iiif-manifest=', layout)
        self.assertIn('openseadragon@6.1.0', layout)
        self.assertIn('/js/dawn-visual-viewer.js', layout)

    def test_registry_records_real_implementation_without_pretending_it_is_mounted(self):
        mount = SurfaceMountRegistry().get('iiif-visual-surface')
        self.assertIsNotNone(mount)
        self.assertEqual(mount.state, 'integration-proven')
        self.assertEqual(mount.implementation, 'static/js/dawn-visual-viewer.js')
        self.assertFalse(SurfaceMountRegistry().executable('iiif-visual-surface'))


if __name__ == '__main__':
    unittest.main()
