#!/usr/bin/env python3
"""Dependency-free OpenTelemetry-compatible trace correlation fields."""
from __future__ import annotations
import os,uuid

def ids(trace_id=None,parent_span_id=None):
 trace_id=(trace_id or uuid.uuid4().hex).lower();span_id=uuid.uuid4().hex[:16].lower()
 return {'trace_id':trace_id,'span_id':span_id,'parent_span_id':parent_span_id,'traceparent':f'00-{trace_id}-{span_id}-01'}
def child(parent):return ids(parent.get('trace_id'),parent.get('span_id'))
if __name__=='__main__':print(ids())
