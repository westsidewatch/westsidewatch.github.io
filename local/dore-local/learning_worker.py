#!/usr/bin/env python3
from __future__ import annotations
import fcntl, json, os, sqlite3, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from autonomous_learner import run_cycle

REPO=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
DORE=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
DB=DORE/'data'/'dore.sqlite3'; LOCK=DORE/'data'/'learning-worker.lock'; STATE=DORE/'data'/'learning-worker-state.json'; LOG=DORE/'logs'/'learning-worker.jsonl'
MODEL=os.environ.get('DORE_LOCAL_MODEL','qwen3:8b'); OLLAMA=os.environ.get('OLLAMA_BASE_URL','http://127.0.0.1:11434')

def now(): return datetime.now(timezone.utc).isoformat()
def emit(event,**extra):
    LOG.parent.mkdir(parents=True,exist_ok=True)
    with LOG.open('a',encoding='utf-8') as f:f.write(json.dumps({'ts':now(),'event':event,**extra},ensure_ascii=False)+'\n')
def model_call(prompt):
    data=json.dumps({'model':MODEL,'messages':[{'role':'system','content':'You are Doré autonomous learning executor. Follow evidence and output the requested strict JSON. Never self-award capability without the executor gate.'},{'role':'user','content':prompt}],'stream':False,'options':{'temperature':0.2}}).encode()
    req=urllib.request.Request(OLLAMA+'/api/chat',data=data,headers={'Content-Type':'application/json'})
    return json.loads(urllib.request.urlopen(req,timeout=300).read())['message']['content']
def main():
    DORE.joinpath('data').mkdir(parents=True,exist_ok=True); LOCK.touch(exist_ok=True)
    with LOCK.open('r+') as lock:
        try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: return 0
        try:
            c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; cycles=[]; max_depth=int(os.environ.get('DORE_LEARNING_MAX_DEPTH','4'))
            for depth in range(max_depth):
                result=run_cycle(c,REPO,DORE,max_gates=int(os.environ.get('DORE_LEARNING_MAX_GATES','1')),model_call=model_call); cycles.append(result)
                executed=result.get('executed') or []
                progressed=any(r.get('verified') for r in executed)
                productive=bool(result.get('productive_runs'))
                emit('cycle',depth=depth,executed=executed,progressed=progressed)
                # Continue immediately through a newly unlocked dependency chain. Stop when no new capability was verified,
                # or when all remaining work is stagnant/blocked. This is compute-budgeted, not calendar-gated.
                if not progressed: break
                if not productive: break
            payload={'ok':True,'checked_at':now(),'cycles':cycles,'max_depth':max_depth,'calendar_gate':False}; STATE.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
            return 0
        except Exception as e:
            payload={'ok':False,'checked_at':now(),'error':str(e)}; STATE.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8'); emit('error',detail=str(e)); return 1
if __name__=='__main__': raise SystemExit(main())
