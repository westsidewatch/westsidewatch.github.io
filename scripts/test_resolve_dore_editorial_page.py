#!/usr/bin/env python3
import unittest
from resolve_dore_editorial_page import resolve,parse_frontmatter
class PageResolverTests(unittest.TestCase):
 def test_olive_section(self):
  r=resolve('/olive-mountain/')
  self.assertEqual((r['scenario'],r['slot'],r['palette']),('section-hero','hero','olive-mountain'))
 def test_journal_requires_palette(self):
  with self.assertRaisesRegex(ValueError,'palette'):
   resolve('/journal/')
 def test_cinema_requires_palette(self):
  with self.assertRaisesRegex(ValueError,'palette'):
   resolve('/cinema/')
 def test_explicit_override(self):
  r=resolve('/journal/',{'dore_scenario':'column-author','dore_slot':'profile-card','dore_palette':'olive-mountain'})
  self.assertEqual((r['scenario'],r['slot']),('column-author','profile-card'))
 def test_unknown_route_fails(self):
  with self.assertRaisesRegex(ValueError,'No explicit'):
   resolve('/not-a-real-section/')
 def test_unknown_palette_fails(self):
  with self.assertRaisesRegex(ValueError,'not implemented'):
   resolve('/journal/',{'dore_palette':'magazine-unknown'})
if __name__=='__main__':unittest.main()
