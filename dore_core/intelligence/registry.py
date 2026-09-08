"""Replaceable physical-provider registry for Doré virtual AI capabilities."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Provider:
    capability: str
    provider: str
    endpoint: str | None = None
    local: bool = True
    paid: bool = False
    residency: str = "on-demand"


def validate(provider: Provider) -> Provider:
    if not provider.local:
        raise ValueError("Doré Local Core provider must be local")
    if provider.paid:
        raise ValueError("paid provider cannot enter Doré Local Core")
    if provider.residency not in {"hot", "on-demand", "single-residency"}:
        raise ValueError("unsupported residency policy")
    return provider


def provider_map(items: list[Provider]) -> dict[str, str]:
    return {validate(item).capability: item.provider for item in items}
