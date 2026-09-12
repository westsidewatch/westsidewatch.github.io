#!/usr/bin/env python3
"""Minimal local inference seam for Doré Design.

No browser/capability-bus dependency. Supports Ollama JSON-schema constrained
responses for executable design patches and visual-critic contracts.
"""
from __future__ import annotations
import json,os,urllib.request
MODEL=os.environ.get('DORE_LOCAL_MODEL') or os.environ.get('DORE_MODEL') or os.environ.get('OLLAMA_MODEL') or 'gemma4:e4b'
OLLAMA=os.environ.get('OLLAMA_BASE_URL') or os.environ.get('OLLAMA_HOST') or 'http://127.0.0.1:11434'
def _chat(messages,format_schema=None):
 payload={'model':MODEL,'messages':messages,'stream':False,'think':False}
 if format_schema is not None:payload['format']=format_schema
 data=json.dumps(payload).encode('utf-8');req=urllib.request.Request(OLLAMA.rstrip('/')+'/api/chat',data=data,headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=300) as response:result=json.loads(response.read().decode('utf-8'))
 msg=result.get('message') or {};content=msg.get('content')
 if isinstance(content,str) and content.strip():return content.strip()
 raise RuntimeError('ollama_empty_content:'+json.dumps({'model':result.get('model'),'done_reason':result.get('done_reason'),'message_keys':sorted(msg.keys())},ensure_ascii=False))
def ollama(messages):return _chat(messages)
def ollama_json(messages,schema):return _chat(messages,format_schema=schema)
