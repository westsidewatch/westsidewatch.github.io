#!/usr/bin/env python3
"""Doré Autonomous Driver v0.1.

Keeps a real parent goal moving without waiting for a human prompt.
Consumes RESEARCH_REQUIRED, inspects local evidence, runs small experiments,
records information-gain steps, promotes a verified lesson, and resumes the
New Westside × Storybook parent goal.
"""
from __future__ import annotations
import json, os, re, shutil, subprocess
from datetime import datetime, timezone
from pathlib import Path

HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
LEARNING=HOME/'coordination'/'learning'
EVIDENCE=ROOT/'dore-design'/'knowledge-lab'/'evidence'
SKILLS=ROOT/'dore-design'/'knowledge-lab'/'skills'
STORYBOOK=ROOT/'dore-design'/'knowledge-lab'/'storybook'
MANUAL=ROOT/'dore-design'/'knowledge-lab'/'tools'/'research-bridge-v0.1.md'

def now(): return datetime.now(timezone.utc).isoformat()

def run(argv,cwd=ROOT,timeout=300):
    cp=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout)
    return {'argv':argv,'cwd':str(cwd),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:]}

def persist(mid,record):
    EVIDENCE.mkdir(parents=True,exist_ok=True)
    p=EVIDENCE/f'autonomous-driver-{mid}.json'
    p.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    return str(p)

def _latest_learning(parent_id):
    p=LEARNING/f'{parent_id}.json'
    if p.exists():
        try:return json.loads(p.read_text(encoding='utf-8'))
        except Exception:return None
    return None

def _find_story():
    cands=list((STORYBOOK/'src'/'stories').glob('NewWestsideEditorialHero.stories.*'))
    return cands[0] if cands else None

def _build():
    return run(['npm','run','build-storybook'],cwd=STORYBOOK,timeout=900)

def _promote_jsx_extension_skill(source_before,source_after,build_result):
    SKILLS.mkdir(parents=True,exist_ok=True)
    p=SKILLS/'storybook-jsx-story-extension.md'
    text='''# Storybook JSX story extension repair\n\nTrigger: Storybook/Vite parse failure in a `.stories.js` file that contains JSX markup.\n\nDiagnosis: a JavaScript story containing JSX may be parsed as plain JS by tooling/plugins.\n\nReusable repair: rename the story to `.stories.jsx` (or otherwise configure the parser explicitly) before changing component logic.\n\nVerification: run `npm run build-storybook`; promote only if the static build passes.\n\nProvenance: local Storybook/Vite parser behavior observed in the New Westside real-work loop; compatible with the project package model.\n\nScope: only apply when JSX is present and the parse failure points at JSX syntax; do not use for unrelated syntax errors.\n'''
    p.write_text(text,encoding='utf-8')
    return str(p)

def drive(msg):
    mid=str(msg.get('message_id') or 'autonomous-driver')
    task=msg.get('task') if isinstance(msg.get('task'),dict) else {}
    parent=str(task.get('parent_source_message_id') or msg.get('parent_source_message_id') or 'new-westside-storybook-real-loop-2')
    goal=str(task.get('parent_goal') or msg.get('related_goal') or 'New Westside visual construction')
    record={'driver':'dore.autonomous-driver.v0.1','message_id':mid,'parent_message_id':parent,'parent_goal':goal,'started_at':now(),'states':[],'parent_goal_preserved':True}
    def state(name,**extra): record['states'].append({'state':name,'at':now(),**extra}); persist(mid,record)

    if not MANUAL.exists():
        state('HUMAN_GATE',reason='research_bridge_manual_missing')
        return {'ok':False,'driver':record,'error':'research_bridge_manual_missing'}
    manual=MANUAL.read_text(encoding='utf-8')
    state('GOAL',manual=str(MANUAL),manual_read='RESEARCH_REQUIRED' in manual and 'RESUME_PARENT' in manual)

    learning=_latest_learning(parent)
    if not learning or learning.get('state')!='RESEARCH_REQUIRED':
        state('GAP_DETECTED',note='No matching persisted RESEARCH_REQUIRED; reconstruct from real Storybook build evidence.')
    else:
        state('RESEARCH_QUEUED',failure_fingerprint=learning.get('failure_fingerprint','')[-2000:])

    story=_find_story()
    if not story:
        state('RESEARCHING',hypothesis='specimen may not exist; regenerate parent specimen')
        gen=ROOT/'dore-design'/'knowledge-lab'/'training'/'new_westside_storybook_real_loop.py'
        if not gen.exists(): return {'ok':False,'driver':record,'error':'parent_generator_missing'}
        exp=run(['python3',str(gen)],cwd=ROOT,timeout=900); state('EXPERIMENTING',experiment='regenerate specimen',result=exp)
        story=_find_story()
        if not story:return {'ok':False,'driver':record,'error':'specimen_not_generated'}

    text=story.read_text(encoding='utf-8')
    jsx=bool(re.search(r'<[A-Za-z][^>]*>',text))
    state('RESEARCHING',local_evidence=[str(story),str(STORYBOOK/'package.json')],hypothesis='JSX is present in a .stories.js file and Storybook parser is treating it as plain JavaScript' if story.suffix=='.js' and jsx else 'run build to obtain fresh parser evidence')

    baseline=_build(); state('EXPERIMENTING',experiment='fresh Storybook static build before repair',result=baseline)
    if baseline['returncode']==0:
        state('VERIFIED',signal='build already passes'); state('RESUME_PARENT'); state('PASS')
        record['completed_at']=now(); return {'ok':True,'driver':record,'build':baseline,'resumed_parent_goal':True}

    combined=(baseline.get('stderr','')+'\n'+baseline.get('stdout','')).lower()
    parse_failure='parse error' in combined or 'failed to parse' in combined or 'inject-export-order-plugin' in combined
    changed=False; old_path=str(story); new_path=old_path
    if story.suffix=='.js' and jsx and parse_failure:
        target=story.with_suffix('.jsx')
        if target.exists(): target.unlink()
        story.rename(target); story=target; changed=True; new_path=str(target)
        state('KNOWLEDGE_RETURNED',lesson='Treat JSX Storybook stories as JSX source; test extension/parser mismatch before editing component logic.',provenance=['local generated story','Storybook build parser evidence'])
        state('EXPERIMENTING',experiment='rename .stories.js to .stories.jsx without changing story logic',changed_from=old_path,changed_to=new_path)
        verified=_build()
    else:
        state('REJECTED',reason='first hypothesis not supported by evidence',information_gain={'jsx_detected':jsx,'parse_failure':parse_failure,'story':str(story)})
        return {'ok':False,'driver':record,'error':'research_required_after_first_hypothesis','build':baseline}

    state('VERIFYING',result=verified)
    if verified['returncode']!=0:
        state('REJECTED',reason='extension hypothesis failed verification',information_gain=(verified.get('stderr','')+'\n'+verified.get('stdout',''))[-4000:])
        return {'ok':False,'driver':record,'error':'verified_experiment_failed','build':verified}

    skill=_promote_jsx_extension_skill(old_path,new_path,verified); state('PROMOTED',skill=skill,scope='Storybook JSX extension/parser mismatch only')
    state('RESUME_PARENT',deliverable=str(story)); state('PASS')
    record['completed_at']=now(); record['control_modified']=False
    path=persist(mid,record)
    return {'ok':True,'driver':record,'evidence_path':path,'build':verified,'specimen':str(story),'promoted_skill':skill,'resumed_parent_goal':True,'control_modified':False}

if __name__=='__main__':
    import sys
    msg=json.loads(sys.stdin.read() or '{}')
    out=drive(msg); print(json.dumps(out,ensure_ascii=False)); raise SystemExit(0 if out.get('ok') else 2)
