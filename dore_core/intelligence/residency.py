"""Policy-only residency state for Doré specialist cores.

No inference engine is implemented here. This is the replaceable boundary used to
compare oMLX, mlx-serve, macMLX or an existing local provider.
"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class ResidencyState:
    max_large_resident: int = 1
    tiny: dict[str, str] = field(default_factory=dict)
    large: dict[str, str] = field(default_factory=dict)

    def resident_map(self) -> dict[str, str]:
        return {**self.tiny, **self.large}

    def admit(self, capability: str, provider: str, *, large: bool) -> tuple[str, ...]:
        """Admit a provider and return capabilities evicted by single-residency policy."""
        if not large:
            self.tiny[capability] = provider
            return ()
        evicted: list[str] = []
        if capability not in self.large and len(self.large) >= self.max_large_resident:
            while len(self.large) >= self.max_large_resident:
                old = next(iter(self.large))
                self.large.pop(old)
                evicted.append(old)
        self.large[capability] = provider
        return tuple(evicted)

    def release(self, capability: str) -> bool:
        return self.large.pop(capability, None) is not None or self.tiny.pop(capability, None) is not None
