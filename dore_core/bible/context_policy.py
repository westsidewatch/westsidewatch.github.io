from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List


@dataclass(frozen=True)
class SearchContextPolicy:
    host: str = "multiwrite"
    mode: str = "prepare"
    embedded: bool = False

    def __post_init__(self) -> None:
        if self.host not in {"multiwrite", "one", "unknown"}:
            raise ValueError("unsupported_search_host")
        if self.mode not in {"prepare", "live", "present"}:
            raise ValueError("unsupported_search_mode")

    @property
    def ambient_enabled(self) -> bool:
        return self.mode == "prepare"

    @property
    def search_enabled(self) -> bool:
        return self.mode != "present"

    @property
    def suppressed_source_kinds(self) -> set[str]:
        suppressed: set[str] = set()
        if self.host == "one" and self.embedded:
            suppressed.add("one")
        return suppressed

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema": "dore.search-context-policy.v1",
            "host": self.host,
            "mode": self.mode,
            "embedded": self.embedded,
            "ambient_enabled": self.ambient_enabled,
            "search_enabled": self.search_enabled,
            "suppressed_source_kinds": sorted(self.suppressed_source_kinds),
        }


def _source_kind(result: Dict[str, Any]) -> str:
    value = result.get("source_kind") or result.get("kind") or ""
    return str(value).strip().lower()


def apply_search_context_policy(
    results: Iterable[Dict[str, Any]], policy: SearchContextPolicy
) -> List[Dict[str, Any]]:
    """Apply product-context policy without exposing provider internals.

    Present mode disables result delivery. Embedded Multiwrite in ONE suppresses
    ONE self-promotion while preserving all other result classes.
    """

    if not policy.search_enabled:
        return []

    suppressed = policy.suppressed_source_kinds
    out: List[Dict[str, Any]] = []
    for result in results:
        if not isinstance(result, dict):
            continue
        if _source_kind(result) in suppressed:
            continue
        item = dict(result)
        item.setdefault("actions", ["keep", "flow", "present"])
        out.append(item)
    return out
