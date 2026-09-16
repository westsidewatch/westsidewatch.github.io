#!/usr/bin/env python3
from __future__ import annotations
import importlib,json,os,tempfile

def main():
 with tempfile.TemporaryDirectory() as td:
  os.environ["DORE_TWO_DAYS_HOME"]=td
  import two_days_artifact_ledger as ledger;ledger=importlib.reload(ledger)
  import two_days_today as today;today=importlib.reload(today)
  import two_days_capability_bridge as bridge;bridge=importlib.reload(bridge)
  aid="the-gate/03";v1="第三篇｜V1\n这是已经确认的正文。";v2="第三篇｜V2\n正在继续的正文。"
  ledger.put_version(aid,"V1",v1);ledger.apply("e1",aid,"TEXT_PROPOSED",to_version="V1");ledger.apply("e2",aid,"TEXT_ACCEPTED",to_version="V1")
  ledger.put_version(aid,"V2",v2);ledger.apply("e3",aid,"TEXT_REPLACED",from_version="V1",to_version="V2")
  resume={"artifact_id":aid,"instruction":"继续第三篇","unfinished_edge":"V2 尚未确认"}
  today.commit(aid,resume)
  pack=bridge.resolve("writing")
  check=bridge.verify(pack);assert check["ok"]
  assert pack["task"]["active_artifact"]==aid
  assert pack["task"]["accepted_head"]["version_id"]=="V1"
  assert pack["task"]["working_head"]["version_id"]=="V2"
  assert pack["task"]["resume_head"]==resume
  ids=[c["id"] for c in pack["capability_refs"]]
  assert ids==["context.fuzzy-search","knowledge.recall","publishing.dimensional-writing"]
  assert pack["authority"]["state"]=="TODAY" and pack["authority"]["capability"]=="dore-core-registry"
  assert pack["authority"]["may_rewrite_author_thesis"] is False
  try:bridge.resolve("writing",["invented.magic.writer"]);raise AssertionError("unknown capability admitted")
  except ValueError as e:assert str(e).startswith("two_days_unknown_capability:")
  assert ledger.content(aid,"V1")==v1 and ledger.content(aid,"V2")==v2
  print(json.dumps({"ok":True,"code":"TWO_DAYS_CAPABILITY_BRIDGE_PHASE4_PASS","profile":"writing","capabilities":ids,"unknown":"BLOCKED","accepted_head":"V1","working_head":"V2"},ensure_ascii=False))
if __name__=="__main__":main()
