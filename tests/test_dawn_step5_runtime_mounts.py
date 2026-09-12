import unittest
from pathlib import Path

from dore_core.capabilities.surface_mounts import SurfaceMountRegistry
from dore_core.capabilities.url_surface import UrlSurfaceResolver

ROOT = Path(__file__).resolve().parents[1]


class DawnStep5RuntimeMountTests(unittest.TestCase):
    def test_only_production_surfaces_are_promoted(self):
        registry = SurfaceMountRegistry()
        for adapter in ('iiif-visual-surface', 'pdfjs', 'book-reader', 'video-surface'):
            self.assertEqual(registry.state(adapter), 'mounted')
            self.assertTrue(registry.executable(adapter))
            self.assertTrue((ROOT / registry.get(adapter).implementation).exists())

        for adapter in ('zotero-translate', 'readability', 'cover-resolve'):
            self.assertEqual(registry.state(adapter), 'integration-proven')
            self.assertFalse(registry.executable(adapter))

    def test_real_pointer_plans_are_now_executable(self):
        resolver = UrlSurfaceResolver()
        plans = (
            resolver.plan('https://data.artmuseum.princeton.edu/iiif/objects/56244'),
            resolver.plan('https://upload.wikimedia.org/wikipedia/commons/5/55/The_confessions_of_S._Augustine%2C_books_I-X_%28IA_confessionsofsau00augurich%29.pdf'),
            resolver.plan('https://archive.org/details/completeworksofj19002jose'),
            resolver.plan('https://www.youtube.com/watch?v=or22I3KOerA'),
        )
        for plan in plans:
            self.assertEqual(plan.mount_state, 'mounted')
            self.assertTrue(plan.executable)
            self.assertTrue(plan.external)
            self.assertEqual(plan.ownership, 'external')


if __name__ == '__main__':
    unittest.main()
