#!/usr/bin/env python3
"""Doré semantic capability bus."""
from __future__ import annotations
import importlib.util, json, os
from pathlib import Path
from typing import Any
from urllib import request
from dore_core.bible.query_planner import plan_bible_query
from dore_core.retrieval.living import retrieve as living_retrieve
from dore_core.substrates.longmemory import LongMemoryConfig, available as longmemory_available, recall as longmemory_recall
from dore_core.substrates.qmd import PRODUCTION_COLLECTION, QMDConfig, available as qmd_available, production_config, search as qmd_search
HERE=Path(__file__).resolve().parent

def _load_sibling(name:str):
    path=HERE/f"{name}.py"; spec=importlib.util.spec_from_file_location(f"dore_bus_{name}",path)
    if spec is None or spec.loader is None: raise RuntimeError(f"cannot load {path}")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
REGISTRY=_load_sibling("capability_registry")
NATIVE_CAPABILITIES={
 "image.generate":{"id":"image.generate","type":"production","service":"visual","status":"existing","execution":"core-adapter","provider":"dore-image-local","load":"on-demand","result":"image-artifact"},
 "context.fuzzy-search":{"id":"context.fuzzy-search","type":"context","service":"retrieval","status":"existing","execution":"core-adapter","provider":"dore-search","load":"deferred","authority":False,"result":"dore-search-results"},
 "bible.query-plan":{"id":"bible.query-plan","type":"context","service":"bible-routing","status":"existing","execution":"core-adapter","provider":"dore-core","load":"always-light","authority":False,"result":"bible-query-plan"},
 "knowledge.recall":{"id":"knowledge.recall","type":"knowledge","service":"memory","status":"existing","execution":"core-adapter","provider":"longmemory-local","load":"deferred","authority":False},
}

def _post_json(url,payload,headers=None,timeout=1500):
    raw=json.dumps(payload,ensure_ascii=False).encode(); merged={"Content-Type":"application/json","Accept":"application/json"}; merged.update(headers or {})
    req=request.Request(url,data=raw,method="POST",headers=merged)
    with request.urlopen(req,timeout=timeout) as response:return json.loads(response.read().decode())
def discover(production,*,include_planned=False):
    by_id={}
    for item in REGISTRY.discover(include_planned=include_planned):
        d=dict(item);d["owner"]="dore-core";d["callable"]=False;by_id[str(d["id"])]=d
    for capability in sorted(production.CAPABILITIES):by_id[capability]={"id":capability,"type":"production","status":"existing","execution":"production-action","owner":"dore-core","callable":True}
    for capability,item in NATIVE_CAPABILITIES.items():d=dict(item);d["owner"]="dore-core";d["callable"]=True;by_id[capability]=d
    return [by_id[k] for k in sorted(by_id)]
def resolve(capability,production):return next((x for x in discover(production,include_planned=True) if x.get("id")==capability),None)
def _image_generate(args,caller_product=None):
    message=str(args.get("message") or args.get("prompt") or "").strip()
    if not message:return {"ok":False,"status":"failed","error":{"code":"invalid_args","message":"message or prompt is required"}}
    payload=dict(args);payload["message"]=message; result=_post_json("http://127.0.0.1:8790/generate",payload,{"X-Dore-Origin":caller_product or "dore-core"})
    if isinstance(result,dict):result=dict(result);result["core_route"]={"capability":"image.generate","caller_product":caller_product,"provider":"dore-image-local","transport":"core-adapter"}
    return result
def _search_host(args,caller_product):
    explicit=str(args.get("host") or "").strip().lower()
    if explicit:return explicit
    p=str(caller_product or "").strip().lower()
    if p=="one" or p.startswith("one-"):return "one"
    if p=="multiwrite" or p.startswith("multiwrite-"):return "multiwrite"
    return "unknown"
def _bible_query_plan(args):
    query=str(args.get("query") or args.get("text") or "").strip()
    if not query:return {"ok":False,"status":"failed","error":{"code":"invalid_args","message":"query or text is required"}}
    plan=plan_bible_query(query,explicit_search=bool(args.get("explicit_search",False)),deep=bool(args.get("deep",False)))
    return {"ok":True,"status":"completed","capability":"bible.query-plan","plan":plan.to_dict(),"authority":False,"large_model_invoked":False}
def _fuzzy_search(args,caller_product=None):
    query=str(args.get("query") or args.get("text") or "").strip()
    if not query:return {"ok":False,"status":"failed","error":{"code":"invalid_args","message":"query or text is required"}}
    if not qmd_available():return {"ok":False,"status":"not_ready","capability":"context.fuzzy-search","authority":False,"error":{"code":"substrate_unavailable","message":"local retrieval substrate is not installed on this runtime"}}
    requested=str(args.get("collection") or os.environ.get("DORE_QMD_COLLECTION") or "").strip(); qmd_config=production_config(collection=PRODUCTION_COLLECTION) if not requested or requested==PRODUCTION_COLLECTION else QMDConfig(collection=requested)
    db=Path(os.environ.get("DORE_LONGMEMORY_DB") or (Path.home()/".dore"/"knowledge"/"longmemory.db")); project=str(args.get("project") or os.environ.get("DORE_LONGMEMORY_PROJECT") or "dore"); memory_config=LongMemoryConfig(db=db,project=project)
    def search_documents(text,*,semantic,deep,limit):return qmd_search(text,qmd_config,semantic=semantic,deep=deep,limit=limit)
    def recall_current(text,*,mode):return longmemory_recall(text,memory_config,mode=mode) if longmemory_available() else {"ok":False,"authority":False,"error":"memory_unavailable"}
    internal=living_retrieve(query,qmd_search=search_documents,memory_recall=recall_current,explicit_search=bool(args.get("explicit_search",False)),deep_requested=bool(args.get("deep",False)),limit=int(args.get("limit") or 8),host=_search_host(args,caller_product),mode=str(args.get("mode") or "prepare").strip().lower(),embedded=bool(args.get("embedded",False)))
    plan=internal["plan"]; bible_plan=plan_bible_query(query,explicit_search=bool(args.get("explicit_search",False)),deep=bool(args.get("deep",False))) if bool(args.get("bible",False)) or _search_host(args,caller_product) in {"one","multiwrite"} else None
    return {"ok":internal.get("ok",False),"status":"completed" if internal.get("ok",False) else "failed","capability":"context.fuzzy-search","query":query,"results":internal.get("results",[]),"retrieval":{"lexical":plan.lexical,"semantic":plan.semantic,"deep":plan.deep,"memory_recall":plan.recall_memory,"reason":plan.reason},"bible_query_plan":bible_plan.to_dict() if bible_plan else None,"context_policy":internal.get("context_policy"),"search_scope":"production" if qmd_config.collection==PRODUCTION_COLLECTION else "requested-collection","authority":False,"large_model_invoked":False,"core_route":{"capability":"context.fuzzy-search","caller_product":caller_product,"transport":"core-adapter"}}
def _knowledge_recall(args):
    query=str(args.get("query") or args.get("text") or "").strip()
    if not query:return {"ok":False,"status":"failed","error":{"code":"invalid_args","message":"query or text is required"}}
    if not longmemory_available():return {"ok":False,"status":"not_ready","capability":"knowledge.recall","authority":False,"error":{"code":"substrate_unavailable","message":"longmemory is not installed on this runtime"}}
    db=Path(os.environ.get("DORE_LONGMEMORY_DB") or (Path.home()/".dore"/"knowledge"/"longmemory.db")); project=str(args.get("project") or os.environ.get("DORE_LONGMEMORY_PROJECT") or "dore"); mode=str(args.get("mode") or "strict")
    return longmemory_recall(query,LongMemoryConfig(db=db,project=project),mode=mode)
def call(capability,args,production,*,caller_product=None):
    descriptor=resolve(capability,production)
    if descriptor is None:return {"ok":False,"status":"failed","error":{"code":"capability_not_found","message":capability}}
    try:
        if capability=="image.generate":return _image_generate(args,caller_product)
        if capability=="context.fuzzy-search":result=_fuzzy_search(args,caller_product)
        elif capability=="bible.query-plan":result=_bible_query_plan(args)
        elif capability=="knowledge.recall":result=_knowledge_recall(args)
        elif capability in production.CAPABILITIES:result=production.execute(capability,args)
        else:return {"ok":False,"status":"failed","capability":capability,"error":{"code":"capability_not_callable","message":"registered for discovery but not yet connected to the Core execution path"}}
    except Exception as exc:return {"ok":False,"status":"failed","capability":capability,"error":{"code":"provider_error","message":str(exc)}}
    if isinstance(result,dict):result=dict(result);result.setdefault("core_route",{"capability":capability,"caller_product":caller_product,"provider":descriptor.get("provider") or "production-actions","transport":"core-adapter" if capability in NATIVE_CAPABILITIES else "in-process"})
    return result
