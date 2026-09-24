import unittest
import design_runtime_capture_contract as c
class RuntimeCaptureContractTests(unittest.TestCase):
 def good(self):return {'schema':c.SCHEMA,'finalUrl':'https://www.example.com/page','screenshot':{'real_browser_render':True,'sha256':'abc'},'observerPayload':{'schema':'dore.design-observation-evidence.v1'},'canonical_workspace_mutated':False,'production_promoted':False}
 def test_good_source_bound_capture(self):self.assertEqual(c.validate(self.good(),'https://example.com/'),(True,'ok'))
 def test_observer_is_mandatory(self):
  s=self.good();s.pop('observerPayload');self.assertEqual(c.validate(s,'https://example.com/')[1],'design_observer_evidence_required')
 def test_cross_source_redirect_fails(self):self.assertEqual(c.validate(self.good(),'https://different.example/')[1],'source_identity_mismatch')
 def test_source_probe_projection_is_generic(self):self.assertEqual(c.source_probe_snapshot(self.good())['collector'],c.SCHEMA)
if __name__=='__main__':unittest.main()
