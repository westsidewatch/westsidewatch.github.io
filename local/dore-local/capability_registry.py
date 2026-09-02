#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/'dore-design'/'knowledge-lab'/'capabilities'/'registry.json'
def load_registry(path:Path=REGISTRY)->dict[str,Any]:
 data=json.loads(path.read_text(encoding='utf-8'))
 if data.get('schema')!='dore.capability-registry.v1': raise ValueError('unsupported capability registry schema')
 return data
def discover(*,capability_type:str|None=None,service:str|None=None,include_planned:bool=False)->list[dict[str,Any]]:
 out=[]
 for item in load_registry().get('capabilities',[]):
  if not include_planned and item.get('status')!='existing': continue
  if capability_type and item.get('type')!=capability_type: continue
  if service and item.get('service')!=service: continue
  out.append(item)
 return out
def get(capability_id:str,*,include_planned:bool=False)->dict[str,Any]|None:
 return next((x for x in discover(include_planned=include_planned) if x.get('id')==capability_id),None)
if __name__=='__main__': print(json.dumps(discover(include_planned=True),ensure_ascii=False,indent=2))
