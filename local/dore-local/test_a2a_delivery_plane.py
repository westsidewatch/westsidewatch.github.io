import tempfile,unittest
from pathlib import Path
from a2a_delivery_plane import accept,durable_messages
def message(body='review',message_id='peer-1'):return {'schema':'dore.mail.v1','message_id':message_id,'sender':'chatgpt','recipient':'dore','body':body}
class DeliveryPlaneTest(unittest.TestCase):
 def test_durable_accept_and_replay_dedupe(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);first=accept(message(),source_ref='origin/main',source_commit='abc',source_path='x',delivery_root=root);replay=accept(message(),source_ref='origin/main',source_commit='def',source_path='x',delivery_root=root);self.assertEqual(first['delivery_status'],'DURABLE_ACCEPTED');self.assertEqual(replay['status'],'REPLAY_DEDUPLICATED');self.assertEqual(len(durable_messages(root)),1)
 def test_same_identity_different_content_is_quarantined(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);accept(message(),source_ref='origin/main',source_commit='abc',source_path='x',delivery_root=root);conflict=accept(message('changed'),source_ref='origin/main',source_commit='def',source_path='x',delivery_root=root);self.assertEqual(conflict['status'],'REJECTED_IDENTITY_CONFLICT');self.assertEqual(len(durable_messages(root)),1)
 def test_invalid_identity_is_not_delivered(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);bad=message();bad['sender']='unknown';result=accept(bad,source_ref='origin/main',source_commit='abc',source_path='x',delivery_root=root);self.assertEqual(result['status'],'REJECTED_INVALID');self.assertEqual(durable_messages(root),[])
if __name__=='__main__':unittest.main()
