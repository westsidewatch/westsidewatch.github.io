"""Doré Local Intelligence Fabric: minimum-capability routing.

This module owns Doré-specific policy only. Physical model runtimes remain replaceable
providers. Products request virtual capabilities and never address model processes.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

VIRTUAL_CAPABILITIES = (
    "tiny-reflex", "language", "reasoning", "coding", "research", "vision",
    "embedding", "rerank", "voice", "image",
)

@dataclass(frozen=True)
class RouteDecision:
    capability: str
    lane: str
    provider: str | None
    load: str
    reason: str


def choose_route(
    capability: str,
    *,
    deterministic_available: bool = False,
    tiny_sufficient: bool = False,
    resident: Mapping[str, str] | None = None,
    providers: Mapping[str, str] | None = None,
) -> RouteDecision:
    """Choose the smallest sufficient local lane without binding product APIs to models."""
    if capability not in VIRTUAL_CAPABILITIES:
        raise ValueError(f"unknown virtual capability: {capability}")
    if deterministic_available:
        return RouteDecision(capability, "deterministic", None, "none", "deterministic path is sufficient")
    resident = resident or {}
    providers = providers or {}
    if tiny_sufficient and capability not in {"image", "vision", "voice"}:
        provider = resident.get("tiny-reflex") or providers.get("tiny-reflex")
        return RouteDecision(capability, "tiny-hot", provider, "reuse" if resident.get("tiny-reflex") else "on-demand", "tiny core is sufficient")
    if capability in resident:
        return RouteDecision(capability, "resident-specialist", resident[capability], "reuse", "required specialist is already resident")
    provider = providers.get(capability)
    return RouteDecision(capability, "cold-specialist", provider, "on-demand", "specialist required; load only for this task")
