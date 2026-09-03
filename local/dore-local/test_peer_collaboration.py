import unittest
from peer_collaboration import respond
class PeerCollaborationTest(unittest.TestCase):
 def test_review_is_substantive(self):
  out=respond({'kind':'peer_review','message_id':'m','body':'Newsroom packaging and four risks'},'.');self.assertTrue(out['ok']);self.assertEqual(out['response_type'],'SUBSTANTIVE_PEER_REVIEW');self.assertTrue(out['architecture_judgment']['additional_risks'])
 def test_stall_finds_first_transition(self):
  out=respond({'kind':'peer_diagnostic','body':{}},'.');self.assertEqual(out['first_missing_transition'],'RECEIVED -> TASK_REGISTERED')
if __name__=='__main__':unittest.main()
