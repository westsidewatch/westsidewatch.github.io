#!/usr/bin/env python3
"""Autonomy termination and human-gate policy for Doré."""
from __future__ import annotations
import json,time
DEFAULT_MAX_TURNS=50;DEFAULT_MAX_SECONDS=1800
HUMAN_ONLY={'os_security_prompt','account_login_approval','payment_approval','product_intent_change','legal_consent'}
TERMINAL={'PASS','FAIL','CANCELED','HUMAN_GATE'}
def decide(*,state,turn,started_epoch,reason=None,max_turns=DEFAULT_MAX_TURNS,max_seconds=DEFAULT_MAX_SECONDS):
 if state in TERMINAL:return {'continue':False,'terminal':state,'reason':'terminal_state'}
 if reason in HUMAN_ONLY:return {'continue':False,'terminal':'HUMAN_GATE','reason':reason}
 if turn>=max_turns:return {'continue':False,'terminal':'RESEARCH_REQUIRED','reason':'autonomous_turn_budget_exhausted'}
 if time.time()-started_epoch>=max_seconds:return {'continue':False,'terminal':'RESEARCH_REQUIRED','reason':'wall_clock_budget_exhausted'}
 return {'continue':True,'terminal':None,'reason':'within_autonomy_budget'}
if __name__=='__main__':print(json.dumps(decide(state='RUNNING',turn=1,started_epoch=time.time()),ensure_ascii=False))
