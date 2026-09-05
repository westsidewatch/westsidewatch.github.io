#!/usr/bin/env python3
"""Doré Autonomous Capability Loop v0.2.

Core recovery rule:
BLOCKED -> RESEARCH -> COMPARE -> ADOPT -> VERIFY -> RESUME PARENT GOAL.

Research is part of the parent task, never a terminal substitute for it. New
infrastructure capabilities should also be researched before being rebuilt.
"""
from __future__ import annotations
import json, os, re, subprocess
from datetime import datetime, timezone
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
STATE_DIR=HOME/'coordination'/'learning'; REGISTRY=ROOT/'dore-design'/'knowledge-lab'/'skills'/'registry.json'
RESEARCH_TRIGGERS=('blocked','forbidden','unsupported','not implemented','unknown capability','permission denied','safety','architecture','transport','protocol','connector','mcp')
def now():return datetime.now(timezone.utc).isoformat()
def _text_failure(result):
 parts=[]
 for key in ('error','cause','failed_stderr','failed_stdout','stderr','stdout'):
  if result.get(key):parts.append(str(result[key]))
 for item in result.get('results') or []:
  if isinstance(item,dict):parts.extend(str(item.get(k) or '') for k in ('stderr','stdout'))
 return '\n'.join(parts)
def _load_registry():
 try:return json.loads(REGISTRY.read_text(encoding='utf-8')).get('skills') or []
 except Exception:return []
def _match(skill,text):
 triggers=skill.get('triggers') or [];low=text.lower();return bool(triggers) and all(str(t).lower() in low for t in triggers)
def _safe_script(path):
 target=(ROOT/path).resolve();allowed=(ROOT/'dore-design'/'knowledge-lab'/'training').resolve()
 if not(target==allowed or allowed in target.parents):raise RuntimeError('learning_script_outside_training_root:'+str(target))
 if target.suffix!='.py' or not target.exists():raise RuntimeError('learning_script_unavailable:'+str(target))
 return target
def _persist(mid,record):
 STATE_DIR.mkdir(parents=True,exist_ok=True);path=STATE_DIR/f'{mid}.json';tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(path);return path
def research_required(failure_text, *, new_infrastructure=False):
 low=failure_text.lower()
 return new_infrastructure or any(x in low for x in RESEARCH_TRIGGERS)
def research_brief(failure_text,parent_goal):
 return {'question':'Research mature official implementations, maintained open-source projects, and relevant technical research for this capability gap. Compare architecture, license, security, maintenance, and integration cost; prefer adoption/integration over rebuilding; verify the chosen approach; then resume the preserved parent goal.','parent_goal':parent_goal,'failure':re.sub(r'\s+',' ',failure_text)[-4000:],'source_priority':['official implementation','mature maintained open source','technical research','proven production pattern'],'compare':['fit','license','security','maintenance','integration cost'],'reuse_before_rebuild':True,'must_resume_parent_goal':True}
def attempt_learning_recovery(msg,failure_result):
 mid=str(msg.get('message_id') or 'unknown');parent_goal=str(msg.get('related_goal') or mid);failure_text=_text_failure(failure_result)
 base={'loop':'dore.autonomous-capability-loop.v0.2','policy':'BLOCKED_RESEARCH_ADOPT_VERIFY_RESUME','message_id':mid,'parent_goal':parent_goal,'observed_at':now(),'state':'GAP_DETECTED','parent_goal_preserved':True,'failure_fingerprint':re.sub(r'\s+',' ',failure_text)[-4000:]}
 skill=next((s for s in _load_registry() if _match(s,failure_text)),None)
 if not skill:
  record={**base,'state':'RESEARCH_REQUIRED','retry_parent':False,'knowledge_request':research_brief(failure_text,parent_goal)};path=_persist(mid,record);return {**record,'evidence_path':str(path)}
 record={**base,'state':'LEARNING','selected_skill':skill.get('id'),'provenance':skill.get('provenance') or []};_persist(mid,record)
 try:
  script=_safe_script(str(skill['script']));cp=subprocess.run(['python3',str(script)],cwd=str(ROOT),text=True,capture_output=True,timeout=min(int(skill.get('timeout') or 180),900));verified=cp.returncode==0
  record.update({'state':'VERIFIED' if verified else 'LEARNING_FAILED','retry_parent':verified,'skill_returncode':cp.returncode,'skill_stdout':(cp.stdout or '')[-12000:],'skill_stderr':(cp.stderr or '')[-12000:],'verified_at':now() if verified else None})
 except Exception as exc:record.update({'state':'LEARNING_FAILED','retry_parent':False,'error':type(exc).__name__+': '+str(exc)})
 path=_persist(mid,record);return {**record,'evidence_path':str(path)}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--message-id',default='acl-self-test');p.add_argument('--failure',required=True);a=p.parse_args();out=attempt_learning_recovery({'message_id':a.message_id,'related_goal':'dore-autonomous-loop-self-test'},{'ok':False,'error':a.failure});print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out.get('retry_parent') else 2)
