"""Doré sparse capability runtime.

This package keeps capability metadata cheap and dormant by default. Full skill
bodies and providers are activated only after routing.
"""
from .model import ArtifactRef, CapabilityManifest, RouteDecision, TaskState
from .registry import CapabilityRegistry
from .router import SparseCapabilityRouter

__all__ = [
    "ArtifactRef",
    "CapabilityManifest",
    "RouteDecision",
    "TaskState",
    "CapabilityRegistry",
    "SparseCapabilityRouter",
]
