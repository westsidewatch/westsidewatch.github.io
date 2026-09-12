#!/usr/bin/env python3
"""Core/A2A worker for executable Doré Design exploration candidates."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import a2a_execution_plane as plane

REPO_ROOT = Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).resolve()
DESIGN_ROOT = REPO_ROOT / 'dore-design'
if str(DESIGN_ROOT) not in sys.path:
    sys.path.insert(0, str(DESIGN_ROOT))
import design_intelligence_sandbox as sandbox

HOME = Path(os.environ.get('DORE_LOCAL_HOME', Path.home() / '.dore')).expanduser()
ROOT = HOME / 'design-intelligence-a2a'
REQUESTS = ROOT / 'requests'


def _request_path(task_id: str) -> Path:
    return REQUESTS / f'{task_id}.json'


def _json_object(text: str) -> dict:
    raw = str(text or '').strip()
    if raw.startswith('```'):
        lines = raw.splitlines()[1:]
        if lines and lines[-1].strip() == '```': lines = lines[:-1]
        raw = '\n'.join(lines).strip()
    start, end = raw.find('{'), raw.rfind('}')
    if start < 0 or end < start: raise ValueError('model_json_object_missing')
    obj = json.loads(raw[start:end + 1])
    if not isinstance(obj, dict): raise ValueError('model_json_object_required')
    return obj


def _first_node(snapshot):
    nodes = ((snapshot.get('page') or {}).get('nodes') or [])
    if not nodes: raise ValueError('sandbox_surface_has_no_nodes')
    return nodes[0]


def _fixture(payload: dict) -> dict:
    node = _first_node(payload['base_snapshot'])
    nid = str(node.get('id'))
    x = float(node.get('x', 0) or 0); y = float(node.get('y', 0) or 0)
    size = float(node.get('size', 24) or 24)
    variants = [
        {'id':'A','direction':'preserve-current-gravity','patch':{'schema':'dore.design.candidate-patch.v1','ops':[{'op':'move','node_id':nid,'x':x,'y':y+4}]}},
        {'id':'B','direction':'clarify-focal-gravity','patch':{'schema':'dore.design.candidate-patch.v1','ops':[{'op':'move','node_id':nid,'x':x,'y':max(0,y-12)},{'op':'font_size','node_id':nid,'size':min(320,max(6,size+4))}]}},
    ]
    candidates = [sandbox.materialize(payload['base_snapshot'], v['patch'], v['id']) for v in variants]
    disagree = os.environ.get('DORE_DESIGN_A2A_DISAGREE_FIXTURE') == '1'
    votes = [
        {'presentation':'forward','winner':'B','winner_reason':'B has clearer focal geometry.','loser_reason':'A changes the composition too little.','brand_fit':'pass','usability_floor_passed':True,'confidence':0.88},
        {'presentation':'reversed','winner':'A' if disagree else 'B','winner_reason':'Reversed-order check.','loser_reason':'Reversed-order check loser.','brand_fit':'pass','usability_floor_passed':True,'confidence':0.84},
    ]
    consensus = votes[0]['winner'] == votes[1]['winner']
    winner = votes[0]['winner'] if consensus else None
    critic = {
        'winner': winner,'consensus':consensus,'memory_admission':bool(consensus),'votes':votes,
        'winner_reason': votes[0]['winner_reason'] if consensus else '',
        'loser_reason': votes[0]['loser_reason'] if consensus else '',
        'brand_fit':'pass','usability_floor_passed':True,
        'confidence': min(v['confidence'] for v in votes) if consensus else 0.0,
        'failure_domains': [] if consensus else ['judge-disagreement'],
    }
    return {'variants':variants,'candidates':candidates,'critic':critic,'provider':'deterministic-ci-fixture','model':'fixture'}


def _judge(ollama, payload, candidates, presentation):
    ordered = candidates if presentation == 'forward' else list(reversed(candidates))
    aliases = {'X': ordered[0]['candidate_id'], 'Y': ordered[1]['candidate_id']}
    compact=[]
    for alias,c in zip(('X','Y'),ordered):
        compact.append({'alias':alias,'patch':c['patch'],'render_sha256':c['render_sha256'],'geometry':c['geometry']})
    system=(
      'You are an independent Doré design critic. Judge only the two anonymized executable sandbox candidates. '
      'Use actual patch and rendered geometry evidence, brand constraints, usability floor, and task context. '
      'Return JSON only: winner (X or Y), winner_reason, loser_reason, brand_fit, usability_floor_passed, confidence, failure_domains.'
    )
    user=json.dumps({'task_context':payload.get('task_context'),'primary_axis':payload.get('primary_axis'),'constraints':payload.get('constraints') or [],'candidates':compact},ensure_ascii=False)
    raw=_json_object(ollama([{'role':'system','content':system},{'role':'user','content':user}]))
    if raw.get('winner') not in {'X','Y'}: raise ValueError('critic_winner_required')
    canonical=aliases[raw['winner']]
    out={**raw,'winner':canonical,'presentation':presentation,'confidence':max(0.0,min(1.0,float(raw.get('confidence',0.5)))),'usability_floor_passed':bool(raw.get('usability_floor_passed'))}
    if not str(out.get('winner_reason') or '').strip() or not str(out.get('loser_reason') or '').strip(): raise ValueError('critic_reasons_required')
    return out


def _model(payload: dict) -> dict:
    from dore_local import ollama
    base = payload['base_snapshot']
    nodes = sandbox.geometry_evidence(base)
    system=(
      'You are Doré Design Core. Generate exactly two materially different, brand-faithful executable patches against the supplied node geometry. '
      'Return JSON only with variants [A,B]. Each variant must contain id, direction, and patch. patch schema is dore.design.candidate-patch.v1 and ops may only be '
      'move(node_id,x,y), resize(node_id,w,h), font_size(node_id,size), text_align(node_id,value). Do not choose a winner.'
    )
    user=json.dumps({'task_context':payload.get('task_context'),'primary_axis':payload.get('primary_axis'),'constraints':payload.get('constraints') or [],'bounded_taste':payload.get('preference_pack') or {},'surface_geometry':nodes},ensure_ascii=False)
    generated=_json_object(ollama([{'role':'system','content':system},{'role':'user','content':user}]))
    variants=generated.get('variants') or []
    if not isinstance(variants,list) or len(variants)!=2 or [str(v.get('id')) for v in variants]!=['A','B']: raise ValueError('exactly_A_B_variants_required')
    candidates=[]
    for v in variants:
        candidates.append(sandbox.materialize(base,v.get('patch'),v['id']))
    votes=[_judge(ollama,payload,candidates,'forward'),_judge(ollama,payload,candidates,'reversed')]
    consensus=votes[0]['winner']==votes[1]['winner']
    usability=all(v.get('usability_floor_passed') for v in votes)
    brand=all(str(v.get('brand_fit','')).lower() not in {'fail','false','reject'} for v in votes)
    winner=votes[0]['winner'] if consensus else None
    critic={
      'winner':winner,'consensus':consensus,'memory_admission':bool(consensus and usability and brand),'votes':votes,
      'winner_reason':votes[0]['winner_reason'] if consensus else '','loser_reason':votes[0]['loser_reason'] if consensus else '',
      'brand_fit':'pass' if brand else 'fail','usability_floor_passed':usability,
      'confidence':min(v['confidence'] for v in votes) if consensus else 0.0,
      'failure_domains':[] if consensus else ['judge-disagreement'],
    }
    return {'variants':variants,'candidates':candidates,'critic':critic,'provider':'dore-local','model':os.environ.get('DORE_MODEL') or os.environ.get('OLLAMA_MODEL') or 'local-default'}


def execute(task_id: str) -> dict:
    path=_request_path(task_id)
    if not path.exists(): raise FileNotFoundError('design_intelligence_request_missing:'+task_id)
    payload=json.loads(path.read_text(encoding='utf-8'))
    sandbox.geometry_evidence(payload.get('base_snapshot') or {})
    owner=plane.worker_id(); claimed=plane.claim(task_id,owner)
    if not claimed.get('ok'): raise RuntimeError('a2a_claim_failed:'+str(claimed.get('code')))
    started=plane.transition(task_id,'RUNNING',consumer=owner)
    if not started.get('ok'): raise RuntimeError('a2a_start_failed:'+str(started.get('code')))
    try:
        result=_fixture(payload) if os.environ.get('DORE_DESIGN_A2A_FIXTURE')=='1' else _model(payload)
        artifact={
          'type':'dore.design-intelligence-exploration.v3','task_id':task_id,'surface_id':payload.get('surface_id'),
          'variants':result['variants'],'candidates':result['candidates'],'critic':result['critic'],'provider':result['provider'],'model':result['model'],
          'canonical_workspace_mutated':False,'evidence_kind':'executable-sandbox-render+geometry',
        }
        recorded=plane.record_artifact(task_id,artifact,consumer=owner)
        if not recorded.get('ok'): raise RuntimeError('a2a_artifact_failed:'+str(recorded.get('code')))
        critic=result['critic']; candidates=result['candidates']
        verification={
          'ok':len(candidates)==2 and all(c.get('render_sha256') and c.get('geometry') for c in candidates) and len(critic.get('votes') or [])==2,
          'method':'dore.design-intelligence-a2a-worker.v3','blind_order_reversal':True,'judge_count':2,
          'executable_candidate_artifacts':True,'canonical_workspace_mutated':False,
        }
        verified=plane.verify(task_id,verification,consumer=owner)
        if not verified.get('ok'): raise RuntimeError('a2a_verification_failed')
        completed=plane.complete(task_id,{'ok':True,**result},consumer=owner)
        if not completed.get('ok'): raise RuntimeError('a2a_complete_failed:'+str(completed.get('code')))
        return {'ok':True,'task_id':task_id,'status':'PASS',**result}
    except Exception as exc:
        try: plane.transition(task_id,'FAIL',consumer=owner,result={'ok':False,'error':type(exc).__name__+': '+str(exc)})
        except Exception: pass
        raise


def main():
    if len(sys.argv)!=2: raise SystemExit('usage: design_intelligence_a2a_worker.py <task-id>')
    print(json.dumps(execute(sys.argv[1]),ensure_ascii=False)); return 0

if __name__=='__main__': raise SystemExit(main())
