"""Doré-owned contracts for replaceable Knowledge/Retrieval substrates.

LongMemory/QMD are candidates below these boundaries. They never become Doré authority.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Substrate:
    name: str
    role: str
    local: bool = True
    paid: bool = False
    authoritative: bool = False
    network_required: bool = False


def validate(substrate: Substrate) -> Substrate:
    if not substrate.local or substrate.paid or substrate.network_required:
        raise ValueError("Doré Local substrate must remain free and offline-capable")
    if substrate.authoritative:
        raise ValueError("substrate cannot own Doré Knowledge authority")
    if substrate.role not in {"knowledge", "retrieval", "durability", "runtime", "residency"}:
        raise ValueError("unsupported substrate role")
    return substrate


LONGMEMORY = Substrate("longmemory", "knowledge")
QMD = Substrate("qmd", "retrieval")
WAKE = Substrate("wake", "durability")
