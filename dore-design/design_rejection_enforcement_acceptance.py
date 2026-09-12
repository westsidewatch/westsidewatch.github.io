#!/usr/bin/env python3
from __future__ import annotations
import json
import design_rejection_enforcement as enforcement


def check():
    guardrails=[{'failure_domain':'scale-hierarchy','confidence':0.9},{'failure_domain':'alignment-drift','confidence':0.8}]
    clean=[{'candidate_id':'A','risk_domains':[]},{'candidate_id':'B','risk_domains':['spacing-rhythm']}]
    repeated=[{'candidate_id':'A','risk_domains':['scale-hierarchy']},{'candidate_id':'B','risk_domains':[]}]
    a=enforcement.enforce(clean,guardrails)
    b=enforcement.enforce(repeated,guardrails)
    assert a['all_admitted'] and not a['regeneration_required'], a
    assert not b['all_admitted'] and b['regeneration_required'], b
    assert b['blocked_count']==1, b
    assert b['candidates'][0]['repeated_failure_domains']==['scale-hierarchy'], b
    assert b['max_regenerations']==2, b
    return {'ok':True,'policy':'rejection-enforcement-acceptance-v1','checks':{'clean_admitted':True,'repeat_blocked':True,'bounded_regeneration':True}}

if __name__=='__main__':
    out=check(); print(json.dumps(out,sort_keys=True)); raise SystemExit(0)
