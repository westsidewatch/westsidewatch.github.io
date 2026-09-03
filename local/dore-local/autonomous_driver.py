#!/usr/bin/env python3
"""Doré Autonomous Driver v0.5 — Storybook evidence-driven experiment driver.

A successful build is only the first gate. The driver now bootstraps the free OSS
Storybook/Vitest/Playwright stack when needed, runs browser component tests,
captures desktop/mobile visual evidence, and returns structured observations to
Agent Core. No paid API is used.
"""
from __future__ import annotations
import json, os, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser();CONTROL_ROOT=Path(os.environ.get('DORE_CONTROL_ROOT',ROOT)).expanduser();LOCAL=CONTROL_ROOT/'local'/'dore-local';LEARNING=HOME/'coordination'/'learning';EVIDENCE=ROOT/'dore-design'/'knowledge-lab'/'evidence';SKILLS=ROOT/'dore-design'/'knowledge-lab'/'skills';STORYBOOK=ROOT/'dore-design'/'knowledge-lab'/'storybook';MANUAL=CONTROL_ROOT/'dore-design'/'knowledge-lab'/'tools'/'research-bridge-v0.1.md';COMMON_BIN=['/opt/homebrew/bin','/usr/local/bin',str(Path.home()/'.nvm/current/bin')]
sys.path.insert(0,str(LOCAL))
VERSION='dore.autonomous-driver.v0.5'
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
  cp=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout,input=input_text);return {'argv':argv,'cwd':str(cwd),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-16000:],'stderr':(cp.stderr or '')[-12000:]}
 except Exception as e:return {'argv':argv,'cwd':str(cwd),'returncode':126,'stdout':'','stderr':repr(e),'capability_gap':'EXECUTION_ENVIRONMENT'}
def persist(mid,record):
 EVIDENCE.mkdir(parents=True,exist_ok=True);p=EVIDENCE/f'autonomous-driver-{mid}.json';p.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');return str(p)
def latest_learning(parent):
 p=LEARNING/f'{parent}.json'
 try:return json.loads(p.read_text(encoding='utf-8')) if p.exists() else None
 except Exception:return None
def queued_metadata(parent):
 try:
  from goal_queue import get
  row=get(parent) or {};return row.get('metadata') or {}
 except Exception:return {}
def find_story():
 c=list((STORYBOOK/'src'/'stories').glob('NewWestsideEditorialHero.stories.*'));return c[0] if c else None
def build():return run(['npm','run','build-storybook'],cwd=STORYBOOK,timeout=900)
def parse_last_json(text):
 for line in reversed((text or '').splitlines()):
  try:return json.loads(line)
  except Exception:pass
 return None
def ensure_evidence_stack(state):
 required=[STORYBOOK/'node_modules'/'@storybook'/'addon-vitest',STORYBOOK/'node_modules'/'@playwright'/'test',STORYBOOK/'node_modules'/'vitest']
 if all(p.exists() for p in required):return {'ok':True,'changed':False}
 state('RESEARCHING',sources=['Storybook official Vitest addon','Vitest browser mode','Playwright Chromium'],reason='free OSS browser evidence stack missing locally')
 install=run(['npm','install','--no-audit','--no-fund'],cwd=STORYBOOK,timeout=1200);state('EXPERIMENTING',experiment='install declared free OSS Storybook evidence dependencies',result=install)
 return {'ok':install['returncode']==0,'changed':True,'install':install}
def browser_missing(result):
 text=((result or {}).get('stderr','')+'\n'+(result or {}).get('stdout','')).lower();return any(x in text for x in ['executable doesn\'t exist','browser executable','playwright install','chromium is not found','failed to launch browser'])
def run_browser_evidence(state):
 stack=ensure_evidence_stack(state)
 if not stack.get('ok'):return {'ok':False,'stage':'dependency_install','detail':stack}
 tests=run(['npm','run','test-storybook'],cwd=STORYBOOK,timeout=1200)
 if tests['returncode']!=0 and browser_missing(tests):
  install_browser=run(['npx','playwright','install','chromium'],cwd=STORYBOOK,timeout=1200);state('EXPERIMENTING',experiment='install Playwright Chromium browser binary',result=install_browser)
  if install_browser['returncode']==0:tests=run(['npm','run','test-storybook'],cwd=STORYBOOK,timeout=1200)
 state('VERIFYING',gate='FUNCTION+A11Y browser tests',result=tests)
 if tests['returncode']!=0:return {'ok':False,'stage':'vitest_browser','tests':tests}
 visual=run(['npm','run','evidence-storybook'],cwd=STORYBOOK,timeout=1200)
 if visual['returncode']!=0 and browser_missing(visual):
  install_browser=run(['npx','playwright','install','chromium'],cwd=STORYBOOK,timeout=1200);state('EXPERIMENTING',experiment='repair missing Playwright Chromium for visual evidence',result=install_browser)
  if install_browser['returncode']==0:visual=run(['npm','run','evidence-storybook'],cwd=STORYBOOK,timeout=1200)
 parsed=parse_last_json(visual.get('stdout'));state('VERIFYING',gate='desktop/mobile visual evidence',result=visual,observation=parsed)
 return {'ok':visual['returncode']==0 and isinstance(parsed,dict) and bool(parsed.get('ok')),'stage':'visual_evidence','tests':tests,'visual':visual,'observation':parsed}
def promote_tool(tool,resolved):
 SKILLS.mkdir(parents=True,exist_ok=True);p=SKILLS/'resident-runtime-tool-resolution.md';p.write_text(f'# Resident runtime tool resolution\n\nTrigger: tool missing under launchd.\n\nRepair: PATH → common package-manager dirs → login-shell lookup.\n\nVerified tool: `{tool}` → `{resolved}`.\n',encoding='utf-8');return str(p)
def promote_jsx(before,after):
 SKILLS.mkdir(parents=True,exist_ok=True);p=SKILLS/'storybook-jsx-story-extension.md';p.write_text('# Storybook JSX story extension repair\n\nTrigger: parser failure in `.stories.js` containing JSX.\n\nRepair: test `.stories.jsx` before changing component logic.\n\nVerification: `npm run build-storybook` must pass.\n',encoding='utf-8');return str(p)
def promote_evidence(observation):
 SKILLS.mkdir(parents=True,exist_ok=True);p=SKILLS/'storybook-browser-evidence-loop.md';p.write_text('# Storybook browser evidence loop\n\nUse after a static build passes. Run Storybook Vitest browser tests, then Playwright desktop/mobile evidence capture. Treat build success as insufficient by itself. Preserve the six observation gates and use failed gates as the next research/experiment input.\n\nLast verified observation:\n```json\n'+json.dumps(observation or {},ensure_ascii=False,indent=2)+'\n```\n',encoding='utf-8');return str(p)
def summarize_artifact(a):
 sources=a.get('sources') or {};names=[]
 for group,items in sources.items():
  for x in (items or [])[:6]:names.append(str(x.get('id') or x.get('name') or x.get('path') or x.get('url') or group))
 return {'knowledge_id':a.get('knowledge_id'),'research_id':a.get('research_id'),'source_count':sum(len(v or []) for v in sources.values() if isinstance(v,list)),'sources':names[:12],'provenance_preserved':bool(a.get('provenance_preserved')),'lesson':a.get('lesson'),'hypothesis_status':a.get('hypothesis_status'),'has_structured_experiment':bool(a.get('experiment'))}
def run_coordination_goal(meta,knowledge_artifact,state):
 original=meta.get('message') if isinstance(meta,dict) else None
 if not isinstance(original,dict):return {'ok':False,'error':'preserved_coordination_message_missing','information_gain':True}
 if knowledge_artifact and knowledge_artifact.get('experiment'):
  state('EXPERIMENTING',experiment='knowledge-artifact structured experiment');exp=run(['python3',str(LOCAL/'knowledge_experiment.py')],cwd=ROOT,timeout=900,input_text=json.dumps({'knowledge_artifact':knowledge_artifact},ensure_ascii=False));state('VERIFYING',experiment_result=exp)
  if exp['returncode']!=0:return {'ok':False,'error':'knowledge_experiment_failed','experiment':exp,'information_gain':True}
 state('RESUME_PARENT',execution_kind='coordination_message',source_message_id=original.get('message_id'));cp=run(['python3',str(LOCAL/'coordination_goal_executor.py')],cwd=ROOT,timeout=1200,input_text=json.dumps({'message':original},ensure_ascii=False));parsed=parse_last_json(cp.get('stdout'))
 if cp['returncode']==0 and isinstance(parsed,dict) and parsed.get('ok'):state('VERIFIED',signal='preserved coordination goal passed after research detour');state('PASS');return {'ok':True,'coordination_goal':parsed,'resumed_parent_goal':True,'control_modified':False}
 state('RESEARCH_REQUIRED',reason='preserved coordination goal still fails after new research/experiment',information_gain={'executor':parsed,'stdout':cp.get('stdout'),'stderr':cp.get('stderr')});return {'ok':False,'error':'coordination_goal_requires_further_research','executor':parsed,'stdout':cp.get('stdout'),'stderr':cp.get('stderr'),'information_gain':True}
def finish_storybook_success(record,state,baseline,npm,extra_skills=None):
 state('VERIFYING',signal='baseline build passes; build alone is not acceptance');evidence=run_browser_evidence(state)
 if not evidence.get('ok'):
  state('RESEARCH_REQUIRED',reason='browser evidence gate failed after build PASS',information_gain=evidence);record['completed_at']=None;return {'ok':False,'driver':record,'error':'storybook_browser_evidence_failed','build':baseline,'browser_evidence':evidence,'information_gain':True}
 skills=list(extra_skills or [])+[promote_tool('npm',npm),promote_evidence(evidence.get('observation'))];state('VERIFIED',signal='build + real-browser tests + desktop/mobile evidence pass',observation=evidence.get('observation'));state('PROMOTED',skills=skills);state('RESUME_PARENT');state('PASS');record['completed_at']=now();return {'ok':True,'driver':record,'build':baseline,'browser_evidence':evidence,'promoted_skills':skills,'resumed_parent_goal':True,'control_modified':False}
def drive(msg):
 mid=str(msg.get('message_id') or 'autonomous-driver');task=msg.get('task') if isinstance(msg.get('task'),dict) else {};parent=str(task.get('parent_source_message_id') or 'new-westside-storybook-real-loop-2');goal=str(task.get('parent_goal') or msg.get('related_goal') or 'New Westside visual construction');knowledge_artifact=task.get('knowledge_artifact') if isinstance(task.get('knowledge_artifact'),dict) else None;meta=queued_metadata(parent)
 record={'driver':VERSION,'message_id':mid,'parent_message_id':parent,'parent_goal':goal,'project_loop':task.get('project_loop') or meta.get('project_loop') or 'A2A <-> Storybook','started_at':now(),'states':[],'parent_goal_preserved':True,'research_job':task.get('research_job'),'execution_kind':meta.get('execution_kind') or 'storybook','paid_api_used':False}
 def state(name,**extra):record['states'].append({'state':name,'at':now(),**extra});persist(mid,record)
 if not MANUAL.exists():state('HUMAN_GATE',reason='research_bridge_manual_missing');return {'ok':False,'driver':record,'error':'research_bridge_manual_missing'}
 state('GOAL',manual=str(MANUAL),trigger=task.get('trigger'),execution_kind=record['execution_kind']);research_context=None
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
 text=story.read_text(encoding='utf-8');jsx=bool(re.search(r'<[A-Za-z][^>]*>',text));state('PLAN',story=str(story),jsx=jsx,research_context=research_context);baseline=build();state('EXPERIMENTING',experiment='fresh Storybook static build',result=baseline,research_context=research_context)
 if baseline['returncode']==0:return finish_storybook_success(record,state,baseline,npm)
 combined=(baseline.get('stderr','')+'\n'+baseline.get('stdout','')).lower();parse_failure=any(x in combined for x in ['parse error','failed to parse','inject-export-order-plugin'])
 if story.suffix=='.js' and jsx and parse_failure:
  before=str(story);target=story.with_suffix('.jsx')
  if target.exists():target.unlink()
  story.rename(target);state('EXPERIMENTING',experiment='rename JSX story .js -> .jsx',changed_from=before,changed_to=str(target),basis={'fresh_build_parse_failure':True,'research_context':research_context});verified=build();state('VERIFYING',result=verified)
  if verified['returncode']==0:return finish_storybook_success(record,state,verified,npm,[promote_jsx(before,str(target))])
  state('RESEARCH_REQUIRED',reason='JSX extension experiment rejected',information_gain=(verified.get('stderr','')+'\n'+verified.get('stdout',''))[-5000:]);return {'ok':False,'driver':record,'error':'verified_experiment_failed','information_gain':True,'build':verified}
 state('RESEARCH_REQUIRED',reason='current hypothesis unsupported; research fresh build evidence',information_gain={'jsx':jsx,'parse_failure':parse_failure,'story':str(story),'npm':npm,'build_tail':combined[-5000:],'research_context':research_context});return {'ok':False,'driver':record,'error':'research_required_after_fresh_evidence','information_gain':True,'build':baseline}
if __name__=='__main__':
 try:out=drive(json.loads(sys.stdin.read() or '{}'))
 except Exception as e:out={'ok':False,'driver':VERSION,'error':'driver_uncaught_exception','detail':repr(e),'information_gain':True}
 print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out.get('ok') else 2)
