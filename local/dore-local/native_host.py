#!/usr/bin/env python3
"""DORÉ Firefox Native Messaging host: on-demand, zero-cloud local control plane."""
from __future__ import annotations
import importlib.util,json,os,struct,sys
from pathlib import Path
from typing import Any,BinaryIO
PROTOCOL="dore.a2a/1";SERVICE="dore-a2a-native";HOST_NAME="ca.dore.companion";LEGACY_CAPABILITY="design2.stage2.acceptance";MAX_MESSAGE_BYTES=1024*1024;CARRIER_ID_KEY="__dore_transport_id"
ROOT=Path(os.environ.get("DORE_REPO_ROOT") or Path(__file__).resolve().parents[2]).expanduser().resolve()
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
def _load(name):
 p=Path(__file__).with_name(name+".py");s=importlib.util.spec_from_file_location("dore_"+name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
ADAPTER=_load("a2a_adapter");PRODUCTION=_load("production_actions")
def _read_exact(stream,size):
 b=b""
 while len(b)<size:
  c=stream.read(size-len(b))
  if not c:raise EOFError("unexpected EOF")
  b+=c
 return b
def read_message(stream):
 h=stream.read(4)
 if not h:return None
 if len(h)!=4:raise EOFError("truncated header")
 n=struct.unpack("<I",h)[0]
 if n<=0 or n>MAX_MESSAGE_BYTES:raise ValueError("invalid message length")
 p=json.loads(_read_exact(stream,n).decode())
 if not isinstance(p,dict):raise ValueError("payload must be object")
 return p
def write_message(stream,payload):
 raw=json.dumps(payload,ensure_ascii=False,separators=(",",":")).encode();stream.write(struct.pack("<I",len(raw)));stream.write(raw);stream.flush()
def _with_id(req,res):
 if req.get(CARRIER_ID_KEY):res=dict(res);res[CARRIER_ID_KEY]=req[CARRIER_ID_KEY]
 return res
def health_payload():return {"ok":True,"service":SERVICE,"host":HOST_NAME,"protocol":PROTOCOL,"transport":"firefox-native-messaging","resident":False,"paid_runtime":False,"assistant_directives":True,"production_capabilities":sorted(PRODUCTION.CAPABILITIES)}
def route_payload(payload):
 if payload.get("action") in {"native.health","health"}:return _with_id(payload,health_payload())
 cap=str(payload.get("capability") or "")
 if cap in PRODUCTION.CAPABILITIES:return _with_id(payload,PRODUCTION.execute(cap,payload.get("args") or {}))
 try:typed=ADAPTER.handle_companion_payload(payload)
 except Exception as exc:return _with_id(payload,{"ok":False,"protocol":PROTOCOL,"status":"failed","error":{"code":"adapter_error","message":str(exc)}})
 if typed is not None:return _with_id(payload,typed)
 cmd=str(payload.get("command") or payload.get("text") or "").strip().lower()
 if cap==LEGACY_CAPABILITY or cmd in {"/dore stage2","dore stage2"}:return _with_id(payload,{"ok":True,"service":SERVICE,"protocol":PROTOCOL,"capability":LEGACY_CAPABILITY,"available":True,"status":"PASS","diagnostic":True,"transport":"firefox-native-messaging"})
 return _with_id(payload,{"ok":False,"protocol":PROTOCOL,"status":"failed","error":{"code":"unsupported_payload","message":"unsupported Companion payload"}})
def serve(stdin=None,stdout=None):
 source=stdin or sys.stdin.buffer;sink=stdout or sys.stdout.buffer
 while True:
  try:
   p=read_message(source)
   if p is None:return 0
   r=route_payload(p)
  except Exception as exc:r={"ok":False,"protocol":PROTOCOL,"status":"failed","error":{"code":"native_host_error","message":str(exc)}}
  write_message(sink,r)
if __name__=="__main__":raise SystemExit(serve())
