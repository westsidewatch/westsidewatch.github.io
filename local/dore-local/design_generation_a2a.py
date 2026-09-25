#!/usr/bin/env python3
"""A2A surface for Doré canonical design-generation authority.

Operations:
- resolve: resolve canonical editorial grammar/evidence into generator_prompt
- verify: compare a generator result/readback against the resolved package

This module does not generate images and does not invent design authority.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
from typing import Any

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
RESOLVER=ROOT/'scripts'/'resolve_design_generation_prompt.py'


def _resolver():
    spec=importlib.util.spec_from_file_location('dore_generation_resolver',RESOLVER)
    if spec is None or spec.loader is None: raise RuntimeError('design_generation_resolver_unavailable')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


def _resolve(args:dict[str,Any])->dict[str,Any]:
    era=str(args.get('grammar_id') or args.get('era') or '').strip()
    if not era: return {'ok':False,'status':'failed','error':{'code':'invalid_args','message':'grammar_id or era is required'}}
    result=_resolver().resolve(
        era,
        modules=args.get('modules'),
        subject=args.get('subject'),
        artifact_type=str(args.get('artifact_type') or 'image'),
        consumer=str(args.get('consumer') or args.get('caller_product') or 'chatgpt-a2a'),
        exploration=bool(args.get('exploration',False)),
    )
    return {'ok':True,'status':'completed','capability':'design.generation','operation':'resolve','generation_package':result,'generator_prompt':result['canonical_prompt'],'authority':True}


def _verify(args:dict[str,Any])->dict[str,Any]:
    package=args.get('generation_package')
    if not isinstance(package,dict): return {'ok':False,'status':'failed','error':{'code':'invalid_args','message':'generation_package from resolve is required'}}
    if package.get('schema')!='dore.design-generation-resolution.v1': return {'ok':False,'status':'failed','error':{'code':'invalid_package','message':'unrecognized generation package schema'}}
    # Visual inspection may be performed by the caller/model; A2A owns the authority checklist.
    observations=args.get('observations') or {}
    if not isinstance(observations,dict): observations={}
    required=('grammar_fidelity','evidence_fidelity','subject_fidelity','forbidden_artifacts_absent')
    missing=[k for k in required if k not in observations]
    if missing:
        return {'ok':False,'status':'needs_visual_readback','capability':'design.generation','operation':'verify','verified':False,'required_observations':list(required),'missing_observations':missing,'grammar_id':package.get('grammar_id'),'visual_evidence':package.get('visual_evidence',[])}
    failures=[k for k in required if observations.get(k) is not True]
    corrections=args.get('corrections') or []
    if failures:
        return {'ok':True,'status':'revision_required','capability':'design.generation','operation':'verify','verified':False,'failed_checks':failures,'corrections':corrections,'grammar_id':package.get('grammar_id'),'visual_evidence':package.get('visual_evidence',[]),'canonical_prompt':package.get('canonical_prompt')}
    return {'ok':True,'status':'completed','capability':'design.generation','operation':'verify','verified':True,'grammar_id':package.get('grammar_id'),'visual_evidence':package.get('visual_evidence',[]),'truth_state':'verified-specimen'}


def execute(args:dict[str,Any])->dict[str,Any]:
    op=str(args.get('operation') or 'resolve').strip().lower()
    if op=='resolve': return _resolve(args)
    if op=='verify': return _verify(args)
    return {'ok':False,'status':'failed','error':{'code':'invalid_operation','message':'operation must be resolve or verify'}}
