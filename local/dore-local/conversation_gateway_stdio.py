#!/usr/bin/env python3
"""Line-delimited JSON tool surface for Doré Conversation Gateway.

Transport only. Canonical capability identity and execution remain in Doré Core/A2A.
Each input line is one JSON object using operation discover|describe|call.
"""
from __future__ import annotations
import json,sys
import conversation_gateway

SERVICE="dore-conversation-gateway"
PROTOCOL="dore.conversation-gateway/1"

def serve(source=None,sink=None):
    source=source or sys.stdin
    sink=sink or sys.stdout
    for raw in source:
        raw=raw.strip()
        if not raw: continue
        try:
            request=json.loads(raw)
            if not isinstance(request,dict): raise ValueError("request_must_be_object")
            response=conversation_gateway.dispatch(request)
        except Exception as exc:
            response={"schema":PROTOCOL,"ok":False,"service":SERVICE,"error":"gateway_error","detail":str(exc)}
        sink.write(json.dumps(response,ensure_ascii=False,separators=(",",":"))+"\n")
        sink.flush()
    return 0

if __name__=="__main__": raise SystemExit(serve())
