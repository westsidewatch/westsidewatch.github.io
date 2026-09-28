#!/usr/bin/env python3
from __future__ import annotations
import importlib,os,tempfile

def main():
 with tempfile.TemporaryDirectory() as td:
  os.environ["DORE_TWO_DAYS_HOME"]=td
  import two_days_artifact_ledger as ledger;ledger=importlib.reload(ledger)
  aid="the-gate/03"
  v1="第三篇｜V1\n这是已经确认的正文。"
  v2="第三篇｜V2\n这是后来被否定的正文。"
  v3="第三篇｜V2 的标题\n这是已经确认的正文。"
  ledger.put_version(aid,"V1",v1);ledger.apply("e1",aid,"TEXT_PROPOSED",to_version="V1");ledger.apply("e2",aid,"TEXT_ACCEPTED",to_version="V1")
  ledger.put_version(aid,"V2",v2);ledger.apply("e3",aid,"TEXT_REPLACED",from_version="V1",to_version="V2")
  s=ledger.state(aid);assert s["accepted_head"]=="V1" and s["working_head"]=="V2",s
  ledger.apply("e4",aid,"TEXT_REJECTED",from_version="V2")
  s=ledger.state(aid);assert s["accepted_head"]=="V1" and s["working_head"]=="V1",s
  ledger.put_version(aid,"V3",v3);ledger.apply("e5",aid,"TEXT_REPLACED",from_version="V1",to_version="V3",metadata={"reason":"保留 V2 标题，恢复 V1 正文"})
  s=ledger.state(aid);assert s["accepted_head"]=="V1" and s["working_head"]=="V3",s
  # Crash/restart: no in-memory state may be required.
  ledger=importlib.reload(ledger);s=ledger.state(aid)
  assert s["accepted_head"]=="V1" and s["working_head"]=="V3",s
  assert ledger.content(aid,"V1")==v1 and ledger.content(aid,"V3")==v3
  # Idempotent replay cannot move heads; conflicting reuse of event id is blocked.
  replay=ledger.apply("e5",aid,"TEXT_REPLACED",from_version="V1",to_version="V3",metadata={"reason":"保留 V2 标题，恢复 V1 正文"});assert replay["working_head"]=="V3"
  try:ledger.apply("e5",aid,"TEXT_ACCEPTED",to_version="V3")
  except ValueError as exc:assert str(exc)=="artifact_event_identity_conflict"
  else:raise AssertionError("event identity conflict not blocked")
  # Only an explicit acceptance may advance ACCEPTED_HEAD.
  ledger.apply("e6",aid,"TEXT_ACCEPTED",to_version="V3");s=ledger.state(aid);assert s["accepted_head"]=="V3" and s["working_head"]=="V3",s
  ledger.apply("e7",aid,"TEXT_LOCKED",to_version="V3",metadata={"lock_id":"final-body","instruction":"前面不要动"})
  print("TWO_DAYS_ARTIFACT_LEDGER_PHASE2_PASS",s)
if __name__=="__main__":main()
