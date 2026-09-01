#!/usr/bin/env python3
"""Doré Autonomous Driver v0.2.

Keeps a real parent goal moving without waiting for a human prompt.
A2A ↔ Storybook is the current real-work learning loop: Storybook exposes
capability gaps; the driver diagnoses/repairs them, verifies the repair,
promotes reusable knowledge, and resumes the parent product goal.
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
COMMON_BIN=['/opt/homebrew/bin','/usr/local/bin',str(Path.home()/'.nvm/current/bin')]

def now(): return datetime.now(timezone.utc).isoformat()

def resolve_tool(name):
    """Recover tools hidden by launchd's intentionally small PATH.

    This is a generic capability repair, not an npm special case: first use the
    current PATH, then known user package-manager locations, then ask the user's
    login shell for the executable. A missing tool becomes structured evidence
    instead of crashing the driver.
    """
    if '/' in name:
        return name if Path(name).exists() else None
    found=shutil.which(name)
    if found:return found
    for d in COMMON_BIN:
        p=Path(d)/name
        if p.exists() and os.access(p,os.X_OK):return str(p)
    try:
        cp=subprocess.run(['/bin/zsh','-lc',f'command -v {name}'],text=True,capture_output=True,timeout=20)
        p=(cp.stdout or '').strip().splitlines()
        if cp.returncode==0 and p and Path(p[-1]).exists():return p[-1]
    except Exception:
        pass
    return None

def run(argv,cwd=ROOT,timeout=300):
    argv=list(argv)
    resolved=resolve_tool(argv[0])
    if not resolved:
        return {'argv':argv,'cwd':str(cwd),'returncode':127,'stdout':'','stderr':f'tool_not_found:{argv[0]}','capability_gap':'TOOL_RESOLUTION'}
    argv[0]=resolved
    try:
        cp=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout)
        return {'argv':argv,'cwd':str(cwd),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:]}
    except Exception as exc:
        return {'argv':argv,'cwd':str(cwd),'returncode':126,'stdout':'','stderr':repr(exc),'capability_gap':'EXECUTION_ENVIRONMENT'}

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

def _promote_tool_resolution_skill(tool,resolved):
    SKILLS.mkdir(parents=True,exist_ok=True)
    p=SKILLS/'resident-runtime-tool-resolution.md'
    p.write_text(f'''# Resident runtime tool resolution\n\nTrigger: a tool works interactively but is missing when Doré runs under macOS launchd.\n\nDiagnosis: launchd normally supplies a minimal PATH, so user-installed tools such as Node/npm may not be discoverable.\n\nRepair order: current PATH → common package-manager locations → `/bin/zsh -lc "command -v <tool>"`.\n\nVerification: resolve the executable and rerun the original real-work command.\n\nObserved tool: `{tool}` → `{resolved}`.\n\nScope: environment/tool discovery only; do not treat a real program failure as a PATH problem.\n''',encoding='utf-8')
    return str(p)

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
    record={'driver':'dore.autonomous-driver.v0.2','message_id':mid,'parent_message_id':parent,'parent_goal':goal,'started_at':now(),'states':[],'parent_goal_preserved':True}
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

    # Environment capability probe. This is deliberately generic because the
    # resident runtime must be able to recover tools without a human shell.
    npm=resolve_tool('npm')
    if not npm:
        state('GAP_DETECTED',layer='tool/environment',gap='npm not visible to resident launchd process')
        state('RESEARCHING',sources=['current PATH','Homebrew/local bin conventions','user login-shell command lookup'])
        probe=run(['npm','--version'])
        state('EXPERIMENTING',experiment='resolve npm outside launchd PATH',result=probe)
        if probe['returncode']!=0:
            state('RESEARCH_REQUIRED',reason='tool resolution strategies exhausted',information_gain=probe)
            return {'ok':False,'driver':record,'error':'npm_unresolved','information_gain':True}
        npm=probe['argv'][0]
    state('CAPABILITY_AVAILABLE',tool='npm',resolved=npm)

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
        skill=_promote_tool_resolution_skill('npm',npm)
        state('PROMOTED',skill=skill,scope='resident tool discovery')
        state('VERIFIED',signal='Storybook build passes in resident runtime'); state('RESUME_PARENT'); state('PASS')
        record['completed_at']=now(); return {'ok':True,'driver':record,'build':baseline,'resumed_parent_goal':True}

    combined=(baseline.get('stderr','')+'\n'+baseline.get('stdout','')).lower()
    parse_failure='parse error' in combined or 'failed to parse' in combined or 'inject-export-order-plugin' in combined
    old_path=str(story); new_path=old_path
    if story.suffix=='.js' and jsx and parse_failure:
        target=story.with_suffix('.jsx')
        if target.exists(): target.unlink()
        story.rename(target); story=target; new_path=str(target)
        state('KNOWLEDGE_RETURNED',lesson='Treat JSX Storybook stories as JSX source; test extension/parser mismatch before editing component logic.',provenance=['local generated story','Storybook build parser evidence'])
        state('EXPERIMENTING',experiment='rename .stories.js to .stories.jsx without changing story logic',changed_from=old_path,changed_to=new_path)
        verified=_build()
    else:
        # Do not blind-retry. Persist fresh failure evidence for the next research
        # hypothesis, including the exact tool path and build output.
        state('RESEARCH_REQUIRED',reason='extension hypothesis not supported; next hypothesis must use fresh build evidence',information_gain={'jsx_detected':jsx,'parse_failure':parse_failure,'story':str(story),'npm':npm,'build_tail':combined[-5000:]})
        return {'ok':False,'driver':record,'error':'research_required_after_fresh_evidence','information_gain':True,'build':baseline}

    state('VERIFYING',result=verified)
    if verified['returncode']!=0:
        state('RESEARCH_REQUIRED',reason='extension hypothesis failed; preserve new build evidence for a different hypothesis',information_gain=(verified.get('stderr','')+'\n'+verified.get('stdout',''))[-5000:])
        return {'ok':False,'driver':record,'error':'verified_experiment_failed','information_gain':True,'build':verified}

    skills=[_promote_jsx_extension_skill(old_path,new_path,verified),_promote_tool_resolution_skill('npm',npm)]
    state('PROMOTED',skills=skills,scope='verified Storybook repair + resident tool discovery')
    state('RESUME_PARENT',deliverable=str(story)); state('PASS')
    record['completed_at']=now(); record['control_modified']=False
    path=persist(mid,record)
    return {'ok':True,'driver':record,'evidence_path':path,'build':verified,'specimen':str(story),'promoted_skills':skills,'resumed_parent_goal':True,'control_modified':False}

if __name__=='__main__':
    import sys
    try:
        msg=json.loads(sys.stdin.read() or '{}')
        out=drive(msg)
    except Exception as exc:
        out={'ok':False,'driver':'dore.autonomous-driver.v0.2','error':'driver_uncaught_exception','detail':repr(exc),'information_gain':True}
    print(json.dumps(out,ensure_ascii=False)); raise SystemExit(0 if out.get('ok') else 2)
