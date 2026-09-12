#!/usr/bin/env python3
"""Static contract for the real-Mac Doré Design Intelligence acceptance path."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;LOCAL=ROOT/'local'/'dore-local'
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def check():
 action=load('design_live_acceptance_action',LOCAL/'design_live_acceptance_action.py')
 assert 'design.intelligence.live.acceptance' in action.CAPABILITIES
 source=(LOCAL/'design_live_acceptance_action.py').read_text(encoding='utf-8');native=(LOCAL/'native_host.py').read_text(encoding='utf-8');relay=(LOCAL/'github_issue_bridge.py').read_text(encoding='utf-8');unix=(LOCAL/'unix_rpc_server.py').read_text(encoding='utf-8')
 assert "pop('DORE_DESIGN_A2A_FIXTURE'" in source
 assert 'bridge.explore' in source and 'second_reads_rejection_memory' in source
 assert 'first_real_browser_pixels' in source and 'production_not_promoted' in source and 'canonical_workspace_unchanged' in source
 assert 'design_live_acceptance_action' in native and '_execute(name,cap,args)' in native
 assert 'PRODUCTION=_load' not in native and 'BUS=_load' not in native
 assert 'native_host.route_payload' in unix and 'native_host.health_payload' in unix
 assert 'design.intelligence.live.acceptance' in relay
 return {'ok':True,'policy':'dore-design-real-model-a2a-live-contract-v2','lazy_optional_core':True}
if __name__=='__main__':
 import json
 out=check();print(json.dumps(out,sort_keys=True));raise SystemExit(0)
