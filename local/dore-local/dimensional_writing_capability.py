#!/usr/bin/env python3
"""Doré Dimensional Writing v0: author-safe diagnostics + semantic co-writing seam."""
from __future__ import annotations
import json,re
from pathlib import Path
from typing import Any,Callable

ROOT=Path(__file__).resolve().parents[2]
CANON=ROOT/'dore-core'/'runtime'/'dimensional-writing-canon.v0.json'
SCHEMA='dore.dimensional-writing-report.v0'

def canon()->dict[str,Any]:return json.loads(CANON.read_text(encoding='utf-8'))
def _text(v:Any)->str:return v.strip() if isinstance(v,str) else ''
def _paragraphs(text:str)->list[str]:return [p.strip() for p in re.split(r'\n\s*\n',text) if p.strip()]
def _sentences(text:str)->list[str]:return [s.strip() for s in re.split(r'(?<=[。！？!?])',text) if s.strip()]
def diagnostics(text:str)->dict[str,Any]:
 c=canon();pars=_paragraphs(text);chars=max(1,len(re.sub(r'\s+','',text)))
 isolated=[]
 for i,p in enumerate(pars):
  ss=_sentences(p)
  if len(ss)==1 and len(re.sub(r'\s+','',p))<=24:isolated.append({'paragraph':i,'text':p})
 lex=c['diagnosticLexicon'];connect={w:text.count(w) for w in lex['connectives'] if text.count(w)};adverbs={w:text.count(w) for w in lex['adverbs'] if text.count(w)}
 nav=sum(connect.values());adv=sum(adverbs.values());questions=len(re.findall(r'[？?]',text));short_after_question=len(re.findall(r'[？?]\s*(?:\n\s*){1,2}[^\n。！？!?]{1,28}[。！!]',text))
 risks=[]
 if isolated:risks.append('isolated-short-paragraphs')
 if nav*1000/chars>8:risks.append('connective-density')
 if adv*1000/chars>8:risks.append('adverb-density')
 if questions>=2 and short_after_question>=2:risks.append('question-punchline-cadence')
 if len(pars)>=6 and sum(1 for p in pars if len(_sentences(p))==1)/len(pars)>.45:risks.append('paragraph-fragmentation')
 return {'characters':chars,'paragraphs':len(pars),'isolatedShortParagraphs':isolated,'connectives':connect,'adverbs':adverbs,'connectivesPer1000':round(nav*1000/chars,2),'adverbsPer1000':round(adv*1000/chars,2),'questions':questions,'questionPunchlineSignals':short_after_question,'risks':risks}

def _messages(args:dict[str,Any],d:dict[str,Any])->list[dict[str,str]]:
 c=canon();payload={'mode':args.get('mode','revise'),'authorThesis':_text(args.get('authorThesis')),'manuscript':_text(args.get('manuscript')),'research':args.get('research',[]),'diagnostics':d,'canon':{'loop':c['loop'],'movement':c['movement'],'principles':c['principles'],'judgeGates':c['judgeGates']}}
 system=('You are Doré Writing Intelligence, co-writing under author authority. Preserve the author thesis and theological insight. '
 'Do not imitate a named writer. Let evidence, scene, verbs, information order, scale change and paragraph movement carry rhythm. '
 'Do not manufacture rhythm with isolated one-line paragraphs or connective scaffolding. Do not announce conclusions before material earns them. '
 'Research must enter the body of the argument rather than remain annotation. Return exactly one JSON object with keys manuscript, semanticAdmission, revisions, unresolved. '
 'semanticAdmission must assess paragraphIntegrity, semanticPressure, evidenceBeforeIntensity, depthBeforeAnalogy, prematureCoherence, authorAuthority, each with pass:boolean and reason:string.')
 return [{'role':'system','content':system},{'role':'user','content':json.dumps(payload,ensure_ascii=False)}]

def _parse(raw:str)->dict[str,Any]:
 value=json.loads(raw.strip());
 if not isinstance(value,dict):raise ValueError('writing inference must return object')
 return value

def execute(args:dict[str,Any]|None,infer:Callable[[list[dict[str,str]]],str]|None=None)->dict[str,Any]:
 args=args or {};text=_text(args.get('manuscript'))
 if not text:return {'ok':False,'status':'failed','capability':'publishing.dimensional-writing','error':{'code':'invalid_args','message':'manuscript is required'}}
 d=diagnostics(text);base={'schema':SCHEMA,'authority':{'authorThesis':'author','mayRewriteThesis':False},'diagnostics':d,'canon':str(CANON.relative_to(ROOT))}
 if infer is None:return {'ok':True,'status':'completed','capability':'publishing.dimensional-writing','report':{**base,'semantic':False,'admission':'diagnostics-only','manuscript':text}}
 try:value=_parse(infer(_messages(args,d)))
 except Exception as exc:return {'ok':True,'status':'completed','capability':'publishing.dimensional-writing','report':{**base,'semantic':False,'admission':'degraded','manuscript':text,'reason':type(exc).__name__}}
 revised=_text(value.get('manuscript')) or text;post=diagnostics(revised);semantic=value.get('semanticAdmission') if isinstance(value.get('semanticAdmission'),dict) else {};semantic_pass=bool(semantic) and all(isinstance(v,dict) and v.get('pass') is True for v in semantic.values());deterministic_pass=not post['risks'];admitted=semantic_pass and deterministic_pass
 return {'ok':True,'status':'completed','capability':'publishing.dimensional-writing','report':{**base,'semantic':True,'preDiagnostics':d,'postDiagnostics':post,'semanticAdmission':semantic,'admission':'pass' if admitted else 'revise','manuscript':revised,'revisions':value.get('revisions',[]),'unresolved':value.get('unresolved',[]),'publishable':admitted}}
