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
 def test_portrait_reference_gate_and_direction(self):
  a=Namespace(subject='speaker',recipe='overscale-collision',material='engraving',palette='olive-mountain',verified_reference=False,portrait_style='face-fragment')
  spec,prompt,_=compile_brief(a)
  self.assertTrue(spec['portrait_reference_required'])
  self.assertIn('Hold the identity-bearing render',prompt)
  a.verified_reference=True
  _,prompt,_=compile_brief(a)
  self.assertIn('Preserve identity-critical features',prompt)
 def test_magazine_scenarios_and_slots(self):
  from dore_editorial_scenarios import SCENARIOS,SLOTS
  for scenario in SCENARIOS:
   for slot in SLOTS:
    with self.subTest(scenario=scenario,slot=slot):
     a=Namespace(subject='editorial subject',recipe='quiet-field',material='engraving',palette='olive-mountain',verified_reference=False,portrait_style='none',scenario=scenario,slot=slot)
     spec,prompt,css=compile_brief(a)
     self.assertEqual(spec['scenario'],scenario)
     self.assertEqual(spec['slot'],slot)
     self.assertIn(SLOTS[slot]['ratio'],prompt)
     self.assertIn('SCENARIO-SPECIFIC SAFETY',prompt)
     self.assertIn('Slot layout policy',css)
if __name__=='__main__':unittest.main()
