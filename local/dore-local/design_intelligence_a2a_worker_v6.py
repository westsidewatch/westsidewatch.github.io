#!/usr/bin/env python3
"""Phase 14 worker: enforce rejection memory before visual critique."""
from __future__ import annotations
import json, os, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO_ROOT=Path(os.environ.get('DORE_REPO_ROOT') or HERE.parents[1]).resolve()
DESIGN_ROOT=REPO_ROOT/'dore-design'
if str(DESIGN_ROOT) not in sys.path: sys.path.insert(0,str(DESIGN_ROOT))
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
import design_intelligence_a2a_worker_v5 as legacy
import design_rejection_enforcement as enforcement

def _guardrails(payload):
    return [g for g in ((payload.get('preference_pack') or {}).get('rejection_guardrails') or []) if isinstance(g,dict) and g.get('failure_domain')]
def _generate(ollama,payload,base,nodes,attempt):
    guardrails=_guardrails(payload)
    system=('You are Doré Design Core. Generate exactly two materially different, brand-faithful executable patches. Return JSON only with variants [A,B]. Each variant must contain id, direction, patch, and risk_domains. risk_domains must truthfully list any known failure-domain risk the proposal may reproduce. patch schema is dore.design.candidate-patch.v1; allowed ops: move, resize, font_size, text_align. The rejection guardrails are bounded negative precedent: do not repeat them. Do not choose a winner.')
    user=json.dumps({'task_context':payload.get('task_context'),'primary_axis':payload.get('primary_axis'),'constraints':payload.get('constraints') or [],'bounded_taste':payload.get('preference_pack') or {},'rejection_guardrails':guardrails,'regeneration_attempt':attempt,'surface_geometry':nodes},ensure_ascii=False)
    generated=legacy._json_object(ollama([{'role':'system','content':system},{'role':'user','content':user}]))
    variants=generated.get('variants') or []
    if not isinstance(variants,list) or len(variants)!=2 or [str(v.get('id')) for v in variants]!=['A','B']: raise ValueError('exactly_A_B_variants_required')
    candidates=[]
    for v in variants:
        item=legacy.sandbox.materialize(base,v.get('patch'),v['id']); item['risk_domains']=[str(x) for x in (v.get('risk_domains') or [])]; candidates.append(item)
    return variants,candidates

def _model(payload):
    from dore_local import ollama
    base=payload['base_snapshot']; nodes=legacy.sandbox.geometry_evidence(base); guardrails=_guardrails(payload); enforcement_result=None
    for attempt in range(enforcement.MAX_REGENERATIONS+1):
        variants,candidates=_generate(ollama,payload,base,nodes,attempt); enforcement_result=enforcement.enforce(candidates,guardrails)
        if enforcement_result['all_admitted']: break
        if attempt>=enforcement.MAX_REGENERATIONS: raise RuntimeError('rejection_enforcement_exhausted')
    candidates=legacy._rasterize_candidates(payload,candidates)
    votes=[legacy._judge(ollama,payload,candidates,'forward'),legacy._judge(ollama,payload,candidates,'reversed')]
    consensus=votes[0]['winner']==votes[1]['winner']; usability=all(v.get('usability_floor_passed') for v in votes); brand=all(str(v.get('brand_fit','')).lower() not in {'fail','false','reject'} for v in votes); winner=votes[0]['winner'] if consensus else None; loser_failures=legacy._consensus_failures(votes) if consensus else []
    critic={'winner':winner,'consensus':consensus,'memory_admission':bool(consensus and usability and brand),'votes':votes,'winner_reason':votes[0]['winner_reason'] if consensus else '','loser_reason':votes[0]['loser_reason'] if consensus else '','loser_failures':loser_failures,'failure_domain_policy':'pixel-observable-consensus-v1','brand_fit':'pass' if brand else 'fail','usability_floor_passed':usability,'confidence':min(v['confidence'] for v in votes) if consensus else 0.0,'failure_domains':[f['domain'] for f in loser_failures],'evidence_mode':'real-browser-png+vision'}
    return {'variants':variants,'candidates':candidates,'critic':critic,'provider':'dore-local','model':os.environ.get('DORE_MODEL') or os.environ.get('OLLAMA_MODEL') or 'local-default','rejection_enforcement':enforcement_result}
legacy._model=_model
if __name__=='__main__': raise SystemExit(legacy.main())
