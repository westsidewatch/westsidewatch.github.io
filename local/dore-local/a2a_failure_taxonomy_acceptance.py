#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,os,tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent

def load(name):
 p=HERE/(name+'.py');s=importlib.util.spec_from_file_location('accept_'+name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
 with tempfile.TemporaryDirectory() as td:
  os.environ['DORE_LOCAL_HOME']=td
  policy=load('a2a_failure_policy')
  cases={
   'retryable':policy.classify({'error':{'code':'timeout'}},descriptor={'retry_safe':True}),
   'unknown':policy.classify({'error':{'code':'connection_reset'}},descriptor={'requires_verified_execution':True},binding={'kind':'production-action'}),
   'quarantined':policy.classify({'error':{'code':'invalid_schema'}}),
   'research':policy.classify({'error':{'code':'timeout'}},descriptor={'retry_safe':True},attempt=3,max_attempts=3),
   'terminal':policy.classify({'error':{'code':'authority_rejected'}}),
  }
  expected={'retryable':'RETRYABLE','unknown':'UNKNOWN','quarantined':'QUARANTINED','research':'RESEARCH_REQUIRED','terminal':'TERMINAL_FAIL'}
  assert {k:v['state'] for k,v in cases.items()}==expected
  q=policy.decision('poison-1',{'error':{'code':'invalid_schema'}},context={'queue_index':1})
  assert q['state']=='QUARANTINED'
  assert (policy.QUARANTINE/'poison-1.json').exists()
  processed=[]
  for task_id,failure in [('bad',{'error':{'code':'malformed_message'}}),('good',None)]:
   if failure:
    d=policy.decision(task_id,failure)
    processed.append((task_id,d['state']))
    continue
   processed.append((task_id,'PASS'))
  assert processed==[('bad','QUARANTINED'),('good','PASS')]
  events=(policy.FAILURES).read_text(encoding='utf-8').splitlines()
  assert len(events)>=2
  result={'ok':True,'code':'A2A_FAILURE_TAXONOMY_ACCEPTANCE_PASS','vocabulary':list(policy.VOCABULARY),'cases':{k:v['state'] for k,v in cases.items()},'poison_isolation':processed,'quarantine_file':str(policy.QUARANTINE/'poison-1.json')}
  print(json.dumps(result,ensure_ascii=False));return 0

if __name__=='__main__':raise SystemExit(main())
