#!/usr/bin/env python3
import tempfile,unittest
from pathlib import Path
from capture_dore_editorial_screenshots import WIDTHS,capture
class ScreenshotTests(unittest.TestCase):
 def test_expected_widths(self):
  self.assertEqual(WIDTHS,(320,375,768,1440))
 def test_missing_preview_fails_before_browser(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(FileNotFoundError):
    capture(Path(d)/'missing.html',Path(d)/'out')
if __name__=='__main__':unittest.main()
