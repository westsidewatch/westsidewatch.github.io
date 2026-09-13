#!/usr/bin/env python3
from __future__ import annotations
import json
import design_intelligence_sandbox as sandbox
import design_rejection_enforcement as enforcement
import design_repair_loop as repair
import design_intelligence_a2a_worker_v7 as worker_v7


def snapshot():
    return {
      'schema':'dore.design.publish-snapshot.v1','workspace_id':'repair','revision':1,'page_id':'p',
      'page':{'id':'p','canvas':{'w':1200,'h':800},'nodes':[
        {'id':'hero','type':'text','text':'WATCH','x':100,'y':120,'w':700,'h':100,'size':56,'text_align':'left'},
        {'id':'rule','type':'rule','x':100,'y':260,'w':900,'h':1},
      ]},'tokens':{},'sha256':'base','created_at':0,
    }


def fake_ollama(_messages):
    return json.dumps({
      'repair_patch':{'schema':'dore.design.candidate-patch.v1','ops':[{'op':'font_size','node_id':'hero','size':72}]},
      'risk_domains':[],
    })


def check():
    scale=repair.repair_contract(['scale-hierarchy'])
    assert scale['repair_possible'] and scale['repairable']['scale-hierarchy']==['resize','font_size'],scale
    contrast=repair.repair_contract(['contrast-hierarchy'])
    assert not contrast['repair_possible'] and contrast['fallback_regeneration_domains']==['contrast-hierarchy'],contrast

    good={'schema':'dore.design.candidate-patch.v1','ops':[{'op':'font_size','node_id':'hero','size':72}]}
    bad={'schema':'dore.design.candidate-patch.v1','ops':[{'op':'move','node_id':'hero','x':80,'y':100}]}
    assert repair.validate_repair_ops(['scale-hierarchy'],good)['ok'] is True
    assert repair.validate_repair_ops(['scale-hierarchy'],bad)['ok'] is False

    original=sandbox.materialize(snapshot(),{'schema':'dore.design.candidate-patch.v1','ops':[{'op':'move','node_id':'hero','x':140,'y':120}]},'A')
    original['risk_domains']=['scale-hierarchy']
    before=original['snapshot']['page']['nodes'][0]
    repaired,event=worker_v7._repair_candidate(fake_ollama,{'task_context':'repair acceptance'},original,['scale-hierarchy'],1)
    assert repaired is not None and event['status']=='repaired',event
    after=repaired['snapshot']['page']['nodes'][0]
    assert after['x']==before['x']==140.0 and after['y']==before['y'],(before,after)
    assert after['size']==72.0 and after['w']==before['w'],(before,after)
    assert repaired['risk_domains']==[] and len(repaired['repair_history'])==1,repaired

    guard=[{'failure_domain':'scale-hierarchy'}]
    blocked=enforcement.enforce([original],guard)
    admitted=enforcement.enforce([repaired],guard)
    assert blocked['regeneration_required'] is True
    assert admitted['all_admitted'] is True

    unsupported,event2=worker_v7._repair_candidate(fake_ollama,{'task_context':'repair acceptance'},original,['contrast-hierarchy'],1)
    assert unsupported is None and event2['status']=='regenerate',event2

    return {'ok':True,'policy':'minimal-domain-repair-acceptance-v2','checks':{
      'repair_is_domain_specific':True,
      'unsupported_domain_falls_back_to_regeneration':True,
      'out_of_domain_op_rejected':True,
      'active_v7_repair_path_executes':True,
      'repair_preserves_unaffected_geometry':True,
      'repaired_candidate_reenters_enforcement':True,
      'repair_history_is_recorded':True,
      'repair_attempts_bounded':repair.MAX_REPAIR_ATTEMPTS==2,
    }}

if __name__=='__main__':
    out=check(); print(json.dumps(out,sort_keys=True)); raise SystemExit(0)
