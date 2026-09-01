#!/usr/bin/env python3
"""Doré Resident Runtime v0.3.

Resident macOS control loop. Core invariant:
RESEARCH_REQUIRED is never retried as the same execution. It must transition
into RESEARCH_QUEUED first, preserving the parent goal and producing a durable
research job. Only new knowledge/evidence may unlock another execution attempt.
"""
from __future__ import annotations

import fcntl, hashlib, json, os, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

VERSION = "dore.resident-runtime.v0.3"
HOME = Path(os.environ.get("DORE_LOCAL_HOME", Path.home() / ".dore")).expanduser()
ROOT = Path(os.environ.get("DORE_REPO_ROOT", Path.home() / "westsidewatch.github.io")).expanduser()
RUNTIME = HOME / "runtime"
LEARNING = HOME / "coordination" / "learning"
RESEARCH = HOME / "coordination" / "research"
DRIVER = ROOT / "local" / "dore-local" / "autonomous_driver.py"
SELF = ROOT / "local" / "dore-local" / "resident_runtime.py"
STATE = RUNTIME / "state.json"
EVENTS = RUNTIME / "events.jsonl"
HEARTBEAT = RUNTIME / "heartbeat.json"
LOCK = RUNTIME / "runtime.lock"
TELEMETRY_REPO = RUNTIME / "telemetry-repo"
TELEMETRY_BRANCH = os.environ.get("DORE_RUNTIME_TELEMETRY_BRANCH", "dore-runtime-telemetry")
TELEMETRY_INTERVAL = max(60, int(os.environ.get("DORE_RUNTIME_TELEMETRY_SECONDS", "120")))
SELF_UPDATE_INTERVAL = max(120, int(os.environ.get("DORE_RUNTIME_SELF_UPDATE_SECONDS", "300")))
INTERVAL = max(10, int(os.environ.get("DORE_RUNTIME_INTERVAL_SECONDS", "30")))
STALL_AFTER = max(INTERVAL * 2, int(os.environ.get("DORE_RUNTIME_STALL_SECONDS", "90")))
PARENT_ID = os.environ.get("DORE_RUNTIME_PARENT_ID", "new-westside-storybook-real-loop-2")
PARENT_GOAL = os.environ.get("DORE_RUNTIME_PARENT_GOAL", "New Westside visual construction")


def now(): return datetime.now(timezone.utc).isoformat()

def run(argv, cwd=ROOT, timeout=120):
    return subprocess.run(argv, cwd=str(cwd), text=True, capture_output=True, timeout=timeout)

def read_json(path, default=None):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception: return default

def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)

def append_event(kind, **data):
    RUNTIME.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"at": now(), "event": kind, **data}, ensure_ascii=False) + "\n")

def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()

def tail_events(limit=30):
    if not EVENTS.exists(): return []
    out=[]
    for line in EVENTS.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]:
        try: out.append(json.loads(line))
        except Exception: out.append({"event":"UNPARSEABLE_EVENT","raw":line[-1000:]})
    return out

def latest_learning():
    direct = LEARNING / f"{PARENT_ID}.json"
    if direct.exists():
        data=read_json(direct)
        if isinstance(data,dict): return direct,data
    if not LEARNING.exists(): return None,None
    for p in sorted(LEARNING.glob("*.json"), key=lambda x:x.stat().st_mtime, reverse=True):
        data=read_json(p)
        if isinstance(data,dict) and data.get("state")=="RESEARCH_REQUIRED": return p,data
    return None,None

def research_id_for(learning):
    fp=(learning or {}).get("failure_fingerprint") or fingerprint(learning or {"parent":PARENT_ID})
    return f"research-{PARENT_ID}-{str(fp)[:16]}"

def ensure_research_job(learning_path, learning):
    """Executable Research Bridge transition.

    This is the anti-regression invariant: once a capability gap is classified
    RESEARCH_REQUIRED, the runtime creates/maintains a durable research job and
    MUST NOT call the same execution path again until the job gains new evidence.
    """
    RESEARCH.mkdir(parents=True, exist_ok=True)
    rid=research_id_for(learning)
    p=RESEARCH/f"{rid}.json"
    existing=read_json(p,{}) or {}
    if existing.get("state") in {"KNOWLEDGE_RETURNED","VERIFIED","PROMOTED","RESUME_PARENT"}:
        return p, existing, True
    job={
        "schema":"dore.research-job.v0.1",
        "research_id":rid,
        "state":"RESEARCH_QUEUED",
        "created_at":existing.get("created_at") or now(),
        "updated_at":now(),
        "parent_message_id":PARENT_ID,
        "parent_goal":PARENT_GOAL,
        "failure_fingerprint":(learning or {}).get("failure_fingerprint"),
        "question":(learning or {}).get("question") or "Determine the missing capability/knowledge causing the current parent task failure and find a verified repair path.",
        "local_evidence_checked":[str(learning_path)] if learning_path else [],
        "preferred_sources":["local Knowledge Lab","existing skills/failure memory","official docs","maintained mature OSS","standards/specs"],
        "acceptance_test":"Run the smallest experiment that can falsify/verify the returned hypothesis, then resume the same parent goal only on verified evidence.",
        "promotion_target":"verified reusable skill/failure memory/candidate",
        "human_gate":False,
        "transport":"A2A research bridge",
        "knowledge_artifact":existing.get("knowledge_artifact"),
    }
    atomic_json(p,job)
    append_event("RESEARCH_QUEUED",research_id=rid,parent_goal=PARENT_GOAL,research_job=str(p))
    return p,job,False

def run_driver(reason, learning_path, learning):
    if not DRIVER.exists(): return {"ok":False,"error":"driver_missing","driver":str(DRIVER)}
    msg={"schema":"dore.runtime.v0.3","message_id":f"resident-{int(time.time())}","kind":"autonomous_driver","sender":"dore-resident-runtime","recipient":"dore","related_goal":PARENT_GOAL,"task":{"parent_source_message_id":PARENT_ID,"parent_goal":PARENT_GOAL,"trigger":reason,"learning_evidence":str(learning_path) if learning_path else None,"failure_fingerprint":(learning or {}).get("failure_fingerprint")}}
    cp=subprocess.run([sys.executable,str(DRIVER)],cwd=str(ROOT),input=json.dumps(msg,ensure_ascii=False),text=True,capture_output=True,timeout=1200)
    parsed=None
    try: parsed=json.loads((cp.stdout or "").strip().splitlines()[-1])
    except Exception: pass
    return {"ok":cp.returncode==0 and isinstance(parsed,dict) and bool(parsed.get("ok")),"returncode":cp.returncode,"stdout":(cp.stdout or "")[-12000:],"stderr":(cp.stderr or "")[-12000:],"result":parsed}

def telemetry_snapshot():
    state=read_json(STATE,{}) or {}; heartbeat=read_json(HEARTBEAT,{}) or {}
    research_jobs=[]
    if RESEARCH.exists():
        for p in sorted(RESEARCH.glob("*.json"), key=lambda x:x.stat().st_mtime, reverse=True)[:5]:
            j=read_json(p,{}) or {}; research_jobs.append({"path":str(p),"research_id":j.get("research_id"),"state":j.get("state"),"updated_at":j.get("updated_at"),"question":j.get("question")})
    return {"schema":"dore.runtime.telemetry.v0.2","published_at":now(),"runtime":VERSION,"host_role":"dore-local-mac","parent_goal":PARENT_GOAL,"parent_message_id":PARENT_ID,"heartbeat":heartbeat,"state":state,"research_jobs":research_jobs,"events":tail_events(30)}

def ensure_telemetry_repo():
    remote=run(["git","remote","get-url","origin"],timeout=30)
    if remote.returncode!=0 or not remote.stdout.strip(): raise RuntimeError("origin_remote_unavailable")
    url=remote.stdout.strip()
    if not (TELEMETRY_REPO/".git").exists():
        if TELEMETRY_REPO.exists(): shutil.rmtree(TELEMETRY_REPO)
        cp=run(["git","clone","--filter=blob:none","--no-checkout",url,str(TELEMETRY_REPO)],cwd=RUNTIME,timeout=180)
        if cp.returncode!=0: raise RuntimeError("telemetry_clone_failed:"+(cp.stderr or cp.stdout)[-1500:])
        run(["git","config","user.name","DORE-RUNTIME"],cwd=TELEMETRY_REPO,timeout=30)
        run(["git","config","user.email","westsidewatchca@gmail.com"],cwd=TELEMETRY_REPO,timeout=30)
    return TELEMETRY_REPO

def publish_telemetry(force=False):
    state=read_json(STATE,{}) or {}; last=float(state.get("last_telemetry_epoch") or 0)
    if not force and time.time()-last<TELEMETRY_INTERVAL:return False
    repo=ensure_telemetry_repo(); run(["git","fetch","origin",TELEMETRY_BRANCH],cwd=repo,timeout=90)
    exists=run(["git","show-ref","--verify",f"refs/remotes/origin/{TELEMETRY_BRANCH}"],cwd=repo,timeout=30).returncode==0
    cp=run(["git","checkout","-B",TELEMETRY_BRANCH,f"origin/{TELEMETRY_BRANCH}"],cwd=repo,timeout=60) if exists else run(["git","checkout","--orphan",TELEMETRY_BRANCH],cwd=repo,timeout=60)
    if cp.returncode!=0: raise RuntimeError("telemetry_checkout_failed:"+(cp.stderr or cp.stdout)[-1500:])
    (repo/"runtime-latest.json").write_text(json.dumps(telemetry_snapshot(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    run(["git","add","runtime-latest.json"],cwd=repo,timeout=30)
    if run(["git","diff","--cached","--quiet"],cwd=repo,timeout=30).returncode!=0:
        c=run(["git","commit","-m","chore(dore): publish resident runtime telemetry"],cwd=repo,timeout=60)
        if c.returncode!=0: raise RuntimeError("telemetry_commit_failed:"+(c.stderr or c.stdout)[-1500:])
        p=run(["git","push","origin",f"HEAD:{TELEMETRY_BRANCH}"],cwd=repo,timeout=120)
        if p.returncode!=0: raise RuntimeError("telemetry_push_failed:"+(p.stderr or p.stdout)[-1500:])
    state["last_telemetry_epoch"]=time.time(); state["last_telemetry_at"]=now(); state["telemetry_branch"]=TELEMETRY_BRANCH; atomic_json(STATE,state); return True

def maybe_self_update():
    state=read_json(STATE,{}) or {}; last=float(state.get("last_self_update_check_epoch") or 0)
    if time.time()-last<SELF_UPDATE_INTERVAL:return False
    state["last_self_update_check_epoch"]=time.time(); state["last_self_update_check_at"]=now(); atomic_json(STATE,state)
    fetch=run(["git","fetch","origin","main"],timeout=120)
    if fetch.returncode!=0: append_event("SELF_UPDATE_FETCH_FAILED",detail=(fetch.stderr or fetch.stdout)[-1200:]); return False
    changed=[]
    for rel,target in [("local/dore-local/resident_runtime.py",SELF),("local/dore-local/autonomous_driver.py",DRIVER)]:
        show=run(["git","show",f"origin/main:{rel}"],timeout=60)
        if show.returncode!=0:continue
        remote_text=show.stdout; local_text=target.read_text(encoding="utf-8") if target.exists() else ""
        if remote_text!=local_text:
            tmp=target.with_suffix(target.suffix+".remote"); tmp.write_text(remote_text,encoding="utf-8"); tmp.replace(target); changed.append(rel)
    if changed:
        append_event("SELF_UPDATED",files=changed,source="origin/main"); publish_telemetry(force=True)
        if "local/dore-local/resident_runtime.py" in changed: os.execv(sys.executable,[sys.executable,str(SELF)])
    return bool(changed)

def tick():
    state=read_json(STATE,{}) or {}; lp,learning=latest_learning(); learning_fp=fingerprint(learning) if learning else None
    if learning and learning.get("state")=="RESEARCH_REQUIRED":
        job_path,job,knowledge_ready=ensure_research_job(lp,learning)
        if not knowledge_ready:
            atomic_json(HEARTBEAT,{"runtime":VERSION,"at":now(),"state":"RESEARCH_QUEUED","parent_goal":PARENT_GOAL,"research_id":job.get("research_id"),"next_tick_seconds":INTERVAL})
            new={**state,"runtime":VERSION,"parent_goal":PARENT_GOAL,"parent_message_id":PARENT_ID,"last_event":"RESEARCH_QUEUED","last_learning_fingerprint":learning_fp,"research_job":str(job_path),"research_id":job.get("research_id"),"driver_passed":False}
            atomic_json(STATE,new); publish_telemetry(force=True); return
        reason="KNOWLEDGE_RETURNED_RESUME"
    elif not state.get("driver_passed"): reason="NO_USER_INPUT_CONTINUE"
    else:
        atomic_json(HEARTBEAT,{"runtime":VERSION,"at":now(),"state":"IDLE_HEALTHY","parent_goal":PARENT_GOAL,"next_tick_seconds":INTERVAL}); return

    append_event("CONTINUE",reason=reason,parent_goal=PARENT_GOAL,learning=str(lp) if lp else None)
    before=time.time(); result=run_driver(reason,lp,learning); progressed=bool(result.get("ok")) or fingerprint(result)!=state.get("last_result_fingerprint")
    new={**state,"runtime":VERSION,"parent_goal":PARENT_GOAL,"parent_message_id":PARENT_ID,"last_event":reason,"last_attempt_at":now(),"last_attempt_epoch":before,"last_driver_ok":bool(result.get("ok")),"last_learning_fingerprint":learning_fp,"last_result_fingerprint":fingerprint(result),"driver_passed":bool(result.get("ok")),"last_driver_diagnostic":{"returncode":result.get("returncode"),"stdout_tail":(result.get("stdout") or "")[-4000:],"stderr_tail":(result.get("stderr") or "")[-4000:],"parsed_result":result.get("result")}}
    if progressed: new["last_progress_at"]=now(); new["last_progress_epoch"]=time.time()
    atomic_json(STATE,new)
    atomic_json(HEARTBEAT,{"runtime":VERSION,"at":now(),"state":"PASS" if result.get("ok") else "RUNNING_WITH_FAILURE_EVIDENCE","parent_goal":PARENT_GOAL,"last_event":reason,"driver_ok":bool(result.get("ok")),"next_tick_seconds":INTERVAL})
    append_event("DRIVER_RESULT",reason=reason,ok=bool(result.get("ok")),returncode=result.get("returncode"),information_gain=progressed,result=(result.get("result") or {}).get("error") if isinstance(result.get("result"),dict) else None)
    publish_telemetry(force=True)

def main():
    RUNTIME.mkdir(parents=True,exist_ok=True)
    with LOCK.open("w") as lock_file:
        try: fcntl.flock(lock_file.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return 0
        append_event("RUNTIME_STARTED",pid=os.getpid(),interval_seconds=INTERVAL,supervisor="launchd",runtime=VERSION)
        while True:
            try: maybe_self_update(); tick(); publish_telemetry(force=False)
            except subprocess.TimeoutExpired as exc: append_event("ACTION_TIMEOUT",command=str(exc.cmd),timeout=exc.timeout)
            except Exception as exc: append_event("RUNTIME_ERROR",error=repr(exc))
            time.sleep(INTERVAL)

if __name__=="__main__": raise SystemExit(main())
