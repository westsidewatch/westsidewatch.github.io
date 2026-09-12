#!/usr/bin/env python3
"""Phase 15 worker: minimally repair guarded failures before regeneration."""
from __future__ import annotations
import json, os, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO_ROOT=Path(os.environ.get('DORE_REPO_ROOT') or HERE.parents[1]).resolve()
DESIGN_ROOT=REPO_ROOT/'dore-design'
if str(DESIGN_ROOT) not in sys.path: sys.path.insert(0,str(DESIGN_ROOT))
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
import design_intelligence_a2a_worker_v6 as v6
import design_repair_loop as repair
import design_local_inference as local_inference
legacy=v6.legacy
enforcement=v6.enforcement

def _repair_candidate(ollama,payload,candidate,domains,attempt):
    contract=repair.repair_contract(domains)
    if not contract['repair_possible']:
        return None, {'attempt':attempt,'status':'regenerate','contract':contract}
    system=(
      'You are Doré Design Repair. Repair only the supplied proven failure domains. '
      'Return JSON only with repair_patch and risk_domains. repair_patch schema is dore.design.candidate-patch.v1. '
      'Use only the allowed operations in repair_contract. Preserve every unaffected design decision. '
      'Do not redesign the composition and do not choose a winner.'
    )
    user=json.dumps({'task_context':payload.get('task_context'),'candidate_id':candidate.get('candidate_id'),'failure_domains':domains,'repair_contract':contract,'candidate_geometry':candidate.get('geometry'),'current_patch':candidate.get('patch'),'repair_attempt':attempt},ensure_ascii=False)
    raw=legacy._json_object(ollama([{'role':'system','content':system},{'role':'user','content':user}]))
    patch=raw.get('repair_patch') or {};validation=repair.validate_repair_ops(domains,patch)
    if not validation.get('ok'): raise ValueError('repair_patch_invalid:'+str(validation.get('reason')))
    repaired=legacy.sandbox.materialize(candidate['snapshot'],patch,candidate['candidate_id'])
    repaired['original_patch']=candidate.get('patch');repaired['repair_patch']=patch;repaired['risk_domains']=[str(x) for x in (raw.get('risk_domains') or [])]
    repaired['repair_history']=(candidate.get('repair_history') or [])+[{'attempt':attempt,'domains':list(domains),'validation':validation}]
    return repaired, {'attempt':attempt,'status':'repaired','domains':list(domains),'validation':validation}

def _repair_blocked(ollama,payload,candidates,enforcement_result):
    by_id={str(c.get('candidate_id')):c for c in candidates};trace=[];current=list(candidates)
    for attempt in range(1,repair.MAX_REPAIR_ATTEMPTS+1):
        blocked=[r for r in (enforcement_result.get('candidates') or []) if not r.get('admitted_to_critic')]
        if not blocked: break
        changed=False
        for item in blocked:
            cid=str(item.get('candidate_id'));domains=[str(x) for x in (item.get('repeated_failure_domains') or [])];source=by_id.get(cid)
            if source is None: raise RuntimeError('repair_candidate_missing:'+cid)
            repaired,event=_repair_candidate(ollama,payload,source,domains,attempt);trace.append({'candidate_id':cid,**event})
            if repaired is None: return current,enforcement_result,trace,False
            by_id[cid]=repaired;current=[by_id[str(c.get('candidate_id'))] for c in current];changed=True
        if not changed: break
        enforcement_result=enforcement.enforce(current,v6._guardrails(payload))
        if enforcement_result.get('all_admitted'): return current,enforcement_result,trace,True
    return current,enforcement_result,trace,bool(enforcement_result.get('all_admitted'))

def _model(payload):
    ollama=local_inference.ollama
    structured=local_inference.ollama_json
    base=payload['base_snapshot'];nodes=legacy.sandbox.geometry_evidence(base);guardrails=v6._guardrails(payload)
    variants,candidates=v6._generate(ollama,payload,base,nodes,0,structured_json=structured);enforcement_result=enforcement.enforce(candidates,guardrails);repair_trace=[];repaired=False
    if not enforcement_result.get('all_admitted'): candidates,enforcement_result,repair_trace,repaired=_repair_blocked(ollama,payload,candidates,enforcement_result)
    regeneration_count=0
    while not enforcement_result.get('all_admitted') and regeneration_count<enforcement.MAX_REGENERATIONS:
        regeneration_count+=1;variants,candidates=v6._generate(ollama,payload,base,nodes,regeneration_count,structured_json=structured);enforcement_result=enforcement.enforce(candidates,guardrails)
        if not enforcement_result.get('all_admitted'):
            candidates,enforcement_result,extra,was_repaired=_repair_blocked(ollama,payload,candidates,enforcement_result);repair_trace.extend(extra);repaired=repaired or was_repaired
    if not enforcement_result.get('all_admitted'): raise RuntimeError('repair_and_regeneration_exhausted')
    candidates=legacy._rasterize_candidates(payload,candidates);votes=[legacy._judge(ollama,payload,candidates,'forward'),legacy._judge(ollama,payload,candidates,'reversed')]
    consensus=votes[0]['winner']==votes[1]['winner'];usability=all(v.get('usability_floor_passed') for v in votes);brand=all(str(v.get('brand_fit','')).lower() not in {'fail','false','reject'} for v in votes);winner=votes[0]['winner'] if consensus else None;loser_failures=legacy._consensus_failures(votes) if consensus else []
    critic={'winner':winner,'consensus':consensus,'memory_admission':bool(consensus and usability and brand),'votes':votes,'winner_reason':votes[0]['winner_reason'] if consensus else '','loser_reason':votes[0]['loser_reason'] if consensus else '','loser_failures':loser_failures,'failure_domain_policy':'pixel-observable-consensus-v1','brand_fit':'pass' if brand else 'fail','usability_floor_passed':usability,'confidence':min(v['confidence'] for v in votes) if consensus else 0.0,'failure_domains':[f['domain'] for f in loser_failures],'evidence_mode':'real-browser-png+vision'}
    return {'variants':variants,'candidates':candidates,'critic':critic,'provider':'dore-local','model':local_inference.MODEL,'rejection_enforcement':enforcement_result,'repair_loop':{'policy':'minimal-domain-repair-v1','attempts':repair_trace,'repair_used':bool(repair_trace),'repair_succeeded':repaired,'regeneration_count':regeneration_count}}
legacy._model=_model
if __name__=='__main__': raise SystemExit(legacy.main())
