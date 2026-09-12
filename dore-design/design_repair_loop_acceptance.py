#!/usr/bin/env python3
from __future__ import annotations
import json
import design_intelligence_sandbox as sandbox
import design_rejection_enforcement as enforcement
import design_repair_loop as repair


def snapshot():
    return {
      'schema':'dore.design.publish-snapshot.v1','workspace_id':'repair','revision':1,'page_id':'p',
      'page':{'id':'p','canvas':{'w':1200,'h':800},'nodes':[
        {'id':'hero','type':'text','text':'WATCH','x':100,'y':120,'w':700,'h':100,'size':56,'text_align':'left'},
        {'id':'rule','type':'rule','x':100,'y':260,'w':900,'h':1},
      ]},'tokens':{},'sha256':'base','created_at':0,
    }


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
    before=original['snapshot']['page']['nodes'][0]
    repaired=sandbox.materialize(original['snapshot'],good,'A')
    after=repaired['snapshot']['page']['nodes'][0]
    assert after['x']==before['x']==140.0 and after['y']==before['y'],(before,after)
    assert after['size']==72.0 and after['w']==before['w'],(before,after)

    guard=[{'failure_domain':'scale-hierarchy'}]
    blocked=enforcement.enforce([{'candidate_id':'A','risk_domains':['scale-hierarchy']}],guard)
    admitted=enforcement.enforce([{'candidate_id':'A','risk_domains':[]}],guard)
    assert blocked['regeneration_required'] is True
    assert admitted['all_admitted'] is True

    return {'ok':True,'policy':'minimal-domain-repair-acceptance-v1','checks':{
      'repair_is_domain_specific':True,
      'unsupported_domain_falls_back_to_regeneration':True,
      'out_of_domain_op_rejected':True,
      'repair_preserves_unaffected_geometry':True,
      'repaired_candidate_can_reenter_enforcement':True,
      'repair_attempts_bounded':repair.MAX_REPAIR_ATTEMPTS==2,
    }}

if __name__=='__main__':
    out=check(); print(json.dumps(out,sort_keys=True)); raise SystemExit(0)
