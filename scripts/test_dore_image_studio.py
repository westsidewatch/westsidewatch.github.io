#!/usr/bin/env python3
"""Smoke tests for the Doré localhost Image Studio."""
import importlib.util
import unittest
from pathlib import Path
MODULE=Path(__file__).resolve().parents[1]/"local/dore-local/image_studio.py"
spec=importlib.util.spec_from_file_location("dore_image_studio",MODULE)
studio=importlib.util.module_from_spec(spec)
spec.loader.exec_module(studio)

class StudioContractTests(unittest.TestCase):
 def test_clipboard_paste_supported(self):
  self.assertIn("addEventListener('paste'",studio.PAGE)
  self.assertIn("item.getAsFile()",studio.PAGE)
 def test_drop_and_picker_supported(self):
  self.assertIn("drop.ondrop=",studio.PAGE)
  self.assertIn('type="file"',studio.PAGE)
 def test_local_only(self):
  self.assertEqual(studio.HOST,"127.0.0.1")
  self.assertEqual(studio.MODEL,"http://127.0.0.1:8790")
 def test_reference_conditioning_is_required(self):
  self.assertIn('reference_conditioned',Path(MODULE).read_text())
  self.assertIn('reference_image',Path(MODULE).read_text())
if __name__=="__main__":unittest.main()
