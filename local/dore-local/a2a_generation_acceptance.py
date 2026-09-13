#!/usr/bin/env python3
"""Acceptance gate for runtime generation identity and stale-resident detection."""
from __future__ import annotations
import hashlib,importlib.util,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'local'/'dore-local'
if str(LOCAL) not in sys.path:sys.path.insert(0,str(LOCAL))
import a2a_generation as generation
import native_host

def require(ok,msg):
 if not ok:raise AssertionError(msg)

def main():
 registry=ROOT/'dore-core'/'runtime'/'capability-registry.v1.json'
 expected=hashlib.sha256(registry.read_bytes()).hexdigest()
 base=generation.identity()
 require(base.get('schema')=='dore.a2a-runtime-generation.v1','generation schema missing')
 require(bool(base.get('runtime_generation')),'runtime generation id missing')
 require(base.get('active_registry_sha256')==expected,'active registry hash must identify loaded generation')
 require('active_control_plane_commit' in base,'active control-plane commit field missing')
 require('checkout' in base and 'commit' in base['checkout'],'current checkout state missing')
 original=generation.checkout_state
 try:
  generation.checkout_state=lambda:{'commit':'definitely-different-generation','ref':'synthetic','registry_sha256':expected}
  drift=generation.identity()
  require(drift.get('restart_required') is True,'commit drift must require out-of-band restart')
 finally:generation.checkout_state=original
 health=native_host.health_payload()
 runtime=health.get('runtime_generation') or {}
 require(runtime.get('runtime_generation')==generation.GENERATION_ID,'native health must expose resident generation')
 require('loaded_modules' in runtime,'loaded module generations missing')
 require(runtime.get('loaded_modules'),'health discovery should record loaded module source generations')
 for name,meta in runtime['loaded_modules'].items():
  require(meta.get('runtime_generation')==generation.GENERATION_ID,f'{name}: module attached to wrong generation')
  require(bool(meta.get('source_sha256')),f'{name}: source hash missing')
 spec=importlib.util.spec_from_file_location('generation_unix',LOCAL/'unix_rpc_server.py');unix=importlib.util.module_from_spec(spec);spec.loader.exec_module(unix)
 response=unix.dispatch({'jsonrpc':'2.0','id':'generation-health','method':'dore.health','params':{}})
 result=response.get('result') or {};unix_runtime=result.get('runtime_generation') or {}
 require(unix_runtime.get('runtime_generation')==generation.GENERATION_ID,'Unix health must preserve native runtime generation')
 require(result.get('restart_required')==unix_runtime.get('restart_required'),'Unix restart flag must derive from generation contract')
 print(json.dumps({'ok':True,'schema':'dore.a2a-generation-acceptance.v1','runtime_generation':generation.GENERATION_ID,'active_commit':generation.ACTIVE_COMMIT,'registry_sha256':expected,'loaded_modules':sorted(runtime['loaded_modules'])},sort_keys=True))

if __name__=='__main__':main()
