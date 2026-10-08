#!/usr/bin/env python3
"""Dependency-free structural checks for editorial brief compilation."""
import unittest
from argparse import Namespace
from compile_dore_editorial_brief import RECIPES,compile_brief
class EditorialBriefTests(unittest.TestCase):
 def test_all_recipes_have_coordinates_and_no_text_pixels(self):
  for recipe in RECIPES:
   with self.subTest(recipe=recipe):
    spec,prompt,css=compile_brief(Namespace(subject='olive tree',recipe=recipe,material='halftone',palette='olive-mountain',verified_reference=False))
    self.assertEqual(len(spec['composition']['subject_box']),4)
    self.assertEqual(len(spec['composition']['type_box']),4)
    self.assertIn('NO text',prompt)
    self.assertIn('CSS',css)
    self.assertFalse(spec['publication_approved'])
 def test_reference_guard(self):
  spec,prompt,_=compile_brief(Namespace(subject='named speaker',recipe='quiet-field',material='engraving',palette='olive-mountain',verified_reference=False))
  self.assertIn('Do not claim an invented face',prompt)
if __name__=='__main__':unittest.main()
