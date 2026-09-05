"""DORÉ A2A capability contract.

Transport-neutral boundary for ChatGPT Plus bridges. External transports submit
named capabilities, never caller-supplied shell commands. Local implementations
remain inside DORÉ and can be shared by MCP and browser-companion transports.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class Capability:
    name: str
    description: str
    mutating: bool = False

CAPABILITIES = {
    'dore.health': Capability('dore.health','Read resident and bridge health.'),
    'design2.stage2.acceptance': Capability('design2.stage2.acceptance','Run the fixed DORÉ DESIGN Stage 2 acceptance suite.'),
    'design2.tests': Capability('design2.tests','Run the registered DORÉ DESIGN tests.'),
    'design2.preview': Capability('design2.preview','Open or inspect the registered Design preview.'),
    'resident.update': Capability('resident.update','Update the registered DORÉ resident using its guarded updater.',True),
}

class CapabilityError(RuntimeError): pass

class Registry:
    def __init__(self): self._handlers: dict[str,Callable[[dict[str,Any]],dict[str,Any]]] = {}
    def register(self,name:str,handler:Callable[[dict[str,Any]],dict[str,Any]]):
        if name not in CAPABILITIES: raise CapabilityError('unknown_capability:'+name)
        if name in self._handlers: raise CapabilityError('duplicate_handler:'+name)
        self._handlers[name]=handler
    def describe(self):
        return [{'name':c.name,'description':c.description,'mutating':c.mutating,'available':c.name in self._handlers} for c in CAPABILITIES.values()]
    def invoke(self,name:str,params:dict[str,Any]|None=None):
        if name not in CAPABILITIES: raise CapabilityError('unknown_capability:'+str(name))
        if name not in self._handlers: raise CapabilityError('capability_unavailable:'+name)
        if params is not None and not isinstance(params,dict): raise CapabilityError('invalid_params')
        return self._handlers[name](params or {})
