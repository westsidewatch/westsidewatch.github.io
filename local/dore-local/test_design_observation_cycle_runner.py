import json,tempfile,unittest
from pathlib import Path
import design_observation_cycle_runner as runner
class CycleRunnerContract(unittest.TestCase):
 def test_job_identity_is_stable(self):
  s={'id':'x','url':'https://example.com/'};self.assertEqual(runner._id(s,'desktop'),runner._id(s,'desktop'));self.assertNotEqual(runner._id(s,'desktop'),runner._id(s,'mobile'))
 def test_atomic_result_roundtrip(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'x.json';runner._atomic(p,{'status':'partial','canonicalWrites':0});self.assertEqual(json.loads(p.read_text())['canonicalWrites'],0)
if __name__=='__main__':unittest.main()
