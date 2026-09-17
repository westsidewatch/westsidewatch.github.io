import unittest
from unittest.mock import patch
import design_observation_action as action

class ObservationActionTests(unittest.TestCase):
 def test_requires_https_source(self):
  self.assertFalse(action.execute('design.observe.capture',{'sourceId':'x','url':'http://example.com'})['ok'])
 def test_no_raster_is_not_ready(self):
  class Bridge:
   @staticmethod
   def explore(payload): return {'provider':'dore-local','candidates':[]}
  with patch.object(action.importlib,'import_module',return_value=Bridge):
   r=action.execute('design.observe.capture',{'sourceId':'x','url':'https://example.com','viewport':'desktop'})
  self.assertEqual(r['status'],'not_ready')
 def test_proven_raster_remains_observation_only(self):
  class Bridge:
   @staticmethod
   def explore(payload): return {'provider':'dore-local','model':'real','candidates':[{'raster':{'real_browser_render':True,'sha256':'abc'}}],'canonical_workspace_mutated':False,'production_promoted':False}
  with patch.object(action.importlib,'import_module',return_value=Bridge):
   r=action.execute('design.observe.capture',{'sourceId':'x','url':'https://example.com','viewport':'desktop'})
  self.assertTrue(r['ok']);self.assertFalse(r['authority']['mayPromoteCanonical']);self.assertTrue(r['authority']['requiresBeautifulGate']);self.assertFalse(r['canonical_workspace_mutated']);self.assertFalse(r['production_promoted'])
if __name__=='__main__':unittest.main()
