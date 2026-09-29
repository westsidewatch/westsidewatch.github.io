"""Doré sparse capability runtime.

This package keeps capability metadata cheap and dormant by default. Full skill
bodies and providers are activated only after routing. Product areas expose
thin emergence surfaces over these shared faculties instead of duplicating
implementations.
"""
from .model import ArtifactRef, CapabilityManifest, RouteDecision, TaskState
from .registry import CapabilityRegistry
from .router import SparseCapabilityRouter
from .surface import CapabilitySurface, DEFAULT_SURFACES, SurfaceRegistry

__all__ = [
    "ArtifactRef",
    "CapabilityManifest",
    "RouteDecision",
    "TaskState",
    "CapabilityRegistry",
    "SparseCapabilityRouter",
    "CapabilitySurface",
    "SurfaceRegistry",
    "DEFAULT_SURFACES",
]
