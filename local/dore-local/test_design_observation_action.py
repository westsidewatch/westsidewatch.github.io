import unittest
import design_observation_action as action
class ObservationActionTests(unittest.TestCase):
 def test_requires_https_source(self):
  self.assertFalse(action.execute('design.observe.capture',{'sourceId':'x','url':'http://example.com'})['ok'])
 def test_without_external_navigation_is_not_ready(self):
  r=action.execute('design.observe.capture',{'sourceId':'x','url':'https://example.com','viewport':'desktop'});self.assertEqual(r['status'],'not_ready');self.assertEqual(r['reason'],'external_navigation_evidence_required')
 def test_wrong_final_url_fails(self):
  snap={'finalUrl':'https://other.example/','screenshot':{'real_browser_render':True,'sha256':'abc'},'canonical_workspace_mutated':False,'production_promoted':False}
  r=action.execute('design.observe.capture',{'sourceId':'x','url':'https://example.com','runtimeSnapshot':snap});self.assertFalse(r['ok']);self.assertEqual(r['error']['code'],'source_identity_mismatch')
 def test_source_bound_raster_remains_observation_only(self):
  snap={'finalUrl':'https://www.example.com/page','renderedAt':'2026-09-17T00:00:00Z','screenshot':{'real_browser_render':True,'sha256':'abc','ref':'artifact://shot'},'observerPayload':{'schema':'dore.design-observation-evidence.v1'},'canonical_workspace_mutated':False,'production_promoted':False}
  r=action.execute('design.observe.capture',{'sourceId':'x','url':'https://example.com','viewport':'desktop','runtimeSnapshot':snap});self.assertTrue(r['ok']);self.assertEqual(r['observerStatus'],'captured');self.assertFalse(r['authority']['mayPromoteCanonical']);self.assertTrue(r['authority']['requiresBeautifulGate'])
 def test_authority_violation_fails(self):
  snap={'finalUrl':'https://example.com/','screenshot':{'real_browser_render':True,'sha256':'abc'},'canonical_workspace_mutated':True,'production_promoted':False}
  r=action.execute('design.observe.capture',{'sourceId':'x','url':'https://example.com','runtimeSnapshot':snap});self.assertEqual(r['status'],'failed');self.assertEqual(r['error']['code'],'authority_boundary_violation')
if __name__=='__main__':unittest.main()
