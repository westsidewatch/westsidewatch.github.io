#!/usr/bin/env python3
"""Doré Resident Runtime v0.5.

Executable invariant:
GAP/RESEARCH_REQUIRED -> RESEARCH_QUEUED -> RESEARCHING -> KNOWLEDGE_RETURNED
-> EXPERIMENTING -> VERIFIED/REJECTED -> PROMOTED -> RESUME_PARENT.
No unchanged failure may be retried without new evidence. Unknown technical
knowledge is never a HUMAN_GATE by default.
"""
from __future__ import annotations
import fcntl, hashlib, json, os, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
VERSION='dore.resident-runtime.v0.5'
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
RUNTIME=HOME/'runtime';LEARNING=HOME/'coordination'/'learning';RESEARCH=HOME/'coordination'/'research';LOCAL=ROOT/'local'/'dore-local';A2A_DIR=ROOT/'dore-design'/'knowledge-lab'/'a2a'
DRIVER=LOCAL/'autonomous_driver.py';RESEARCH_EXECUTOR=LOCAL/'research_executor.py';SELF=LOCAL/'resident_runtime.py';PROJECT_STATE=A2A_DIR/'project-state.json'
STATE=RUNTIME/'state.json';EVENTS=RUNTIME/'events.jsonl';HEARTBEAT=RUNTIME/'heartbeat.json';LOCK=RUNTIME/'runtime.lock';TELEMETRY_REPO=RUNTIME/'telemetry-repo';TELEMETRY_BRANCH=os.environ.get('DORE_RUNTIME_TELEMETRY_BRANCH','dore-runtime-telemetry')
TELEMETRY_INTERVAL=max(60,int(os.environ.get('DORE_RUNTIME_TELEMETRY_SECONDS','120')));SELF_UPDATE_INTERVAL=max(120,int(os.environ.get('DORE_RUNTIME_SELF_UPDATE_SECONDS','300')));INTERVAL=max(10,int(os.environ.get('DORE_RUNTIME_INTERVAL_SECONDS','30')))
try:_ps=json.loads(PROJECT_STATE.read_text(encoding='utf-8')).get('active_relationship') or {}
except Exception:_ps={}
PARENT_ID=os.environ.get('DORE_RUNTIME_PARENT_ID',str(_ps.get('current_parent_message_id') or 'new-westside-storybook-real-loop-2'));PARENT_GOAL=os.environ.get('DORE_RUNTIME_PARENT_GOAL',str(_ps.get('parent_product_goal') or 'New Westside visual construction'));PROJECT_LOOP=str(_ps.get('loop') or 'A2A <-> Storybook')
sys.path.insert(0,str(LOCAL))

def now():return datetime.now(timezone.utc).isoformat()
def run(argv,cwd=ROOT,timeout=120):return subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout)
def read_json(path,default=None):
    try:return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception:return default
def atomic_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(path)
def append_event(kind,**data):
    RUNTIME.mkdir(parents=True,exist_ok=True)
    with EVENTS.open('a',encoding='utf-8') as f:f.write(json.dumps({'at':now(),'event':kind,**data},ensure_ascii=False)+'\n')
def fingerprint(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,default=str).encode()).hexdigest()
def tail_events(limit=40):
    if not EVENTS.exists():return []
    out=[]
    for line in EVENTS.read_text(encoding='utf-8',errors='replace').splitlines()[-limit:]:
        try:out.append(json.loads(line))
        except Exception:out.append({'event':'UNPARSEABLE_EVENT','raw':line[-1000:]})
    return out
def latest_learning():
    direct=LEARNING/f'{PARENT_ID}.json'
    if direct.exists():
        data=read_json(direct)
        if isinstance(data,dict):return direct,data
    if LEARNING.exists():
        for p in sorted(LEARNING.glob('*.json'),key=lambda x:x.stat().st_mtime,reverse=True):
            data=read_json(p)
            if isinstance(data,dict) and data.get('state')=='RESEARCH_REQUIRED':return p,data
    return None,None
def research_id_for(learning):
    fp=(learning or {}).get('failure_fingerprint') or fingerprint(learning or {'parent':PARENT_ID});return f'research-{PARENT_ID}-{fingerprint(fp)[:16]}'
def transition(job_path,job,state,**extra):
    history=list(job.get('history') or []);history.append({'at':now(),'state':state,**{k:v for k,v in extra.items() if k in {'reason','evidence'}}});job={**job,'state':state,'updated_at':now(),'history':history,**extra};atomic_json(job_path,job);append_event(state,research_id=job.get('research_id'),parent_goal=PARENT_GOAL);return job
def ensure_research_job(learning_path,learning):
    RESEARCH.mkdir(parents=True,exist_ok=True);rid=research_id_for(learning);p=RESEARCH/f'{rid}.json';existing=read_json(p,{}) or {}
    if existing:return p,existing
    question=((learning or {}).get('knowledge_request') or {}).get('question') or (learning or {}).get('question') or 'Find a mature, evidence-backed way to resolve this capability gap, verify it in isolation, promote reusable knowledge, then resume the parent goal.'
    job={'schema':'dore.research-job.v0.2','research_id':rid,'state':'RESEARCH_QUEUED','created_at':now(),'updated_at':now(),'iteration':1,'parent_message_id':PARENT_ID,'parent_goal':PARENT_GOAL,'project_loop':PROJECT_LOOP,'parent_goal_preserved':True,'failure_fingerprint':(learning or {}).get('failure_fingerprint'),'question':question,'local_evidence_checked':[str(learning_path)] if learning_path else [],'preferred_sources':['local Knowledge Lab','verified skills/failure memory','official docs','maintained mature OSS','standards/specs'],'acceptance_test':'Run the smallest falsifiable parent-specific experiment. Promotion and resume require verification.','promotion_target':'verified reusable skill/failure memory/candidate','human_gate':False,'transport':'research_executor + dore.mail peer escalation','history':[{'at':now(),'state':'RESEARCH_QUEUED'}]};atomic_json(p,job);append_event('RESEARCH_QUEUED',research_id=rid,parent_goal=PARENT_GOAL,research_job=str(p));return p,job
def run_research(job_path):
    if not RESEARCH_EXECUTOR.exists():return {'ok':False,'state':'RESEARCH_BLOCKED','error':'research_executor_missing'}
    cp=subprocess.run([sys.executable,str(RESEARCH_EXECUTOR),str(job_path)],cwd=str(ROOT),text=True,capture_output=True,timeout=600);parsed=None
    try:parsed=json.loads((cp.stdout or '').strip().splitlines()[-1])
    except Exception:pass
    return {'ok':cp.returncode==0 and isinstance(parsed,dict) and bool(parsed.get('ok')),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:],'result':parsed}
def run_driver(reason,learning_path,learning,research_job_path=None,research_job=None):
    if not DRIVER.exists():return {'ok':False,'error':'driver_missing','driver':str(DRIVER)}
    msg={'schema':'dore.runtime.v0.5','message_id':f'resident-{int(time.time())}','kind':'autonomous_driver','sender':'dore-resident-runtime','recipient':'dore','related_goal':PARENT_GOAL,'task':{'parent_source_message_id':PARENT_ID,'parent_goal':PARENT_GOAL,'project_loop':PROJECT_LOOP,'trigger':reason,'learning_evidence':str(learning_path) if learning_path else None,'failure_fingerprint':(learning or {}).get('failure_fingerprint'),'research_job':str(research_job_path) if research_job_path else None,'knowledge_artifact':(research_job or {}).get('knowledge_artifact')}}
    cp=subprocess.run([sys.executable,str(DRIVER)],cwd=str(ROOT),input=json.dumps(msg,ensure_ascii=False),text=True,capture_output=True,timeout=1200);parsed=None
    try:parsed=json.loads((cp.stdout or '').strip().splitlines()[-1])
    except Exception:pass
    return {'ok':cp.returncode==0 and isinstance(parsed,dict) and bool(parsed.get('ok')),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:],'result':parsed}
def remember_failure(job,result,verified=False,resolution=None):
    try:
        from failure_memory import remember_failure as rf
        diag=((result.get('stderr') or '')+'\n'+(result.get('stdout') or ''))[-6000:];return rf(PARENT_GOAL,diag,evidence=result.get('result'),resolution=resolution,verified=verified)
    except Exception as e:return {'error':repr(e)}
def sync_learning(job,status,verification=None):
    artifact=(job or {}).get('knowledge_artifact') or {}
    if not artifact:return None
    try:
        from shared_learning import record
        return record(artifact,learned_by='dore',status=status,verification=verification,parent_goal=PARENT_GOAL)
    except Exception as e:return {'ok':False,'error':repr(e)}
def requeue_after_rejected(job_path,job,result):
    diag={'returncode':result.get('returncode'),'stdout_tail':(result.get('stdout') or '')[-2500:],'stderr_tail':(result.get('stderr') or '')[-2500:],'parsed_result':result.get('result')};ex=list(job.get('experiments') or []);ex.append({'at':now(),'status':'REJECTED','diagnostic':diag});memory=remember_failure(job,result,verified=False)
    job={**job,'iteration':int(job.get('iteration') or 1)+1,'experiments':ex,'failure_memory':memory,'knowledge_artifact':None,'question':str(job.get('question') or '')+' Previous experiment was rejected. Research this new evidence before another execution: '+json.dumps(diag,ensure_ascii=False)[-3000:]};job=transition(job_path,job,'REJECTED',evidence='experiment failed with new diagnostic');return transition(job_path,job,'RESEARCH_QUEUED',reason='experiment_rejected_new_evidence')
def finish_verified(job_path,job,result):
    verification={'at':now(),'signal':'parent-specific experiment passed','driver_result':result.get('result')};job=transition(job_path,job,'VERIFIED',evidence='parent-specific experiment passed');sync=sync_learning(job,'VERIFIED',verification=verification);parsed=result.get('result') if isinstance(result.get('result'),dict) else {};promoted=parsed.get('promoted_skills') or parsed.get('promoted_skill') or parsed.get('promotion') or parsed.get('skill');memory=remember_failure(job,result,verified=True,resolution=promoted or 'verified parent experiment')
    job=transition(job_path,{**job,'shared_learning':sync,'failure_memory':memory},'PROMOTED',promotion=promoted or 'verified capability/evidence retained');return transition(job_path,job,'RESUME_PARENT',resumed=True)
def a2a_snapshot(state_name):
    try:
        from a2a_adapter import dore_to_a2a_task
        return dore_to_a2a_task(source_message_id=PARENT_ID,parent_goal=PARENT_GOAL,state=state_name,metadata={'projectLoop':PROJECT_LOOP,'runtime':VERSION})
    except Exception as e:return {'error':repr(e)}
def telemetry_snapshot():
    state=read_json(STATE,{}) or {};heartbeat=read_json(HEARTBEAT,{}) or {};jobs=[]
    if RESEARCH.exists():
        for p in sorted(RESEARCH.glob('*.json'),key=lambda x:x.stat().st_mtime,reverse=True)[:6]:
            j=read_json(p,{}) or {};jobs.append({'path':str(p),'research_id':j.get('research_id'),'state':j.get('state'),'iteration':j.get('iteration'),'updated_at':j.get('updated_at'),'question':j.get('question'),'peer_research':j.get('peer_research'),'evidence_count':((j.get('knowledge_artifact') or {}).get('evidence_count'))})
    current=str(heartbeat.get('state') or state.get('last_event') or 'RUNNING');return {'schema':'dore.runtime.telemetry.v0.4','published_at':now(),'runtime':VERSION,'host_role':'dore-local-mac','project_loop':PROJECT_LOOP,'parent_goal':PARENT_GOAL,'parent_message_id':PARENT_ID,'heartbeat':heartbeat,'state':state,'a2a_task':a2a_snapshot(current),'research_jobs':jobs,'events':tail_events(40)}
def ensure_telemetry_repo():
    remote=run(['git','remote','get-url','origin'],timeout=30)
    if remote.returncode!=0 or not remote.stdout.strip():raise RuntimeError('origin_remote_unavailable')
    url=remote.stdout.strip()
    if not (TELEMETRY_REPO/'.git').exists():
        if TELEMETRY_REPO.exists():shutil.rmtree(TELEMETRY_REPO)
        cp=run(['git','clone','--filter=blob:none','--no-checkout',url,str(TELEMETRY_REPO)],cwd=RUNTIME,timeout=180)
        if cp.returncode!=0:raise RuntimeError('telemetry_clone_failed:'+(cp.stderr or cp.stdout)[-1500:])
        run(['git','config','user.name','DORE-RUNTIME'],cwd=TELEMETRY_REPO,timeout=30);run(['git','config','user.email','westsidewatchca@gmail.com'],cwd=TELEMETRY_REPO,timeout=30)
    return TELEMETRY_REPO
def publish_telemetry(force=False):
    state=read_json(STATE,{}) or {};last=float(state.get('last_telemetry_epoch') or 0)
    if not force and time.time()-last<TELEMETRY_INTERVAL:return False
    repo=ensure_telemetry_repo();run(['git','fetch','origin',TELEMETRY_BRANCH],cwd=repo,timeout=90);exists=run(['git','show-ref','--verify',f'refs/remotes/origin/{TELEMETRY_BRANCH}'],cwd=repo,timeout=30).returncode==0;cp=run(['git','checkout','-B',TELEMETRY_BRANCH,f'origin/{TELEMETRY_BRANCH}'],cwd=repo,timeout=60) if exists else run(['git','checkout','--orphan',TELEMETRY_BRANCH],cwd=repo,timeout=60)
    if cp.returncode!=0:raise RuntimeError('telemetry_checkout_failed:'+(cp.stderr or cp.stdout)[-1500:])
    (repo/'runtime-latest.json').write_text(json.dumps(telemetry_snapshot(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');run(['git','add','runtime-latest.json'],cwd=repo,timeout=30)
    if run(['git','diff','--cached','--quiet'],cwd=repo,timeout=30).returncode!=0:
        c=run(['git','commit','-m','chore(dore): publish resident runtime telemetry'],cwd=repo,timeout=60)
        if c.returncode!=0:raise RuntimeError('telemetry_commit_failed:'+(c.stderr or c.stdout)[-1500:])
        p=run(['git','push','origin',f'HEAD:{TELEMETRY_BRANCH}'],cwd=repo,timeout=120)
        if p.returncode!=0:raise RuntimeError('telemetry_push_failed:'+(p.stderr or p.stdout)[-1500:])
    state['last_telemetry_epoch']=time.time();state['last_telemetry_at']=now();state['telemetry_branch']=TELEMETRY_BRANCH;atomic_json(STATE,state);return True
def maybe_self_update():
    state=read_json(STATE,{}) or {};last=float(state.get('last_self_update_check_epoch') or 0)
    if time.time()-last<SELF_UPDATE_INTERVAL:return False
    state['last_self_update_check_epoch']=time.time();state['last_self_update_check_at']=now();atomic_json(STATE,state);fetch=run(['git','fetch','origin','main'],timeout=120)
    if fetch.returncode!=0:append_event('SELF_UPDATE_FETCH_FAILED',detail=(fetch.stderr or fetch.stdout)[-1200:]);return False
    rels=['local/dore-local/resident_runtime.py','local/dore-local/autonomous_driver.py','local/dore-local/research_executor.py','local/dore-local/autonomous_capability_loop.py','local/dore-local/failure_memory.py','local/dore-local/shared_learning.py','local/dore-local/a2a_adapter.py','local/dore-local/loop_contract_acceptance.py','dore-design/knowledge-lab/resources/source-catalog.json','dore-design/knowledge-lab/a2a/project-state.json','dore-design/knowledge-lab/a2a/loop-contract-v1.json','dore-design/knowledge-lab/a2a/agent-card.json','dore-design/knowledge-lab/skills/registry.json'];changed=[]
    for rel in rels:
        target=ROOT/rel;show=run(['git','show',f'origin/main:{rel}'],timeout=60)
        if show.returncode!=0:continue
        remote_text=show.stdout;local_text=target.read_text(encoding='utf-8') if target.exists() else ''
        if remote_text!=local_text:
            target.parent.mkdir(parents=True,exist_ok=True);tmp=target.with_suffix(target.suffix+'.remote');tmp.write_text(remote_text,encoding='utf-8');tmp.replace(target);changed.append(rel)
    if changed:
        append_event('SELF_UPDATED',files=changed,source='origin/main');publish_telemetry(force=True)
        if 'local/dore-local/resident_runtime.py' in changed:os.execv(sys.executable,[sys.executable,str(SELF)])
    return bool(changed)
def tick():
    state=read_json(STATE,{}) or {};lp,learning=latest_learning();learning_fp=fingerprint(learning) if learning else None;job_path=None;job=None
    if learning and learning.get('state')=='RESEARCH_REQUIRED':
        job_path,job=ensure_research_job(lp,learning)
        if job.get('state') in {'RESEARCH_QUEUED','RESEARCHING','RESEARCH_BLOCKED'}:
            append_event('RESEARCHING',research_id=job.get('research_id'),parent_goal=PARENT_GOAL);rr=run_research(job_path);job=read_json(job_path,job) or job;state={**state,'last_research_diagnostic':rr,'research_id':job.get('research_id'),'research_job':str(job_path),'last_event':job.get('state'),'driver_passed':False};atomic_json(STATE,state);atomic_json(HEARTBEAT,{'runtime':VERSION,'at':now(),'state':job.get('state'),'parent_goal':PARENT_GOAL,'research_id':job.get('research_id'),'next_tick_seconds':INTERVAL});publish_telemetry(force=True)
            if job.get('state')!='KNOWLEDGE_RETURNED':return
        if job.get('state')=='PEER_RESEARCH_QUEUED':atomic_json(HEARTBEAT,{'runtime':VERSION,'at':now(),'state':'PEER_RESEARCH_QUEUED','parent_goal':PARENT_GOAL,'research_id':job.get('research_id'),'next_tick_seconds':INTERVAL});return
        if job.get('state') in {'KNOWLEDGE_RETURNED','VERIFIED','PROMOTED'}:job=transition(job_path,job,'EXPERIMENTING',evidence='knowledge artifact available');reason='KNOWLEDGE_RETURNED_EXPERIMENT'
        elif job.get('state')=='RESUME_PARENT':reason='RESUME_PARENT'
        else:return
    elif not state.get('driver_passed'):reason='NO_USER_INPUT_CONTINUE'
    else:atomic_json(HEARTBEAT,{'runtime':VERSION,'at':now(),'state':'IDLE_HEALTHY','parent_goal':PARENT_GOAL,'next_tick_seconds':INTERVAL});return
    append_event('CONTINUE',reason=reason,parent_goal=PARENT_GOAL,learning=str(lp) if lp else None);before=time.time();result=run_driver(reason,lp,learning,job_path,job);progressed=bool(result.get('ok')) or fingerprint(result)!=state.get('last_result_fingerprint');new={**state,'runtime':VERSION,'project_loop':PROJECT_LOOP,'parent_goal':PARENT_GOAL,'parent_message_id':PARENT_ID,'last_event':reason,'last_attempt_at':now(),'last_attempt_epoch':before,'last_driver_ok':bool(result.get('ok')),'last_learning_fingerprint':learning_fp,'last_result_fingerprint':fingerprint(result),'driver_passed':bool(result.get('ok')),'last_driver_diagnostic':{'returncode':result.get('returncode'),'stdout_tail':(result.get('stdout') or '')[-4000:],'stderr_tail':(result.get('stderr') or '')[-4000:],'parsed_result':result.get('result')}}
    if progressed:new['last_progress_at']=now();new['last_progress_epoch']=time.time()
    if job_path and job:
        if result.get('ok'):job=finish_verified(job_path,job,result);new['last_event']='RESUME_PARENT';new['research_state']=job.get('state')
        else:job=requeue_after_rejected(job_path,job,result);new['driver_passed']=False;new['last_event']='RESEARCH_QUEUED';new['research_state']='RESEARCH_QUEUED'
    atomic_json(STATE,new);atomic_json(HEARTBEAT,{'runtime':VERSION,'at':now(),'state':'PASS' if result.get('ok') else ('RESEARCH_QUEUED' if job_path else 'RUNNING_WITH_FAILURE_EVIDENCE'),'parent_goal':PARENT_GOAL,'last_event':new.get('last_event'),'driver_ok':bool(result.get('ok')),'next_tick_seconds':INTERVAL});append_event('DRIVER_RESULT',reason=reason,ok=bool(result.get('ok')),returncode=result.get('returncode'),information_gain=progressed,result=(result.get('result') or {}).get('error') if isinstance(result.get('result'),dict) else None);publish_telemetry(force=True)
def main():
    RUNTIME.mkdir(parents=True,exist_ok=True)
    with LOCK.open('w') as lock_file:
        try:fcntl.flock(lock_file.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return 0
        append_event('RUNTIME_STARTED',pid=os.getpid(),interval_seconds=INTERVAL,supervisor='launchd',runtime=VERSION,project_loop=PROJECT_LOOP)
        while True:
            try:maybe_self_update();tick();publish_telemetry(force=False)
            except subprocess.TimeoutExpired as exc:append_event('ACTION_TIMEOUT',command=str(exc.cmd),timeout=exc.timeout)
            except Exception as exc:append_event('RUNTIME_ERROR',error=repr(exc))
            time.sleep(INTERVAL)
if __name__=='__main__':raise SystemExit(main())
