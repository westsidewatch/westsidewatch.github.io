#!/usr/bin/env python3
import unittest
from review_dore_editorial_art import review,CHECKS
class EditorialQATests(unittest.TestCase):
 def setUp(self):
  self.spec={'publication_approved':False,'scenario':'essay-concept','verified_reference':False}
 def test_empty_review_is_pending(self):
  r=review(self.spec,{})
  self.assertFalse(r['ready_for_editorial_approval'])
  self.assertEqual(len(r['pending']),len(CHECKS))
 def test_fail_requires_attention(self):
  r=review(self.spec,{'crop':{'status':'fail','evidence':'subject centered'}})
  self.assertTrue(r['failed'])
 def test_claimed_pass_without_evidence_rejected(self):
  r=review(self.spec,{'crop':'pass'})
  self.assertIn('crop: evidence required',r['failed'])
 def test_all_evidenced_passes_ready_for_human_approval(self):
  answers={k:{'status':'pass','evidence':'Reviewed proof at final size'} for k in CHECKS}
  r=review(self.spec,answers)
  self.assertTrue(r['ready_for_editorial_approval'])
  self.assertFalse(r['publication_approved'])
 def test_named_person_needs_reference(self):
  self.spec['scenario']='speaker'
  answers={k:{'status':'pass','evidence':'Reviewed'} for k in CHECKS}
  r=review(self.spec,answers)
  self.assertFalse(r['ready_for_editorial_approval'])
  self.assertTrue(any('verified reference' in x for x in r['failed']))
 def test_not_applicable_restricted(self):
  r=review(self.spec,{'palette':{'status':'not-applicable','evidence':'none'}})
  self.assertFalse(r['ready_for_editorial_approval'])
  self.assertTrue(any('not-applicable not permitted' in x for x in r['failed']))
if __name__=='__main__':unittest.main()
