#!/usr/bin/env python3
"""Portable anti-regression acceptance for the Doré autonomous loop."""
from __future__ import annotations
import json, os, py_compile, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve();DISCOVERED=HERE.parents[2]
ROOT=Path(os.environ.get('DORE_REPO_ROOT') or DISCOVERED).expanduser().resolve()
CONTRACT=ROOT/'dore-design'/'knowledge-lab'/'a2a'/'loop-contract-v1.json'
def mark(checks,name,value,detail=None):checks.append({'check':name,'pass':bool(value),**({'detail':str(detail)[-1200:]} if detail else {})})
def main():
    checks=[]
    try:contract=json.loads(CONTRACT.read_text(encoding='utf-8'));mark(checks,'contract parses',True)
    except Exception as e:print(json.dumps({'ok':False,'error':'contract_unreadable:'+repr(e),'root':str(ROOT)}));return 2
    for name,value in (contract.get('components') or {}).items():
        if isinstance(value,str) and value.startswith(('local/','dore-design/')):mark(checks,'component exists: '+name,(ROOT/value).exists(),value)
    pyfiles=['resident_runtime.py','autonomous_driver.py','autonomous_capability_loop.py','research_executor.py','peer_research_bridge.py','failure_memory.py','shared_learning.py','a2a_adapter.py','coordination_mailbox.py','coordination_worker.py']
    for name in pyfiles:
        rel=ROOT/'local'/'dore-local'/name
        try:py_compile.compile(str(rel),doraise=True);mark(checks,'python compiles: '+name,True)
        except Exception as e:mark(checks,'python compiles: '+name,False,e)
    runtime=(ROOT/'local/dore-local/resident_runtime.py').read_text(encoding='utf-8')
    for token in ['RESEARCH_QUEUED','RESEARCHING','PEER_RESEARCH_QUEUED','KNOWLEDGE_RETURNED','EXPERIMENTING','VERIFIED','REJECTED','PROMOTED','RESUME_PARENT','research_executor.py','peer_research_bridge.py','failure_memory.py','shared_learning.py','a2a_adapter.py','project-state.json','SELF_UPDATED','last_driver_diagnostic']:mark(checks,'runtime owns '+token,token in runtime)
    executor=(ROOT/'local/dore-local/research_executor.py').read_text(encoding='utf-8')
    for token in ['local_search','failure_memory','catalog_search','external_search','peer_escalate','provenance_preserved','reuse_before_rebuild','shared_learning','coordination_mailbox']:mark(checks,'research owns '+token,token in executor)
    driver=(ROOT/'local/dore-local/autonomous_driver.py').read_text(encoding='utf-8')
    mark(checks,'driver consumes knowledge artifact','knowledge_artifact' in driver)
    project=json.loads((ROOT/'dore-design/knowledge-lab/a2a/project-state.json').read_text(encoding='utf-8'));projects=(project.get('active_relationship') or {}).get('projects') or []
    mark(checks,'project relationship persists A2A <-> Storybook',len(projects)==2 and 'A2A' in projects[0] and 'Storybook' in projects[1])
    catalog=json.loads((ROOT/'dore-design/knowledge-lab/resources/source-catalog.json').read_text(encoding='utf-8'));ids={x.get('id') for x in catalog.get('sources') or []}
    for source in ['a2a-protocol','a2a-python','storybook','vite','langgraph','openhands']:mark(checks,'resource catalog contains '+source,source in ids)
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
        research=Path(td)/'research.json';research.write_text(json.dumps({'schema':'dore.research-job.v0.2','research_id':'accept-storybook-gap','state':'RESEARCH_QUEUED','parent_message_id':'accept-parent','parent_goal':'A2A <-> Storybook acceptance','question':'Storybook Vite JSX parse error in stories file; search mature official resources','failure_fingerprint':'[storybook:inject-export-order-plugin] Parse error JSX .stories.js'}),encoding='utf-8')
        cp=subprocess.run([sys.executable,str(ROOT/'local/dore-local/research_executor.py'),str(research)],cwd=str(ROOT),text=True,capture_output=True,timeout=180)
        try:payload=json.loads((cp.stdout or '').strip().splitlines()[-1])
        except Exception:payload={}
        mark(checks,'research executor discovers real evidence',cp.returncode==0 and payload.get('state')=='KNOWLEDGE_RETURNED' and ((payload.get('knowledge_artifact') or {}).get('evidence_count') or 0)>0,cp.stderr or cp.stdout)
    passed=all(x['pass'] for x in checks);print(json.dumps({'ok':passed,'schema':'dore.loop-contract-acceptance.v3','root':str(ROOT),'checks':checks,'passed':sum(1 for x in checks if x['pass']),'total':len(checks)},ensure_ascii=False));return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
