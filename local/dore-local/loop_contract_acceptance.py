#!/usr/bin/env python3
"""Portable anti-regression acceptance for the Doré autonomous loop."""
from __future__ import annotations
import json, os, py_compile, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve();ROOT=Path(os.environ.get('DORE_REPO_ROOT') or HERE.parents[2]).expanduser().resolve();CONTRACT=ROOT/'dore-design'/'knowledge-lab'/'a2a'/'loop-contract-v1.json'
def mark(checks,name,value,detail=None):checks.append({'check':name,'pass':bool(value),**({'detail':str(detail)[-1200:]} if detail else {})})
def source(rel):return (ROOT/rel).read_text(encoding='utf-8')
def main():
 checks=[]
 try:contract=json.loads(CONTRACT.read_text(encoding='utf-8'));mark(checks,'contract parses',True)
 except Exception as e:print(json.dumps({'ok':False,'error':'contract_unreadable:'+repr(e),'root':str(ROOT)}));return 2
 for name,value in (contract.get('components') or {}).items():
  if isinstance(value,str) and value.startswith(('local/','dore-design/','.github/')):mark(checks,'component exists: '+name,(ROOT/value).exists(),value)
 pyfiles=['resident_runtime.py','dore_agent_core.py','goal_queue.py','autonomous_driver.py','autonomous_capability_loop.py','research_executor.py','peer_research_bridge.py','knowledge_experiment.py','failure_memory.py','shared_learning.py','a2a_adapter.py','coordination_mailbox.py','coordination_worker.py']
 for name in pyfiles:
  rel=ROOT/'local'/'dore-local'/name
  try:py_compile.compile(str(rel),doraise=True);mark(checks,'python compiles: '+name,True)
  except Exception as e:mark(checks,'python compiles: '+name,False,e)
 runtime=source('local/dore-local/resident_runtime.py');agent=source('local/dore-local/dore_agent_core.py')
 for token in ['AGENT','agent_step','WAKE','AGENT_OBSERVATION','SELF_UPDATED','+refs/heads/main:refs/remotes/origin/main','runtime-control-manifest.json','heartbeat','telemetry']:mark(checks,'thin runtime owns '+token,token in runtime)
 for forbidden in ['def ensure_job(','def synthetic_gap(','def reject(','def verified(','RESEARCH_EXECUTOR=','PEER_BRIDGE=']:
  mark(checks,'thin runtime does not own '+forbidden,forbidden not in runtime)
 for token in ['RESEARCH_REQUIRED','RESEARCH_QUEUED','RESEARCHING','PEER_RESEARCH_QUEUED','KNOWLEDGE_RETURNED','EXPERIMENTING','VERIFIED','REJECTED','PROMOTED','RESUME_PARENT','ensure_job','synthetic_gap','research_executor.py','peer_research_bridge.py','failure_memory','shared_learning','a2a_adapter','goal_queue','NO_USER_INPUT_CONTINUE']:
  mark(checks,'agent core owns '+token,token in agent)
 mark(checks,'runtime delegates to Agent Core',"AGENT=LOCAL/'dore_agent_core.py'" in runtime and "agent_step()" in runtime)
 mark(checks,'Agent Core owns durable goal selection','from goal_queue import ensure_default,current' in agent)
 executor=source('local/dore-local/research_executor.py')
 for token in ['local_search','failure_memory','catalog_search','external_search','peer_escalate','provenance_preserved','reuse_before_rebuild','shared_learning','coordination_mailbox']:mark(checks,'research owns '+token,token in executor)
 bridge=source('local/dore-local/peer_research_bridge.py')
 for token in ['PEER_RESEARCH_QUEUED','KNOWLEDGE_RETURNED','research_id','provenance_required','chatgpt-to-dore.jsonl']:mark(checks,'peer bridge owns '+token,token in bridge)
 driver=source('local/dore-local/autonomous_driver.py');mark(checks,'driver consumes knowledge artifact','knowledge_artifact' in driver and 'research_context' in driver)
 queue=source('local/dore-local/goal_queue.py')
 for token in ['enqueue','current','set_status','PENDING','ACTIVE','PASS']:mark(checks,'goal queue owns '+token,token in queue)
 project=json.loads((ROOT/'dore-design/knowledge-lab/a2a/project-state.json').read_text(encoding='utf-8'));projects=(project.get('active_relationship') or {}).get('projects') or [];mark(checks,'project relationship persists A2A <-> Storybook',len(projects)==2 and 'A2A' in projects[0] and 'Storybook' in projects[1])
 manifest=json.loads((ROOT/'dore-design/knowledge-lab/a2a/runtime-control-manifest.json').read_text(encoding='utf-8'));files=manifest.get('files') or [];mark(checks,'manifest includes Agent Core','local/dore-local/dore_agent_core.py' in files);ownership=manifest.get('ownership') or {};mark(checks,'manifest separates runtime and Agent Core','resident_runtime' in ownership and 'dore_agent_core' in ownership)
 catalog=json.loads((ROOT/'dore-design/knowledge-lab/resources/source-catalog.json').read_text(encoding='utf-8'));ids={x.get('id') for x in catalog.get('sources') or []}
 for item in ['a2a-protocol','a2a-python','storybook','vite','langgraph','openhands']:mark(checks,'resource catalog contains '+item,item in ids)
 cp=subprocess.run([sys.executable,str(ROOT/'local/dore-local/a2a_adapter.py')],cwd=str(ROOT),text=True,capture_output=True,timeout=30)
 try:a2a=json.loads((cp.stdout or '').strip().splitlines()[-1])
 except Exception:a2a={}
 mark(checks,'A2A adapter emits canonical task',cp.returncode==0 and a2a.get('ok') and (a2a.get('task') or {}).get('kind')=='task',cp.stderr)
 code="import sys,json;sys.path.insert(0,'local/dore-local');from shared_learning import record;print(json.dumps(record({'knowledge_id':'x','sources':{},'provenance_preserved':True},status='PROMOTED')))"
 cp=subprocess.run([sys.executable,'-c',code],cwd=str(ROOT),text=True,capture_output=True,timeout=30)
 try:gate=json.loads((cp.stdout or '').strip().splitlines()[-1])
 except Exception:gate={}
 mark(checks,'shared learning blocks unverified promotion',gate.get('ok') is False and gate.get('error')=='verification_required_before_promotion')
 with tempfile.TemporaryDirectory(prefix='dore-loop-accept-') as td:
  research=Path(td)/'research.json';research.write_text(json.dumps({'schema':'dore.research-job.v0.3','research_id':'accept-storybook-gap','state':'RESEARCH_QUEUED','parent_message_id':'accept-parent','parent_goal':'A2A <-> Storybook acceptance','question':'Storybook Vite JSX parse error in stories file; search mature official resources','failure_fingerprint':'[storybook:inject-export-order-plugin] Parse error JSX .stories.js'}),encoding='utf-8')
  env={**os.environ,'DORE_REPO_ROOT':str(ROOT),'DORE_LOCAL_HOME':str(Path(td)/'home')};cp=subprocess.run([sys.executable,str(ROOT/'local/dore-local/research_executor.py'),str(research)],cwd=str(ROOT),env=env,text=True,capture_output=True,timeout=180)
  try:payload=json.loads((cp.stdout or '').strip().splitlines()[-1])
  except Exception:payload={}
  art=payload.get('knowledge_artifact') or {};mark(checks,'research executor discovers real evidence',cp.returncode==0 and payload.get('state')=='KNOWLEDGE_RETURNED' and (art.get('evidence_count') or 0)>0 and art.get('provenance_preserved') is True,cp.stderr or cp.stdout)
  code="import sys,json;sys.path.insert(0,'local/dore-local');import goal_queue as q;q.enqueue('accept-goal','accept');a=q.current();p=q.set_status('accept-goal','PASS');print(json.dumps({'active':a.get('status'),'pass':p.get('status')}))";cp=subprocess.run([sys.executable,'-c',code],cwd=str(ROOT),env=env,text=True,capture_output=True,timeout=30)
  try:q=json.loads((cp.stdout or '').strip().splitlines()[-1])
  except Exception:q={}
  mark(checks,'goal queue executes durable lifecycle',q.get('active')=='ACTIVE' and q.get('pass')=='PASS',cp.stderr)
 passed=all(x['pass'] for x in checks);print(json.dumps({'ok':passed,'schema':'dore.loop-contract-acceptance.v5','root':str(ROOT),'checks':checks,'passed':sum(1 for x in checks if x['pass']),'total':len(checks)},ensure_ascii=False));return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
