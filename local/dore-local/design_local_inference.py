#!/usr/bin/env python3
"""Minimal local inference seam for Doré Design.

No browser/capability-bus dependency. Supports Ollama JSON-schema constrained
responses for executable design patches and visual-critic contracts.
"""
from __future__ import annotations
import json,os,urllib.error,urllib.request
MODEL=os.environ.get('DORE_LOCAL_MODEL') or os.environ.get('DORE_MODEL') or os.environ.get('OLLAMA_MODEL') or 'gemma4:e4b'
OLLAMA=os.environ.get('OLLAMA_BASE_URL') or os.environ.get('OLLAMA_HOST') or 'http://127.0.0.1:11434'

def _ollama_schema(schema):
 if not isinstance(schema,dict):return schema
 schema=json.loads(json.dumps(schema))
 def walk(node):
  if isinstance(node,dict):
   t=node.get('type')
   if isinstance(t,list):
    non_null=[x for x in t if x!='null']
    if len(non_null)==1 and len(non_null)!=len(t):
     node['type']=non_null[0]
     node['nullable']=True
   for value in node.values():walk(value)
  elif isinstance(node,list):
   for value in node:walk(value)
 walk(schema)
 return schema

def _chat(messages,format_schema=None):
 payload={'model':MODEL,'messages':messages,'stream':False,'think':False}
 if format_schema is not None:payload['format']=_ollama_schema(format_schema)
 data=json.dumps(payload).encode('utf-8');req=urllib.request.Request(OLLAMA.rstrip('/')+'/api/chat',data=data,headers={'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(req,timeout=300) as response:result=json.loads(response.read().decode('utf-8'))
 except urllib.error.HTTPError as exc:
  body=exc.read().decode('utf-8','replace')
  raise RuntimeError(f'ollama_http_{exc.code}:{body}') from exc
 msg=result.get('message') or {};content=msg.get('content')
 if isinstance(content,str) and content.strip():return content.strip()
 raise RuntimeError('ollama_empty_content:'+json.dumps({'model':result.get('model'),'done_reason':result.get('done_reason'),'message_keys':sorted(msg.keys())},ensure_ascii=False))
def ollama(messages):return _chat(messages)
def ollama_json(messages,schema):return _chat(messages,format_schema=schema)
