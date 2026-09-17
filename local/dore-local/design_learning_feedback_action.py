#!/usr/bin/env python3
"""Beautiful-Gate feedback admission for Doré Design Learning.

A candidate can influence future search priorities only after a proven real
render and explicit human Beautiful Gate decision. This action never writes
canonical design and never promotes production.
"""
from __future__ import annotations
from typing import Any
CAPABILITIES={'design.learning.feedback'}

def execute(capability:str,args:dict[str,Any]|None=None)->dict[str,Any]:
 if capability not in CAPABILITIES:return {'ok':False,'status':'failed','error':{'code':'unsupported_action','message':capability}}
 a=args or {};candidate=a.get('candidate') or {};render=a.get('renderEvidence') or {};gate=a.get('beautifulGate') or {}
 if candidate.get('schema')!='dore.design-grammar-candidate.v1':return {'ok':False,'status':'failed','reason':'candidate_required'}
 if render.get('real_browser_render') is not True or not render.get('sha256'):return {'ok':False,'status':'not_ready','reason':'real_render_required'}
 if gate.get('authority')!='human' or gate.get('decision') not in ('accept','reject'):return {'ok':False,'status':'not_ready','reason':'human_beautiful_gate_required'}
 accepted=gate['decision']=='accept';sources=((candidate.get('evidence') or {}).get('sourceIds') or [])
 return {'ok':True,'status':'completed','candidateId':candidate.get('id'),'beautifulGate':{'decision':gate['decision'],'authority':'human'},'learning':{'eligible':accepted,'target':'ui-skill-growth' if accepted else 'negative-feedback','sourceIds':sources,'canonicalWrite':False,'productionPromotion':False},'nextCycleFeedback':{'rewardSourceContinuity':sources if accepted else [],'penalizePattern':candidate.get('id') if not accepted else None,'preserveDiversityFloor':True,'allowSourceMonoculture':False},'authority':{'class':'learning-feedback-only','mayPromoteCanonical':False,'requiresHumanAuthorityForCanonicalPromotion':True}}
