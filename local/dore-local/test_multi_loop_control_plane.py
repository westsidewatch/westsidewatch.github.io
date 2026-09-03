import tempfile,unittest
from pathlib import Path
from multi_loop_control_plane import register,wake,route,complete,load
class ControlPlaneTest(unittest.TestCase):
 def test_higher_priority_wakes_yields_and_resumes(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'s.json';register('a','A',kind='storybook',priority=50,state_path=p);wake('a','start',state_path=p);route(state_path=p);register('b','B',kind='library',priority=60,state_path=p);wake('b','asset',gravity=10,state_path=p);self.assertEqual(route(state_path=p)['loop_id'],'b');self.assertEqual(load(p)['workflows']['a']['status'],'YIELDED');self.assertEqual(complete('b',state_path=p)['loop_id'],'a')
if __name__=='__main__':unittest.main()
