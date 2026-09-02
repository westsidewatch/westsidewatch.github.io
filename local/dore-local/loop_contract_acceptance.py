#!/usr/bin/env python3
"""Portable anti-regression acceptance for Doré autonomous Storybook/A2A loop."""
from __future__ import annotations
import json, os, py_compile, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve();ROOT=Path(os.environ.get('DORE_REPO_ROOT') or HERE.parents[2]).expanduser().resolve();CONTRACT=ROOT/'dore-design'/'knowledge-lab'/'a2a'/'loop-contract-v1.json'
def mark(checks,name,value,detail=None):checks.append({'check':name,'pass':bool(value),**({'detail':str(detail)[-1200:]} if detail else {})})
def source(rel):return (ROOT/rel).read_text(encoding='utf-8')
def last_json(text):
 for line in reversed((text or '').splitlines()):
  try:return json.loads(line)
  except Exception:pass
 return {}
def main():
 checks=[]
 try:contract=json.loads(CONTRACT.read_text(encoding='utf-8'));mark(checks,'contract parses',True)
 except Exception as e:print(json.dumps({'ok':False,'error':'contract_unreadable:'+repr(e),'root':str(ROOT)}));return 2
 mark(checks,'contract is asynchronous peer model',contract.get('schema')=='dore.autonomous-loop-contract.v1.4' and (contract.get('operating_model') or {}).get('chatgpt')=='conversation-activated asynchronous peer')
 inv=set(contract.get('hard_invariants') or [])
 for item in ['chatgpt-offline-is-normal-not-failure','peer-research-request-is-durable-and-non-blocking','no-waiting-peer-state-may-freeze-storybook-or-design-lab','storybook-build-pass-alone-is-not-design-lab-acceptance','no-paid-openai-api']:mark(checks,'contract invariant '+item,item in inv)
 for name,value in (contract.get('components') or {}).items():
  if isinstance(value,str) and value.startswith(('local/','dore-design/','.github/')):mark(checks,'component exists: '+name,(ROOT/value).exists(),value)
 pyfiles=['resident_runtime.py','a2a_supervisor.py','dore_agent_core.py','goal_queue.py','autonomous_driver.py','autonomous_capability_loop.py','research_executor.py','peer_research_bridge.py','knowledge_experiment.py','failure_memory.py','shared_learning.py','a2a_adapter.py','coordination_mailbox.py','coordination_worker.py']
 for name in pyfiles:
  rel=ROOT/'local'/'dore-local'/name
  try:py_compile.compile(str(rel),doraise=True);mark(checks,'python compiles: '+name,True)
  except Exception as e:mark(checks,'python compiles: '+name,False,e)
 runtime=source('local/dore-local/resident_runtime.py');agent=source('local/dore-local/dore_agent_core.py');supervisor=source('local/dore-local/a2a_supervisor.py');driver=source('local/dore-local/autonomous_driver.py')
 for forbidden in ['def ensure_job(','def synthetic_gap(','def reject(','def verified(','RESEARCH_EXECUTOR=','PEER_BRIDGE=']:mark(checks,'thin runtime does not own '+forbidden,forbidden not in runtime)
 for token in ['PENDING_PEER_NONBLOCKING','PEER_PENDING_CONTINUE_AUTONOMOUS','peer_blocking=False','INFORMATION_GAIN_ROTATION','NO_USER_INPUT_CONTINUE']:mark(checks,'Agent Core autonomous peer token '+token,token in agent)
 mark(checks,'Agent Core still polls peer bridge','peer_research_bridge.py' in agent and 'research_id' in agent)
 for token in ['A2A_PEER_PENDING_NONBLOCKING','CONTINUE_AUTONOMOUS_WORK','chatgpt_presence_required','peer_blocking']:mark(checks,'supervisor nonblocking token '+token,token in supervisor)
 mark(checks,'old blocking peer state removed from supervisor',"A2A_WAITING_PEER" not in supervisor and "PEER_RESPONSE_REQUIRED" not in supervisor)
 for token in ['run_browser_evidence','test-storybook','evidence-storybook','Playwright Chromium','browser evidence gate failed','paid_api_used']:mark(checks,'driver evidence token '+token,token in driver)
 package=json.loads((ROOT/'dore-design/knowledge-lab/storybook/package.json').read_text(encoding='utf-8'));dev=package.get('devDependencies') or {};scripts=package.get('scripts') or {}
 for dep in ['@storybook/addon-vitest','@storybook/addon-a11y','@playwright/test','@vitest/browser-playwright','vitest']:mark(checks,'storybook evidence dependency '+dep,dep in dev)
 for script in ['test-storybook','evidence-storybook','autonomy-check']:mark(checks,'storybook evidence script '+script,script in scripts)
 mainjs=source('dore-design/knowledge-lab/storybook/.storybook/main.js');mark(checks,'Storybook registers Vitest addon','@storybook/addon-vitest' in mainjs);mark(checks,'Storybook registers a11y addon','@storybook/addon-a11y' in mainjs)
 vitest=source('dore-design/knowledge-lab/storybook/vitest.config.js');mark(checks,'Vitest uses Playwright browser mode','@vitest/browser-playwright' in vitest and "browser: 'chromium'" in vitest)
 evidence=source('dore-design/knowledge-lab/storybook/scripts/storybook-evidence.mjs')
 for token in ['desktop','mobile','VISUAL_STABLE','RESPONSIVE_PASS','DESIGN_DISTINCT','WESTSIDE_FIT','sha256']:mark(checks,'browser evidence owns '+token,token in evidence)
 manifest=json.loads((ROOT/'dore-design/knowledge-lab/a2a/runtime-control-manifest.json').read_text(encoding='utf-8'));files=manifest.get('files') or []
 for rel in ['local/dore-local/dore_agent_core.py','local/dore-local/a2a_supervisor.py','local/dore-local/autonomous_driver.py','dore-design/knowledge-lab/storybook/package.json','dore-design/knowledge-lab/storybook/vitest.config.js','dore-design/knowledge-lab/storybook/scripts/storybook-evidence.mjs']:mark(checks,'runtime manifest syncs '+rel,rel in files)
 # Isolated supervisor acceptance: a pending peer request must classify as non-blocking.
 with tempfile.TemporaryDirectory(prefix='dore-loop-accept-') as td:
  env={**os.environ,'DORE_LOCAL_HOME':td,'DORE_REPO_ROOT':str(ROOT)};sample={'result':{'state':'PENDING_PEER_NONBLOCKING','continue':True,'peer_pending':True,'peer_blocking':False,'parent':{'goal_id':'accept','project_loop':'Doré autonomous Storybook'},'research_job':{'research_id':'r-1','state':'PEER_RESEARCH_QUEUED','peer_request_pending':True,'human_gate':False}}}
  cp=subprocess.run([sys.executable,str(ROOT/'local/dore-local/a2a_supervisor.py')],cwd=str(ROOT),env=env,text=True,input=json.dumps(sample),capture_output=True,timeout=30);sup=last_json(cp.stdout)
  mark(checks,'pending peer is nonblocking in executable supervisor',cp.returncode==0 and sup.get('a2a_state')=='A2A_PEER_PENDING_NONBLOCKING' and sup.get('action_required')=='CONTINUE_AUTONOMOUS_WORK' and sup.get('peer_blocking') is False,cp.stderr or cp.stdout)
  sample['result']['state']='HUMAN_GATE';sample['result']['peer_pending']=False;sample['result']['research_job']['peer_request_pending']=False;sample['result']['research_job']['human_gate']=True
  cp=subprocess.run([sys.executable,str(ROOT/'local/dore-local/a2a_supervisor.py')],cwd=str(ROOT),env=env,text=True,input=json.dumps(sample),capture_output=True,timeout=30);sup=last_json(cp.stdout);mark(checks,'true human gate remains explicit',sup.get('a2a_state')=='A2A_HUMAN_GATE' and sup.get('user_gate') is True)
 # Existing safety gates remain intact.
 bridge=source('local/dore-local/peer_research_bridge.py')
 for token in ['PEER_RESEARCH_QUEUED','KNOWLEDGE_RETURNED','research_id','provenance_required','chatgpt-to-dore.jsonl']:mark(checks,'peer bridge owns '+token,token in bridge)
 queue=source('local/dore-local/goal_queue.py')
 for token in ['enqueue','current','set_status','PENDING','ACTIVE','PASS']:mark(checks,'goal queue owns '+token,token in queue)
 cp=subprocess.run([sys.executable,str(ROOT/'local/dore-local/a2a_adapter.py')],cwd=str(ROOT),text=True,capture_output=True,timeout=30);a2a=last_json(cp.stdout);mark(checks,'A2A adapter emits canonical task',cp.returncode==0 and a2a.get('ok') and (a2a.get('task') or {}).get('kind')=='task',cp.stderr)
 code="import sys,json;sys.path.insert(0,'local/dore-local');from shared_learning import record;print(json.dumps(record({'knowledge_id':'x','sources':{},'provenance_preserved':True},status='PROMOTED')))";cp=subprocess.run([sys.executable,'-c',code],cwd=str(ROOT),text=True,capture_output=True,timeout=30);gate=last_json(cp.stdout);mark(checks,'shared learning blocks unverified promotion',gate.get('ok') is False and gate.get('error')=='verification_required_before_promotion')
 passed=all(x['pass'] for x in checks);print(json.dumps({'ok':passed,'schema':'dore.loop-contract-acceptance.v6','root':str(ROOT),'checks':checks,'passed':sum(1 for x in checks if x['pass']),'total':len(checks)},ensure_ascii=False));return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
