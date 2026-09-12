#!/usr/bin/env python3
"""Minimal local inference seam for Doré Design.

This module deliberately has no dependency on browser/capability-bus packages.
It exists so the Design A2A worker can call the local Ollama engine even when an
unrelated optional Doré capability family is degraded.
"""
from __future__ import annotations
import json,os,urllib.request
MODEL=os.environ.get('DORE_LOCAL_MODEL') or os.environ.get('DORE_MODEL') or os.environ.get('OLLAMA_MODEL') or 'gemma4:e4b'
OLLAMA=os.environ.get('OLLAMA_BASE_URL') or os.environ.get('OLLAMA_HOST') or 'http://127.0.0.1:11434'
def ollama(messages):
 data=json.dumps({'model':MODEL,'messages':messages,'stream':False,'think':False}).encode('utf-8')
 req=urllib.request.Request(OLLAMA.rstrip('/')+'/api/chat',data=data,headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=300) as response:payload=json.loads(response.read().decode('utf-8'))
 msg=payload.get('message') or {};content=msg.get('content')
 if isinstance(content,str) and content.strip():return content.strip()
 raise RuntimeError('ollama_empty_content:'+json.dumps({'model':payload.get('model'),'done_reason':payload.get('done_reason'),'message_keys':sorted(msg.keys())},ensure_ascii=False))
