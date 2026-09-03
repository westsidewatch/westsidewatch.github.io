import unittest
from peer_collaboration import respond
class PeerCollaborationTest(unittest.TestCase):
 def test_review_is_substantive(self):
  out=respond({'kind':'peer_review','message_id':'m','body':'Newsroom packaging and four risks'},'.');self.assertTrue(out['ok']);self.assertEqual(out['response_type'],'SUBSTANTIVE_PEER_REVIEW');self.assertTrue(out['architecture_judgment']['additional_risks'])
 def test_diagnostic_is_nonterminal_and_source_bound(self):
  out=respond({'kind':'peer_diagnostic','message_id':'d','body':{'classification':'SEMANTIC_RESPONSE_MISMATCH','transition':'RESEARCH_QUEUED -> RESEARCH_STARTED'}},'.');self.assertFalse(out['ok']);self.assertFalse(out['terminal_eligible']);self.assertEqual(out['reviewed_message_id'],'d');self.assertEqual(out['requested_transition'],'RESEARCH_QUEUED -> RESEARCH_STARTED')
 def test_followup_is_not_routed_to_stale_diagnostic(self):
  out=respond({'kind':'peer_review_followup','message_id':'f','body':{'peer_question':'Newsroom next step'}},'.');self.assertTrue(out['ok']);self.assertEqual(out['response_type'],'SUBSTANTIVE_PEER_REVIEW_FOLLOWUP');self.assertEqual(out['reviewed_message_id'],'f')
if __name__=='__main__':unittest.main()
