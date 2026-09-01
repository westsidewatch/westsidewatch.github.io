#!/usr/bin/env python3
"""Static + executable anti-regression acceptance for the Doré autonomous loop."""
from __future__ import annotations
import json, os, py_compile, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
CONTRACT=ROOT/'dore-design'/'knowledge-lab'/'a2a'/'loop-contract-v1.json'

def fail(msg,checks):checks.append({'check':msg,'pass':False})
def ok(msg,checks):checks.append({'check':msg,'pass':True})
def main():
    checks=[]
    try:contract=json.loads(CONTRACT.read_text(encoding='utf-8'));ok('contract parses',checks)
    except Exception as e:print(json.dumps({'ok':False,'error':'contract_unreadable:'+repr(e)}));return 2
    required_paths=[]
    for _,value in (contract.get('components') or {}).items():
        if isinstance(value,str) and not value.startswith('dore-runtime-telemetry:') and ('/' in value):
            # Strip descriptive prefix only for exact repo-relative component values.
            candidate=value.split(' via ')[-1] if ' via ' in value else value
            if candidate.startswith(('local/','dore-design/')):required_paths.append(candidate)
    for rel in required_paths:
        (ok if (ROOT/rel).exists() else fail)('component exists: '+rel,checks)
    pyfiles=['local/dore-local/resident_runtime.py','local/dore-local/autonomous_driver.py','local/dore-local/autonomous_capability_loop.py','local/dore-local/research_executor.py','local/dore-local/coordination_mailbox.py','local/dore-local/coordination_worker.py']
    for rel in pyfiles:
        try:py_compile.compile(str(ROOT/rel),doraise=True);ok('python compiles: '+rel,checks)
        except Exception as e:fail('python compiles: '+rel+' :: '+repr(e),checks)
    runtime=(ROOT/'local/dore-local/resident_runtime.py').read_text(encoding='utf-8')
    for token in ['RESEARCH_QUEUED','RESEARCHING','KNOWLEDGE_RETURNED','EXPERIMENTING','VERIFIED','PROMOTED','RESUME_PARENT','PEER_RESEARCH_QUEUED','research_executor.py','SELF_UPDATED','last_driver_diagnostic']:
        (ok if token in runtime else fail)('runtime owns '+token,checks)
    executor=(ROOT/'local/dore-local/research_executor.py').read_text(encoding='utf-8')
    for token in ['local_search','catalog_search','external_search','peer_escalate','provenance_preserved','reuse_before_rebuild','coordination_mailbox']:
        (ok if token in executor else fail)('research executor owns '+token,checks)
    acl=(ROOT/'local/dore-local/autonomous_capability_loop.py').read_text(encoding='utf-8')
    for token in ['GAP_DETECTED','RESEARCH_REQUIRED','retry_parent','failure_fingerprint']:
        (ok if token in acl else fail)('gap detector owns '+token,checks)
    catalog=json.loads((ROOT/'dore-design/knowledge-lab/resources/source-catalog.json').read_text(encoding='utf-8'))
    ids={x.get('id') for x in catalog.get('sources') or []}
    for source in ['a2a-protocol','a2a-python','storybook','vite','langgraph','openhands']:
        (ok if source in ids else fail)('resource catalog contains '+source,checks)
    # Executable research smoke test: use a Storybook/Vite unknown-gap query and
    # require actual local/catalog discovery. No parent execution is performed.
    with tempfile.TemporaryDirectory(prefix='dore-loop-accept-') as td:
        research=Path(td)/'research.json'
        research.write_text(json.dumps({'schema':'dore.research-job.v0.2','research_id':'accept-storybook-gap','state':'RESEARCH_QUEUED','parent_message_id':'accept-parent','parent_goal':'A2A <-> Storybook acceptance','question':'Storybook Vite JSX parse error in stories file; search mature official resources','failure_fingerprint':'[storybook:inject-export-order-plugin] Parse error JSX .stories.js'}),encoding='utf-8')
        cp=subprocess.run([sys.executable,str(ROOT/'local/dore-local/research_executor.py'),str(research)],cwd=str(ROOT),text=True,capture_output=True,timeout=180)
        payload={}
        try:payload=json.loads((cp.stdout or '').strip().splitlines()[-1])
        except Exception:pass
        if cp.returncode==0 and payload.get('state')=='KNOWLEDGE_RETURNED' and ((payload.get('knowledge_artifact') or {}).get('evidence_count') or 0)>0:ok('research executor discovers real evidence',checks)
        else:fail('research executor discovers real evidence :: '+(cp.stderr or cp.stdout)[-1500:],checks)
    passed=all(x['pass'] for x in checks)
    print(json.dumps({'ok':passed,'schema':'dore.loop-contract-acceptance.v1','checks':checks,'passed':sum(1 for x in checks if x['pass']),'total':len(checks)},ensure_ascii=False))
    return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
