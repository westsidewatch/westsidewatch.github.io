#!/usr/bin/env python3
"""Canonical handoff contract for external design-source browser evidence.

This module does not implement or own a browser. It defines the one snapshot
shape that an existing/future Doré runtime-browser collector must return before
source.probe or design.observe.capture may consume the evidence.
"""
from __future__ import annotations
from typing import Any
from urllib.parse import urlparse

SCHEMA='dore.runtime-design-capture.v1'

def _host(url:str)->str:return (urlparse(url).hostname or '').lower().rstrip('.')
def same_source(requested:str,final:str)->bool:
 a,b=_host(requested),_host(final);return bool(a and b and (a==b or a.endswith('.'+b) or b.endswith('.'+a)))

def validate(snapshot:dict[str,Any],requested_url:str)->tuple[bool,str]:
 if snapshot.get('schema')!=SCHEMA:return False,'wrong_schema'
 final=str(snapshot.get('finalUrl') or '')
 if not same_source(requested_url,final):return False,'source_identity_mismatch'
 shot=snapshot.get('screenshot') or {}
 if shot.get('real_browser_render') is not True or not shot.get('sha256'):return False,'unproven_screenshot'
 if snapshot.get('canonical_workspace_mutated') is not False:return False,'canonical_mutation_forbidden'
 if snapshot.get('production_promoted') is not False:return False,'production_promotion_forbidden'
 observer=snapshot.get('observerPayload')
 if not isinstance(observer,dict) or observer.get('schema')!='dore.design-observation-evidence.v1':return False,'design_observer_evidence_required'
 return True,'ok'

def source_probe_snapshot(snapshot:dict[str,Any])->dict[str,Any]:
 """Project design capture into source.probe's existing generic runtimeSnapshot."""
 return {'url':snapshot.get('finalUrl'),'collector':'dore.runtime-design-capture.v1','identity':snapshot.get('identity') or {},'videos':snapshot.get('videos') or [],'sources':snapshot.get('sources') or [],'tracks':snapshot.get('tracks') or [],'iframes':snapshot.get('iframes') or [],'images':snapshot.get('images') or [],'resources':snapshot.get('resources') or []}
