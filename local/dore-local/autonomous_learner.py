#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re, sqlite3, subprocess
from datetime import datetime, timezone
from pathlib import Path
from learning_planner import plan, validate_gate
from self_memory import add_learning, status as learning_status, transition_learning

PHASES=('selected','discovering','synthesizing','challenging','blind_testing','assessment_ready','blocked','completed')
TEXT_EXTS={'.md','.txt','.json','.jsonl','.py','.js','.ts','.tsx','.jsx','.html','.yml','.yaml','.toml','.csv','.xml','.css','.scss'}

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

def _candidate_roots(repo_root:Path,dore_root:Path): return [p for p in (repo_root,dore_root/'archive') if p.exists()]

def _python_search(root:Path,q,limit=30):
    found=[]; ql=q.lower()
    try: paths=root.rglob('*')
    except Exception: return found
    for p in paths:
        if len(found)>=limit: break
        try:
            if not p.is_file() or '.git' in p.parts or p.stat().st_size>2_000_000: continue
            if p.suffix.lower() not in TEXT_EXTS and p.suffix: continue
            text=p.read_text(encoding='utf-8',errors='ignore')
            if ql in text.lower(): found.append(p)
        except Exception: continue
    return found

def discover_evidence(repo_root:Path,dore_root:Path,gate,limit=30):
    hits=[]; seen=set(); queries=[str(q) for q in gate.get('evidence_queries') or []]
    for root in _candidate_roots(repo_root,dore_root):
        for q in queries:
            paths=[]
            try:
                p=subprocess.run(['rg','-l','-F','--hidden','--glob','!.git/**',q,str(root)],capture_output=True,text=True,timeout=20)
                paths=[Path(x) for x in p.stdout.splitlines() if x.strip()]
            except Exception: pass
            if not paths: paths=_python_search(root,q,max(1,limit-len(hits)))
            for path in paths:
                key=str(path)
                if key not in seen: hits.append({'path':key,'query':q}); seen.add(key)
                if len(hits)>=limit: break
            if len(hits)>=limit: break
        if len(hits)>=limit: break
    digest=hashlib.sha256('\n'.join(sorted(h['path']+'|'+h['query'] for h in hits)).encode()).hexdigest() if hits else None
    return hits,digest

def evidence_pack(hits,max_files=10,max_chars_each=4500):
    pack=[]
    for h in hits[:max_files]:
        p=Path(h['path'])
        try: text=p.read_text(encoding='utf-8',errors='ignore')
        except Exception: continue
        q=h.get('query') or ''; pos=text.lower().find(q.lower()) if q else -1; start=max(0,pos-1500) if pos>=0 else 0
        pack.append({'source_ref':str(p),'matched_query':q,'excerpt':text[start:start+max_chars_each]})
    return pack

def _json_from_text(text):
    text=str(text).strip()
    try:return json.loads(text)
    except Exception: pass
    m=re.search(r'\{.*\}',text,re.S)
    if m:
        try:return json.loads(m.group(0))
        except Exception: pass
    return {'raw':text}
def _call_json(model_call,prompt): return _json_from_text(model_call(prompt))

def synthesize(model_call,gate,pack):
    return _call_json(model_call,"You are Doré Researcher. Work only from the supplied evidence pack. Produce strict JSON with keys: thesis, claims (array of {claim,source_refs}), unresolved (array), contradictions (array). Every substantive claim needs source_refs. Do not call inherited claims verified facts merely because they appear in a file.\nGATE:\n"+json.dumps(gate,ensure_ascii=False)+'\nEVIDENCE:\n'+json.dumps(pack,ensure_ascii=False))

def challenge(model_call,gate,pack,synthesis):
    return _call_json(model_call,"Act as an adversarial research examiner independent of the synthesis. Using the evidence, attack unsupported leaps, circular provenance, inherited-memory self-authentication, missing counterevidence, and acceptance criteria not actually demonstrated. Return strict JSON: objections (array), unsupported_claims (array), acceptance_met (array), acceptance_missing (array), verdict_reason. Do not award PASS.\nGATE:\n"+json.dumps(gate,ensure_ascii=False)+'\nEVIDENCE:\n'+json.dumps(pack,ensure_ascii=False)+'\nSYNTHESIS:\n'+json.dumps(synthesis,ensure_ascii=False))

def blind_assessment(model_call,gate,pack):
    questions=_call_json(model_call,'Create 3 difficult blind-test questions from this evidence pack. They must test relational understanding, provenance, and ability to distinguish claim from evidence; avoid trivia and avoid embedding answers. Return strict JSON {questions:[...]} only.\n'+json.dumps(pack,ensure_ascii=False)).get('questions') or []
    answers=_call_json(model_call,'Answer these questions without seeing source material. Be concise and explicitly mark uncertainty. Return strict JSON {answers:[...]} only.\nQUESTIONS:\n'+json.dumps(questions,ensure_ascii=False)).get('answers') or []
    grade=_call_json(model_call,'Grade the blind answers against the evidence pack. Return strict JSON with score from 0.0 to 1.0, errors (array), unsupported (array), provenance_failures (array), and reason. High score requires correct relationships and provenance, not plausible prose.\nQUESTIONS:\n'+json.dumps(questions,ensure_ascii=False)+'\nANSWERS:\n'+json.dumps(answers,ensure_ascii=False)+'\nEVIDENCE:\n'+json.dumps(pack,ensure_ascii=False))
    return {'questions':questions,'answers':answers,'grade':grade}

def _structural_research_method_pass(gate,pack,synthesis,critic):
    refs=[]
    for c in (synthesis.get('claims') or []) if isinstance(synthesis,dict) else []:
        if isinstance(c,dict): refs.extend(c.get('source_refs') or [])
    return len(pack)>=int(gate.get('min_evidence') or 1) and len(set(refs))>=2 and isinstance(critic.get('objections'),list)

def _autonomous_learning_pass(gate,pack,synthesis,critic,blind):
    grade=blind.get('grade') or {}
    try: score=float(grade.get('score') or 0)
    except Exception: score=0
    return len(pack)>=int(gate.get('min_evidence') or 1) and score>=0.85 and not (grade.get('unsupported') or []) and not (grade.get('provenance_failures') or []) and len(critic.get('acceptance_missing') or [])<=1

def execute_gate(conn,repo_root:Path,dore_root:Path,gate,model_call=None):
    ensure_schema(conn); prev=conn.execute('SELECT * FROM dore_autonomous_runs WHERE gate_id=? ORDER BY updated_at DESC LIMIT 1',(gate['id'],)).fetchone(); attempt=(prev['attempt']+1) if prev else 1
    hits,digest=discover_evidence(repo_root,dore_root,gate)
    if prev and prev['evidence_hash']==digest and prev['phase'] in {'blocked','completed'}: return {'gate_id':gate['id'],'phase':'stagnant','attempt':prev['attempt'],'evidence_count':len(hits),'verified':prev['phase']=='completed'}
    rid='run_'+_id(gate['id'],str(attempt),digest or 'none',now()); ref=f'autonomous-run:{rid}'; pack=evidence_pack(hits)
    result={'gate_id':gate['id'],'domain':gate['domain'],'stage':gate.get('stage'),'fresh_problem':gate.get('fresh_problem'),'evidence':hits,'acceptance':gate.get('acceptance') or [],'next_action':gate.get('next_action')}
    phase='blocked'; verified=False
    if len(pack)>=int(gate.get('min_evidence') or 1) and model_call:
        synthesis=synthesize(model_call,gate,pack); critic=challenge(model_call,gate,pack,synthesis); result.update({'synthesis':synthesis,'critic':critic}); phase='assessment_ready'
        if gate['id']=='research-method-i': verified=_structural_research_method_pass(gate,pack,synthesis,critic)
        elif gate['id']=='autonomous-learning-i':
            blind=blind_assessment(model_call,gate,pack); result['blind_assessment']=blind; verified=_autonomous_learning_pass(gate,pack,synthesis,critic,blind)
    result['verified_by_executor']=verified; t=now(); final_phase='completed' if verified else phase
    conn.execute('INSERT INTO dore_autonomous_runs(id,gate_id,phase,attempt,evidence_hash,evidence_ref,result_json,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)',(rid,gate['id'],final_phase,attempt,digest,ref,json.dumps(result,ensure_ascii=False),t,t))
    lid=add_learning(conn,gate['domain'],f"Autonomous learning run {rid} for {gate['id']}.",gate.get('stage'),assessment='fresh executor assessment' if verified else 'pending stronger evidence/assessment',status='pass' if verified else ('researching' if phase=='assessment_ready' else 'blocked'),evidence_ref=ref,source_type='autonomous_executor',epistemic_state='observed')
    if verified: transition_learning(conn,lid,'verified',reason='fresh capability-gated autonomous assessment passed',evidence_ref=ref,status='pass')
    conn.commit(); return {'gate_id':gate['id'],'run_id':rid,'phase':final_phase,'attempt':attempt,'evidence_count':len(pack),'evidence_ref':ref,'verified':verified}

def run_cycle(conn,repo_root:Path,dore_root:Path,max_gates=1,model_call=None):
    ensure_schema(conn); gates=load_gates(Path(__file__).resolve().parent); p=plan(learning_status(conn),gates); executed=[]; productive=0
    for item in p.get('ready') or []:
        if productive>=max_gates: break
        r=execute_gate(conn,repo_root,dore_root,next(g for g in gates if g['id']==item['id']),model_call); executed.append(r)
        if r.get('phase')!='stagnant': productive+=1
    return {'ok':True,'policy':'bounded-autonomous-learning-v3','time_is_gate':False,'executed':executed,'planner':p,'productive_runs':productive}

def status(conn):
    ensure_schema(conn); rows=[dict(r) for r in conn.execute('SELECT * FROM dore_autonomous_runs ORDER BY updated_at DESC LIMIT 50')]
    for r in rows:
        try:r['result']=json.loads(r.pop('result_json'))
        except Exception:r['result']=None
    return {'ok':True,'runs':rows}
