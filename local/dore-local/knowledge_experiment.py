#!/usr/bin/env python3
"""Run the minimal experiment carried by a verified-provenance Knowledge Artifact.

Research proposes; this runner only executes explicitly structured, allowlisted,
repo/local commands. Success is evidence, not automatic promotion.
"""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
ROOT=Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).expanduser().resolve();HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();ALLOWED={'python3','python','git','node','npm','npx','bash','sh','cat','ls','pwd','test','mkdir','touch','cp','mv','chmod','hugo'}
def safe_cwd(raw):
 p=Path(raw or ROOT).expanduser().resolve();roots=(ROOT,HOME,Path.home().resolve())
 if not any(p==r or r in p.parents for r in roots):raise ValueError('experiment_cwd_outside_allowed_roots')
 return p
def commands(artifact):
 exp=artifact.get('experiment')
 if isinstance(exp,dict) and isinstance(exp.get('commands'),list):return exp['commands']
 if isinstance(exp,dict) and isinstance(exp.get('argv'),list):return [exp]
 if isinstance(exp,list):return exp
 return []
def execute(payload):
 artifact=(payload or {}).get('knowledge_artifact') or payload or {}
 if artifact.get('schema')!='dore.knowledge-artifact.v1':return {'ok':False,'error':'knowledge_artifact_schema_required'}
 if not artifact.get('provenance_preserved'):return {'ok':False,'error':'provenance_required'}
 cmds=commands(artifact)
 if not cmds:return {'ok':False,'error':'structured_experiment_required','research_id':artifact.get('research_id')}
 results=[]
 for i,item in enumerate(cmds,1):
  if isinstance(item,list):argv=item;cwd=ROOT;timeout=120
  elif isinstance(item,dict):argv=item.get('argv') or [];cwd=safe_cwd(item.get('cwd'));timeout=min(int(item.get('timeout') or 120),900)
  else:return {'ok':False,'error':'invalid_experiment_command','index':i}
  if not argv or not all(isinstance(x,str) for x in argv):return {'ok':False,'error':'invalid_experiment_argv','index':i}
  if Path(argv[0]).name not in ALLOWED:return {'ok':False,'error':'experiment_executable_not_allowed','executable':Path(argv[0]).name}
  cp=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout);row={'index':i,'argv':argv,'cwd':str(cwd),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-10000:],'stderr':(cp.stderr or '')[-10000:]};results.append(row)
  if cp.returncode:return {'ok':False,'error':'experiment_command_failed','failed_index':i,'results':results,'information_gain':True}
 return {'ok':True,'research_id':artifact.get('research_id'),'knowledge_id':artifact.get('knowledge_id'),'results':results,'verified_signal':'structured experiment commands passed'}
if __name__=='__main__':
 try:out=execute(json.loads(sys.stdin.read() or '{}'))
 except Exception as e:out={'ok':False,'error':'experiment_uncaught:'+repr(e)}
 print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out.get('ok') else 2)
