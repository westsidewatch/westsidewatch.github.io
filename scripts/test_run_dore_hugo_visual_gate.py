#!/usr/bin/env python3
import tempfile,unittest
from pathlib import Path
from run_dore_hugo_visual_gate import build
class HugoVisualGateTests(unittest.TestCase):
 def test_missing_site_config(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);overlay=root/'overlay';(overlay/'content').mkdir(parents=True);(overlay/'static').mkdir()
   with self.assertRaises(FileNotFoundError):build(root,overlay,root/'out')
 def test_missing_overlay(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'hugo.toml').write_text('')
   with self.assertRaises(FileNotFoundError):build(root,root/'absent',root/'out')
if __name__=='__main__':unittest.main()
