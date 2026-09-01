#!/usr/bin/env python3
"""Explicit Doré retry policy: retries require new information."""
from __future__ import annotations
import hashlib,json,math,random,time

def fp(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,default=str).encode()).hexdigest()
def classify(previous,current,attempt,max_attempts=6,base_seconds=5,max_seconds=300):
 prev=fp(previous) if previous is not None else None;cur=fp(current)
 information_gain=prev!=cur
 if attempt>=max_attempts:return {'action':'RESEARCH_OR_STOP','reason':'retry_budget_exhausted','information_gain':information_gain,'delay_seconds':0}
 if not information_gain:return {'action':'BLOCK_IDENTICAL_RETRY','reason':'same_failure_no_information_gain','information_gain':False,'delay_seconds':0}
 raw=min(max_seconds,base_seconds*(2**max(0,attempt-1)));delay=min(max_seconds,raw+random.uniform(0,max(1,raw*0.2)))
 return {'action':'RETRY_WITH_NEW_HYPOTHESIS','reason':'new_evidence','information_gain':True,'delay_seconds':round(delay,2)}
if __name__=='__main__':print(json.dumps(classify({'e':'x'},{'e':'y'},2),ensure_ascii=False))
