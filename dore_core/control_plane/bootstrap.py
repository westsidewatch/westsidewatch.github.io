from __future__ import annotations

from pathlib import Path

# Import concrete runtime modules directly. Do not import these symbols from
# dore_core.capabilities package-level exports: the sparse package intentionally
# exposes only its lightweight public surface.
from dore_core.capabilities.executor import CapabilityExecutor
from dore_core.capabilities.registry import default_registry
from dore_core.capabilities.runtime import LazyCapabilityRuntime
from dore_core.capabilities.synthetic_visual import synthetic_visual_handlers

from .runtime import ControlPlane, build_design_control_plane


def build_local_design_control_plane(root: str | Path = ".") -> ControlPlane:
    """Build the resident zero-metered-cost Design control plane.

    This bootstrap intentionally contains no OpenAI API client and no GitHub
    mailbox transport. It activates only the local typed capability runtime and
    the resident Design consumer handlers used by the A2A control plane.
    """
    registry = default_registry()
    runtime = LazyCapabilityRuntime(registry, root=str(root))
    executor = CapabilityExecutor(registry, runtime, handlers=synthetic_visual_handlers())
    return build_design_control_plane(registry, executor)
