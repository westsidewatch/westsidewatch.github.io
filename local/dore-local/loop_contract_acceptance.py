#!/usr/bin/env python3
"""Static + executable anti-regression acceptance for the Doré autonomous loop."""
from __future__ import annotations
import json, os, py_compile, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser();CONTRACT=ROOT/'dore-design'/'knowledge-lab'/'a2a'/'loop-contract-v1.json'
def fail(msg,checks):checks.append({'check':msg,'pass':False})
def ok(msg,checks):checks.append({'check':msg,'pass':True})
def main():
    checks=[]
    try:contract=json.loads(CONTRACT.read_text(encoding='utf-8'));ok('contract parses',checks)
    except Exception as e:print(json.dumps({'ok':False,'error':'contract_unreadable:'+repr(e)}));return 2
    for _,value in (contract.get('components') or {}).items():
        if isinstance(value,str) and value.startswith(('local/','dore-design/')):(ok if (ROOT/value).exists() else fail)('component exists: '+value,checks)
    pyfiles=['resident_runtime.py','autonomous_driver.py','autonomous_capability_loop.py','research_executor.py','failure_memory.py','shared_learning.py','a2a_adapter.py','coordination_mailbox.py','coordination_worker.py']
    for name in pyfiles:
        rel='local/dore-local/'+name
        try:py_compile.compile(str(ROOT/rel),doraise=True);ok('python compiles: '+rel,checks)
        except Exception as e:fail('python compiles: '+rel+' :: '+repr(e),checks)
    runtime=(ROOT/'local/dore-local/resident_runtime.py').read_text(encoding='utf-8')
    for token in ['RESEARCH_QUEUED','RESEARCHING','KNOWLEDGE_RETURNED','EXPERIMENTING','VERIFIED','REJECTED','PROMOTED','RESUME_PARENT','PEER_RESEARCH_QUEUED','research_executor.py','failure_memory.py','shared_learning.py','a2a_adapter.py','project-state.json','SELF_UPDATED','last_driver_diagnostic']:(ok if token in runtime else fail)('runtime owns '+token,checks)
    executor=(ROOT/'local/dore-local/research_executor.py').read_text(encoding='utf-8')
    for token in ['local_search','failure_memory','catalog_search','external_search','peer_escalate','provenance_preserved','reuse_before_rebuild','shared_learning','coordination_mailbox']:(ok if token in executor else fail)('research executor owns '+token,checks)
    acl=(ROOT/'local/dore-local/autonomous_capability_loop.py').read_text(encoding='utf-8')
    for token in ['GAP_DETECTED','RESEARCH_REQUIRED','retry_parent','failure_fingerprint']:(ok if token in acl else fail)('gap detector owns '+token,checks)
    project=json.loads((ROOT/'dore-design/knowledge-lab/a2a/project-state.json').read_text(encoding='utf-8'));relationship=project.get('active_relationship') or {};projects=relationship.get('projects') or []
    (ok if len(projects)==2 and 'A2A' in projects[0] and 'Storybook' in projects[1] else fail)('project relationship persists A2A <-> Storybook',checks)
    catalog=json.loads((ROOT/'dore-design/knowledge-lab/resources/source-catalog.json').read_text(encoding='utf-8'));ids={x.get('id') for x in catalog.get('sources') or []}
    for source in ['a2a-protocol','a2a-python','storybook','vite','langgraph','openhands']:(ok if source in ids else fail)('resource catalog contains '+source,checks)
    # A2A adapter is executable, not merely documented.
    cp=subprocess.run([sys.executable,str(ROOT/'local/dore-local/a2a_adapter.py')],cwd=str(ROOT),text=True,capture_output=True,timeout=30)
    try:a2a=json.loads((cp.stdout or '').strip().splitlines()[-1])
    except Exception:a2a={}
    (ok if cp.returncode==0 and a2a.get('ok') and (a2a.get('task') or {}).get('kind')=='task' else fail)('A2A adapter emits canonical task',checks)
    # Shared-learning gate must reject promotion without verification.
    code="import sys,json;sys.path.insert(0,'local/dore-local');from shared_learning import record;print(json.dumps(record({'knowledge_id':'x','sources':{},'provenance_preserved':True},status='PROMOTED')))"
    cp=subprocess.run([sys.executable,'-c',code],cwd=str(ROOT),text=True,capture_output=True,timeout=30)
    try:gate=json.loads((cp.stdout or '').strip().splitlines()[-1])
    except Exception:gate={}
    (ok if gate.get('ok') is False and gate.get('error')=='verification_required_before_promotion' else fail)('shared learning blocks unverified promotion',checks)
    # Executable self-research smoke test; no parent mutation.
    with tempfile.TemporaryDirectory(prefix='dore-loop-accept-') as td:
        research=Path(td)/'research.json';research.write_text(json.dumps({'schema':'dore.research-job.v0.2','research_id':'accept-storybook-gap','state':'RESEARCH_QUEUED','parent_message_id':'accept-parent','parent_goal':'A2A <-> Storybook acceptance','question':'Storybook Vite JSX parse error in stories file; search mature official resources','failure_fingerprint':'[storybook:inject-export-order-plugin] Parse error JSX .stories.js'}),encoding='utf-8')
        cp=subprocess.run([sys.executable,str(ROOT/'local/dore-local/research_executor.py'),str(research)],cwd=str(ROOT),text=True,capture_output=True,timeout=180);payload={}
        try:payload=json.loads((cp.stdout or '').strip().splitlines()[-1])
        except Exception:pass
        (ok if cp.returncode==0 and payload.get('state')=='KNOWLEDGE_RETURNED' and ((payload.get('knowledge_artifact') or {}).get('evidence_count') or 0)>0 else fail)('research executor discovers real evidence',checks)
    passed=all(x['pass'] for x in checks);print(json.dumps({'ok':passed,'schema':'dore.loop-contract-acceptance.v2','checks':checks,'passed':sum(1 for x in checks if x['pass']),'total':len(checks)},ensure_ascii=False));return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
