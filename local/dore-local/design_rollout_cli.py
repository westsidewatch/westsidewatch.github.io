#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
import production_actions

p=argparse.ArgumentParser()
p.add_argument('--ref',required=True)
p.add_argument('--expected-sha',required=True)
p.add_argument('--page-id',default='')
p.add_argument('--verify-marker',action='append',default=[])
a=p.parse_args()
result=production_actions.design_production_rollout({
    'ref':a.ref,
    'expected_sha':a.expected_sha,
    'page_id':a.page_id,
    'verify_markers':a.verify_marker,
})
print(json.dumps(result,ensure_ascii=False,sort_keys=True))
raise SystemExit(0 if result.get('ok') else 1)
