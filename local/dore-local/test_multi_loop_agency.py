import tempfile,unittest
from pathlib import Path
from multi_loop_agency import checkpoint,peer_poll_due
class Agency445Replay(unittest.TestCase):
 def goal(self):return {"goal_id":"design-reference-library-expansion-20260901","metadata":{"current_qualified_references":21,"current_source_families":0,"minimum_qualified_references":40,"minimum_source_families":6,"required_homepage_candidates":3}}
 def result(self,ok=False):return {"result":{"browser_evidence":{"observation":{"summary":{"candidate_count":7,"stable_viewports":14,"total_viewports":14},"gates":{"RESPONSIVE_PASS":ok,"VISUAL_STABLE":True},"candidates":[{"viewports":{"desktop":{"responsive_pass":ok},"mobile":{"responsive_pass":ok}}}]}}}}
 def test_iteration_445_routes_local_repair_and_sleeps_peer(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"s.json"; job={"peer_request_pending":True,"observed_replies":0}; checkpoint(self.goal(),self.result(),job,state_path=p); x=checkpoint(self.goal(),self.result(),job,state_path=p)
   self.assertEqual(x["assessment"]["kind"],"REPEATED_ACTIVITY");self.assertEqual(x["decision"]["route"],"LOCAL_RESPONSIVE_REPAIR");self.assertTrue(x["decision"]["yield_peer"])
   self.assertFalse(peer_poll_due(x))
 def test_responsive_fix_is_progress_then_routes_research(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"s.json";job={"peer_request_pending":True,"observed_replies":0};checkpoint(self.goal(),self.result(),job,state_path=p);x=checkpoint(self.goal(),self.result(True),job,state_path=p)
   self.assertTrue(x["assessment"]["progress"]);self.assertEqual(x["assessment"]["evidence_delta"]["responsive_failed"],-1);self.assertEqual(x["decision"]["route"],"LOCAL_REFERENCE_EXPANSION")
if __name__=="__main__":unittest.main()
