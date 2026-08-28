#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, sqlite3, subprocess
from datetime import datetime, timezone
from pathlib import Path
from learning_planner import plan, validate_gate
from self_memory import add_learning, status as learning_status

PHASES=('selected','discovering','synthesizing','challenging','assessment_ready','blocked','completed')

def now(): return datetime.now(timezone.utc).isoformat()
def _id(*parts): return hashlib.sha256('|'.join(parts).encode()).hexdigest()[:24]

def ensure_schema(conn):
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS dore_autonomous_runs(
      id TEXT PRIMARY KEY, gate_id TEXT NOT NULL, phase TEXT NOT NULL, attempt INTEGER NOT NULL DEFAULT 1,
      evidence_hash TEXT, evidence_ref TEXT, result_json TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
    CREATE INDEX IF NOT EXISTS idx_dore_autonomous_gate ON dore_autonomous_runs(gate_id,updated_at DESC);
    '''); conn.commit()

def load_gates(base:Path):
    payload=json.loads((base/'learning-gates'/'core-v1.json').read_text(encoding='utf-8'))
    return [validate_gate(g) for g in payload.get('gates') or []]

def _candidate_roots(repo_root:Path,dore_root:Path):
    roots=[repo_root,dore_root/'archive']
    return [p for p in roots if p.exists()]

def discover_evidence(repo_root:Path,dore_root:Path,gate,limit=30):
    hits=[]
    queries=[str(q) for q in gate.get('evidence_queries') or []]
    for root in _candidate_roots(repo_root,dore_root):
        for q in queries:
            try:
                p=subprocess.run(['rg','-l','-F',q,str(root)],capture_output=True,text=True,timeout=20)
                paths=[Path(x) for x in p.stdout.splitlines() if x.strip()]
            except Exception:
                paths=[]
            for path in paths:
                key=str(path)
                if key not in {h['path'] for h in hits}: hits.append({'path':key,'query':q})
                if len(hits)>=limit: break
            if len(hits)>=limit: break
        if len(hits)>=limit: break
    digest=hashlib.sha256('\n'.join(sorted(h['path']+'|'+h['query'] for h in hits)).encode()).hexdigest() if hits else None
    return hits,digest

def run_cycle(conn,repo_root:Path,dore_root:Path,max_gates=2):
    ensure_schema(conn)
    gates=load_gates(Path(__file__).resolve().parent)
    state=learning_status(conn)
    p=plan(state,gates)
    ready=p.get('ready') or []
    executed=[]
    for item in ready[:max_gates]:
        gate=next(g for g in gates if g['id']==item['id'])
        prev=conn.execute('SELECT * FROM dore_autonomous_runs WHERE gate_id=? ORDER BY updated_at DESC LIMIT 1',(gate['id'],)).fetchone()
        attempt=(prev['attempt']+1) if prev else 1
        hits,digest=discover_evidence(repo_root,dore_root,gate)
        # Avoid burning compute when the evidence set is unchanged across repeated attempts.
        if prev and prev['evidence_hash']==digest and prev['phase'] in {'assessment_ready','blocked'}:
            executed.append({'gate_id':gate['id'],'phase':'stagnant','attempt':prev['attempt'],'evidence_count':len(hits)}); continue
        rid='run_'+_id(gate['id'],str(attempt),digest or 'none',now())
        phase='assessment_ready' if len(hits)>=int(gate.get('min_evidence') or 1) else 'blocked'
        result={'gate_id':gate['id'],'domain':gate['domain'],'stage':gate.get('stage'),'evidence':hits,'acceptance':gate.get('acceptance') or [],'next_action':gate.get('next_action'),'note':'Evidence discovery alone never grants PASS. This run is a candidate for synthesis/challenge/assessment.'}
        ref=f'autonomous-run:{rid}'
        t=now(); conn.execute('INSERT INTO dore_autonomous_runs(id,gate_id,phase,attempt,evidence_hash,evidence_ref,result_json,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)',(rid,gate['id'],phase,attempt,digest,ref,json.dumps(result,ensure_ascii=False),t,t))
        add_learning(conn,gate['domain'],f"Autonomous executor prepared gate {gate['id']} with {len(hits)} evidence references.",gate.get('stage'),assessment='pending blind/adversarial assessment',status='researching' if phase=='assessment_ready' else 'blocked',evidence_ref=ref,source_type='autonomous_executor',epistemic_state='observed')
        conn.commit(); executed.append({'gate_id':gate['id'],'run_id':rid,'phase':phase,'attempt':attempt,'evidence_count':len(hits),'evidence_ref':ref})
    return {'ok':True,'policy':'bounded-autonomous-learning-v1','time_is_gate':False,'executed':executed,'planner':p}

def status(conn):
    ensure_schema(conn)
    rows=[dict(r) for r in conn.execute('SELECT * FROM dore_autonomous_runs ORDER BY updated_at DESC LIMIT 50')]
    for r in rows:
        try:r['result']=json.loads(r.pop('result_json'))
        except Exception:r['result']=None
    return {'ok':True,'runs':rows}
