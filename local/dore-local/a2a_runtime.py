"""Local implementations for the DORÉ A2A capability contract."""
from __future__ import annotations
import json, os, subprocess, urllib.request
from pathlib import Path
from a2a_capabilities import Registry
ROOT=Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).expanduser().resolve()
LOCAL=ROOT/'local'/'dore-local'; DESIGN=ROOT/'dore-design'

def _run(argv,cwd=ROOT,timeout=300):
 cp=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout)
 return {'ok':cp.returncode==0,'returncode':cp.returncode,'stdout':(cp.stdout or '')[-20000:],'stderr':(cp.stderr or '')[-12000:]}
def _health(_):
 out={'ok':True,'repo':str(ROOT),'capability_protocol':'dore.a2a.v1'}
 try:
  with urllib.request.urlopen('http://127.0.0.1:4310/api/health',timeout=3) as r:out['design_resident']=json.loads(r.read().decode())
 except Exception as e:out['design_resident']={'ok':False,'error':type(e).__name__+': '+str(e)}
 return out
def _tests(_):
 tests=['test_design2_commands.py','test_a2a_protocol.py'];rows=[]
 for name in tests:
  p=DESIGN/name if (DESIGN/name).exists() else LOCAL/name
  if not p.exists():continue
  row=_run(['python3','-m','unittest',p.name],p.parent,180);row['test']=name;rows.append(row)
 return {'ok':bool(rows) and all(x['ok'] for x in rows),'results':rows}
def _stage2(_):
 rows=[]
 for name in ('test_design2_commands.py','local_acceptance.py'):
  p=DESIGN/name
  if p.exists():
   row=_run(['python3',p.name],DESIGN,300);row['check']=name;rows.append(row)
 health=_health({});return {'ok':bool(rows) and all(x['ok'] for x in rows) and bool((health.get('design_resident') or {}).get('ok')),'checks':rows,'health':health}
def _preview(_):return {'ok':True,'url':'http://127.0.0.1:4310/editor?page=multiwrite-home','health':_health({})}
def _update(_):
 p=LOCAL/'maintenance_update.py'
 if not p.exists():return {'ok':False,'error':'maintenance_update_unavailable'}
 return _run(['python3',str(p)],ROOT,300)
def build_registry():
 r=Registry();r.register('dore.health',_health);r.register('design2.tests',_tests);r.register('design2.stage2.acceptance',_stage2);r.register('design2.preview',_preview);r.register('resident.update',_update);return r
