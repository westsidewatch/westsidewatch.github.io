#!/usr/bin/env python3
"""Acceptance: Dimensional Writing must be a canonical, callable A2A capability."""
from __future__ import annotations
import json,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import capability_registry as registry
import capability_bindings as bindings
import a2a_adapter

CAP='publishing.dimensional-writing'

def main()->int:
 descriptor=registry.get(CAP,include_planned=True)
 binding=bindings.get(CAP)
 checks={
  'canonical_identity':bool(descriptor and descriptor.get('id')==CAP),
  'execution_binding':bool(binding and binding.get('kind')=='native' and binding.get('handler')==CAP),
 }
 envelope={
  'protocol':'dore.a2a/1','action':'dispatch','request_id':'dimensional-writing-a2a-acceptance-v0',
  'conversation_id':'cross-shadow-writing','session_id':'acceptance','consumer_id':'westside-writing',
  'capability_id':CAP,
  'payload':{'mode':'diagnose','authorThesis':'作者立意不可被改写。','manuscript':'亚伯死在田间。耶和华问该隐：你兄弟的血，有声音从地里向我哀告。'}
 }
 result=a2a_adapter.handle_universal_envelope(envelope) if checks['canonical_identity'] else None
 checks['a2a_routed']=bool(result and result.get('core_route',{}).get('execution_authority')=='a2a_execution_plane')
 checks['completion_evidence']=bool(result and result.get('status')=='succeeded' and result.get('execution',{}).get('completion_evidence'))
 checks['author_authority']=bool(result and ((result.get('result') or {}).get('report') or {}).get('authority',{}).get('mayRewriteThesis') is False)
 out={'schema':'dore.dimensional-writing-a2a-acceptance.v0','capability':CAP,'ok':all(checks.values()),'checks':checks,'result':result}
 print(json.dumps(out,ensure_ascii=False,indent=2))
 return 0 if out['ok'] else 1

if __name__=='__main__':raise SystemExit(main())
