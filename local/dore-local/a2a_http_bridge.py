#!/usr/bin/env python3
"""DORÉ Plus localhost bridge.

Browser-companion transport endpoint. It stays loopback-only and accepts only
registered dore.a2a.v1 capabilities; there is no caller-supplied shell surface.
"""
from __future__ import annotations
import json,os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from a2a_protocol import MAX_REQUEST_BYTES,PROTOCOL,response,validate
from a2a_runtime import build_registry
REGISTRY=build_registry();ALLOWED_ORIGINS={'https://chatgpt.com','https://chat.openai.com'}
class H(BaseHTTPRequestHandler):
 def _origin(self):return self.headers.get('Origin','')
 def _cors(self):
  origin=self._origin()
  if origin in ALLOWED_ORIGINS:self.send_header('Access-Control-Allow-Origin',origin);self.send_header('Vary','Origin');self.send_header('Access-Control-Allow-Headers','Content-Type');self.send_header('Access-Control-Allow-Methods','GET,POST,OPTIONS')
 def _out(self,status,payload):
  b=json.dumps(payload,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self._cors();self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
 def do_OPTIONS(self):
  if self._origin() not in ALLOWED_ORIGINS:return self._out(403,{'ok':False,'error':'origin_not_allowed'})
  self.send_response(204);self._cors();self.end_headers()
 def do_GET(self):
  if self.path=='/health':return self._out(200,{'ok':True,'service':'dore-a2a-plus','protocol':PROTOCOL,'transport':'browser-companion','capabilities':REGISTRY.describe()})
  return self._out(404,{'ok':False,'error':'not_found'})
 def do_POST(self):
  if self.path!='/invoke':return self._out(404,{'ok':False,'error':'not_found'})
  if self._origin() and self._origin() not in ALLOWED_ORIGINS:return self._out(403,{'ok':False,'error':'origin_not_allowed'})
  try:
   n=int(self.headers.get('Content-Length','0'))
   if n<=0 or n>MAX_REQUEST_BYTES:raise ValueError('invalid_content_length')
   req=validate(json.loads(self.rfile.read(n)));result=REGISTRY.invoke(req['capability'],req['params']);return self._out(200 if result.get('ok',True) else 422,response(req,result=result))
  except Exception as e:return self._out(400,{'protocol':PROTOCOL,'ok':False,'error':type(e).__name__+': '+str(e)})
 def log_message(self,*_):pass
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_A2A_PORT','4312'))),H).serve_forever()
