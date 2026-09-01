#!/usr/bin/env python3
"""Doré Autonomous Driver v0.4 — goal-aware experiment driver.

Storybook remains the active real-work laboratory, but queued coordination goals
also preserve their exact original message. Returned Knowledge Artifacts are
consumed before a resumed experiment; a failed experiment yields fresh evidence
instead of an identical retry.
"""
from __future__ import annotations
import json, os, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser();LOCAL=ROOT/'local'/'dore-local';LEARNING=HOME/'coordination'/'learning';EVIDENCE=ROOT/'dore-design'/'knowledge-lab'/'evidence';SKILLS=ROOT/'dore-design'/'knowledge-lab'/'skills';STORYBOOK=ROOT/'dore-design'/'knowledge-lab'/'storybook';MANUAL=ROOT/'dore-design'/'knowledge-lab'/'tools'/'research-bridge-v0.1.md';COMMON_BIN=['/opt/homebrew/bin','/usr/local/bin',str(Path.home()/'.nvm/current/bin')]
sys.path.insert(0,str(LOCAL))
def now():return datetime.now(timezone.utc).isoformat()
def resolve_tool(name):
 if '/' in name:return name if Path(name).exists() else None
 found=shutil.which(name)
 if found:return found
 for d in COMMON_BIN:
  p=Path(d)/name
  if p.exists() and os.access(p,os.X_OK):return str(p)
 try:
  cp=subprocess.run(['/bin/zsh','-lc',f'command -v {name}'],text=True,capture_output=True,timeout=20);lines=(cp.stdout or '').strip().splitlines()
  if cp.returncode==0 and lines and Path(lines[-1]).exists():return lines[-1]
 except Exception:pass
 return None
def run(argv,cwd=ROOT,timeout=300,input_text=None):
 argv=list(argv);resolved=resolve_tool(argv[0])
 if not resolved:return {'argv':argv,'cwd':str(cwd),'returncode':127,'stdout':'','stderr':'tool_not_found:'+argv[0],'capability_gap':'TOOL_RESOLUTION'}
 argv[0]=resolved
 try:
  cp=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout,input=input_text);return {'argv':argv,'cwd':str(cwd),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:]}
 except Exception as e:return {'argv':argv,'cwd':str(cwd),'returncode':126,'stdout':'','stderr':repr(e),'capability_gap':'EXECUTION_ENVIRONMENT'}
def persist(mid,record):
 EVIDENCE.mkdir(parents=True,exist_ok=True);p=EVIDENCE/f'autonomous-driver-{mid}.json';p.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');return str(p)
def latest_learning(parent):
 p=LEARNING/f'{parent}.json'
 try:return json.loads(p.read_text(encoding='utf-8')) if p.exists() else None
 except Exception:return None
def queued_metadata(parent):
 try:
  from goal_queue import current
  row=current() or {}
  return (row.get('metadata') or {}) if str(row.get('goal_id'))==str(parent) else {}
 except Exception:return {}
def find_story():
 c=list((STORYBOOK/'src'/'stories').glob('NewWestsideEditorialHero.stories.*'));return c[0] if c else None
def build():return run(['npm','run','build-storybook'],cwd=STORYBOOK,timeout=900)
def promote_tool(tool,resolved):
 SKILLS.mkdir(parents=True,exist_ok=True);p=SKILLS/'resident-runtime-tool-resolution.md';p.write_text(f'# Resident runtime tool resolution\n\nTrigger: tool missing under launchd.\n\nRepair: PATH → common package-manager dirs → login-shell lookup.\n\nVerified tool: `{tool}` → `{resolved}`.\n',encoding='utf-8');return str(p)
def promote_jsx(before,after):
 SKILLS.mkdir(parents=True,exist_ok=True);p=SKILLS/'storybook-jsx-story-extension.md';p.write_text('# Storybook JSX story extension repair\n\nTrigger: parser failure in `.stories.js` containing JSX.\n\nRepair: test `.stories.jsx` before changing component logic.\n\nVerification: `npm run build-storybook` must pass.\n',encoding='utf-8');return str(p)
def summarize_artifact(a):
 sources=a.get('sources') or {};names=[]
 for group,items in sources.items():
  for x in (items or [])[:6]:names.append(str(x.get('id') or x.get('name') or x.get('path') or x.get('url') or group))
 return {'knowledge_id':a.get('knowledge_id'),'research_id':a.get('research_id'),'source_count':sum(len(v or []) for v in sources.values() if isinstance(v,list)),'sources':names[:12],'provenance_preserved':bool(a.get('provenance_preserved')),'lesson':a.get('lesson'),'hypothesis_status':a.get('hypothesis_status'),'has_structured_experiment':bool(a.get('experiment'))}
def run_coordination_goal(meta,knowledge_artifact,state):
 original=meta.get('message') if isinstance(meta,dict) else None
 if not isinstance(original,dict):return {'ok':False,'error':'preserved_coordination_message_missing','information_gain':True}
 if knowledge_artifact and knowledge_artifact.get('experiment'):
  state('EXPERIMENTING',experiment='knowledge-artifact structured experiment')
  exp=run(['python3',str(LOCAL/'knowledge_experiment.py')],cwd=ROOT,timeout=900,input_text=json.dumps({'knowledge_artifact':knowledge_artifact},ensure_ascii=False));state('VERIFYING',experiment_result=exp)
  if exp['returncode']!=0:return {'ok':False,'error':'knowledge_experiment_failed','experiment':exp,'information_gain':True}
 state('RESUME_PARENT',execution_kind='coordination_message',source_message_id=original.get('message_id'))
 cp=run(['python3',str(LOCAL/'coordination_goal_executor.py')],cwd=ROOT,timeout=1200,input_text=json.dumps({'message':original},ensure_ascii=False));parsed=None
 try:parsed=json.loads((cp.get('stdout') or '').strip().splitlines()[-1])
 except Exception:pass
 if cp['returncode']==0 and isinstance(parsed,dict) and parsed.get('ok'):
  state('VERIFIED',signal='preserved coordination goal passed after research detour');state('PASS');return {'ok':True,'coordination_goal':parsed,'resumed_parent_goal':True,'control_modified':False}
 state('RESEARCH_REQUIRED',reason='preserved coordination goal still fails after new research/experiment',information_gain={'executor':parsed,'stdout':cp.get('stdout'),'stderr':cp.get('stderr')});return {'ok':False,'error':'coordination_goal_requires_further_research','executor':parsed,'stdout':cp.get('stdout'),'stderr':cp.get('stderr'),'information_gain':True}
def drive(msg):
 mid=str(msg.get('message_id') or 'autonomous-driver');task=msg.get('task') if isinstance(msg.get('task'),dict) else {};parent=str(task.get('parent_source_message_id') or 'new-westside-storybook-real-loop-2');goal=str(task.get('parent_goal') or msg.get('related_goal') or 'New Westside visual construction');knowledge_artifact=task.get('knowledge_artifact') if isinstance(task.get('knowledge_artifact'),dict) else None;meta=queued_metadata(parent)
 record={'driver':'dore.autonomous-driver.v0.4','message_id':mid,'parent_message_id':parent,'parent_goal':goal,'project_loop':task.get('project_loop') or meta.get('project_loop') or 'A2A <-> Storybook','started_at':now(),'states':[],'parent_goal_preserved':True,'research_job':task.get('research_job'),'execution_kind':meta.get('execution_kind') or 'storybook'}
 def state(name,**extra):record['states'].append({'state':name,'at':now(),**extra});persist(mid,record)
 if not MANUAL.exists():state('HUMAN_GATE',reason='research_bridge_manual_missing');return {'ok':False,'driver':record,'error':'research_bridge_manual_missing'}
 state('GOAL',manual=str(MANUAL),trigger=task.get('trigger'),execution_kind=record['execution_kind'])
 research_context=None
 if knowledge_artifact:
  research_context=summarize_artifact(knowledge_artifact);state('KNOWLEDGE_RETURNED',research_context=research_context)
  if not research_context.get('provenance_preserved'):state('RESEARCH_REQUIRED',reason='returned knowledge lacks provenance');return {'ok':False,'driver':record,'error':'knowledge_provenance_required','information_gain':True}
 learning=latest_learning(parent)
 if not knowledge_artifact and learning and learning.get('state')=='RESEARCH_REQUIRED':state('RESEARCH_QUEUED',failure_fingerprint=str(learning.get('failure_fingerprint',''))[-2000:])
 if meta.get('execution_kind')=='coordination_message':
  outcome=run_coordination_goal(meta,knowledge_artifact,state);record['completed_at']=now() if outcome.get('ok') else None;outcome['driver']=record;return outcome
 npm=resolve_tool('npm')
 if not npm:
  state('GAP_DETECTED',layer='tool/environment',gap='npm not visible to resident runtime');state('RESEARCHING',sources=['PATH','Homebrew/local bin','login shell']);probe=run(['npm','--version']);state('EXPERIMENTING',experiment='resolve npm',result=probe)
  if probe['returncode']!=0:state('RESEARCH_REQUIRED',information_gain=probe);return {'ok':False,'driver':record,'error':'npm_unresolved','information_gain':True}
  npm=probe['argv'][0]
 state('CAPABILITY_AVAILABLE',tool='npm',resolved=npm)
 story=find_story()
 if not story:
  gen=ROOT/'dore-design'/'knowledge-lab'/'training'/'new_westside_storybook_real_loop.py';state('EXPERIMENTING',experiment='regenerate missing specimen',research_context=research_context);exp=run(['python3',str(gen)],cwd=ROOT,timeout=900) if gen.exists() else {'returncode':127,'stderr':'generator_missing'};story=find_story()
  if not story:return {'ok':False,'driver':record,'error':'specimen_not_generated','experiment':exp,'information_gain':True}
 text=story.read_text(encoding='utf-8');jsx=bool(re.search(r'<[A-Za-z][^>]*>',text));state('PLAN',story=str(story),jsx=jsx,research_context=research_context)
 baseline=build();state('EXPERIMENTING',experiment='fresh Storybook static build',result=baseline,research_context=research_context)
 if baseline['returncode']==0:
  skill=promote_tool('npm',npm);state('VERIFYING',signal='baseline build passes');state('VERIFIED');state('PROMOTED',skills=[skill]);state('RESUME_PARENT');state('PASS');record['completed_at']=now();return {'ok':True,'driver':record,'build':baseline,'promoted_skills':[skill],'resumed_parent_goal':True,'control_modified':False}
 combined=(baseline.get('stderr','')+'\n'+baseline.get('stdout','')).lower();parse_failure=any(x in combined for x in ['parse error','failed to parse','inject-export-order-plugin'])
 if story.suffix=='.js' and jsx and parse_failure:
  before=str(story);target=story.with_suffix('.jsx')
  if target.exists():target.unlink()
  story.rename(target);state('EXPERIMENTING',experiment='rename JSX story .js -> .jsx',changed_from=before,changed_to=str(target),basis={'fresh_build_parse_failure':True,'research_context':research_context});verified=build();state('VERIFYING',result=verified)
  if verified['returncode']==0:
   skills=[promote_jsx(before,str(target)),promote_tool('npm',npm)];state('VERIFIED');state('PROMOTED',skills=skills);state('RESUME_PARENT',deliverable=str(target));state('PASS');record['completed_at']=now();record['control_modified']=False;path=persist(mid,record);return {'ok':True,'driver':record,'evidence_path':path,'build':verified,'specimen':str(target),'promoted_skills':skills,'resumed_parent_goal':True,'control_modified':False}
  state('RESEARCH_REQUIRED',reason='JSX extension experiment rejected',information_gain=(verified.get('stderr','')+'\n'+verified.get('stdout',''))[-5000:]);return {'ok':False,'driver':record,'error':'verified_experiment_failed','information_gain':True,'build':verified}
 state('RESEARCH_REQUIRED',reason='current hypothesis unsupported; research fresh build evidence',information_gain={'jsx':jsx,'parse_failure':parse_failure,'story':str(story),'npm':npm,'build_tail':combined[-5000:],'research_context':research_context});return {'ok':False,'driver':record,'error':'research_required_after_fresh_evidence','information_gain':True,'build':baseline}
if __name__=='__main__':
 try:out=drive(json.loads(sys.stdin.read() or '{}'))
 except Exception as e:out={'ok':False,'driver':'dore.autonomous-driver.v0.4','error':'driver_uncaught_exception','detail':repr(e),'information_gain':True}
 print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out.get('ok') else 2)
