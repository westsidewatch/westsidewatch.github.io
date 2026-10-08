#!/usr/bin/env python3
import unittest
from build_dore_visual_preview import build,dimensions,BREAKPOINTS
class PreviewTests(unittest.TestCase):
 def setUp(self):
  self.spec={'slot':'cover','palette':'olive-mountain','composition':{'type_box':[0,0,22,100],'subject_box':[-10,15,115,115]}}
 def test_four_breakpoints_and_live_text(self):
  s=build(self.spec,'asset.png','Interview <subject>','Interview')
  for width in BREAKPOINTS:self.assertIn(str(width)+'px viewport',s)
  self.assertIn('Interview &lt;subject&gt;',s)
  self.assertIn('<strong>',s)
  self.assertIn('aspect-ratio:3 / 4',s)
  self.assertIn('object-fit:cover',s)
 def test_hero_ratio(self):
  self.spec['slot']='hero'
  self.assertIn('aspect-ratio:16 / 9',build(self.spec,'asset.png','Title','Sub'))
 def test_invalid_png_dimensions(self):
  import tempfile
  from pathlib import Path
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.png';p.write_bytes(b'not a PNG')
   self.assertIsNone(dimensions(p))
if __name__=='__main__':unittest.main()
