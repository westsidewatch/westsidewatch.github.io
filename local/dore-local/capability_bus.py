#!/usr/bin/env python3
"""Doré semantic capability bus.

Capability identity and semantic descriptors come only from the canonical Core
registry. This bus resolves execution through capability_bindings; it must not
create or override capability identity.
"""
from __future__ import annotations
import importlib.util,json,os,sys
from pathlib import Path
from typing import Any
from urllib import request
from dore_core.bible.query_planner import plan_bible_query
from dore_core.retrieval.living import retrieve as living_retrieve
from dore_core.substrates.longmemory import LongMemoryConfig,available as longmemory_available,recall as longmemory_recall
from dore_core.substrates.qmd import PRODUCTION_COLLECTION,QMDConfig,available as qmd_available,production_config,search as qmd_search
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];DESIGN_ROOT=ROOT/'dore-design'
def _load_sibling(name:str):
 path=HERE/f'{name}.py';spec=importlib.util.spec_from_file_location(f'dore_bus_{name}',path)
 if spec is None or spec.loader is None:raise RuntimeError(f'cannot load {path}')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
REGISTRY=_load_sibling('capability_registry');BINDINGS=_load_sibling('capability_bindings');BOOK_INTELLIGENCE=_load_sibling('book_intelligence_capability');DIMENSIONAL_WRITING=_load_sibling('dimensional_writing_capability')
def _post_json(url:str,payload:dict[str,Any],headers:dict[str,str]|None=None,timeout:int=1500)->dict[str,Any]:
 raw=json.dumps(payload,ensure_ascii=False).encode('utf-8');merged={'Content-Type':'application/json','Accept':'application/json'};merged.update(headers or {});req=request.Request(url,data=raw,method='POST',headers=merged)
 with request.urlopen(req,timeout=timeout) as response:return json.loads(response.read().decode('utf-8'))
def discover(production=None,*,include_planned:bool=False)->list[dict[str,Any]]:
 out=[]
 for item in REGISTRY.discover(include_planned=include_planned):
  descriptor=dict(item);descriptor['owner']='dore-core';descriptor['callable']=BINDINGS.get(str(descriptor.get('id'))) is not None;out.append(descriptor)
 return sorted(out,key=lambda item:str(item.get('id') or ''))
def resolve(capability:str,production=None)->dict[str,Any]|None:
 item=REGISTRY.get(capability,include_planned=True)
 if item is None:return None
 descriptor=dict(item);descriptor['owner']='dore-core';descriptor['callable']=BINDINGS.get(capability) is not None;return descriptor
def _ollama_json_infer(messages:list[dict[str,str]])->str:
 runtime=_load_sibling('dore_local');base_url=str(getattr(runtime,'OLLAMA_BASE_URL',os.environ.get('OLLAMA_BASE_URL') or 'http://127.0.0.1:11434')).rstrip('/');model=str(getattr(runtime,'MODEL',os.environ.get('DORE_LOCAL_MODEL') or 'gemma4:e4b'))
 response=_post_json(f'{base_url}/api/chat',{'model':model,'messages':messages,'stream':False,'think':False,'format':'json'});message=response.get('message') if isinstance(response,dict) else None;content=message.get('content') if isinstance(message,dict) else None
 if not isinstance(content,str):raise RuntimeError('structured Doré inference returned no message content')
 return content
def _image_generate(args:dict[str,Any],caller_product:str|None=None)->dict[str,Any]:
 message=str(args.get('message') or args.get('prompt') or '').strip()
 if not message:return {'ok':False,'status':'failed','error':{'code':'invalid_args','message':'message or prompt is required'}}
 payload=dict(args);payload['message']=message;origin=caller_product or 'dore-core';result=_post_json('http://127.0.0.1:8790/generate',payload,{'X-Dore-Origin':origin})
 if isinstance(result,dict):result=dict(result);result['core_route']={'capability':'image.generate','caller_product':caller_product,'provider':'dore-image-local','transport':'core-adapter'}
 return result
def _book_intelligence(args:dict[str,Any])->dict[str,Any]:return BOOK_INTELLIGENCE.execute(args,_ollama_json_infer)
def _dimensional_writing(args:dict[str,Any])->dict[str,Any]:return DIMENSIONAL_WRITING.execute(args,_ollama_json_infer)
def _load_local_capability(module_name:str,args:dict[str,Any])->dict[str,Any]:
 local_path=str(HERE);inserted=local_path not in sys.path
 if inserted:sys.path.insert(0,local_path)
 try:return _load_sibling(module_name).execute(args)
 finally:
  if inserted:
   try:sys.path.remove(local_path)
   except ValueError:pass
def _reflex_project(args):return _load_local_capability('reflex_capability',args)
def _translation_project(args):return _load_local_capability('translation_capability',args)
def _design_intelligence(args):
 if not DESIGN_ROOT.is_dir():raise RuntimeError('dore_design_runtime_missing')
 inserted=str(DESIGN_ROOT) not in sys.path
 if inserted:sys.path.insert(0,str(DESIGN_ROOT))
 try:
  path=DESIGN_ROOT/'design_intelligence_a2a.py';spec=importlib.util.spec_from_file_location('dore_bus_design_intelligence',path)
  if spec is None or spec.loader is None:raise RuntimeError('design_intelligence_loader_unavailable')
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);result=module.explore(dict(args))
  if isinstance(result,dict):result=dict(result);result.setdefault('status','completed' if result.get('ok') else 'failed');result.setdefault('capability','design.intelligence')
  return result
 finally:
  if inserted:
   try:sys.path.remove(str(DESIGN_ROOT))
   except ValueError:pass
def _search_host(args,caller_product):
 explicit=str(args.get('host') or '').strip().lower()
 if explicit:return explicit
 product=str(caller_product or '').strip().lower()
 if product=='one' or product.startswith('one-'):return 'one'
 if product=='multiwrite' or product.startswith('multiwrite-'):return 'multiwrite'
 return 'unknown'
def _bible_query_plan(args):
 query=str(args.get('query') or args.get('text') or '').strip()
 if not query:return {'ok':False,'status':'failed','error':{'code':'invalid_args','message':'query or text is required'}}
 plan=plan_bible_query(query,explicit_search=bool(args.get('explicit_search',False)),deep=bool(args.get('deep',False)));return {'ok':True,'status':'completed','capability':'bible.query-plan','plan':plan.to_dict(),'dore_identity':True,'large_model_invoked':False}
def _fuzzy_search(args,caller_product=None):
 query=str(args.get('query') or args.get('text') or '').strip()
 if not query:return {'ok':False,'status':'failed','error':{'code':'invalid_args','message':'query or text is required'}}
 if not qmd_available():return {'ok':False,'status':'not_ready','capability':'context.fuzzy-search','authority':False,'error':{'code':'substrate_unavailable','message':'local retrieval substrate is not installed on this runtime'}}
 bible_plan=plan_bible_query(query,explicit_search=bool(args.get('explicit_search',False)),deep=bool(args.get('deep',False)));requested_collection=str(args.get('collection') or os.environ.get('DORE_QMD_COLLECTION') or '').strip();qmd_config=production_config(collection=PRODUCTION_COLLECTION) if not requested_collection or requested_collection==PRODUCTION_COLLECTION else QMDConfig(collection=requested_collection);db=Path(os.environ.get('DORE_LONGMEMORY_DB') or (Path.home()/'.dore'/'knowledge'/'longmemory.db'));project=str(args.get('project') or os.environ.get('DORE_LONGMEMORY_PROJECT') or 'dore');memory_config=LongMemoryConfig(db=db,project=project)
 def search_documents(text,*,semantic,deep,limit):return qmd_search(text,qmd_config,semantic=semantic,deep=deep,limit=limit)
 def recall_current(text,*,mode):return longmemory_recall(text,memory_config,mode=mode) if longmemory_available() else {'ok':False,'authority':False,'error':'memory_unavailable'}
 internal=living_retrieve(query,qmd_search=search_documents,memory_recall=recall_current,explicit_search=bool(args.get('explicit_search',False)),deep_requested=bool(args.get('deep',False)),limit=int(args.get('limit') or 8),host=_search_host(args,caller_product),mode=str(args.get('mode') or 'prepare').strip().lower(),embedded=bool(args.get('embedded',False)));plan=internal['plan'];return {'ok':internal.get('ok',False),'status':'completed' if internal.get('ok',False) else 'failed','capability':'context.fuzzy-search','query':query,'results':internal.get('results',[]),'retrieval':{'lexical':plan.lexical,'semantic':plan.semantic,'deep':plan.deep,'memory_recall':plan.recall_memory,'reason':plan.reason},'bible_plan':bible_plan.to_dict(),'authority':False,'large_model_invoked':False}
def _knowledge_recall(args):
 query=str(args.get('query') or args.get('text') or '').strip()
 if not query:return {'ok':False,'status':'failed','error':{'code':'invalid_args','message':'query or text is required'}}
 if not longmemory_available():return {'ok':False,'status':'not_ready','capability':'knowledge.recall','authority':False,'error':{'code':'substrate_unavailable','message':'longmemory is not installed on this runtime'}}
 db=Path(os.environ.get('DORE_LONGMEMORY_DB') or (Path.home()/'.dore'/'knowledge'/'longmemory.db'));project=str(args.get('project') or os.environ.get('DORE_LONGMEMORY_PROJECT') or 'dore');return longmemory_recall(query,LongMemoryConfig(db=db,project=project),mode=str(args.get('mode') or 'strict'))
def _invoke_native(handler,args,caller_product):
 if handler=='image.generate':return _image_generate(args,caller_product)
 if handler=='reflex.project':return _reflex_project(args)
 if handler=='translation.project':return _translation_project(args)
 if handler=='publishing.book-intelligence':return _book_intelligence(args)
 if handler=='publishing.dimensional-writing':return _dimensional_writing(args)
 if handler=='design.intelligence':return _design_intelligence(args)
 if handler=='bible.query-plan':return _bible_query_plan(args)
 if handler=='context.fuzzy-search':return _fuzzy_search(args,caller_product)
 if handler=='knowledge.recall':return _knowledge_recall(args)
 raise RuntimeError('unknown_native_binding:'+handler)
def _provider_error_code(exc):
 if isinstance(exc,TimeoutError):return 'timeout'
 if isinstance(exc,ConnectionResetError):return 'connection_reset'
 if isinstance(exc,ConnectionRefusedError):return 'connection_refused'
 return 'provider_error'
def call(capability,args,production,*,caller_product=None):
 descriptor=resolve(capability)
 if descriptor is None:return {'ok':False,'status':'failed','error':{'code':'capability_not_found','message':capability}}
 binding=BINDINGS.get(capability)
 if binding is None:return {'ok':False,'status':'failed','capability':capability,'error':{'code':'capability_not_callable','message':'canonical capability has no execution binding'}}
 try:
  kind=str(binding.get('kind') or '');handler=str(binding.get('handler') or '')
  if kind=='native':result=_invoke_native(handler,args,caller_product)
  elif kind=='production-action' and handler=='production_actions.execute':result=production.execute(capability,args)
  else:return {'ok':False,'status':'failed','capability':capability,'error':{'code':'binding_not_executable','message':f'{kind}:{handler}'}}
 except Exception as exc:return {'ok':False,'status':'failed','capability':capability,'error':{'code':_provider_error_code(exc),'provider_error_code':'provider_error','exception_type':type(exc).__name__,'message':str(exc)}}
 if isinstance(result,dict):result=dict(result);result.setdefault('core_route',{'capability':capability,'caller_product':caller_product,'provider':descriptor.get('provider') or descriptor.get('service') or 'dore-core','transport':descriptor.get('execution') or binding.get('kind'),'binding_kind':binding.get('kind'),'identity_source':'dore-core/runtime/capability-registry.v1.json'})
 return result
