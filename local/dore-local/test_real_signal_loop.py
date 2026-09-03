import hashlib,tempfile,unittest
from pathlib import Path
from multi_loop_control_plane import load,register,route,wake
from newsroom_control_plane import ingest_and_run
from newsroom_signal_store import ingest,load as load_signals,recoverable
from real_signal_connector import parse_atom
ATOM=b'''<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><entry><id>tag:canada.ca,2026:item-1</id><title>Public safety update</title><summary>Official update for communities.</summary><published>2026-09-03T12:00:00Z</published><link href="https://www.canada.ca/en/example"/></entry></feed>'''
class RealSignalLoopTest(unittest.TestCase):
 def test_atom_provenance_and_dedupe_correction_retraction(self):
  with tempfile.TemporaryDirectory() as d:
   store=Path(d)/"signals.json";obs=parse_atom(ATOM,publisher="Government of Canada",feed_url="https://www.canada.ca/feed.xml")[0]
   self.assertEqual(ingest(obs,store_path=store)["action"],"CREATED");self.assertEqual(ingest(obs,store_path=store)["action"],"DEDUPLICATED")
   corrected={**obs,"summary":"Corrected official update.","content_hash":hashlib.sha256(b"corrected").hexdigest()}
   self.assertEqual(ingest(corrected,store_path=store,update_kind="CORRECTION")["signal"]["revision"],2)
   retracted={**corrected,"content_hash":hashlib.sha256(b"retracted").hexdigest()}
   self.assertEqual(ingest(retracted,store_path=store,update_kind="RETRACTION")["signal"]["status"],"RETRACTED");self.assertEqual(len(recoverable(store)),3)
 def test_episode_is_idempotent_and_human_gated(self):
  with tempfile.TemporaryDirectory() as d:
   state=Path(d)/"state.json";assets=Path(d)/"assets.jsonl";signals=Path(d)/"signals.json"
   register("storybook","Original work",kind="storybook",priority=50,state_path=state);wake("storybook","active",state_path=state);route(state_path=state)
   obs=parse_atom(ATOM,publisher="Government of Canada",feed_url="https://www.canada.ca/feed.xml")[0];obs.update(urgency=5,local_relevance=5,mission_relevance=5,human_impact=5,topics=[])
   first=ingest_and_run(obs,signal_store_path=signals,state_path=state,asset_path=assets);replay=ingest_and_run(obs,signal_store_path=signals,state_path=state,asset_path=assets)
   self.assertEqual(first["code"],"NEWSROOM_DRAFT_READY");self.assertEqual(replay["code"],"WORLD_SIGNAL_DEDUPLICATED");self.assertFalse(first["published"]);self.assertTrue(first["draft"]["requires_human_editor"]);self.assertEqual(first["resumed_loop"],"storybook");self.assertEqual(load(state)["active"],"storybook")
   op=load_signals(signals)["operations"][first["operation_id"]];self.assertEqual(op["state"],"COMMITTED");self.assertFalse(op["published"])
if __name__=="__main__":unittest.main()
