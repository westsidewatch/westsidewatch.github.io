#!/usr/bin/env python3
import unittest
from build_dore_hugo_overlay import render_frontmatter
class HugoOverlayTests(unittest.TestCase):
 def test_real_section(self):
  section,text=render_frontmatter({'page_resolution':{'route':'/olive/'},'palette':'olive-mountain','slot':'hero'},'dore-proof/test.png','Speaker')
  self.assertEqual(section,'olive')
  self.assertIn('layout: "dore-proof"',text)
  self.assertIn('url: "/olive/dore-proof/"',text)
 def test_unmapped_rejected(self):
  with self.assertRaises(ValueError):
   render_frontmatter({'page_resolution':{'route':'/unknown/'},'palette':'magazine','slot':'cover'},'dore-proof/test.png','Test')
 def test_unsafe_asset_rejected(self):
  with self.assertRaises(ValueError):
   render_frontmatter({'page_resolution':{'route':'/olive/'},'palette':'olive-mountain','slot':'cover'},'../escape.png','Test')
if __name__=='__main__':unittest.main()
