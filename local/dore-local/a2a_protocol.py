"""Small JSON protocol shared by DORÉ Plus transports.

This is intentionally not an execution server. MCP/browser adapters translate
their requests into this narrow contract and the local registry decides what
DORÉ is allowed to do.
"""
from __future__ import annotations
from typing import Any

PROTOCOL='dore.a2a.v1'
MAX_REQUEST_BYTES=64*1024

def request(capability:str,params:dict[str,Any]|None=None,request_id:str|None=None):
    if not isinstance(capability,str) or not capability or len(capability)>128: raise ValueError('invalid_capability')
    if params is None: params={}
    if not isinstance(params,dict): raise ValueError('invalid_params')
    return {'protocol':PROTOCOL,'request_id':request_id,'capability':capability,'params':params}

def validate(payload):
    if not isinstance(payload,dict): raise ValueError('invalid_request')
    if payload.get('protocol')!=PROTOCOL: raise ValueError('invalid_protocol')
    allowed={'protocol','request_id','capability','params'}
    if set(payload)-allowed: raise ValueError('unexpected_fields')
    return request(payload.get('capability'),payload.get('params'),payload.get('request_id'))

def response(req,result=None,error=None):
    return {'protocol':PROTOCOL,'request_id':req.get('request_id'),'ok':error is None,'result':result if error is None else None,'error':error}
