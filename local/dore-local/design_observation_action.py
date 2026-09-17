#!/usr/bin/env python3
"""Design Observation A2A action.

This action is intentionally fail-closed. Doré's existing Design Intelligence
browser raster proves generated candidate rendering; it does NOT by itself
prove navigation to an arbitrary external URL. External design observation may
complete only from a runtime snapshot whose final URL and screenshot identity
are explicitly tied to the requested source.
"""
from __future__ import annotations
from typing import Any
from urllib.parse import urlparse

CAPABILITIES={"design.observe.capture"}

def _host(url:str)->str:return (urlparse(url).hostname or '').lower().rstrip('.')
def _same_source(requested:str,final:str)->bool:
 a,b=_host(requested),_host(final);return bool(a and b and (a==b or a.endswith('.'+b) or b.endswith('.'+a)))

def execute(capability:str,args:dict[str,Any]|None=None)->dict[str,Any]:
 if capability not in CAPABILITIES:return {'ok':False,'status':'failed','error':{'code':'unsupported_action','message':capability}}
 args=args or {};url=str(args.get('url') or '').strip();source_id=str(args.get('sourceId') or '').strip();viewport=str(args.get('viewport') or 'desktop')
 if not url.startswith('https://') or not source_id:return {'ok':False,'status':'failed','error':{'code':'invalid_args','message':'https url and sourceId required'}}
 snap=args.get('runtimeSnapshot')
 if not isinstance(snap,dict):
  return {'ok':False,'status':'not_ready','capability':capability,'sourceId':source_id,'reason':'external_navigation_evidence_required','needs':['runtime-browser-navigation','source-bound-screenshot','design-observer-payload']}
 final_url=str(snap.get('finalUrl') or snap.get('url') or '').strip();shot=snap.get('screenshot') or {};sha=str(shot.get('sha256') or snap.get('screenshotSha256') or '').strip();real=shot.get('real_browser_render') is True or snap.get('real_browser_render') is True
 if not final_url or not _same_source(url,final_url):return {'ok':False,'status':'failed','capability':capability,'sourceId':source_id,'error':{'code':'source_identity_mismatch','message':'runtime final URL is not tied to requested source'}}
 if not real or not sha:return {'ok':False,'status':'not_ready','capability':capability,'sourceId':source_id,'reason':'unproven_source_screenshot'}
 if snap.get('canonical_workspace_mutated') is not False or snap.get('production_promoted') is not False:return {'ok':False,'status':'failed','capability':capability,'sourceId':source_id,'error':{'code':'authority_boundary_violation','message':'observation capture mutated canonical workspace or promoted production'}}
 observer=snap.get('observerPayload');observer_ok=isinstance(observer,dict) and observer.get('schema')=='dore.design-observation-evidence.v1'
 return {'ok':True,'status':'completed','capability':capability,'sourceId':source_id,'viewport':viewport,'url':url,'finalUrl':final_url,'renderedAt':snap.get('renderedAt'),'screenshotRef':shot.get('ref') or snap.get('screenshotRef'),'rasterEvidence':[{'real_browser_render':True,'sha256':sha}],'observerPayload':observer if observer_ok else None,'observerStatus':'captured' if observer_ok else 'missing','canonical_workspace_mutated':False,'production_promoted':False,'authority':{'class':'observational-evidence','mayPromoteCanonical':False,'requiresBeautifulGate':True}}
