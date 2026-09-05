import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("design2_stage3",ROOT/"dore-design"/"design2_stage3.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Stage3Tests(unittest.TestCase):
 def gates(self, value=True): return {g:value for g in m.MATURITY_GATES}
 def test_world_breadth_is_material(self):
  self.assertGreaterEqual(len(m.DESIGN_WORLDS),20)
  self.assertIn("swiss-international",m.DESIGN_WORLDS);self.assertIn("japanese-editorial",m.DESIGN_WORLDS);self.assertIn("vernacular-community",m.DESIGN_WORLDS);self.assertIn("sacred-architecture",m.DESIGN_WORLDS)
 def test_screenshot_is_not_maturity(self):
  e=m.ExperimentEvidence("x","swiss-international",{"browser_evidence":True},("shot.png",))
  self.assertFalse(e.mature);self.assertLess(e.maturity_score,1)
 def test_technical_maturity_cannot_self_accept_style(self):
  e=m.ExperimentEvidence("x","swiss-international",self.gates())
  self.assertTrue(e.mature);self.assertFalse(e.record()["style_acceptance"])
 def test_convergence_requires_breadth_depth_and_human_authority(self):
  es=[m.ExperimentEvidence(str(i),w,self.gates()) for i,w in enumerate(m.DESIGN_WORLDS[:8])]
  blocked=m.convergence_gate(es,user_authorized=False)
  self.assertFalse(blocked["ready"]);self.assertIn("user-convergence-authorization-required",blocked["reasons"])
  self.assertTrue(m.convergence_gate(es,user_authorized=True)["ready"])
 def test_build_sequence_reaches_system_not_workspace_only(self):
  self.assertEqual(m.CONVERGENCE_SEQUENCE[-4:],("design_system_foundations","brick_system","living_wall","homepage_implementation"))

if __name__=="__main__":unittest.main()
