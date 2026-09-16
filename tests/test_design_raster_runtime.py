import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'dore-design'))
import design_intelligence_raster as raster

class RuntimeTests(unittest.TestCase):
    def test_retry_does_not_admit_failed_attempt(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / 'candidate.png'
            target.write_bytes(b'stale')
            def attempt(browser, root, output, width, height, number):
                output.write_bytes(b'failed' if number == 1 else b'fresh')
                if number == 1:
                    raise RuntimeError('timeout')
                return 0.1
            with patch.object(raster, 'browser_binary', return_value='firefox'), patch.object(raster, '_render_attempt', side_effect=attempt) as render, patch.object(raster, 'png_dimensions', return_value=(1440,900)):
                evidence = raster.rasterize_html('<html></html>', output=target, width=1440, height=900)
            self.assertEqual(render.call_count, 2)
            self.assertEqual(target.read_bytes(), b'fresh')
            self.assertTrue(evidence['real_browser_render'])

    def test_exhaustion_preserves_diagnostics_and_fails(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / 'candidate.png'
            with patch.object(raster, 'browser_binary', return_value='firefox'), patch.object(raster, '_render_attempt', side_effect=RuntimeError('timeout')):
                with self.assertRaisesRegex(RuntimeError, 'browser_raster_failed'):
                    raster.rasterize_html('<html></html>', output=target, width=1440, height=900)
            self.assertFalse(target.exists())
            self.assertIn('timeout', target.with_suffix('.raster-failure.json').read_text())

if __name__ == '__main__':
    unittest.main()
