#!/usr/bin/env python3
"""Doré Design first-round real-work elimination coordinator.
Runs independent native trials; one provider failure never blocks the round.
OpenPencil's already-verified deterministic Bun failure is retained rather than retried.
"""
from __future__ import annotations
import json, subprocess, os
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
OUT=HOME/'evolution'/'design-bakeoff'
OUT.mkdir(parents=True,exist_ok=True)

BRIEF='Westside Watch homepage: structured editable design; create, render/visible, modify the same artifact, render/verify again.'

def run_script(script, timeout=900):
 p=ROOT/'local/dore-local'/script
 if not p.exists(): return {'ok':False,'terminal':True,'cause':'trial_runner_missing:'+script}
 try:
  cp=subprocess.run(['python3',str(p)],cwd=ROOT,text=True,capture_output=True,timeout=timeout)
  raw=(cp.stdout or '').strip().splitlines()
  data={}
  if raw:
   try:data=json.loads(raw[-1])
   except:data={'stdout':(cp.stdout or '')[-12000:]}
  data.setdefault('ok',cp.returncode==0)
  data['returncode']=cp.returncode
  if cp.stderr:data['stderr']=(cp.stderr or '')[-12000:]
  return data
 except subprocess.TimeoutExpired as e:
  return {'ok':False,'terminal':True,'cause':'timeout','timeout_seconds':timeout,'stdout':(e.stdout or '')[-6000:] if isinstance(e.stdout,str) else ''}
 except Exception as e:
  return {'ok':False,'terminal':True,'cause':type(e).__name__+': '+str(e)}

def classify(name,r):
 # A provider advances only with explicit real-work continuity evidence.
 create=bool(r.get('artifact') or r.get('artifact_path') or r.get('created') or r.get('structured_editable'))
 visible=bool(r.get('render') or r.get('render_path') or r.get('visual_verified') or r.get('visible'))
 second=bool(r.get('second_edit') or r.get('autonomous_second_edit') or r.get('second_edit_verified'))
 second_render=bool(r.get('second_render') or r.get('second_render_path') or r.get('second_visual_verified'))
 passed=bool(r.get('ok')) and create and visible and second and second_render
 cause=None if passed else (r.get('cause') or r.get('error') or ('real_work_gate_incomplete' if r.get('ok') else 'trial_failed'))
 return {'provider':name,'status':'PASS' if passed else 'FAIL','cause':cause,'gates':{'create':create,'visible_or_render':visible,'second_edit_same_artifact':second,'second_render_verify':second_render},'raw':r}

def main():
 results=[]
 results.append({'provider':'openpencil','status':'FAIL','cause':'verified deterministic runtime incompatibility: @open-pencil/cli HTML import invoked through Node/npx requires Bun global','gates':{'create':False,'visible_or_render':False,'second_edit_same_artifact':False,'second_render_verify':False},'learning':['capability probes do not equal real-work acceptance','test first actual mutation early','deterministic failures must terminate rather than retry blindly','runtime assumptions are part of equipment compatibility']})
 # Independent trial adapters. Missing adapter is itself a concrete capability gap and must not block later providers.
 for name,script in [('penpot','dore_design_penpot_trial.py'),('framesmith','dore_design_framesmith_trial.py'),('doop','dore_design_doop_trial.py'),('tela','dore_design_tela_trial.py')]:
  results.append(classify(name,run_script(script)))
 advancing=[x['provider'] for x in results if x['status']=='PASS']
 n=len(advancing)
 strategy='compose_and_fill_gap' if n==0 else ('adopt_and_thin_optimize' if n==1 else 'compare_then_optimize')
 report={'ok':True,'kind':'DORE_DESIGN_REAL_WORK_ELIMINATION','run_at':datetime.now(timezone.utc).isoformat(),'brief':BRIEF,'results':results,'pass_count':n,'advancing':advancing,'strategy':strategy,'round_complete':True,'human_terminal_required':False}
 path=OUT/('elimination-'+datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')+'.json')
 path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 report['evidence_path']=str(path)
 print(json.dumps(report,ensure_ascii=False))
 return 0
if __name__=='__main__': raise SystemExit(main())
