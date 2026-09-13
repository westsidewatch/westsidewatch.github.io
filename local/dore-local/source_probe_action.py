#!/usr/bin/env python3
"""A2A wrapper for the provider-neutral Doré source probe capability."""
from __future__ import annotations
import importlib.util
from pathlib import Path
from typing import Any

CAPABILITIES={"source.probe"}
HERE=Path(__file__).resolve().parent

def _module():
    spec=importlib.util.spec_from_file_location("dore_source_probe_capability",HERE/"source_probe_capability.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("source_probe_capability unavailable")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def execute(capability:str,args:dict[str,Any]|None=None)->dict[str,Any]:
    if capability not in CAPABILITIES:
        return {"ok":False,"status":"failed","error":{"code":"unsupported_capability","message":capability}}
    result=_module().execute(args or {})
    if isinstance(result,dict):
        result=dict(result)
        result.setdefault("capability","source.probe")
        result.setdefault("core_route",{"capability":"source.probe","provider":"dore-core","transport":"in-process"})
    return result
