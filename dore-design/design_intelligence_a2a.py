#!/usr/bin/env python3
"""Doré Design -> Core/A2A executable exploration bridge."""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

import design_intelligence_runtime as intelligence
import design2_snapshot
import app_workspace

REPO_ROOT = Path(__file__).resolve().parent.parent
LOCAL_DORE = REPO_ROOT / 'local' / 'dore-local'
if str(LOCAL_DORE) not in sys.path: sys.path.insert(0, str(LOCAL_DORE))
import a2a_execution_plane as plane


def _home(): return Path(os.environ.get('DORE_LOCAL_HOME', Path.home() / '.dore')).expanduser()
def _request_path(task_id): return _home()/'design-intelligence-a2a'/'requests'/f'{task_id}.json'

def _write_request(task_id,payload):
    target=_request_path(task_id); target.parent.mkdir(parents=True,exist_ok=True); tmp=target.with_suffix('.tmp')
    tmp.write_text(json.dumps(payload,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8'); tmp.replace(target); return target

def _worker(task_id):
    env=dict(os.environ); env['DORE_REPO_ROOT']=str(REPO_ROOT)
    cp=subprocess.run([sys.executable,str(LOCAL_DORE/'design_intelligence_a2a_worker.py'),task_id],cwd=str(REPO_ROOT),env=env,text=True,capture_output=True,timeout=max(30,int(os.environ.get('DORE_DESIGN_A2A_TIMEOUT','360'))))
    if cp.returncode!=0: raise RuntimeError('design_a2a_worker_failed:'+(cp.stderr or cp.stdout or '')[-3000:])
    try:return json.loads((cp.stdout or '').strip().splitlines()[-1])
    except Exception as exc: raise RuntimeError('design_a2a_worker_invalid_result') from exc

def _base_snapshot(payload):
    supplied=payload.get('base_snapshot')
    if isinstance(supplied,dict):
        if supplied.get('schema')!='dore.design.publish-snapshot.v1': raise ValueError('invalid_base_snapshot_schema')
        return copy.deepcopy(supplied)
    if not app_workspace.WS.exists(): raise ValueError('design_workspace_missing_for_sandbox')
    workspace=json.loads(app_workspace.WS.read_text(encoding='utf-8'))
    pages=workspace.get('pages') or []
    if not pages: raise ValueError('design_workspace_has_no_pages')
    requested=str(payload.get('page_id') or '').strip()
    page_id=requested if requested and any(p.get('id')==requested for p in pages) else str(pages[0].get('id'))
    return design2_snapshot.snapshot(workspace,page_id)

def explore(payload):
    routed=intelligence.route_task(payload)
    if routed.get('decision')!='explore':
        return {'ok':True,'decision':'exploit','exploration_started':False,'route':routed,'reason':'stable_contextual_preference_available'}
    task_id='design-explore-'+uuid.uuid4().hex
    base_snapshot=_base_snapshot(payload)
    request={
      'schema':'dore.design-intelligence-a2a-request.v3','task_id':task_id,'surface_id':payload.get('surface_id'),
      'surface_family':payload.get('surface_family'),'task_context':payload.get('task_context'),'primary_axis':payload.get('primary_axis'),
      'viewport_context':payload.get('viewport_context'),'content_context':payload.get('content_context'),'constraints':payload.get('constraints') or [],
      'preference_pack':routed.get('preference_pack') or {},'base_snapshot':base_snapshot,
      'inference_boundary':'core-a2a-only','judge_policy':'blind-order-reversal-consensus-v1','candidate_policy':'immutable-executable-sandbox-v1',
    }
    request_path=_write_request(task_id,request)
    task=plane.register({'message_id':task_id,'kind':'dore_design_intelligence_explore','related_goal':'dore-design-intelligence','body':{'request_path':str(request_path)}})
    if task.get('status')!='ACCEPTED': raise RuntimeError('design_a2a_task_not_accepted')
    worker_result=_worker(task_id); proof=plane.status(task_id)
    if not proof.get('completion_evidence'): raise RuntimeError('design_a2a_completion_evidence_missing')
    artifact=(proof.get('task') or {}).get('artifact') or {}
    variants=artifact.get('variants') or worker_result.get('variants') or []
    candidates=artifact.get('candidates') or worker_result.get('candidates') or []
    critic=artifact.get('critic') or worker_result.get('critic') or {}
    by_id={str(v.get('id')):v for v in variants if isinstance(v,dict)}
    if set(by_id)!={'A','B'} or len(candidates)!=2: raise RuntimeError('design_a2a_executable_candidates_missing')
    if any(not c.get('render_sha256') or not c.get('geometry') for c in candidates): raise RuntimeError('design_a2a_candidate_evidence_missing')
    votes=critic.get('votes') or []
    if len(votes)!=2 or any(v.get('winner') not in {'A','B'} for v in votes): raise RuntimeError('design_a2a_blind_votes_missing')
    consensus=bool(critic.get('consensus')); memory_admission=bool(critic.get('memory_admission')); winner=str(critic.get('winner') or '') if consensus else ''
    observed=None; route_after=None
    if consensus and memory_admission:
        if winner not in by_id: raise RuntimeError('design_a2a_consensus_winner_missing')
        observed=intelligence.record_observed_comparison({**payload,'candidate_a':'A','candidate_b':'B','winner':winner,'winner_reason':str(critic.get('winner_reason') or ''),'loser_reason':str(critic.get('loser_reason') or ''),'brand_fit':critic.get('brand_fit'),'usability_floor_passed':bool(critic.get('usability_floor_passed')),'confidence':float(critic.get('confidence',0.5)),'evidence_refs':['a2a-task:'+task_id,'a2a-artifact:'+str(artifact.get('sha256') or 'recorded'),'sandbox-render:A:'+str(candidates[0].get('render_sha256')),'sandbox-render:B:'+str(candidates[1].get('render_sha256')),'blind-judge:2','order-bias-check:pass','visual-critic:'+winner],'scope':payload.get('scope') or 'local'})
        route_after=observed.get('updated')
    return {
      'ok':True,'decision':'explore','exploration_started':True,'task_id':task_id,'a2a_status':'PASS','completion_evidence':True,
      'provider':artifact.get('provider') or worker_result.get('provider'),'model':artifact.get('model') or worker_result.get('model'),
      'variants':variants,'candidates':candidates,'candidate_evidence':'executable-sandbox-render+geometry','canonical_workspace_mutated':False,
      'critic':critic,'judge_count':len(votes),'blind_order_reversal':True,'consensus':consensus,'winner':winner or None,
      'memory_admitted':bool(observed),'writeback':observed,'writeback_block_reason':None if observed else ('judge_disagreement' if not consensus else 'usability_or_brand_floor_failed'),
      'requires_more_evidence':not bool(observed),'route_before':routed,'route_after':route_after,'production_promoted':False,'inference_boundary':'core-a2a-only',
    }

def health():
    worker=LOCAL_DORE/'design_intelligence_a2a_worker.py'
    return {'ok':worker.exists(),'phase':9,'capability_phase':11,'policy':'dore-design-executable-sandbox-loop-v1','worker_available':worker.exists(),'inference_boundary':'core-a2a-only','design_process_has_model_client':False,'blind_order_reversal':True,'minimum_judges':2,'taste_writeback_requires_consensus':True,'executable_candidate_sandbox':True,'canonical_workspace_mutation_allowed':False,'fixture_mode':os.environ.get('DORE_DESIGN_A2A_FIXTURE')=='1','production_promotion':False}
