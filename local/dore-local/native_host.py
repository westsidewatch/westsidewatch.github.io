#!/usr/bin/env python3
"""DORÉ local routing host: on-demand, zero-cloud local control plane.

Capability families are loaded lazily. A broken optional Core package must not
make unrelated local A2A capabilities unavailable.
"""
from __future__ import annotations
import importlib.util,json,os,struct,sys
from pathlib import Path
PROTOCOL="dore.a2a/1";SERVICE="dore-a2a-native";HOST_NAME="ca.dore.companion";LEGACY_CAPABILITY="design2.stage2.acceptance";MAX_MESSAGE_BYTES=64*1024*1024;CARRIER_ID_KEY="__dore_transport_id"
ROOT=Path(os.environ.get("DORE_REPO_ROOT") or Path(__file__).resolve().parents[2]).expanduser().resolve()
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
_CACHE={};_LOAD_ERRORS={}
def _load(name):
 p=Path(__file__).with_name(name+".py");s=importlib.util.spec_from_file_location("dore_"+name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def _module(name):
 if name in _CACHE:return _CACHE[name]
 try:m=_load(name);_CACHE[name]=m;return m
 except Exception as exc:_LOAD_ERRORS[name]=f"{type(exc).__name__}:{exc}";return None
def _capabilities(name):
 m=_module(name);return set(getattr(m,"CAPABILITIES",set())) if m else set()
def _execute(name,cap,args):
 m=_module(name)
 if not m:return {"ok":False,"protocol":PROTOCOL,"status":"failed","error":{"code":"capability_module_unavailable","message":_LOAD_ERRORS.get(name,name)}}
 return m.execute(cap,args)
def _bus_pair():
 bus=_module("capability_bus");production=_module("production_actions")
 return bus,production
def discover_production(include_planned=False):
 bus,production=_bus_pair()
 if not bus or not production:return []
 try:return bus.discover(production,include_planned=include_planned)
 except Exception:return []
def resolve_production(capability):
 bus,production=_bus_pair()
 if not bus or not production:return None
 try:return bus.resolve(capability,production)
 except Exception:return None
def call_production(capability,args,caller_product=None):
 bus,production=_bus_pair()
 if not bus or not production:return {"ok":False,"protocol":PROTOCOL,"status":"failed","error":{"code":"production_bus_unavailable","message":_LOAD_ERRORS.get("capability_bus") or _LOAD_ERRORS.get("production_actions") or "production bus unavailable"}}
 return bus.call(capability,args,production,caller_product=caller_product)
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
def health_payload():
 direct=[]
 for name in ("self_maintenance_action","theology_acceptance_action","theology_training_action","dawn_publication_action","design_live_acceptance_action"):
  direct.extend(sorted(_capabilities(name)))
 production=[x["id"] for x in discover_production() if x.get("callable")]
 return {"ok":True,"service":SERVICE,"host":HOST_NAME,"protocol":PROTOCOL,"transport":"local-routing-host","resident":False,"paid_runtime":False,"assistant_directives":True,"production_capabilities":sorted(set(production+direct)),"degraded_modules":dict(_LOAD_ERRORS)}
def route_payload(payload):
 if payload.get("action") in {"native.health","health"}:return _with_id(payload,health_payload())
 cap=str(payload.get("capability") or "");args=payload.get("args") or {}
 direct=(("design_live_acceptance_action",), ("self_maintenance_action",), ("theology_acceptance_action",), ("theology_training_action",), ("dawn_publication_action",))
 for entry in direct:
  name=entry[0]
  if cap in _capabilities(name):return _with_id(payload,_execute(name,cap,args))
 descriptor=resolve_production(cap) if cap else None
 if descriptor and descriptor.get("callable"):return _with_id(payload,call_production(cap,args,payload.get("caller_product")))
 adapter=_module("a2a_adapter")
 if adapter:
  try:typed=adapter.handle_companion_payload(payload)
  except Exception as exc:return _with_id(payload,{"ok":False,"protocol":PROTOCOL,"status":"failed","error":{"code":"adapter_error","message":str(exc)}})
  if typed is not None:return _with_id(payload,typed)
 cmd=str(payload.get("command") or payload.get("text") or "").strip().lower()
 if cap==LEGACY_CAPABILITY or cmd in {"/dore stage2","dore stage2"}:return _with_id(payload,{"ok":True,"service":SERVICE,"protocol":PROTOCOL,"capability":LEGACY_CAPABILITY,"available":True,"status":"PASS","diagnostic":True,"transport":"local-routing-host"})
 return _with_id(payload,{"ok":False,"protocol":PROTOCOL,"status":"failed","error":{"code":"unsupported_payload","message":"unsupported local routing payload"}})
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